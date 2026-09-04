"""Run the test suite with concise, readable results.

Usage:
    python tests/run_tests.py
"""

import unittest
from pathlib import Path
import sys


class ReadableTestResult(unittest.TextTestResult):
    def _label(self, test):
        return test.id().removeprefix("tests.").replace(".", " › ")

    def addSuccess(self, test):
        super().addSuccess(test)
        self.stream.writeln(f"  PASS  {self._label(test)}")

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.stream.writeln(f"  SKIP  {self._label(test)} ({reason})")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.stream.writeln(f"  FAIL  {self._label(test)}")

    def addError(self, test, err):
        super().addError(test, err)
        self.stream.writeln(f"  ERROR {self._label(test)}")


class ReadableTestRunner(unittest.TextTestRunner):
    resultclass = ReadableTestResult

    def run(self, test):
        self.stream.writeln("\nMoodle-py test results\n")
        result = super().run(test)
        status = "PASSED" if result.wasSuccessful() else "FAILED"
        self.stream.writeln(
            f"\n{status}: {result.testsRun} tests, "
            f"{len(result.failures)} failures, {len(result.errors)} errors, "
            f"{len(result.skipped)} skipped"
        )
        return result


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(project_root / "src"))
    suite = unittest.defaultTestLoader.discover(
        start_dir=project_root / "tests", top_level_dir=project_root
    )
    ReadableTestRunner(verbosity=0).run(suite)
