#!/usr/bin/env bash
set -euo pipefail

echo "VERIFY-RELEASE: CivicParks v0.1.0"
if [ -n "${CIVICPARKS_RELEASE_PYTHON:-}" ]; then
  PYTHON_BIN="$CIVICPARKS_RELEASE_PYTHON"
else
  PYTHON_BIN=""
  for candidate in python /mnt/c/Users/scott/AppData/Local/Microsoft/WindowsApps/python.exe /c/Users/scott/AppData/Local/Microsoft/WindowsApps/python.exe python3; do
    if (command -v "$candidate" >/dev/null 2>&1 || [ -x "$candidate" ]) && "$candidate" -c 'import pytest, ruff, build' >/dev/null 2>&1; then
      PYTHON_BIN="$candidate"
      break
    fi
  done
  if [ -z "$PYTHON_BIN" ]; then
    echo "VERIFY-RELEASE: python with pytest, ruff, and build is required"
    exit 1
  fi
fi
echo "[INFO] python: $($PYTHON_BIN -c 'import sys; print(sys.executable)')"

bash scripts/verify-docs.sh
$PYTHON_BIN scripts/check-civiccore-placeholder-imports.py
$PYTHON_BIN -m pytest -q
$PYTHON_BIN -m ruff check .
rm -rf dist
$PYTHON_BIN -m build

test -f dist/civicparks-0.1.0-py3-none-any.whl || { echo "missing wheel"; exit 1; }
test -f dist/civicparks-0.1.0.tar.gz || { echo "missing sdist"; exit 1; }
(
  cd dist
  sha256sum civicparks-0.1.0-py3-none-any.whl civicparks-0.1.0.tar.gz > SHA256SUMS.txt
)
echo "[PASS] build artifacts and SHA256SUMS"

$PYTHON_BIN - <<'PY'
import civicparks
assert civicparks.__version__ == "0.1.0", civicparks.__version__
print("[PASS] package version 0.1.0")
PY

echo "VERIFY-RELEASE: PASSED"
