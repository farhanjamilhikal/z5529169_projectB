"""Shared Station 1 cleaning carried forward from the student's Part A."""

from __future__ import annotations

import numpy as np
import pandas as pd

from src import data_access

END_DATE = pd.Timestamp("2023-12-31")


def _prepare_prices(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    out["date"] = pd.to_datetime(out["date"]).dt.tz_localize(None)
    out = out.loc[out["date"] <= END_DATE].copy()
    return (
        out.sort_values(["ticker", "date"])
        .drop_duplicates(["ticker", "date"], keep="first")
        .reset_index(drop=True)
    )


def _price_audit(frame: pd.DataFrame, dataset: str) -> pd.DataFrame:
    ordered = frame.sort_values(["ticker", "date"]).copy()
    returns = ordered.groupby("ticker")["adjClose"].pct_change(fill_method=None)
    med = returns.groupby(ordered["ticker"]).transform("median")
    mad = (returns - med).abs().groupby(ordered["ticker"]).transform("median")
    rz = 0.6745 * (returns - med) / mad.replace(0, np.nan)
    checks = {
        "duplicate_ticker_date": frame.duplicated(["ticker", "date"]).sum(),
        "missing_adjClose": frame["adjClose"].isna().sum(),
        "non_positive_adjClose": (frame["adjClose"] <= 0).sum(),
        "negative_volume": (frame["volume"] < 0).sum(),
        "ohlc_inconsistency": (
            (frame["high"] < frame[["open", "close"]].max(axis=1))
            | (frame["low"] > frame[["open", "close"]].min(axis=1))
            | (frame["low"] > frame["high"])
        ).sum(),
        "extreme_return_review": ((returns.abs() > 0.20) | (rz.abs() > 3.5)).sum(),
    }
    return pd.DataFrame(
        [
            {"dataset": dataset, "check": key, "issue_count": int(value)}
            for key, value in checks.items()
        ]
    )


def load_clean_equities() -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = data_access.load_equity_prices()
    dated = raw.assign(date=pd.to_datetime(raw["date"]).dt.tz_localize(None))
    return _prepare_prices(raw), _price_audit(dated, "equities")


def load_clean_crypto() -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = data_access.load_crypto_prices()
    dated = raw.assign(date=pd.to_datetime(raw["date"]).dt.tz_localize(None))
    filtered = dated.loc[dated["date"] <= END_DATE].copy()
    audit = _price_audit(filtered, "crypto")
    extra = pd.DataFrame(
        [
            {
                "dataset": "crypto",
                "check": "rows_after_2023_12_31",
                "issue_count": int((dated["date"] > END_DATE).sum()),
            }
        ]
    )
    return _prepare_prices(raw), pd.concat([audit, extra], ignore_index=True)


def load_clean_news() -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = data_access.load_news_headlines().copy()
    raw["date"] = pd.to_datetime(raw["date"], utc=True).dt.tz_convert(None)
    raw = raw.loc[raw["date"] <= END_DATE].copy()
    blank = raw["title"].fillna("").str.strip().eq("")
    duplicates = raw.duplicated(["ticker", "date", "title"])
    audit = pd.DataFrame(
        [
            {"dataset": "news_headlines", "check": "blank_title", "issue_count": int(blank.sum())},
            {
                "dataset": "news_headlines",
                "check": "duplicate_ticker_date_title",
                "issue_count": int(duplicates.sum()),
            },
            {
                "dataset": "news_headlines",
                "check": "missing_publisher",
                "issue_count": int(raw["publisher"].fillna("").str.strip().eq("").sum()),
            },
            {
                "dataset": "news_headlines",
                "check": "missing_url",
                "issue_count": int(raw["url"].fillna("").str.strip().eq("").sum()),
            },
        ]
    )
    clean = (
        raw.loc[~blank & ~duplicates]
        .sort_values(["ticker", "date", "title"])
        .reset_index(drop=True)
    )
    return clean, audit
