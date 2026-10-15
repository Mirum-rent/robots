"""Run deterministic, explicitly synthetic fault scenarios without networking."""

import argparse
import json
from pathlib import Path
import sqlite3
import tempfile

from . import __version__
from .core import Engine, IntentStore, Receipt, SafetyError, SimulatedCrash, StateIntegrityError
from .fake_api import FakeAPI


def scenarios(work: Path) -> dict:
    trace = []
    results = []

    def emitter(scenario):
        def emit(**event):
            trace.append({"seq": len(trace) + 1, "scenario": scenario, **event})
        return emit

    for name, mode, expected, crash in [
        ("accepted_unknown", "accept_then_timeout", "CONFIRMED", False),
        ("rejected_unknown", "reject_then_timeout", "NOT_ACCEPTED", False),
        ("restart_before_ack", "accept", "CONFIRMED", True),
    ]:
        folder = work / name
        folder.mkdir()
        intent_id, key = "SYN-INTENT-" + name, "SYN-KEY-" + name
        emit = emitter(name)
        store, api = IntentStore(folder / "intent.sqlite"), FakeAPI(folder / "fake.sqlite", mode)
        engine = Engine(store, api, emit)
        engine.prepare(intent_id, key)
        try:
            engine.dispatch(intent_id, crash_after_send=crash)
        except SimulatedCrash:
            pass
        before = store.get(intent_id).state
        store.close()
        api.close()
        # Re-open both independent stores; no in-memory receipt survives.
        store, api = IntentStore(folder / "intent.sqlite"), FakeAPI(folder / "fake.sqlite", mode)
        engine = Engine(store, api, emit)
        emit(event="state_restored", intent_id=intent_id, idempotency_key=key,
             state=store.get(intent_id).state, details={})
        retry_blocked = False
        try:
            engine.dispatch(intent_id)
        except SafetyError:
            retry_blocked = True
        final = engine.reconcile(intent_id)
        duplicate_ok = None
        if final.state == "CONFIRMED":
            receipt = api.lookup(key)
            engine.deliver(intent_id, receipt)
            duplicate_ok = store.get(intent_id).state == "CONFIRMED"
        checks = {"one_send": api.send_count(key) == 1,
                  "blind_retry_blocked": retry_blocked,
                  "restored_unresolved_state": before == ("IN_FLIGHT" if crash else "UNKNOWN"),
                  "expected_final_state": final.state == expected}
        if duplicate_ok is not None:
            checks["duplicate_receipt_no_state_change"] = duplicate_ok
        results.append({"id": name, "state_before_restart": before,
                        "final_state": store.get(intent_id).state, "checks": checks,
                        "passed": all(checks.values())})
        store.close()
        api.close()

    name = "foreign_key_mismatch"
    folder = work / name
    folder.mkdir()
    intent_id, key = "SYN-INTENT-foreign", "SYN-KEY-foreign"
    store, api = IntentStore(folder / "intent.sqlite"), FakeAPI(folder / "fake.sqlite", "accept_then_timeout")
    engine = Engine(store, api, emitter(name))
    engine.prepare(intent_id, key)
    engine.dispatch(intent_id)
    original = api.lookup(key)
    blocked = False
    try:
        engine.deliver(intent_id, Receipt("SYN-KEY-other", original.payload_digest, "SYN-RECEIPT-other"))
    except SafetyError:
        blocked = True
    retry_blocked = False
    try:
        engine.dispatch(intent_id)
    except SafetyError:
        retry_blocked = True
    checks = {"foreign_receipt_blocked": blocked, "quarantined": store.get(intent_id).state == "ERROR",
              "blind_retry_blocked": retry_blocked, "one_send": api.send_count(key) == 1}
    results.append({"id": name, "final_state": store.get(intent_id).state,
                    "checks": checks, "passed": all(checks.values())})
    store.close()
    api.close()

    name = "corrupt_state"
    folder = work / name
    folder.mkdir()
    intent_id, key = "SYN-INTENT-corrupt", "SYN-KEY-corrupt"
    path = folder / "intent.sqlite"
    store = IntentStore(path)
    store.prepare(intent_id, key)
    store.close()
    # Controlled semantic corruption of synthetic local state, not an original.
    connection = sqlite3.connect(path)
    try:
        with connection:
            connection.execute("UPDATE intents SET state = 'UNTRUSTED'")
    finally:
        connection.close()
    blocked = False
    try:
        store = IntentStore(path)
    except StateIntegrityError:
        blocked = True
    emitter(name)(event="corrupt_state_blocked", intent_id=intent_id, idempotency_key=key,
                  state="UNAVAILABLE", details={"reopen_refused": blocked, "sends": 0})
    checks = {"reopen_refused": blocked, "no_api_constructed": not (folder / "fake.sqlite").exists()}
    results.append({"id": name, "final_state": "UNAVAILABLE", "checks": checks,
                    "passed": all(checks.values())})
    return {"version": __version__, "synthetic": True, "scope": "offline-demo-only",
            "passed": all(item["passed"] for item in results), "scenarios": results,
            "trace": trace}


def run(output: Path | None = None) -> dict:
    # SQLite files stay temporary even with --output. Only safe reports persist.
    with tempfile.TemporaryDirectory(prefix="robots-synthetic-") as temporary:
        report = scenarios(Path(temporary))
    if output is not None:
        output.mkdir(parents=True, exist_ok=True)
        (output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (output / "trace.jsonl").write_text(
            "".join(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n" for event in report["trace"]),
            encoding="utf-8",
        )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Persist only report.json and trace.jsonl here")
    args = parser.parse_args()
    report = run(args.output)
    print(json.dumps({"version": report["version"], "synthetic": True, "passed": report["passed"],
                      "scenarios": len(report["scenarios"]), "events": len(report["trace"]),
                      "reports_saved": args.output is not None}, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
