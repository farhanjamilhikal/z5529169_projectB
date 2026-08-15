from __future__ import annotations

import numpy as np
import pandas as pd

from src import app_logic


def test_allocation_series_and_metrics_are_mathematically_consistent():
    returns = pd.DataFrame(
        {
            "date": pd.to_datetime(["2021-01-01", "2021-01-02"] * 2),
            "fund": ["A", "A", "B", "B"],
            "net_return": [0.10, 0.00, 0.00, 0.20],
        }
    )
    contributions, portfolio = app_logic.allocation_series(returns, {"A": 0.6, "B": 0.4})
    assert np.allclose(portfolio.to_numpy(), [0.06, 0.08])
    assert np.allclose(contributions.sum(axis=1), portfolio)
    result = app_logic.allocation_metrics(portfolio)
    expected_growth = 1.06 * 1.08
    assert np.isclose(result["Return"], expected_growth ** (252 / 2) - 1)
    assert result["Max drawdown"] == 0.0


def test_latest_sector_snapshot_orders_leader_and_laggard():
    frame = pd.DataFrame(
        {
            "date": pd.to_datetime(["2023-01-01", "2023-01-02"] * 2),
            "sector": ["A", "A", "B", "B"],
            "sentiment": [0.1, 0.3, -0.2, -0.4],
            "coverage_rate": [0.8, 1.0, 0.4, 0.6],
        }
    )
    snapshot = app_logic.latest_sector_snapshot(frame, window=2)
    assert snapshot.iloc[0]["sector"] == "A"
    assert snapshot.iloc[-1]["sector"] == "B"
    assert np.isclose(snapshot.iloc[0]["smoothed_coverage"], 0.9)


def test_objective_candidate_never_hides_the_tradeoff():
    metrics = pd.DataFrame(
        {
            "fund": ["Combined Risk Parity", "Crypto Minimum Variance"],
            "family": ["Combined", "Crypto"],
            "annualised_return": [0.13, 0.60],
            "annualised_volatility": [0.16, 0.73],
            "sharpe_ratio": [0.85, 1.01],
            "maximum_drawdown": [-0.20, -0.73],
        }
    )
    row, evidence, drawback = app_logic.objective_candidate(metrics, "Maximum historical growth")
    assert row["fund"] == "Crypto Minimum Variance"
    assert "Highest annualised return" in evidence
    assert "extreme" in drawback
