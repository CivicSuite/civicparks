from __future__ import annotations

import ast
from pathlib import Path

PLACEHOLDERS = {
    "audit",
    "auth",
    "catalog",
    "connectors",
    "exemptions",
    "ingest",
    "notifications",
    "onboarding",
    "scaffold",
    "search",
    "verification",
}
SOURCE_ROOT = Path("civicparks")


def main() -> int:
    failures: list[str] = []
    for path in SOURCE_ROOT.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            module = None
            if isinstance(node, ast.ImportFrom):
                module = node.module
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith("civiccore."):
                        module = alias.name
                        break
            if module and module.startswith("civiccore."):
                name = module.split(".")[1]
                if name in PLACEHOLDERS:
                    failures.append(
                        f"{path}: civiccore.{name} is a placeholder package in v0.2.0. "
                        "Do not import from it."
                    )
    if failures:
        print("\n".join(failures))
        return 1
    print(f"PLACEHOLDER-IMPORT-CHECK: PASSED ({len(list(SOURCE_ROOT.rglob('*.py')))} source files scanned)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
