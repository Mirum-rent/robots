/* Derived from the verified synthetic Python report. Playback only. */
window.DEMO_RECORDING = {
  "synthetic": true,
  "source_report": "demo/reports/report.json",
  "source_report_sha256": "0bfe516e2540813ffbc5cad40d3f29238a65006012189522924f15d905d51f09",
  "metrics": [
    {
      "value": "31",
      "label": "тест демо · PASS"
    },
    {
      "value": "99.06%",
      "label": "строк · 2 модуля · trace"
    },
    {
      "value": "5",
      "label": "сценариев CLI · PASS"
    }
  ],
  "scenarios": [
    {
      "id": "accepted_unknown",
      "result": "CONFIRMED: одна отправка, сверка после перезапуска; повтор квитанции пропущен.",
      "events": [
        {
          "seq": 1,
          "scenario": "accepted_unknown",
          "event": "intent_committed",
          "intent_id": "SYN-INTENT-accepted_unknown",
          "idempotency_key": "SYN-KEY-accepted_unknown",
          "state": "PREPARED",
          "details": {
            "payload_digest": "3dd7cc9df3ae54aae1663cf1f0dc8eb0485d80b6bb6f9dc95a0fb6875d16550c"
          },
          "label": "Намерение сохранено",
          "description": "PREPARED · SYN-INTENT-accepted_unknown"
        },
        {
          "seq": 2,
          "scenario": "accepted_unknown",
          "event": "send_boundary_committed",
          "intent_id": "SYN-INTENT-accepted_unknown",
          "idempotency_key": "SYN-KEY-accepted_unknown",
          "state": "IN_FLIGHT",
          "details": {},
          "label": "Граница отправки сохранена",
          "description": "IN_FLIGHT · SYN-INTENT-accepted_unknown"
        },
        {
          "seq": 3,
          "scenario": "accepted_unknown",
          "event": "outcome_unknown",
          "intent_id": "SYN-INTENT-accepted_unknown",
          "idempotency_key": "SYN-KEY-accepted_unknown",
          "state": "UNKNOWN",
          "details": {},
          "label": "Ответ потерян: исход неизвестен",
          "description": "UNKNOWN · SYN-INTENT-accepted_unknown"
        },
        {
          "seq": 4,
          "scenario": "accepted_unknown",
          "event": "state_restored",
          "intent_id": "SYN-INTENT-accepted_unknown",
          "idempotency_key": "SYN-KEY-accepted_unknown",
          "state": "UNKNOWN",
          "details": {},
          "label": "Состояние восстановлено после перезапуска",
          "description": "UNKNOWN · SYN-INTENT-accepted_unknown"
        },
        {
          "seq": 5,
          "scenario": "accepted_unknown",
          "event": "blind_retry_blocked",
          "intent_id": "SYN-INTENT-accepted_unknown",
          "idempotency_key": "SYN-KEY-accepted_unknown",
          "state": "UNKNOWN",
          "details": {},
          "label": "Слепая повторная отправка запрещена",
          "description": "UNKNOWN · SYN-INTENT-accepted_unknown"
        },
        {
          "seq": 6,
          "scenario": "accepted_unknown",
          "event": "lookup_by_key",
          "intent_id": "SYN-INTENT-accepted_unknown",
          "idempotency_key": "SYN-KEY-accepted_unknown",
          "state": "UNKNOWN",
          "details": {},
          "label": "Сверка результата по ключу",
          "description": "UNKNOWN · SYN-INTENT-accepted_unknown"
        },
        {
          "seq": 7,
          "scenario": "accepted_unknown",
          "event": "receipt_confirmed",
          "intent_id": "SYN-INTENT-accepted_unknown",
          "idempotency_key": "SYN-KEY-accepted_unknown",
          "state": "CONFIRMED",
          "details": {
            "receipt_id": "SYN-RECEIPT-accepted_unknown"
          },
          "label": "Квитанция сверена: результат подтверждён",
          "description": "CONFIRMED · SYN-INTENT-accepted_unknown"
        },
        {
          "seq": 8,
          "scenario": "accepted_unknown",
          "event": "duplicate_receipt_ignored",
          "intent_id": "SYN-INTENT-accepted_unknown",
          "idempotency_key": "SYN-KEY-accepted_unknown",
          "state": "CONFIRMED",
          "details": {
            "receipt_id": "SYN-RECEIPT-accepted_unknown"
          },
          "label": "Повтор квитанции не меняет состояние",
          "description": "CONFIRMED · SYN-INTENT-accepted_unknown"
        }
      ]
    },
    {
      "id": "rejected_unknown",
      "result": "NOT_ACCEPTED: одна отправка. Вывод допустим только для полностью согласованного локального fake.",
      "events": [
        {
          "seq": 9,
          "scenario": "rejected_unknown",
          "event": "intent_committed",
          "intent_id": "SYN-INTENT-rejected_unknown",
          "idempotency_key": "SYN-KEY-rejected_unknown",
          "state": "PREPARED",
          "details": {
            "payload_digest": "3dd7cc9df3ae54aae1663cf1f0dc8eb0485d80b6bb6f9dc95a0fb6875d16550c"
          },
          "label": "Намерение сохранено",
          "description": "PREPARED · SYN-INTENT-rejected_unknown"
        },
        {
          "seq": 10,
          "scenario": "rejected_unknown",
          "event": "send_boundary_committed",
          "intent_id": "SYN-INTENT-rejected_unknown",
          "idempotency_key": "SYN-KEY-rejected_unknown",
          "state": "IN_FLIGHT",
          "details": {},
          "label": "Граница отправки сохранена",
          "description": "IN_FLIGHT · SYN-INTENT-rejected_unknown"
        },
        {
          "seq": 11,
          "scenario": "rejected_unknown",
          "event": "outcome_unknown",
          "intent_id": "SYN-INTENT-rejected_unknown",
          "idempotency_key": "SYN-KEY-rejected_unknown",
          "state": "UNKNOWN",
          "details": {},
          "label": "Ответ потерян: исход неизвестен",
          "description": "UNKNOWN · SYN-INTENT-rejected_unknown"
        },
        {
          "seq": 12,
          "scenario": "rejected_unknown",
          "event": "state_restored",
          "intent_id": "SYN-INTENT-rejected_unknown",
          "idempotency_key": "SYN-KEY-rejected_unknown",
          "state": "UNKNOWN",
          "details": {},
          "label": "Состояние восстановлено после перезапуска",
          "description": "UNKNOWN · SYN-INTENT-rejected_unknown"
        },
        {
          "seq": 13,
          "scenario": "rejected_unknown",
          "event": "blind_retry_blocked",
          "intent_id": "SYN-INTENT-rejected_unknown",
          "idempotency_key": "SYN-KEY-rejected_unknown",
          "state": "UNKNOWN",
          "details": {},
          "label": "Слепая повторная отправка запрещена",
          "description": "UNKNOWN · SYN-INTENT-rejected_unknown"
        },
        {
          "seq": 14,
          "scenario": "rejected_unknown",
          "event": "lookup_by_key",
          "intent_id": "SYN-INTENT-rejected_unknown",
          "idempotency_key": "SYN-KEY-rejected_unknown",
          "state": "UNKNOWN",
          "details": {},
          "label": "Сверка результата по ключу",
          "description": "UNKNOWN · SYN-INTENT-rejected_unknown"
        },
        {
          "seq": 15,
          "scenario": "rejected_unknown",
          "event": "absence_confirmed_by_fake",
          "intent_id": "SYN-INTENT-rejected_unknown",
          "idempotency_key": "SYN-KEY-rejected_unknown",
          "state": "NOT_ACCEPTED",
          "details": {},
          "label": "Локальный fake авторитетно подтвердил отсутствие",
          "description": "NOT_ACCEPTED · SYN-INTENT-rejected_unknown"
        }
      ]
    },
    {
      "id": "restart_before_ack",
      "result": "CONFIRMED: восстановлено IN_FLIGHT, слепой повтор заблокирован; повтор квитанции пропущен.",
      "events": [
        {
          "seq": 16,
          "scenario": "restart_before_ack",
          "event": "intent_committed",
          "intent_id": "SYN-INTENT-restart_before_ack",
          "idempotency_key": "SYN-KEY-restart_before_ack",
          "state": "PREPARED",
          "details": {
            "payload_digest": "3dd7cc9df3ae54aae1663cf1f0dc8eb0485d80b6bb6f9dc95a0fb6875d16550c"
          },
          "label": "Намерение сохранено",
          "description": "PREPARED · SYN-INTENT-restart_before_ack"
        },
        {
          "seq": 17,
          "scenario": "restart_before_ack",
          "event": "send_boundary_committed",
          "intent_id": "SYN-INTENT-restart_before_ack",
          "idempotency_key": "SYN-KEY-restart_before_ack",
          "state": "IN_FLIGHT",
          "details": {},
          "label": "Граница отправки сохранена",
          "description": "IN_FLIGHT · SYN-INTENT-restart_before_ack"
        },
        {
          "seq": 18,
          "scenario": "restart_before_ack",
          "event": "simulated_process_stop",
          "intent_id": "SYN-INTENT-restart_before_ack",
          "idempotency_key": "SYN-KEY-restart_before_ack",
          "state": "IN_FLIGHT",
          "details": {},
          "label": "Остановка до локального подтверждения",
          "description": "IN_FLIGHT · SYN-INTENT-restart_before_ack"
        },
        {
          "seq": 19,
          "scenario": "restart_before_ack",
          "event": "state_restored",
          "intent_id": "SYN-INTENT-restart_before_ack",
          "idempotency_key": "SYN-KEY-restart_before_ack",
          "state": "IN_FLIGHT",
          "details": {},
          "label": "Состояние восстановлено после перезапуска",
          "description": "IN_FLIGHT · SYN-INTENT-restart_before_ack"
        },
        {
          "seq": 20,
          "scenario": "restart_before_ack",
          "event": "blind_retry_blocked",
          "intent_id": "SYN-INTENT-restart_before_ack",
          "idempotency_key": "SYN-KEY-restart_before_ack",
          "state": "IN_FLIGHT",
          "details": {},
          "label": "Слепая повторная отправка запрещена",
          "description": "IN_FLIGHT · SYN-INTENT-restart_before_ack"
        },
        {
          "seq": 21,
          "scenario": "restart_before_ack",
          "event": "lookup_by_key",
          "intent_id": "SYN-INTENT-restart_before_ack",
          "idempotency_key": "SYN-KEY-restart_before_ack",
          "state": "IN_FLIGHT",
          "details": {},
          "label": "Сверка результата по ключу",
          "description": "IN_FLIGHT · SYN-INTENT-restart_before_ack"
        },
        {
          "seq": 22,
          "scenario": "restart_before_ack",
          "event": "receipt_confirmed",
          "intent_id": "SYN-INTENT-restart_before_ack",
          "idempotency_key": "SYN-KEY-restart_before_ack",
          "state": "CONFIRMED",
          "details": {
            "receipt_id": "SYN-RECEIPT-restart_before_ack"
          },
          "label": "Квитанция сверена: результат подтверждён",
          "description": "CONFIRMED · SYN-INTENT-restart_before_ack"
        },
        {
          "seq": 23,
          "scenario": "restart_before_ack",
          "event": "duplicate_receipt_ignored",
          "intent_id": "SYN-INTENT-restart_before_ack",
          "idempotency_key": "SYN-KEY-restart_before_ack",
          "state": "CONFIRMED",
          "details": {
            "receipt_id": "SYN-RECEIPT-restart_before_ack"
          },
          "label": "Повтор квитанции не меняет состояние",
          "description": "CONFIRMED · SYN-INTENT-restart_before_ack"
        }
      ]
    },
    {
      "id": "foreign_key_mismatch",
      "result": "ERROR: конфликт квитанции; повторная отправка заблокирована.",
      "events": [
        {
          "seq": 24,
          "scenario": "foreign_key_mismatch",
          "event": "intent_committed",
          "intent_id": "SYN-INTENT-foreign",
          "idempotency_key": "SYN-KEY-foreign",
          "state": "PREPARED",
          "details": {
            "payload_digest": "3dd7cc9df3ae54aae1663cf1f0dc8eb0485d80b6bb6f9dc95a0fb6875d16550c"
          },
          "label": "Намерение сохранено",
          "description": "PREPARED · SYN-INTENT-foreign"
        },
        {
          "seq": 25,
          "scenario": "foreign_key_mismatch",
          "event": "send_boundary_committed",
          "intent_id": "SYN-INTENT-foreign",
          "idempotency_key": "SYN-KEY-foreign",
          "state": "IN_FLIGHT",
          "details": {},
          "label": "Граница отправки сохранена",
          "description": "IN_FLIGHT · SYN-INTENT-foreign"
        },
        {
          "seq": 26,
          "scenario": "foreign_key_mismatch",
          "event": "outcome_unknown",
          "intent_id": "SYN-INTENT-foreign",
          "idempotency_key": "SYN-KEY-foreign",
          "state": "UNKNOWN",
          "details": {},
          "label": "Ответ потерян: исход неизвестен",
          "description": "UNKNOWN · SYN-INTENT-foreign"
        },
        {
          "seq": 27,
          "scenario": "foreign_key_mismatch",
          "event": "foreign_receipt_blocked",
          "intent_id": "SYN-INTENT-foreign",
          "idempotency_key": "SYN-KEY-foreign",
          "state": "ERROR",
          "details": {},
          "label": "Чужой ключ или содержимое: блокировка",
          "description": "ERROR · SYN-INTENT-foreign"
        },
        {
          "seq": 28,
          "scenario": "foreign_key_mismatch",
          "event": "blind_retry_blocked",
          "intent_id": "SYN-INTENT-foreign",
          "idempotency_key": "SYN-KEY-foreign",
          "state": "ERROR",
          "details": {},
          "label": "Слепая повторная отправка запрещена",
          "description": "ERROR · SYN-INTENT-foreign"
        }
      ]
    },
    {
      "id": "corrupt_state",
      "result": "UNAVAILABLE: повреждённая база не открыта, API не создан, отправок нет.",
      "events": [
        {
          "seq": 29,
          "scenario": "corrupt_state",
          "event": "corrupt_state_blocked",
          "intent_id": "SYN-INTENT-corrupt",
          "idempotency_key": "SYN-KEY-corrupt",
          "state": "UNAVAILABLE",
          "details": {
            "reopen_refused": true,
            "sends": 0
          },
          "label": "Повреждённая база: открытие запрещено",
          "description": "UNAVAILABLE · SYN-INTENT-corrupt"
        }
      ]
    }
  ]
};
