from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent


def test_required_artifact_schemas_and_counts():
    returns = pd.read_csv(ROOT / "results/data/fund_returns.csv")
    weights = pd.read_csv(ROOT / "results/data/fund_weights.csv")
    sectors = pd.read_csv(ROOT / "results/data/sector_sentiment_index.csv")
    metrics = pd.read_csv(ROOT / "results/tables/performance_metrics.csv")

    assert returns["fund"].nunique() == 10
    assert metrics["fund"].nunique() == 10
    assert set(metrics["family"]) == {"Equity", "Crypto", "Combined"}
    assert sectors["sector"].nunique() == 10
    assert set(
        ["annualised_return", "annualised_volatility", "sharpe_ratio", "maximum_drawdown"]
    ).issubset(metrics.columns)
    assert np.allclose(weights.groupby(["fund", "date"])["weight"].sum(), 1.0, atol=1e-8)


def test_sentiment_lag_is_previous_ticker_trading_day():
    signals = pd.read_csv(
        ROOT / "results/data/ticker_sentiment_signals.csv",
        parse_dates=["date"],
    ).sort_values(["ticker", "date"])
    expected = signals.groupby("ticker")["sentiment"].shift(1)
    actual = signals["usable_sentiment_lag1"]
    assert np.allclose(actual.fillna(0.0), expected.fillna(0.0), atol=1e-12)


def test_all_required_figures_exist_and_are_nontrivial():
    names = [
        "growth_of_one_comparison.png",
        "fund_drawdowns.png",
        "combined_weights_over_time.png",
        "risk_return_across_funds.png",
        "sector_sentiment_index.png",
        "fusion_before_after.png",
        "crypto_sleeve_floor_sensitivity.png",
    ]
    for name in names:
        path = ROOT / "results/figures" / name
        assert path.exists()
        assert path.stat().st_size > 50_000


def test_product_assurance_registers_are_complete():
    feasibility = pd.read_csv(ROOT / "results/tables/product_feasibility_scorecard.csv")
    figures = pd.read_csv(ROOT / "results/tables/figure_inventory.csv")
    sentiment_checks = pd.read_csv(ROOT / "results/tables/sentiment_product_app_checks.csv")
    risks = pd.read_csv(ROOT / "results/tables/risk_mitigation_register.csv")
    dual = pd.read_csv(ROOT / "results/tables/dual_domain_sentiment_validation.csv")

    assert np.isclose(feasibility["weight_pct"].sum(), 100)
    assert np.isclose(feasibility["weighted_points"].sum(), 63)
    assert (figures["status"] == "PASS").all()
    assert (sentiment_checks["status"] == "FAIL").sum() == 0
    assert set(risks["status"]).issubset({"Controlled", "Partial", "Open", "Blocker"})
    movie = dual[dual["domain"] == "Movie reviews (NLTK binary)"]
    assert len(movie) == 2
    assert np.allclose(movie["accuracy"], 0.635)


def test_crypto_sleeve_floor_sensitivity_is_research_only():
    sensitivity = pd.read_csv(ROOT / "results/tables/crypto_sleeve_floor_sensitivity.csv")
    assert sensitivity["crypto_floor_pct"].tolist() == [0.0, 10.0, 20.0, 30.0]
    assert np.allclose(
        sensitivity.loc[sensitivity["crypto_floor_pct"] > 0, "latest_crypto_weight"],
        [0.10, 0.20, 0.30],
    )
    assert sensitivity["status"].str.contains("not an offered fund").all()
