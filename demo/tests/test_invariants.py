import json
from pathlib import Path
import sqlite3
import tempfile
import unittest

from demo.core import (Engine, IntentStore, PAYLOAD, Receipt, SafetyError,
                       SimulatedCrash, StateIntegrityError, digest)
from demo.fake_api import FakeAPI
from demo.run import run


class ReliabilityTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="robots-demo-test-")
        self.folder = Path(self.temporary.name)
        self.intent_id, self.key = "SYN-INTENT-test", "SYN-KEY-test"
        self.store = IntentStore(self.folder / "intent.sqlite")
        self.api = FakeAPI(self.folder / "fake.sqlite")
        self.events = []
        self.engine = Engine(self.store, self.api, lambda **event: self.events.append(event))

    def tearDown(self):
        self.store.close()
        self.api.close()
        self.temporary.cleanup()

    def prepare(self):
        return self.engine.prepare(self.intent_id, self.key)

    def use_mode(self, mode):
        self.api.mode = mode

    def restart(self):
        self.store.close()
        self.api.close()
        self.store = IntentStore(self.folder / "intent.sqlite")
        self.api = FakeAPI(self.folder / "fake.sqlite")
        self.engine = Engine(self.store, self.api, lambda **event: self.events.append(event))

    def test_intent_is_committed_before_api_can_observe_send(self):
        self.prepare()
        parent = self

        class ObservingAPI:
            def send(self, key, payload):
                observer = IntentStore(parent.folder / "intent.sqlite")
                try:
                    parent.assertEqual(observer.get(parent.intent_id).state, "IN_FLIGHT")
                    parent.assertEqual(observer.get(parent.intent_id).payload, PAYLOAD)
                finally:
                    observer.close()
                return parent.api.send(key, payload)

        self.engine.api = ObservingAPI()
        self.assertEqual(self.engine.dispatch(self.intent_id).state, "CONFIRMED")
        self.assertEqual([event["event"] for event in self.events],
                         ["intent_committed", "send_boundary_committed", "receipt_confirmed"])

    def test_accepted_unknown_is_reconciled_after_restart_without_second_send(self):
        self.prepare()
        self.use_mode("accept_then_timeout")
        self.assertEqual(self.engine.dispatch(self.intent_id).state, "UNKNOWN")
        self.restart()
        with self.assertRaises(SafetyError):
            self.engine.dispatch(self.intent_id)
        self.assertEqual(self.engine.reconcile(self.intent_id).state, "CONFIRMED")
        self.assertEqual(self.api.send_count(self.key), 1)

    def test_not_accepted_unknown_stays_terminal_without_retry(self):
        self.prepare()
        self.use_mode("reject_then_timeout")
        self.engine.dispatch(self.intent_id)
        self.restart()
        self.assertEqual(self.engine.reconcile(self.intent_id).state, "NOT_ACCEPTED")
        with self.assertRaises(SafetyError):
            self.engine.dispatch(self.intent_id)
        self.assertEqual(self.api.send_count(self.key), 1)
        self.assertIsNone(self.api.lookup(self.key))

    def test_crash_after_effect_before_ack_preserves_uncertainty(self):
        self.prepare()
        with self.assertRaises(SimulatedCrash):
            self.engine.dispatch(self.intent_id, crash_after_send=True)
        self.restart()
        self.assertEqual(self.store.get(self.intent_id).state, "IN_FLIGHT")
        with self.assertRaises(SafetyError):
            self.engine.dispatch(self.intent_id)
        self.assertEqual(self.engine.reconcile(self.intent_id).state, "CONFIRMED")
        self.assertEqual(self.api.send_count(self.key), 1)

    def test_duplicate_receipt_after_restart_is_idempotent(self):
        self.prepare()
        self.engine.dispatch(self.intent_id)
        receipt = self.api.lookup(self.key)
        self.restart()
        self.engine.deliver(self.intent_id, receipt)
        self.engine.deliver(self.intent_id, receipt)
        self.assertEqual(self.store.get(self.intent_id).state, "CONFIRMED")
        self.assertEqual(self.api.send_count(self.key), 1)
        self.assertEqual(self.events[-1]["event"], "duplicate_receipt_ignored")

    def test_foreign_key_receipt_quarantines_unresolved_intent(self):
        intent = self.prepare()
        self.use_mode("accept_then_timeout")
        self.engine.dispatch(self.intent_id)
        foreign = Receipt("SYN-KEY-someone-else", intent.payload_digest, "SYN-RECEIPT-foreign")
        with self.assertRaises(SafetyError):
            self.engine.deliver(self.intent_id, foreign)
        self.assertEqual(self.store.get(self.intent_id).state, "ERROR")
        with self.assertRaises(SafetyError):
            self.engine.dispatch(self.intent_id)
        self.assertEqual(self.api.send_count(self.key), 1)

    def test_same_key_wrong_payload_receipt_cannot_confirm(self):
        self.prepare()
        self.use_mode("accept_then_timeout")
        self.engine.dispatch(self.intent_id)
        with self.assertRaises(SafetyError):
            self.engine.deliver(self.intent_id, Receipt(self.key, "0" * 64, "SYN-RECEIPT-wrong"))
        self.assertEqual(self.store.get(self.intent_id).state, "ERROR")

    def test_foreign_receipt_also_quarantines_already_confirmed_state(self):
        self.prepare()
        self.engine.dispatch(self.intent_id)
        with self.assertRaises(SafetyError):
            self.engine.deliver(self.intent_id, Receipt("SYN-KEY-foreign", digest(PAYLOAD), "SYN-RECEIPT-foreign"))
        self.assertEqual(self.store.get(self.intent_id).state, "ERROR")

    def test_error_state_cannot_be_confirmed_by_later_receipt(self):
        self.prepare()
        self.use_mode("accept_then_timeout")
        self.engine.dispatch(self.intent_id)
        receipt = self.api.lookup(self.key)
        self.store.transition(self.intent_id, {"UNKNOWN"}, "ERROR")
        with self.assertRaises(SafetyError):
            self.engine.deliver(self.intent_id, receipt)
        self.assertEqual(self.store.get(self.intent_id).state, "ERROR")

    def test_receipt_before_dispatch_cannot_skip_send_boundary(self):
        intent = self.prepare()
        with self.assertRaises(SafetyError):
            self.engine.deliver(self.intent_id, Receipt(self.key, intent.payload_digest, "SYN-RECEIPT-early"))
        self.assertEqual(self.store.get(self.intent_id).state, "PREPARED")
        self.assertEqual(self.api.send_count(self.key), 0)

    def test_unknown_intent_does_not_send(self):
        with self.assertRaises(SafetyError):
            self.engine.dispatch("SYN-INTENT-missing")
        self.assertEqual(self.api.send_count(self.key), 0)

    def test_one_idempotency_key_cannot_authorize_two_intents(self):
        self.prepare()
        with self.assertRaises(SafetyError):
            self.store.prepare("SYN-INTENT-second", self.key)
        with self.assertRaises(SafetyError):
            self.store.prepare(self.intent_id, "SYN-KEY-second")
        self.assertEqual(self.store.get(self.intent_id).state, "PREPARED")

    def test_invalid_synthetic_identifier_is_rejected_before_persisting(self):
        with self.assertRaises(StateIntegrityError):
            self.store.prepare("real-identifier", self.key)
        self.assertEqual(self.api.send_count(self.key), 0)

    def test_terminal_state_cannot_be_reset_to_prepared(self):
        self.prepare()
        self.engine.dispatch(self.intent_id)
        with self.assertRaises(SafetyError):
            self.store.transition(self.intent_id, {"CONFIRMED"}, "PREPARED")
        with self.assertRaises(SafetyError):
            self.store.transition(self.intent_id, {"UNKNOWN"}, "ERROR")
        with self.assertRaises(SafetyError):
            self.store.transition(self.intent_id, set(), "UNKNOWN")
        with self.assertRaises(SafetyError):
            self.store.transition(self.intent_id, {"CONFIRMED"}, "INVALID")
        self.assertEqual(self.store.get(self.intent_id).state, "CONFIRMED")

    def test_reconcile_requires_an_unresolved_send(self):
        self.prepare()
        with self.assertRaises(SafetyError):
            self.engine.reconcile(self.intent_id)
        self.assertEqual(self.api.send_count(self.key), 0)

    def test_unavailable_lookup_does_not_infer_nonacceptance(self):
        self.prepare()
        self.use_mode("accept_then_timeout")
        self.engine.dispatch(self.intent_id)

        class UnavailableLookup:
            def lookup(self, key):
                raise RuntimeError("synthetic lookup unavailable")

        self.engine.api = UnavailableLookup()
        with self.assertRaises(SafetyError):
            self.engine.reconcile(self.intent_id)
        self.assertEqual(self.store.get(self.intent_id).state, "UNKNOWN")
        self.assertEqual(self.api.send_count(self.key), 1)

    def test_unexpected_adapter_error_after_acceptance_is_unknown(self):
        self.prepare()
        parent = self

        class UnexpectedFailure:
            def send(self, key, payload):
                parent.api.send(key, payload)
                raise RuntimeError("synthetic response decoder failed")

        self.engine.api = UnexpectedFailure()
        self.assertEqual(self.engine.dispatch(self.intent_id).state, "UNKNOWN")
        self.engine.api = self.api
        self.assertEqual(self.engine.reconcile(self.intent_id).state, "CONFIRMED")
        self.assertEqual(self.api.send_count(self.key), 1)

    def test_fake_reuses_a_matching_receipt_for_the_same_key(self):
        first = self.api.send(self.key, PAYLOAD)
        second = self.api.send(self.key, dict(PAYLOAD))
        self.assertEqual(first, second)
        self.assertEqual(self.api.send_count(self.key), 2)

    def test_fake_refuses_same_key_with_changed_payload(self):
        first = self.api.send(self.key, PAYLOAD)
        with self.assertRaises(SafetyError):
            self.api.send(self.key, {"operation": "changed"})
        self.assertEqual(self.api.lookup(self.key), first)

    def test_fake_rejects_unknown_mode(self):
        with self.assertRaises(ValueError):
            FakeAPI(self.folder / "unused.sqlite", mode="real-network")
        self.assertFalse((self.folder / "unused.sqlite").exists())

    def assert_reopen_rejected(self):
        with self.assertRaises(StateIntegrityError):
            IntentStore(self.folder / "intent.sqlite")

    def test_semantically_corrupt_state_disables_startup(self):
        self.prepare()
        self.store.db.execute("UPDATE intents SET state = 'CORRUPT'")
        self.store.db.commit()
        self.store.close()
        self.assert_reopen_rejected()
        self.assertEqual(self.api.send_count(self.key), 0)

    def test_payload_tampering_disables_startup(self):
        self.prepare()
        self.store.db.execute("UPDATE intents SET payload = ?", (json.dumps({"operation": "changed"}),))
        self.store.db.commit()
        self.store.close()
        self.assert_reopen_rejected()

    def test_digest_tampering_disables_startup(self):
        self.prepare()
        self.store.db.execute("UPDATE intents SET payload_digest = 'invalid'")
        self.store.db.commit()
        self.store.close()
        self.assert_reopen_rejected()

    def test_malformed_json_disables_startup(self):
        self.prepare()
        self.store.db.execute("UPDATE intents SET payload = 'invalid-json'")
        self.store.db.commit()
        self.store.close()
        self.assert_reopen_rejected()

    def test_unsupported_schema_disables_startup(self):
        self.store.db.execute("UPDATE metadata SET version = 2")
        self.store.db.commit()
        self.store.close()
        self.assert_reopen_rejected()

    def test_ambiguous_schema_disables_startup(self):
        self.store.db.execute("INSERT INTO metadata VALUES (1)")
        self.store.db.commit()
        self.store.close()
        self.assert_reopen_rejected()

    def test_unreadable_database_is_not_silently_recreated(self):
        self.store.close()
        path = self.folder / "intent.sqlite"
        path.write_bytes(b"SYNTHETIC INVALID SQLITE FILE")
        before = path.read_bytes()
        self.assert_reopen_rejected()
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(self.api.send_count(self.key), 0)

    def test_existing_empty_file_is_not_treated_as_new_state(self):
        self.store.close()
        (self.folder / "intent.sqlite").write_bytes(b"")
        self.assert_reopen_rejected()

    def test_two_open_engines_do_not_send_a_confirmed_intent_twice(self):
        self.prepare()
        second = IntentStore(self.folder / "intent.sqlite")
        try:
            other = Engine(second, self.api, lambda **event: None)
            self.engine.dispatch(self.intent_id)
            with self.assertRaises(SafetyError):
                other.dispatch(self.intent_id)
            self.assertEqual(self.api.send_count(self.key), 1)
        finally:
            second.close()


class ScenarioTests(unittest.TestCase):
    def test_all_scenarios_pass_and_report_is_deterministic(self):
        first, second = run(), run()
        self.assertEqual(first, second)
        self.assertTrue(first["passed"])
        self.assertEqual(len(first["scenarios"]), 5)
        self.assertEqual([event["seq"] for event in first["trace"]], list(range(1, len(first["trace"]) + 1)))
        self.assertTrue(all(event["intent_id"].startswith("SYN-INTENT-") for event in first["trace"]))

    def test_explicit_output_persists_only_safe_reports(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "reports"
            report = run(output)
            self.assertEqual({path.name for path in output.iterdir()}, {"report.json", "trace.jsonl"})
            self.assertEqual(json.loads((output / "report.json").read_text(encoding="utf-8")), report)
            trace = [json.loads(line) for line in (output / "trace.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual(trace, report["trace"])


if __name__ == "__main__":
    unittest.main()
