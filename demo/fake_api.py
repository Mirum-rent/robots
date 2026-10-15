"""An in-process SQLite fake. It has no socket, URL, account or credentials."""

from pathlib import Path
import sqlite3

from .core import OutcomeUnknown, Receipt, SafetyError, digest


class FakeAPI:
    MODES = {"accept", "accept_then_timeout", "reject_then_timeout"}

    def __init__(self, path: Path, mode: str = "accept"):
        if mode not in self.MODES:
            raise ValueError("Unknown fake mode")
        self.mode = mode
        self.db = sqlite3.connect(path)
        with self.db:
            self.db.execute("""CREATE TABLE IF NOT EXISTS receipts (
                key TEXT PRIMARY KEY, payload_digest TEXT NOT NULL, receipt_id TEXT NOT NULL)""")
            self.db.execute("CREATE TABLE IF NOT EXISTS calls (key TEXT NOT NULL)")

    def close(self) -> None:
        self.db.close()

    def send(self, key: str, payload: dict) -> Receipt:
        payload_digest = digest(payload)
        with self.db:
            self.db.execute("INSERT INTO calls VALUES (?)", (key,))
            existing = self.lookup(key)
            if existing is not None and existing.payload_digest != payload_digest:
                raise SafetyError("Same key with different payload")
            if self.mode != "reject_then_timeout" and existing is None:
                receipt_id = "SYN-RECEIPT-" + key.removeprefix("SYN-KEY-")
                self.db.execute("INSERT INTO receipts VALUES (?, ?, ?)",
                                (key, payload_digest, receipt_id))
        if self.mode in {"accept_then_timeout", "reject_then_timeout"}:
            raise OutcomeUnknown("Simulated response loss; acceptance is unknown to caller")
        return self.lookup(key)

    def lookup(self, key: str) -> Receipt | None:
        row = self.db.execute("SELECT key, payload_digest, receipt_id FROM receipts WHERE key = ?", (key,)).fetchone()
        return Receipt(*row) if row else None

    def send_count(self, key: str) -> int:
        return self.db.execute("SELECT COUNT(*) FROM calls WHERE key = ?", (key,)).fetchone()[0]
