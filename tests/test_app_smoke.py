from __future__ import annotations

from pathlib import Path

import pandas as pd
from streamlit.testing.v1 import AppTest

from app import missing_required_files

ROOT = Path(__file__).resolve().parent.parent


def _nav(app: AppTest, page: str) -> AppTest:
    next(radio for radio in app.radio if radio.label == "Navigation").set_value(page).run(timeout=12)
    return app


def test_all_required_pages_render():
    app_path = ROOT / "streamlit_app.py"
    for page in [
        "Overview",
        "Compare Funds",
        "Fund Fact Sheet",
        "Holdings & Allocation",
        "News Sentiment",
        "Movie-to-Market Lab",
        "Methodology & Limitations",
    ]:
        app = AppTest.from_file(app_path).run(timeout=12)
        _nav(app, page)
        assert not app.exception


def test_core_signal_scope_labels_render():
    app = AppTest.from_file(ROOT / "streamlit_app.py").run(timeout=12)
    assert not app.exception
    assert any("SignalScope" in title.value for title in app.title)
    assert any("See risk, returns and sentiment in one view." in caption.value for caption in app.caption)

    _nav(app, "Movie-to-Market Lab")
    assert any("Movie-to-Market Lab: Spider-Man versus Barbie" in subheader.value for subheader in app.subheader)

    _nav(app, "Compare Funds")
    assert not app.exception


def test_prohibited_strings_absent_from_app_shell_files():
    prohibited = [
        "NovaFinance",
        "Signal & Story",
        "Spider-Man x Barbie",
        "premium fintech demo",
        "Total Portfolio Value",
        "Daily P&L",
    ]
    for relative in ["app.py", "streamlit_app.py", "README.md"]:
        text = (ROOT / relative).read_text(encoding="utf-8")
        for phrase in prohibited:
            assert phrase not in text


def test_metric_source_register_references_existing_csvs():
    register = pd.read_csv(ROOT / "results/app/METRIC_SOURCE_REGISTER.csv")
    assert not register.empty
    csv_columns = {"source_csv", "displayed_metric", "verification_status"}
    assert csv_columns.issubset(register.columns)
    for source_csv in register["source_csv"].dropna():
        assert (ROOT / source_csv).exists()


def test_missing_file_helper_reports_absence(tmp_path: Path):
    missing = missing_required_files(tmp_path)
    assert missing
