#!/usr/bin/env bash
set -euo pipefail

for file in README.md README.txt USER-MANUAL.md USER-MANUAL.txt CHANGELOG.md CONTRIBUTING.md LICENSE LICENSE-CODE LICENSE-DOCS SECURITY.md SUPPORT.md CODE_OF_CONDUCT.md docs/index.html; do
  test -f "$file" || { echo "VERIFY-DOCS: missing $file"; exit 1; }
done

for pattern in CivicUtility civicutility CivicElections civicelections CivicCourt civiccourt CivicSafety civicsafety CivicLibrary civiclibrary "0.1.0.dev0" "~=0.2" MIT; do
  if grep -Fq "$pattern" README.md README.txt USER-MANUAL.md USER-MANUAL.txt docs/index.html CHANGELOG.md; then
    echo "VERIFY-DOCS: stale marker found: $pattern"
    exit 1
  fi
done

for file in CONTRIBUTING.md LICENSE LICENSE-CODE LICENSE-DOCS SECURITY.md SUPPORT.md CODE_OF_CONDUCT.md docs/architecture.md docs/architecture-civicparks.svg docs/github-discussions-seed.md; do
  test -f "$file" || { echo "VERIFY-DOCS: missing professional artifact $file"; exit 1; }
done

echo "VERIFY-DOCS: PASSED"
