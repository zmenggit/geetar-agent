"""一键运行所有代码质量检查。

用法: uv run check
"""

import subprocess
import sys


def main() -> None:
    steps: list[tuple[str, list[str]]] = [
        ("ruff lint", ["ruff", "check", "."]),
        ("ruff format check", ["ruff", "format", "--check", "."]),
        ("mypy", ["mypy", "src"]),
        ("pytest", ["pytest"]),
    ]

    for name, cmd in steps:
        print(f"\n━━━ {name} ━━━")
        result = subprocess.run(cmd, check=False)
        if result.returncode != 0:
            print(f"\n✗ {name} failed", file=sys.stderr)
            sys.exit(result.returncode)


print("\n✓ All checks passed")
