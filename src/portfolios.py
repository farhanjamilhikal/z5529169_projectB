"""Leakage-safe walk-forward portfolio construction for Station 3."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import minimize

METHOD_LABELS = {
    "equal_weight": "Equal Weight",
    "min_variance": "Minimum Variance",
    "risk_parity": "Risk Parity",
}


def _clean_estimation_window(window: pd.DataFrame) -> pd.DataFrame:
    return window.replace([np.inf, -np.inf], np.nan).dropna(how="all").fillna(0.0)


def estimate_weights(
    window: pd.DataFrame,
    method: str,
    max_weight: float = 0.20,
    minimum_group: set[str] | None = None,
    minimum_group_weight: float = 0.0,
) -> pd.Series:
    """Estimate long-only weights from past returns only."""
    x = _clean_estimation_window(window)
    n = x.shape[1]
    if n == 0:
        raise ValueError("No assets in estimation window")
    cap = max(max_weight, 1.0 / n)
    equal = np.full(n, 1.0 / n)
    group_mask = np.array([column in (minimum_group or set()) for column in x.columns])
    if minimum_group_weight and not group_mask.any():
        raise ValueError("minimum_group does not match any asset")
    if not 0.0 <= minimum_group_weight <= 1.0:
        raise ValueError("minimum_group_weight must be between zero and one")
    initial = equal.copy()
    if minimum_group_weight > initial[group_mask].sum():
        initial[group_mask] = minimum_group_weight / group_mask.sum()
        initial[~group_mask] = (1.0 - minimum_group_weight) / (~group_mask).sum()
    if initial.max() > cap + 1e-12:
        raise ValueError("Group floor is infeasible under the asset cap")
    if method == "equal_weight":
        return pd.Series(equal, index=x.columns)

    if method == "risk_parity":
        # Inverse-volatility risk parity is stable in a 60-asset short sample and
        # equals volatility-contribution parity under a diagonal covariance model.
        vol = x.std(ddof=1).replace(0, np.nan)
        raw = (1.0 / vol).replace([np.inf, -np.inf], np.nan).fillna(0.0)
        weights = raw / raw.sum() if raw.sum() > 0 else pd.Series(equal, index=x.columns)
        for _ in range(20):
            over = weights > cap
            if not over.any():
                break
            excess = float((weights[over] - cap).sum())
            weights.loc[over] = cap
            room = (cap - weights[~over]).clip(lower=0)
            if room.sum() <= 0:
                break
            weights.loc[~over] += excess * room / room.sum()
        return weights / weights.sum()

    sample_cov = x.cov().to_numpy() * 252.0
    diag = np.diag(np.diag(sample_cov))
    cov = 0.90 * sample_cov + 0.10 * diag + np.eye(n) * 1e-8
    bounds = [(0.0, cap)] * n
    constraints: tuple[dict, ...] = ({"type": "eq", "fun": lambda w: np.sum(w) - 1.0},)
    if minimum_group_weight:
        constraints += (
            {
                "type": "ineq",
                "fun": lambda w: np.sum(w[group_mask]) - minimum_group_weight,
            },
        )

    if method == "min_variance":

        def objective(w):
            return float(w @ cov @ w)
    else:
        raise ValueError(f"Unknown portfolio method: {method}")

    result = minimize(
        objective,
        initial,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={"maxiter": 500, "ftol": 1e-12},
    )
    if not result.success or not np.isfinite(result.x).all():
        raise RuntimeError(f"{method} optimisation failed: {result.message}")
    weights = np.clip(result.x, 0, cap)
    weights /= weights.sum()
    return pd.Series(weights, index=x.columns)


def _monthly_rebalance_dates(index: pd.DatetimeIndex, min_history: int) -> list[pd.Timestamp]:
    live = pd.Series(index[min_history:], index=index[min_history:])
    return list(live.groupby(live.index.to_period("M")).first().values)


def returns_from_rebalance_weights(
    returns: pd.DataFrame,
    weights: pd.DataFrame,
    transaction_cost_bps: float = 10.0,
) -> pd.DataFrame:
    """Apply dated target weights from each rebalance until the next rebalance."""
    r = returns.sort_index().copy()
    w = weights.sort_index().reindex(columns=r.columns, fill_value=0.0)
    daily_w = w.reindex(r.index).ffill().dropna(how="all")
    r = r.loc[daily_w.index].fillna(0.0)
    daily_w = daily_w.reindex(columns=r.columns).fillna(0.0)
    gross = (r * daily_w).sum(axis=1)

    turnover_at_rebalance = w.diff().abs().sum(axis=1)
    if len(turnover_at_rebalance):
        turnover_at_rebalance.iloc[0] = float(w.iloc[0].abs().sum())
    turnover = pd.Series(0.0, index=gross.index)
    turnover.loc[turnover.index.intersection(turnover_at_rebalance.index)] = (
        turnover_at_rebalance.reindex(turnover.index.intersection(turnover_at_rebalance.index))
    )
    cost = turnover * (transaction_cost_bps / 10_000.0)
    net = gross - cost
    growth = (1.0 + net).cumprod()
    drawdown = growth / growth.cummax() - 1.0
    return pd.DataFrame(
        {
            "gross_return": gross,
            "turnover": turnover,
            "transaction_cost": cost,
            "net_return": net,
            "growth_of_1": growth,
            "drawdown": drawdown,
        }
    )


def oos_backtest(
    returns: pd.DataFrame,
    method: str = "min_variance",
    estimation_window: int = 252,
    max_weight: float = 0.20,
    transaction_cost_bps: float = 10.0,
    minimum_group: set[str] | None = None,
    minimum_group_weight: float = 0.0,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Monthly walk-forward backtest; date t weights use observations strictly before t."""
    wide = returns.sort_index().copy()
    dates = _monthly_rebalance_dates(wide.index, estimation_window)
    weight_rows = []
    for date in dates:
        loc = wide.index.get_loc(date)
        history = wide.iloc[max(0, loc - estimation_window) : loc]
        estimated = estimate_weights(
            history,
            method=method,
            max_weight=max_weight,
            minimum_group=minimum_group,
            minimum_group_weight=minimum_group_weight,
        )
        estimated.name = date
        weight_rows.append(estimated)
    if not weight_rows:
        raise ValueError("Insufficient observations for the requested estimation window")
    weights = pd.DataFrame(weight_rows)
    weights.index.name = "date"
    backtest = returns_from_rebalance_weights(wide, weights, transaction_cost_bps)
    backtest.index.name = "date"
    return backtest, weights


def performance_metrics(daily_returns: pd.Series, periods_per_year: int = 252) -> dict:
    series = pd.Series(daily_returns).dropna()
    if series.empty:
        return {
            key: np.nan
            for key in (
                "annualised_return",
                "annualised_volatility",
                "sharpe_ratio",
                "maximum_drawdown",
            )
        }
    growth = (1.0 + series).cumprod()
    years = len(series) / periods_per_year
    ann_return = (
        growth.iloc[-1] ** (1.0 / years) - 1.0 if years > 0 and growth.iloc[-1] > 0 else np.nan
    )
    ann_vol = series.std(ddof=1) * np.sqrt(periods_per_year)
    sharpe = (
        series.mean() / series.std(ddof=1) * np.sqrt(periods_per_year)
        if series.std(ddof=1) > 0
        else np.nan
    )
    return {
        "annualised_return": float(ann_return),
        "annualised_volatility": float(ann_vol),
        "sharpe_ratio": float(sharpe),
        "maximum_drawdown": float((growth / growth.cummax() - 1.0).min()),
        "ending_value": float(growth.iloc[-1]),
        "observations": len(series),
        "total_turnover": np.nan,
    }
