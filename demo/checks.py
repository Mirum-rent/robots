"""Run only this demo's unittest suite and measure its core with stdlib trace."""

import argparse
from datetime import datetime, timedelta, timezone
import dis
import hashlib
import io
import json
from pathlib import Path
import platform
import sys
import tempfile
import trace
from types import CodeType
import unittest


def executable_lines(code: CodeType) -> set[int]:
    lines = {line for _, line in dis.findlinestarts(code) if line > 0}
    for item in code.co_consts:
        if isinstance(item, CodeType):
            lines |= executable_lines(item)
    return lines


def check(output: Path) -> dict:
    folder = Path(__file__).resolve().parent
    # Accurate import-time counts require a fresh process, as documented.
    if any(module in sys.modules for module in ("demo.core", "demo.fake_api")):
        raise RuntimeError("Run python -m demo.checks in a fresh process")
    output.mkdir(parents=True, exist_ok=True)
    stream = io.StringIO()

    def run_suite():
        suite = unittest.defaultTestLoader.discover(str(folder / "tests"), pattern="test_*.py")
        return unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)

    tracer = trace.Trace(count=True, trace=False, ignoredirs=[sys.base_prefix, sys.prefix])
    result = tracer.runfunc(run_suite)
    counts = tracer.results().counts
    modules = []
    for name in ("core.py", "fake_api.py"):
        path = folder / name
        source = path.read_text(encoding="utf-8")
        executable = executable_lines(compile(source, str(path), "exec"))
        covered = {line for (filename, line), count in counts.items()
                   if Path(filename).resolve() == path and count > 0} & executable
        missing = sorted(executable - covered)
        modules.append({"path": "demo/" + name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                        "executable_lines": len(executable),
                        "covered_lines": len(covered), "missing_lines": missing,
                        "line_percent": round(100 * len(covered) / len(executable), 2)})
        annotated = []
        for line_number, line in enumerate(source.splitlines(), 1):
            count = counts.get((str(path), line_number), 0)
            prefix = f"{count:7d}" if count else ("MISSING" if line_number in executable else "       ")
            annotated.append(f"{prefix} {line_number:4d}: {line}")
        (output / (name + ".cover.txt")).write_text("\n".join(annotated) + "\n", encoding="utf-8")
    total = sum(module["executable_lines"] for module in modules)
    covered = sum(module["covered_lines"] for module in modules)
    report = {
        "status": "VERIFIED_RUNTIME", "synthetic": True,
        "generated_at_moscow": datetime.now(timezone(timedelta(hours=3))).isoformat(timespec="seconds"),
        "version": "0.1.0", "python": platform.python_version(),
        "tool": "Python stdlib trace.Trace; executable lines from recursive dis.findlinestarts",
        "command": "python -m demo.checks --output demo/reports",
        "scope": ["demo/core.py", "demo/fake_api.py"],
        "test_sources": [{"path": "demo/tests/test_invariants.py",
                          "sha256": hashlib.sha256((folder / "tests" / "test_invariants.py").read_bytes()).hexdigest()}],
        "measurement": "executed Python source lines; module imports included; branch coverage not measured",
        "excluded": ["demo/run.py", "demo/checks.py", "demo/tests/", "all source robot projects"],
        "tests": {"run": result.testsRun, "failures": len(result.failures),
                  "errors": len(result.errors), "skipped": len(result.skipped),
                  "passed": result.wasSuccessful()},
        "modules": modules,
        "total": {"executable_lines": total, "covered_lines": covered,
                  "line_percent": round(100 * covered / total, 2)},
        "limitations": ["Line counts depend on the Python version and this exact source version.",
                        "This is not branch coverage, production reliability or profitability proof.",
                        "The source robots were not executed; their test and coverage metrics are separate."],
    }
    (output / "coverage.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "test-results.txt").write_text(stream.getvalue(), encoding="utf-8")
    print(stream.getvalue(), end="")
    print(json.dumps(report["total"], sort_keys=True))
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Save test/line-coverage reports here")
    args = parser.parse_args()
    if args.output is not None:
        report = check(args.output)
    else:
        with tempfile.TemporaryDirectory(prefix="robots-demo-checks-") as temporary:
            report = check(Path(temporary))
    return 0 if report["tests"]["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
