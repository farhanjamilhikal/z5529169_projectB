"""Project B smoke and leakage-control tests.

Run from the project root: python tests/test_smoke.py
"""

from __future__ import annotations

import pathlib
import sys

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src import features, portfolios  # noqa: E402


def test_daily_returns_stay_within_ticker():
    prices = pd.DataFrame(
        {
            "ticker": ["A", "A", "B", "B"],
            "date": pd.to_datetime(["2020-01-01", "2020-01-02"] * 2),
            "adjClose": [100.0, 110.0, 50.0, 45.0],
        }
    )
    result = features.daily_returns(prices)
    assert result.groupby("ticker")["return"].nth(0).isna().all()
    assert np.isclose(
        result.loc[(result.ticker == "A") & result["return"].notna(), "return"].iloc[0], 0.10
    )
    assert np.isclose(
        result.loc[(result.ticker == "B") & result["return"].notna(), "return"].iloc[0], -0.10
    )


def test_weights_are_feasible_and_methods_differ():
    rng = np.random.default_rng(5529169)
    dates = pd.bdate_range("2020-01-01", periods=320)
    data = pd.DataFrame(
        rng.normal(0.0002, [0.01, 0.02, 0.03], size=(320, 3)), index=dates, columns=list("ABC")
    )
    ew = portfolios.estimate_weights(data, "equal_weight", 0.6)
    mv = portfolios.estimate_weights(data, "min_variance", 0.6)
    rp = portfolios.estimate_weights(data, "risk_parity", 0.6)
    for weights in (ew, mv, rp):
        assert np.isclose(weights.sum(), 1.0)
        assert (weights >= 0).all() and (weights <= 0.6 + 1e-9).all()
    assert not np.allclose(ew, mv)
    assert not np.allclose(mv, rp)


def test_backtest_starts_after_estimation_window():
    rng = np.random.default_rng(7)
    returns = pd.DataFrame(
        rng.normal(0, 0.01, size=(300, 3)),
        index=pd.bdate_range("2020-01-01", periods=300),
        columns=list("ABC"),
    )
    backtest, weights = portfolios.oos_backtest(
        returns, "equal_weight", estimation_window=252, max_weight=0.5
    )
    assert backtest.index.min() == weights.index.min()
    assert weights.index.min() >= returns.index[252]


def test_minimum_group_floor_is_enforced():
    rng = np.random.default_rng(22)
    data = pd.DataFrame(
        rng.normal(0, [0.01, 0.02, 0.04, 0.05], size=(300, 4)),
        index=pd.bdate_range("2020-01-01", periods=300),
        columns=["A", "B", "C", "D"],
    )
    weights = portfolios.estimate_weights(
        data,
        "min_variance",
        max_weight=0.6,
        minimum_group={"C", "D"},
        minimum_group_weight=0.30,
    )
    assert weights[["C", "D"]].sum() >= 0.30 - 1e-8
    assert np.isclose(weights.sum(), 1.0)


def test_required_artifacts_and_weight_sums():
    required = [
        ROOT / "results/data/fund_returns.csv",
        ROOT / "results/data/fund_weights.csv",
        ROOT / "results/data/sector_sentiment_index.csv",
        ROOT / "results/tables/performance_metrics.csv",
    ]
    assert all(path.exists() for path in required)
    weights = pd.read_csv(required[1])
    sums = weights.groupby(["fund", "date"])["weight"].sum()
    assert np.allclose(sums, 1.0, atol=1e-8)
    assert weights["fund"].nunique() >= 10


if __name__ == "__main__":
    test_daily_returns_stay_within_ticker()
    test_weights_are_feasible_and_methods_differ()
    test_backtest_starts_after_estimation_window()
    test_required_artifacts_and_weight_sums()
    print("Project B smoke tests passed")
