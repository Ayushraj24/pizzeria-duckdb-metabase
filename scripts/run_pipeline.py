from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(script_name: str) -> None:
    script = ROOT / "scripts" / script_name
    print(f"\n==> {script_name}")
    subprocess.run([sys.executable, str(script)], check=True)


def main() -> None:
    run("generate_data.py")
    run("build_warehouse.py")
    run("validate_warehouse.py")


if __name__ == "__main__":
    main()

