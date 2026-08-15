# SignalScope — FINS3645 Project B

Student: `z5529169`

SignalScope is a local, PyCharm-ready academic analytics prototype built from
the latest verified Project B finale outputs. It compares ten systematic funds
across equity, crypto and combined families; shows fact-sheet, holdings and
allocation evidence; explains the news-sentiment extension; and keeps the
Spider-Man versus Barbie comparison in a separate Movie-to-Market Lab.

Tagline: **See risk, returns and sentiment in one view.**

Long description: **Transparent systematic fund comparison with news-sentiment evidence and a Movie-to-Market Lab.**

## Local run

1. Open `z5529169_projectB` as the project root.
2. Create or select a Python 3.12 or 3.13 virtual environment.
3. Install requirements and run the checked local app:

```bash
python -m pip install -r requirements.txt -r requirements-dev.txt
python scripts/run_all.py
streamlit run streamlit_app.py
```

On Windows, `run_project_b.bat` performs the same rebuild and verification.

## What SignalScope loads

SignalScope loads only precomputed artefacts from `results/` during normal app
use. It does not rerun the backtest, download external data or regenerate the
sentiment pipeline when a user opens the interface.

Primary artefacts include:

- `results/data/fund_returns.csv`
- `results/data/fund_weights.csv`
- `results/data/sector_sentiment_index.csv`
- `results/tables/performance_metrics.csv`
- `results/tables/current_holdings.csv`
- `results/tables/fusion_comparison.csv`
- `results/tables/dual_domain_sentiment_validation.csv`
- `results/tables/movie_lab_event_summary.csv`
- `results/data/movie_lab_event_windows.csv`
- `results/data/movie_lab_external_prices_2020_2023.csv`

## Verified analytical scope

- monthly walk-forward backtests with past-only weights;
- 252-period annualisation for equity and combined funds;
- 365-period annualisation for crypto-only funds;
- long-only equal-weight, minimum-variance and inverse-volatility risk-parity methods;
- 10 bps transaction-cost deduction per unit of one-way turnover;
- equity-only sentiment fusion with a one-trading-day lag;
- no-news neutral treatment plus observed-only sensitivity;
- separate Movie-to-Market Lab using descriptive external-price event windows.

## Movie-to-Market Lab boundary

Movie-to-Market Lab: Spider-Man versus Barbie is a secondary research extension.
It does not alter the ten offered funds.

SONY, MAT and WBD are outside the supplied 50-equity course universe. The app
therefore keeps the film evidence separate from the official fund comparison
and does not present movie-market associations as causal proof or portfolio
signals.

## Reproduce and verify

```bash
python -m pytest -q
python -m ruff check .
python scripts/check_handin.py
```

## Student-controlled finalisation

The package remains local and pre-submission until the student personally:

- approves or rewrites the interpretation in their own voice;
- verifies the citations in `CITATION_VERIFICATION.md`;
- completes the authorship reflection in `ai/AI_NOTES.md`;
- later creates the public GitHub repository and public Streamlit deployment.
