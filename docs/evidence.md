# Реестр доказательств и метрик

[На главную](../README.md) · [Машинный реестр](../data/evidence.json)

Проверено чтением материалов 15.10.2026. Оригиналы реальных проектов не изменялись и не запускались; сырые источники в комплект не включены. Исторические результаты относятся только к указанной версии. Публичный реестр — обезличенная сводка, а не публикация исходных отчётов.

| Статус | Значение |
| --- | --- |
| VERIFIED_STATIC | В этом проходе прочитан/хеширован файл, проверена структура или состав |
| HISTORICAL_REPORT | Прочитан сохранённый результат; соответствующее исполнение здесь не повторялось |
| VERIFIED_RUNTIME | В этом проходе выполнен точно описанный сценарий нового демо |
| USER_REPORT | Сведения сообщены владельцем, уровень технического подтверждения указан отдельно |
| PROPOSAL | Предложение, а не реализованное поведение |
| UNKNOWN | Требуемых доказательств пока нет |

<a id="dart"></a>

## DARTherapeX

### DTX-EVOLUTION

**Документирована эволюция от сценария/монолита к структуре: совместимость SDK/Protobuf, согласование состояния, устранение fallback-путей и систематические аудиты**

Версия: Паспорт 14.09.2026; последующий снимок 30.02 рассматривается отдельно. Дата: 2026-09-14. Статус: **HISTORICAL_REPORT**.

Проверка: Прочитаны разделы паспорта об эволюции и работе над ошибками; структура более позднего снимка проверена отдельно.

Источник: [DTX-PASSPORT](#source-dtx-passport), [DTX-APPENDIX](#source-dtx-appendix).

Граница: Исторический анализ процесса не подтверждает автоматически отсутствие дефектов или исполнение всех путей последующего выпуска.

### DTX-30-SCALE

**622 main Java; 721 test Java; 1369 файлов архива**

Версия: 30.02 / sourceTree bb85e20d. Дата: 2026-10-13. Статус: **VERIFIED_STATIC**.

Проверка: Список ZIP, SHA256 raw bytes; 1368 внутренних контрольных сумм и 1355 файлов source manifest сверены без расхождений.

Источник: [DTX-ARCHIVE](#source-dtx-archive), [DTX-BUILD](#source-dtx-build), [DTX-MANIFEST](#source-dtx-manifest).

Граница: Файлы тестового кода не равны тестам. Для этого архива результаты полного тестового прогона и измеренное покрытие не установлены.

### DTX-30-ARCH

**8 именованных слоёв; 39 интерфейсов domain ports; Java 17 / SDK / gRPC / Protobuf**

Версия: 30.02. Дата: 2026-10-13. Статус: **VERIFIED_STATIC**.

Проверка: Структура архива, декларации pom.xml, выбранные порты и службы прочитаны.

Источник: [DTX-ARCHIVE](#source-dtx-archive), [DTX-POM](#source-dtx-pom), [DTX-CODE-1](#source-dtx-code-1), [DTX-CODE-2](#source-dtx-code-2), [DTX-CODE-3](#source-dtx-code-3), [DTX-CODE-4](#source-dtx-code-4), [DTX-CODE-5](#source-dtx-code-5).

Граница: Наличие архитектурных границ не подтверждает успешное исполнение всех ветвей восстановления.

### DTX-OLD-TESTS

**5471 tests; failures/errors/skipped 0/0/0; 262 XML suites по паспорту**

Версия: 30.01 / tf-policy-split-20260914; 488 main / 274 test Java. Дата: 2026-09-14. Статус: **HISTORICAL_REPORT**.

Проверка: Сверены исходные паспорт и приложение DOCX. Вложенный source.zip пересчитан и сопоставлен по SHA256.

Источник: [DTX-PASSPORT](#source-dtx-passport), [DTX-APPENDIX](#source-dtx-appendix), [DTX-OLD-SOURCE](#source-dtx-old-source).

Граница: Точное время прогона и raw Surefire XML не найдены в доступном контейнере. Подтверждено содержание исторического документа, а не повторный прогон. Не относится к выпуску 622/721.

### DTX-OLD-COVERAGE

**JaCoCo global LINE 67.8461%; 248 критических классов: порог LINE ≥80.01%, минимум 81.4978%**

Версия: 30.01 / tf-policy-split-20260914. Дата: 2026-09-14. Статус: **HISTORICAL_REPORT**.

Проверка: Числа и область сопоставлены в паспорте и приложении; глобальный BRANCH неизвестен.

Источник: [DTX-PASSPORT](#source-dtx-passport), [DTX-APPENDIX](#source-dtx-appendix).

Граница: Raw JaCoCo-отчёт не найден во вложенном source.zip. Это историческое документальное утверждение; не покрытие выпуска 30.02 и не гарантия качества.

<a id="neuro"></a>

## DARNeuroX

### N26-ARCH

**Python runtime, REST/WebSocket, координация чтений, TradingEngine/runtime mixins, SQLite ledger, версионные JSON/JSONL**

Версия: Карта CodeX_active_path_v.2.4 + выбранные исходники релиза 2.6. Дата: 2026-10-15 (дата чтения). Статус: **VERIFIED_STATIC**.

Проверка: Прочитаны карта активного пути и выбранные файлы 2.6: engine.py, cli.py, runtime_io.py, ledger.py, storage.py.

Источник: [N-ARCH](#source-n-arch), [N-ENGINE](#source-n-engine), [N-CLI](#source-n-cli), [N-IO](#source-n-io), [N-LEDGER](#source-n-ledger), [N-STORAGE](#source-n-storage), [N-MANIFEST](#source-n-manifest).

Граница: Карта 2.4 и исходники 2.6 имеют самостоятельное происхождение. Проверены архитектурные связи; не заявлено исполнение всех путей и успешное завершение 2.7.

### N26-SCALE

**69 Python-файлов src; 225 Python-файлов tests**

Версия: 2.6. Дата: 2026-10-15. Статус: **VERIFIED_STATIC**.

Проверка: Перечислены *.py внутри закреплённого релиза без импорта и запуска.

Источник: [N-MANIFEST](#source-n-manifest).

Граница: Включены исторические модули и __init__.py. Это количество файлов, а не число активных компонентов или тестов.

### N26-TESTS

**3334 основных теста + отдельно 30 legacy; failures/errors/skipped 0/0/0 в обоих XML**

Версия: 2.6 / source cf6617d7. Дата: 2026-10-15T09:09:54+03:00. Статус: **HISTORICAL_REPORT**.

Проверка: Сверены сохранённые pytest XML и verification summary; основной и legacy exit code 0.

Источник: [N-MANIFEST](#source-n-manifest), [N-VERIFY](#source-n-verify), [N-OFFLINE](#source-n-offline), [N-XML](#source-n-xml), [N-LEGACYXML](#source-n-legacyxml).

Граница: OFFLINE, network DENIED; исходные тесты для портфолио не перезапускались. Не подтверждает live acceptance или результат версии 2.7.

### N26-BENCH

**790 уникальных instrument/bar за 43.188 s; duplicates 0; 5 синтетических защищённых позиций**

Версия: 2.6 / source cf6617d7. Дата: 2026-10-15. Статус: **HISTORICAL_REPORT**.

Проверка: Сохранённый SYNTHETIC_790_WHOLE_ENGINE_REAL_CADENCE: реальное течение времени, искусственный wire delay 50 ms.

Источник: [N-CAPACITY](#source-n-capacity), [N-MANIFEST](#source-n-manifest).

Граница: Это локальный синтетический стенд исходного проекта; network/profile/logs DENIED. Не live SLA, не рыночные наблюдения и не результаты нового портфолио-демо.

### N09-COVERAGE

**coverage.py 7.16.2: 5844/6020 = 97.0764% statements/lines; 29 src paths**

Версия: 0.9-src; привязка полного измеренного дерева к source pin не установлена. Дата: 2026-10-04T23:18:35.587606 (timezone UNKNOWN). Статус: **HISTORICAL_REPORT**.

Проверка: Прочитан и хеширован сохранённый coverage.json. branch_coverage=false.

Источник: [N-COVERAGE09](#source-n-coverage09).

Граница: Отчёт исторического выпуска 0.9. Не переносить на 2.6/2.7; их числовое покрытие UNKNOWN. Часовой пояс исходного timestamp отсутствует.

<a id="cardio"></a>

## DARCardioX

### C105-ARCH

**EA/MQL4, Watchdog, ограниченное хранение и диагностические потребители; владение, намерение, исход и ACK разделены**

Версия: 10.5 + датированный Start_here. Дата: 2026-10-15 (дата чтения). Статус: **VERIFIED_STATIC**.

Проверка: Прочитаны Start_here.md и отчёт подготовленного пакета 10.5.

Источник: [C-ENTRY](#source-c-entry), [C-REPORT105](#source-c-report105), [C-MANIFEST105](#source-c-manifest105).

Граница: Подтверждена документированная схема и границы подготовки; текущие службы и native broker execution для портфолио не запускались.

### C105-SCALE

**24164 физических строки MQ4; 1543046 raw bytes**

Версия: 10.5 / PREPARED_NOT_INSTALLED. Дата: 2026-10-15T21:04:05+03:00. Статус: **VERIFIED_STATIC**.

Проверка: Raw SHA256, размер байтов и число строк в исходном файле версии 10.5.

Источник: [C-SOURCE105](#source-c-source105), [C-MANIFEST105](#source-c-manifest105).

Граница: Размер включает комментарии, пустые строки, стратегию и инфраструктуру. Оригинальный исходник не включён. Измеренное LINE/BRANCH-покрытие UNKNOWN.

### C105-COMPILE

**MetaEditor: 0 errors, 0 warnings; 2501 ms**

Версия: 10.5 / PREPARED_NOT_INSTALLED. Дата: 2026-10-15T21:06:21+03:00. Статус: **HISTORICAL_REPORT**.

Проверка: Сохранённая квитанция компиляции PASS_NATIVE_COMPILER и метаданные пакета.

Источник: [C-COMPILE105](#source-c-compile105), [C-MANIFEST105](#source-c-manifest105), [C-REPORT105](#source-c-report105).

Граница: Код процесса 1 оценён источником по логу и бинарному файлу; это не общий exit code PASS. Здесь компилятор не запускался. Подготовленный пакет не означает установку или брокерское исполнение.

### C105-HOST

**Отдельные HOST-группы: 40 reservation; 14 quote/lot; 12 independent reservation; 36 independent source review; 29 typed readers**

Версия: 10.5. Дата: 2026-10-15. Статус: **HISTORICAL_REPORT**.

Проверка: Сопоставлены отдельные JSON-результаты групп, без суммирования в число уникальных тестов.

Источник: [C-RESERVATION105](#source-c-reservation105), [C-QUOTE105](#source-c-quote105), [C-RESERVATION-INDEP105](#source-c-reservation-indep105), [C-REVIEW105](#source-c-review105), [C-READERS105](#source-c-readers105).

Граница: HOST/source-body проверки и TEMP/mocks не равны native broker execution. Пересечение групп не определено; единого числа независимых тестов нет.

### C105-REGRESSION

**486 одинаковых controls × 3 варианта = 1458 PASS-исполнений; 21 run**

Версия: 10.5; варианты планов 10.3 / 10.4 / 10.5. Дата: 2026-10-15. Статус: **HISTORICAL_REPORT**.

Проверка: Сохранённый ComposedHOST Run_summary.json.

Источник: [C-REGRESSION105](#source-c-regression105).

Граница: 1458 — повторные исполнения controls, не 1458 независимых тестов. Число не объединяется с HOST-группами или покрытиями других проектов.

<a id="koshka"></a>

## Koshka

### KOSHKA-IDENTITY

**Существует отдельный application.properties-Koshka, упомянутый в метаданных поставки**

Версия: конфигурационный артефакт поставки 13.10.2026. Дата: 2026-10-13. Статус: **VERIFIED_STATIC**.

Проверка: Проверены имя, размер, SHA256 и упоминание в report/build identity. Значения конфигурации не публикуются.

Источник: [KOSHKA-CONFIG-METADATA](#source-koshka-config-metadata), [DTX-BUILD](#source-dtx-build), [DTX-EXTERNAL-REPORT](#source-dtx-external-report).

Граница: Название робота также подтверждено владельцем (USER_REPORT). Самостоятельная кодовая база, отдельный стек и числовые метрики UNKNOWN.

<a id="workflow"></a>

## ИИ-координация

### WF-PROCESS

**Документы задают роли, проверку понимания, ссылки на пункты, паспорт, журнал и передачу контекста**

Версия: Кодекс/Вводная 02.10 + уточнение 15.10.2026. Дата: 2026-10-15. Статус: **VERIFIED_STATIC**.

Проверка: Прочитаны первичные Кодекс и Вводная роли. Текущие роли и личный вклад — по сообщению владельца (USER_REPORT).

Источник: [DTX-CODEX](#source-dtx-codex), [DTX-ROLE-INTRO](#source-dtx-role-intro), [WF-ROLE-ACCOUNT](#source-wf-role-account), [WF-CYCLE-ACCOUNT](#source-wf-cycle-account).

Граница: Наличие регламента не гарантирует соблюдение каждого пункта, полной автономности или отсутствия ошибок ИИ. Аудит авторства каждого коммита не проводился.

### WF-CAPTCHA31

**Сдача понимания/проектирования и приёмка архитектурной ИИ-ролью с уточнениями; S01–S30 NOT_RUN**

Версия: итерация 31. Дата: 2026-10-15. Статус: **VERIFIED_STATIC**.

Проверка: Два сохранённых текста сверены с оригинальными вложениями: SHA256 совпадают.

Источник: [E31-01](#source-e31-01), [E31-02](#source-e31-02), [WF-CAPTCHA-REVIEW](#source-wf-captcha-review).

Граница: Не подтверждает реализацию, 30 пройденных тестов или разрешение владельца на запуск. Пример пересказан и обезличен; полные инструкции закрыты.

<a id="demo"></a>

## Отдельный демонстратор

### DEMO-RUNTIME

**31 unittest, failures/errors/skipped 0/0/0; 5 CLI-сценариев PASS**

Версия: 0.1.0. Дата: 2026-10-15T21:24:37+03:00. Статус: **VERIFIED_RUNTIME**.

Проверка: Bundled Python 3.12.14; unittest + python -m demo.checks; python -m demo.run; только синтетические данные.

Источник: [DEMO-COVERAGE](#source-demo-coverage), [DEMO-REPORT](#source-demo-report).

Граница: Результаты только нового демо; ни один исходный робот или его тесты в этом прогоне не запускались.

### DEMO-LINE

**211/213 = 99.06% исполняемых строк**

Версия: 0.1.0. Дата: 2026-10-15T21:24:37+03:00. Статус: **VERIFIED_RUNTIME**.

Проверка: Python stdlib trace.Trace; executable lines from recursive dis.findlinestarts; demo/core.py + demo/fake_api.py

Источник: [DEMO-COVERAGE](#source-demo-coverage).

Граница: Модульные импорты включены; run.py, checks.py и тесты вне области. BRANCH не измерено. Это метод trace/dis для точной версии Python, не переносимое сравнение со стандартным JaCoCo/coverage.py.

## Идентификаторы источников

Полные пути и контрольные суммы закрытых материалов сохраняются владельцем во внутреннем реестре. Здесь приведены только безопасное имя, SHA256 и доступность. Хеш не означает, что закрытый источник доступен читателю.

<a id="source-n-arch"></a>

**N-ARCH** — CodeX_active_path_v.2.4.md; закрытый оригинал, не включён.

SHA256: `75f83c1edda42dd6d98053ec636f268347913b3181e66db299bc9f74acd38892`

<a id="source-n-engine"></a>

**N-ENGINE** — engine.py; закрытый оригинал, не включён.

SHA256: `6c206a02d1a1975ede7512e4fbc513e9e88d9d5978bb322930abf160c780dfa4`

<a id="source-n-cli"></a>

**N-CLI** — cli.py; закрытый оригинал, не включён.

SHA256: `242f16ebaeeae32450dff6f5967ef57ab9432c0ef417a641b11ffae193e249fa`

<a id="source-n-io"></a>

**N-IO** — runtime_io.py; закрытый оригинал, не включён.

SHA256: `4dea0c9be7d6b368238764d90ee10afb9b1889094d0fae1d5de564d8121c9023`

<a id="source-n-ledger"></a>

**N-LEDGER** — ledger.py; закрытый оригинал, не включён.

SHA256: `817683dbd36c234bf2c525f4746e66945beb7a210850cbb415e32bdeb71827f8`

<a id="source-n-storage"></a>

**N-STORAGE** — storage.py; закрытый оригинал, не включён.

SHA256: `cd8fb212cd019e2063a91c18335f1ad59ff949362b989894bac12ff1948e3d0a`

<a id="source-n-manifest"></a>

**N-MANIFEST** — release_manifest.json; закрытый оригинал, не включён.

SHA256: `839dd287befacffff3a7d274e61e5d399e7fd29569e3d8c16f43b1c5a22d57f6`

<a id="source-c-entry"></a>

**C-ENTRY** — Start_here.md; закрытый оригинал, не включён.

SHA256: `27303482cb43047feb08be01f219eaa20e57dbe023affcca659b590ba4876d37`

<a id="source-c-report105"></a>

**C-REPORT105** — Runtime105_repair_report.md; закрытый оригинал, не включён.

SHA256: `05af3804d9aa45bc014b681264bc2bc0247b1b11be5968f3ed7fa37dde5dbb31`

<a id="source-c-manifest105"></a>

**C-MANIFEST105** — DARCardioX_v_10.5_manifest.json; закрытый оригинал, не включён.

SHA256: `c7b63c5fb0dc12ebb9e31b752d7f314cb31a30fe6f39325dba78057407b1ffd0`

<a id="source-dtx-passport"></a>

**DTX-PASSPORT** — 2026-09-14 ПАСПОРТ DARTherapeX.docx; закрытый оригинал, не включён.

SHA256: `1cd9fd9c09aa49e5aebba02f24407dd368bcc5d7c2b271305e21d3bd3df0ab27`

<a id="source-dtx-appendix"></a>

**DTX-APPENDIX** — 2026-09-14 Приложение №1 DARTherapeX.docx; закрытый оригинал, не включён.

SHA256: `fe3a3dcad613ef4bcda0968bbc123d34c3cb9c6287cdfc1a7274aaa3a62aaf80`

<a id="source-dtx-archive"></a>

**DTX-ARCHIVE** — 2026-10-13_11-29_bb85e20d.zip; закрытый оригинал, не включён.

SHA256: `65c0aa886dd2ae016fd82f2443ee3e90b07c5412ee39258e502028cae5676eef`

<a id="source-dtx-build"></a>

**DTX-BUILD** — DARTherapeX ZIP :: build-identity.json; закрытый оригинал, не включён.

SHA256: `71cf07577606f42cfa5dd73830e0f9f96db5ab8ee6475459224b9e10a8a1b457`

<a id="source-dtx-manifest"></a>

**DTX-MANIFEST** — DARTherapeX ZIP :: SOURCE-MANIFEST.json; закрытый оригинал, не включён.

SHA256: `91608863d3870b5d4356cc94ba86b00907222a92f2024fad1fc2032a2c4d60fa`

<a id="source-dtx-pom"></a>

**DTX-POM** — DARTherapeX ZIP :: pom.xml; закрытый оригинал, не включён.

SHA256: `bb6eef0c4116fe551f809b6abc7d05a984ccd765a5b194078e3f5d2962793375`

<a id="source-dtx-code-1"></a>

**DTX-CODE-1** — DARTherapeX ZIP :: src/main/java/ru/myrobot/domain/ports/OrderGateway.java; закрытый оригинал, не включён.

SHA256: `006fb8c819f088b92fa19ba02ecfe5f65ed3871561e0f206a4c4c8de129eb2b4`

<a id="source-dtx-code-2"></a>

**DTX-CODE-2** — DARTherapeX ZIP :: src/main/java/ru/myrobot/service/state/StateReconciliationService.java; закрытый оригинал, не включён.

SHA256: `c4c7a64e78fb5872b98b4e61e7d32636aa8346a57e3ce2f7ef5f84dab659896f`

<a id="source-dtx-code-3"></a>

**DTX-CODE-3** — DARTherapeX ZIP :: src/main/java/ru/myrobot/infrastructure/runtime/RuntimeInstanceContext.java; закрытый оригинал, не включён.

SHA256: `6effe11c65db53d37504ed73271c821d5773355c17b47a28556f8b5cd4e1e9b5`

<a id="source-dtx-code-4"></a>

**DTX-CODE-4** — DARTherapeX ZIP :: src/main/java/ru/myrobot/infrastructure/state/JournalFileTransaction.java; закрытый оригинал, не включён.

SHA256: `d0a080f7fa75a3adf632f0902c1f6200cce1f00b0182d56950ab626479e3224e`

<a id="source-dtx-code-5"></a>

**DTX-CODE-5** — DARTherapeX ZIP :: src/main/java/ru/myrobot/infrastructure/diagnostics/TradeDiagnosticsJournal.java; закрытый оригинал, не включён.

SHA256: `8da41165e52d49ac977c470d4cb0d35b5ff18dac1ceb355f041a3e11864e3060`

<a id="source-dtx-old-source"></a>

**DTX-OLD-SOURCE** — DARTherapeX ZIP :: reconstruction/source.zip; закрытый оригинал, не включён.

SHA256: `464f9ac1953dced3989004597700cfce674b53650347ab799404f45471fe0d7a`

<a id="source-n-verify"></a>

**N-VERIFY** — v26_verification_summary.json; закрытый оригинал, не включён.

SHA256: `27581b1ad4a2424584a1709dd168c24acbacfabf716728c92e120983d398a9ab`

<a id="source-n-offline"></a>

**N-OFFLINE** — v1_offline_verification.json; закрытый оригинал, не включён.

SHA256: `2eb330559c3a5febbb99022b5c6c3c8f35b85e7c5b502e891846062f72138f42`

<a id="source-n-xml"></a>

**N-XML** — v1_tests.xml; закрытый оригинал, не включён.

SHA256: `6b4fac12edaaed960dc029b051492bb5bfe52a66d458f5ed6a49f1c8e5a04758`

<a id="source-n-legacyxml"></a>

**N-LEGACYXML** — v1_legacy_entry_tests.xml; закрытый оригинал, не включён.

SHA256: `6551e6584de341b2016755c4fc8c076ecc6b8069cc67dfc96f76b38facb34213`

<a id="source-n-capacity"></a>

**N-CAPACITY** — v20_real_clock_capacity.json; закрытый оригинал, не включён.

SHA256: `1d28aeec960e8403cd5bd1540674febcc9e1e45a048194d0e292e1b43d8d2608`

<a id="source-n-coverage09"></a>

**N-COVERAGE09** — coverage.json; закрытый оригинал, не включён.

SHA256: `da1ae3200a255afe4d95b1b73367a899e9a2035b440f247f0db63d36b2ca9c1c`

<a id="source-c-source105"></a>

**C-SOURCE105** — DARCardioX_v_10.5.mq4; закрытый оригинал, не включён.

SHA256: `aa96b96f55fe046683e0fd64f4c5836d87475e7f15b421b9db5c0cb7391ef1b2`

<a id="source-c-compile105"></a>

**C-COMPILE105** — compile_attempt_1.json; закрытый оригинал, не включён.

SHA256: `8b113b888ca32069289f7f4c88ed64d2ca79d1f904966bd5ccbcbb683b17b0e5`

<a id="source-c-reservation105"></a>

**C-RESERVATION105** — Reservation105_integrated_HOST.json; закрытый оригинал, не включён.

SHA256: `c33e39c043429063f1a48f840274c3755320cb0baef50281a4a3a334f68bb7ba`

<a id="source-c-quote105"></a>

**C-QUOTE105** — Integrated_Quote_lot105_HOST.json; закрытый оригинал, не включён.

SHA256: `e39e700b0b581effa20d89d942416c139b227c75bbb28a59e4a3abc5e877909b`

<a id="source-c-reservation-indep105"></a>

**C-RESERVATION-INDEP105** — Integrated_Reservation105_independent_HOST.json; закрытый оригинал, не включён.

SHA256: `7c9ad18bbeca48acc386ba38f21eb48a96c82028208c70b2e7eba6367fce6011`

<a id="source-c-review105"></a>

**C-REVIEW105** — Integrated_independent_source_review.json; закрытый оригинал, не включён.

SHA256: `7597a543c511c13059fcacb5902abcb68dd9eb672bee6a69b1e06b8adfc3fffc`

<a id="source-c-readers105"></a>

**C-READERS105** — Consumer105_HOST.json; закрытый оригинал, не включён.

SHA256: `41fa41f368c1b0c25135b17514b37708495306130b13f2d51e7ec45776180af2`

<a id="source-c-regression105"></a>

**C-REGRESSION105** — Run_summary.json; закрытый оригинал, не включён.

SHA256: `9d9b358b0a17374280d3b274b7bec12c2ea09d15e6ec0ff789e0911905e6f0f7`

<a id="source-koshka-config-metadata"></a>

**KOSHKA-CONFIG-METADATA** — application.properties-Koshka; закрытый оригинал, не включён.

SHA256: `9e4a16df906678e20f30f1a6ba1dcf6e8b4abc0aee7acd32470c3d224bd24595`

<a id="source-dtx-external-report"></a>

**DTX-EXTERNAL-REPORT** — report.md; закрытый оригинал, не включён.

SHA256: `b223410c95cec5c640bee62cf41c8e489e2dcf61aef138f89903c501c7bf0b52`

<a id="source-dtx-codex"></a>

**DTX-CODEX** — 2026-10-02 Кодекс DARTherapeX.docx; закрытый оригинал, не включён.

SHA256: `ee66b88312cb511e3e282dacdd69062563bfe2952d564fb58163fd959b3f744e`

<a id="source-dtx-role-intro"></a>

**DTX-ROLE-INTRO** — 2026-10-02 Вводная Ока Бога DARTherapeX.docx; закрытый оригинал, не включён.

SHA256: `d4c65d633edb65c1e5b75c5c0cec47801a7bbac9104f6af886644c5982df339d`

<a id="source-wf-role-account"></a>

**WF-ROLE-ACCOUNT** — 2026-10-15 Устройство ИИ-команд - уточнение.json; закрытый оригинал, не включён.

SHA256: `54eac1de1c4ca3a324adeb211fd08c8cc5840bd9f5efb2ea0244cebfff0678ce`

<a id="source-wf-cycle-account"></a>

**WF-CYCLE-ACCOUNT** — 2026-10-15 Ускоренный цикл разработки - пример.json; закрытый оригинал, не включён.

SHA256: `ce5caebd4041ef655a8e9604d91dcc1fef051e5f687765f740797659f83497b6`

<a id="source-e31-01"></a>

**E31-01** — 01 Сдача Капчи и проект Codex.txt; закрытый оригинал, не включён.

SHA256: `e8f6eea4072610e504517c6b4c4c077672798c3672d1de28bcebefcabaa58d25`

<a id="source-e31-02"></a>

**E31-02** — 02 Разбор и приёмка Оком.txt; закрытый оригинал, не включён.

SHA256: `56eb1de927f509e79177d098ccfdb1bc95c325e0b67ad61d8cd3db754e57fbe2`

<a id="source-wf-captcha-review"></a>

**WF-CAPTCHA-REVIEW** — 2026-10-15 Капча итерация 31 - проверка доказательств.json; закрытый оригинал, не включён.

SHA256: `cfaa70b4e64d02d4d3839f2256a28229dcd72c67a6712f049028991353d15f37`

<a id="source-demo-coverage"></a>

**DEMO-COVERAGE** — demo/reports/coverage.json; публичный файл в комплекте.

SHA256: `98b02079622d7746c9572e1b4ae9725a1b4f4ee70efaf9daec2927dd02284f67`

<a id="source-demo-report"></a>

**DEMO-REPORT** — demo/reports/report.json; публичный файл в комплекте.

SHA256: `0bfe516e2540813ffbc5cad40d3f29238a65006012189522924f15d905d51f09`

