"""Pure presentation calculations for the Signal & Story dashboard."""

from __future__ import annotations

import numpy as np
import pandas as pd


def pct(value: float) -> str:
    """Format a decimal as a percentage for investor-facing displays."""
    return "-" if pd.isna(value) else f"{value:.2%}"


def allocation_series(
    fund_returns: pd.DataFrame,
    allocations: dict[str, float],
) -> tuple[pd.DataFrame, pd.Series]:
    """Create a decision-calendar allocation and fund return contributions.

    Equity and combined funds have no weekend observations. When mixed with a
    crypto-only fund, those non-trading-day returns are explicitly zero while
    crypto continues to move. This preserves the supplied funds' native
    calendars without fabricating equity returns.
    """
    chosen = list(allocations)
    daily = fund_returns[fund_returns["fund"].isin(chosen)].pivot(
        index="date",
        columns="fund",
        values="net_return",
    )
    daily = daily.sort_index().reindex(columns=chosen).dropna(how="all").fillna(0.0)
    contributions = daily.mul(pd.Series(allocations), axis="columns")
    portfolio = contributions.sum(axis=1).rename("allocation_return")
    return contributions, portfolio


def allocation_metrics(series: pd.Series, periods_per_year: int = 252) -> dict[str, float]:
    """Annualised metrics for a custom allocation.

    periods_per_year should be 365 for a crypto-only selection (native seven-day
    calendar) and 252 for anything that includes an equity or combined fund
    (equity decision calendar), matching the annualisation convention used
    elsewhere in the app and report.
    """
    clean = series.dropna()
    if clean.empty:
        return {key: np.nan for key in ("Return", "Volatility", "Sharpe", "Max drawdown")}
    growth = (1.0 + clean).cumprod()
    volatility = clean.std(ddof=1) * np.sqrt(periods_per_year)
    return {
        "Return": growth.iloc[-1] ** (periods_per_year / len(clean)) - 1.0,
        "Volatility": volatility,
        "Sharpe": (
            clean.mean() / clean.std(ddof=1) * np.sqrt(periods_per_year) if clean.std(ddof=1) > 0 else np.nan
        ),
        "Max drawdown": (growth / growth.cummax() - 1.0).min(),
    }


def allocation_export(
    contributions: pd.DataFrame,
    portfolio: pd.Series,
) -> pd.DataFrame:
    """Return a downloadable date-level allocation audit."""
    result = contributions.copy()
    result["allocation_return"] = portfolio
    result["growth_of_1"] = (1.0 + portfolio).cumprod()
    result["drawdown"] = result["growth_of_1"] / result["growth_of_1"].cummax() - 1.0
    return result.reset_index()


def build_status_frame(metrics: pd.DataFrame) -> tuple[pd.Timestamp, pd.Timestamp, int]:
    """Summarise live dates and the number of offered funds."""
    return (
        pd.to_datetime(metrics["first_live_date"]).min(),
        pd.to_datetime(metrics["last_live_date"]).max(),
        int(metrics["fund"].nunique()),
    )


def fund_leaders(metrics: pd.DataFrame) -> dict[str, pd.Series]:
    """Identify transparent comparison anchors without hiding downside risk."""
    combined = metrics.loc[metrics["family"] == "Combined"]
    return {
        "diversified_balance": combined.loc[combined["sharpe_ratio"].idxmax()],
        "lowest_volatility": metrics.loc[metrics["annualised_volatility"].idxmin()],
        "highest_return": metrics.loc[metrics["annualised_return"].idxmax()],
    }


def objective_candidate(metrics: pd.DataFrame, objective: str) -> tuple[pd.Series, str, str]:
    """Map an educational objective to historical evidence and its main caveat."""
    if objective == "Capital stability":
        row = metrics.loc[metrics["annualised_volatility"].idxmin()]
        return (
            row,
            "Lowest annualised volatility in the live sample.",
            "Low volatility came with lower return and does not prevent losses.",
        )
    if objective == "Diversified balance":
        combined = metrics.loc[metrics["family"] == "Combined"]
        row = combined.loc[combined["sharpe_ratio"].idxmax()]
        return (
            row,
            "Highest Sharpe ratio among the combined funds.",
            "The fund still experienced a material drawdown and has modest crypto exposure.",
        )
    if objective == "Transparent simplicity":
        row = metrics.loc[metrics["fund"] == "Equity Equal Weight"].iloc[0]
        return (
            row,
            "Simple allocation rule, broad equity exposure and low turnover.",
            "Equal weighting ignores differences in asset risk and covariance.",
        )
    if objective == "Maximum historical growth":
        row = metrics.loc[metrics["annualised_return"].idxmax()]
        return (
            row,
            "Highest annualised return in the live sample.",
            "The result carries extreme volatility, drawdown and concentration risk.",
        )
    if objective == "Sentiment research":
        row = metrics.loc[metrics["fund"] == "Equity Reliability-Gated Sentiment"].iloc[0]
        return (
            row,
            "Transparent, lagged fusion of market prices and headline sentiment.",
            "The improvement is modest, highly correlated with the base fund and non-causal.",
        )
    raise ValueError(f"Unknown objective: {objective}")


def fact_sheet_interpretation(row: pd.Series, metrics: pd.DataFrame) -> str:
    """Generate a restrained, evidence-based interpretation of a selected fund."""
    vol_rank = metrics["annualised_volatility"].rank(method="min").loc[row.name]
    return_rank = metrics["annualised_return"].rank(ascending=False, method="min").loc[row.name]
    if row["maximum_drawdown"] <= -0.50:
        risk = "Its historical drawdown exceeds 50%, so it is a high-risk satellite rather than a capital-preservation fund."
    elif vol_rank <= 3:
        risk = "It sits among the three lowest-volatility funds in this sample."
    else:
        risk = "Its risk is material and should be read beside the drawdown chart, not from return alone."
    return (
        f"{row['fund']} ranks {int(return_rank)} of {len(metrics)} by annualised return. "
        f"{risk} The result is historical and sample-dependent."
    )


def latest_sector_snapshot(
    sector_index: pd.DataFrame,
    window: int = 21,
) -> pd.DataFrame:
    """Return latest smoothed sentiment and coverage for every sector."""
    frame = sector_index.copy().sort_values(["sector", "date"])
    frame["smoothed_sentiment"] = frame.groupby("sector")["sentiment"].transform(
        lambda series: series.rolling(window, min_periods=1).mean()
    )
    frame["smoothed_coverage"] = frame.groupby("sector")["coverage_rate"].transform(
        lambda series: series.rolling(window, min_periods=1).mean()
    )
    return (
        frame.groupby("sector", as_index=False)
        .tail(1)
        .sort_values(
            "smoothed_sentiment",
            ascending=False,
        )
    )
