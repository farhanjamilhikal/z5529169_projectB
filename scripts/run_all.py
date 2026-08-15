"""Rebuild and verify the complete local Project B prototype."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".runtime_cache"


def run(*args: str) -> None:
    """Run one required command and stop if it fails."""
    print(f"\n> {' '.join(args)}", flush=True)
    subprocess.run(args, cwd=ROOT, env=os.environ, check=True)


def main() -> None:
    CACHE.mkdir(exist_ok=True)
    (CACHE / "matplotlib").mkdir(exist_ok=True)
    (CACHE / "nltk_data").mkdir(exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(CACHE / "matplotlib"))
    os.environ.setdefault("NLTK_DATA", str(CACHE / "nltk_data"))

    python = sys.executable
    run(python, "scripts/run_part_b.py")
    run(python, "scripts/build_report.py")
    run(python, "scripts/build_product_assurance.py")

    office = shutil.which("libreoffice") or shutil.which("soffice")
    if office:
        run(
            office,
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(ROOT / "report"),
            str(ROOT / "report/report.docx"),
        )
    else:
        print("\nPDF export skipped: open report/report.docx in Word and export as PDF.")

    run(python, "-m", "pytest", "-q")
    run(python, "-m", "ruff", "check", ".")
    run(python, "scripts/check_handin.py")
    print("\nProject B rebuild and verification completed.")


if __name__ == "__main__":
    main()
