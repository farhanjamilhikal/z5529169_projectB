"""Station 2 features reused consistently in Part B."""

from __future__ import annotations

import numpy as np
import pandas as pd


def daily_returns(prices: pd.DataFrame, price_col: str = "adjClose") -> pd.DataFrame:
    frame = prices.copy()
    frame["date"] = pd.to_datetime(frame["date"]).dt.tz_localize(None)
    frame = frame.sort_values(["ticker", "date"]).reset_index(drop=True)
    frame["return"] = frame.groupby("ticker")[price_col].pct_change(fill_method=None)
    return frame


def returns_wide(return_frame: pd.DataFrame) -> pd.DataFrame:
    return return_frame.pivot(index="date", columns="ticker", values="return").sort_index()


def align_headlines_to_trading_days(
    headlines: pd.DataFrame, equity_dates: pd.Series
) -> pd.DataFrame:
    """Assign non-trading-day headlines to the next equity trading day."""
    frame = headlines.copy()
    frame["publication_date"] = (
        pd.to_datetime(frame["date"]).dt.tz_localize(None).dt.normalize().astype("datetime64[ns]")
    )
    calendar = pd.DataFrame(
        {
            "aligned_date": sorted(
                pd.to_datetime(equity_dates)
                .dt.tz_localize(None)
                .dt.normalize()
                .astype("datetime64[ns]")
                .unique()
            )
        }
    )
    frame = frame.sort_values("publication_date").reset_index(drop=True)
    aligned = pd.merge_asof(
        frame,
        calendar,
        left_on="publication_date",
        right_on="aligned_date",
        direction="forward",
        allow_exact_matches=True,
    ).dropna(subset=["aligned_date"])
    aligned["shift_days"] = (aligned["aligned_date"] - aligned["publication_date"]).dt.days
    return aligned.reset_index(drop=True)


def asset_data_use_register() -> pd.DataFrame:
    """Account for every supplied field without forcing metadata into optimisation."""
    rows = [
        (
            "equity_prices",
            "ticker",
            "Model input / identifier",
            "Defines assets, holdings and per-asset calculations",
        ),
        (
            "equity_prices",
            "date",
            "Model timing",
            "Controls ordering, estimation windows and no-look-ahead application",
        ),
        ("equity_prices", "adjClose", "Model input", "Creates total-return-adjusted daily returns"),
        (
            "equity_prices",
            "open, high, low, close",
            "Diagnostic",
            "Checks OHLC consistency and documents intraday price range",
        ),
        (
            "equity_prices",
            "volume",
            "Diagnostic / product disclosure",
            "Measures trading activity; not treated as a return predictor",
        ),
        (
            "equity_prices",
            "sector",
            "Model grouping",
            "Defines equity universe reporting and sector sentiment aggregation",
        ),
        (
            "crypto_prices",
            "ticker, date, adjClose",
            "Model input",
            "Creates seven-day crypto returns before calendar alignment",
        ),
        (
            "crypto_prices",
            "open, high, low, close, volume",
            "Diagnostic",
            "Checks source integrity and describes market activity",
        ),
        (
            "news_headlines",
            "title",
            "Sentiment model input",
            "Scored without stripping punctuation, casing or negation",
        ),
        (
            "news_headlines",
            "date",
            "Model timing",
            "Mapped to the next equity trading day then lagged one trading day",
        ),
        (
            "news_headlines",
            "ticker, sector",
            "Model grouping",
            "Builds ticker-day signals and equal-weight sector indices",
        ),
        (
            "news_headlines",
            "publisher",
            "Reliability diagnostic",
            "Measures publisher completeness and diversity",
        ),
        (
            "news_headlines",
            "url",
            "Provenance / audit",
            "Retained for traceability; never used as a predictor",
        ),
    ]
    return pd.DataFrame(rows, columns=["dataset", "field", "role", "justification"])


def asset_liquidity_diagnostics(equities: pd.DataFrame, crypto: pd.DataFrame) -> pd.DataFrame:
    frames = []
    for name, source in (("Equity", equities), ("Crypto", crypto)):
        f = source.copy()
        f["dollar_volume_proxy"] = f["close"].abs() * f["volume"].clip(lower=0)
        g = (
            f.groupby("ticker")
            .agg(
                median_daily_volume=("volume", "median"),
                median_dollar_volume_proxy=("dollar_volume_proxy", "median"),
            )
            .reset_index()
        )
        ranges = (
            ((f["high"] - f["low"]) / f["close"].replace(0, np.nan)).groupby(f["ticker"]).median()
        )
        g["median_intraday_range_pct"] = g["ticker"].map(ranges)
        g.insert(1, "asset_class", name)
        frames.append(g)
    return pd.concat(frames, ignore_index=True)
