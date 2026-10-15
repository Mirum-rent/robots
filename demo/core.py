"""Durable intent and reconciliation, independent of any network or strategy."""

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import sqlite3
from typing import Callable, Protocol


STATES = frozenset({"PREPARED", "IN_FLIGHT", "UNKNOWN", "CONFIRMED", "NOT_ACCEPTED", "ERROR"})
TRANSITIONS = {
    "PREPARED": {"IN_FLIGHT"},
    "IN_FLIGHT": {"UNKNOWN", "CONFIRMED", "NOT_ACCEPTED", "ERROR"},
    "UNKNOWN": {"CONFIRMED", "NOT_ACCEPTED", "ERROR"},
    "CONFIRMED": {"ERROR"},
    "NOT_ACCEPTED": set(),
    "ERROR": set(),
}
PAYLOAD = {"operation": "record_sample", "sample": "SYNTHETIC-SAMPLE"}


class SafetyError(Exception):
    """The local state cannot authorize this operation."""


class StateIntegrityError(SafetyError):
    """Stored data is unreadable or violates the demonstrator's contract."""


class OutcomeUnknown(Exception):
    """The caller cannot infer acceptance from this transport outcome."""


class SimulatedCrash(Exception):
    """Deliberate stop after the fake service responds, before local ack."""


def digest(payload: dict) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Intent:
    intent_id: str
    key: str
    payload: dict
    payload_digest: str
    state: str


@dataclass(frozen=True)
class Receipt:
    key: str
    payload_digest: str
    receipt_id: str


class SampleAPI(Protocol):
    def send(self, key: str, payload: dict) -> Receipt: ...

    def lookup(self, key: str) -> Receipt | None: ...


class IntentStore:
    """SQLite commits the intent and send boundary before an external effect.

    This is a small single-process demonstration, not a production database
    migration or remote-service exactly-once contract.
    """

    def __init__(self, path: Path):
        existing = path.exists()
        self.db = None
        try:
            self.db = sqlite3.connect(path)
            self.db.row_factory = sqlite3.Row
            self.db.execute("PRAGMA synchronous=FULL")
            if not existing:
                with self.db:
                    self.db.execute("CREATE TABLE metadata (version INTEGER NOT NULL)")
                    self.db.execute("INSERT INTO metadata VALUES (1)")
                    self.db.execute("""CREATE TABLE intents (
                        intent_id TEXT PRIMARY KEY, key TEXT NOT NULL UNIQUE,
                        payload TEXT NOT NULL, payload_digest TEXT NOT NULL,
                        state TEXT NOT NULL)""")
            versions = self.db.execute("SELECT version FROM metadata").fetchall()
            if len(versions) != 1 or versions[0][0] != 1:
                raise StateIntegrityError("Unsupported or ambiguous state version")
            if self.db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                raise StateIntegrityError("SQLite integrity check failed")
            for row in self.db.execute("SELECT * FROM intents"):
                self._decode(row)
        except (sqlite3.Error, StateIntegrityError) as exc:
            self.close()
            raise StateIntegrityError("State cannot be trusted; sending is disabled") from exc

    def close(self) -> None:
        if self.db is not None:
            self.db.close()
            self.db = None

    @staticmethod
    def _decode(row: sqlite3.Row) -> Intent:
        try:
            payload = json.loads(row["payload"])
            valid = (
                row["state"] in STATES
                and row["intent_id"].startswith("SYN-INTENT-")
                and row["key"].startswith("SYN-KEY-")
                and payload == PAYLOAD
                and digest(payload) == row["payload_digest"]
            )
            if not valid:
                raise ValueError("Invalid intent")
            return Intent(row["intent_id"], row["key"], payload, row["payload_digest"], row["state"])
        except (TypeError, ValueError, IndexError, KeyError, AttributeError) as exc:
            raise StateIntegrityError("Invalid durable intent") from exc

    def prepare(self, intent_id: str, key: str) -> Intent:
        payload = json.dumps(PAYLOAD, sort_keys=True)
        candidate = {"intent_id": intent_id, "key": key, "payload": payload,
                     "payload_digest": digest(PAYLOAD), "state": "PREPARED"}
        self._decode(candidate)
        try:
            with self.db:
                self.db.execute("INSERT INTO intents VALUES (?, ?, ?, ?, ?)", tuple(candidate.values()))
        except sqlite3.IntegrityError as exc:
            raise SafetyError("Intent or idempotency key already exists") from exc
        return self.get(intent_id)

    def get(self, intent_id: str) -> Intent:
        row = self.db.execute("SELECT * FROM intents WHERE intent_id = ?", (intent_id,)).fetchone()
        if row is None:
            raise SafetyError("Unknown intent")
        return self._decode(row)

    def transition(self, intent_id: str, expected: set[str], target: str) -> Intent:
        if target not in STATES or not expected or not expected <= STATES:
            raise SafetyError("Invalid state transition request")
        with self.db:
            current = self.get(intent_id)
            if current.state not in expected:
                raise SafetyError("Current state does not authorize this transition")
            if target not in TRANSITIONS[current.state]:
                raise SafetyError("The state machine forbids this transition")
            result = self.db.execute(
                "UPDATE intents SET state = ? WHERE intent_id = ? AND state = ?",
                (target, intent_id, current.state),
            )
            if result.rowcount != 1:
                raise SafetyError("State changed concurrently")
        return self.get(intent_id)


class Engine:
    def __init__(self, store: IntentStore, api: SampleAPI, emit: Callable[..., None]):
        self.store, self.api, self.emit = store, api, emit

    def _event(self, event: str, intent: Intent, **details) -> None:
        self.emit(event=event, intent_id=intent.intent_id, idempotency_key=intent.key,
                  state=intent.state, details=details)

    def prepare(self, intent_id: str, key: str) -> Intent:
        intent = self.store.prepare(intent_id, key)
        self._event("intent_committed", intent, payload_digest=intent.payload_digest)
        return intent

    def dispatch(self, intent_id: str, *, crash_after_send: bool = False) -> Intent:
        intent = self.store.get(intent_id)
        if intent.state != "PREPARED":
            self._event("blind_retry_blocked", intent)
            raise SafetyError("Only a never-sent PREPARED intent may be sent")
        intent = self.store.transition(intent_id, {"PREPARED"}, "IN_FLIGHT")
        self._event("send_boundary_committed", intent)
        try:
            receipt = self.api.send(intent.key, intent.payload)
        except OutcomeUnknown:
            intent = self.store.transition(intent_id, {"IN_FLIGHT"}, "UNKNOWN")
            self._event("outcome_unknown", intent)
            return intent
        except Exception:
            # An unexpected adapter failure is equally ambiguous. Never retry.
            intent = self.store.transition(intent_id, {"IN_FLIGHT"}, "UNKNOWN")
            self._event("adapter_error_unknown", intent)
            return intent
        if crash_after_send:
            self._event("simulated_process_stop", intent)
            raise SimulatedCrash("Restart required; do not dispatch again")
        return self.deliver(intent_id, receipt)

    def deliver(self, intent_id: str, receipt: Receipt) -> Intent:
        intent = self.store.get(intent_id)
        if receipt.key != intent.key or receipt.payload_digest != intent.payload_digest:
            if intent.state in {"IN_FLIGHT", "UNKNOWN", "CONFIRMED"}:
                intent = self.store.transition(intent_id, {intent.state}, "ERROR")
            self._event("foreign_receipt_blocked", intent)
            raise SafetyError("Receipt key or payload digest does not match")
        if intent.state == "CONFIRMED":
            self._event("duplicate_receipt_ignored", intent, receipt_id=receipt.receipt_id)
            return intent
        if intent.state not in {"IN_FLIGHT", "UNKNOWN"}:
            self._event("receipt_state_blocked", intent)
            raise SafetyError("Receipt cannot confirm this state")
        intent = self.store.transition(intent_id, {intent.state}, "CONFIRMED")
        self._event("receipt_confirmed", intent, receipt_id=receipt.receipt_id)
        return intent

    def reconcile(self, intent_id: str) -> Intent:
        intent = self.store.get(intent_id)
        if intent.state not in {"IN_FLIGHT", "UNKNOWN"}:
            raise SafetyError("Only an unresolved send may be reconciled")
        self._event("lookup_by_key", intent)
        try:
            receipt = self.api.lookup(intent.key)
        except Exception as exc:
            self._event("lookup_unavailable", intent)
            raise SafetyError("Lookup failed; uncertainty is preserved") from exc
        if receipt is not None:
            return self.deliver(intent_id, receipt)
        # This in-process fake is authoritative and strongly consistent.
        # A real eventually-consistent API must NOT infer rejection this way.
        intent = self.store.transition(intent_id, {intent.state}, "NOT_ACCEPTED")
        self._event("absence_confirmed_by_fake", intent)
        return intent
