"""
Syntax and Code Integrity Validator
Validates that all Python files in the project compile cleanly with zero syntax errors.
"""

import py_compile
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

python_files = list(BASE_DIR.glob("**/*.py"))
has_error = False

print(f"Checking {len(python_files)} Python source files for syntax errors...")

for f in python_files:
    if "venv" in f.parts or ".pytest_cache" in f.parts:
        continue
    try:
        py_compile.compile(str(f), doraise=True)
        print(f"  [OK] {f.relative_to(BASE_DIR)}")
    except py_compile.PyCompileError as e:
        print(f"  [SYNTAX ERROR] {f.relative_to(BASE_DIR)}: {e}")
        has_error = True

if not has_error:
    print("\nAll Python files compiled cleanly with 0 syntax errors!")
else:
    print("\nSyntax errors detected.")
    sys.exit(1)
