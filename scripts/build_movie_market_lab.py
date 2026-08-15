"""Build the external Spider-Man versus Barbie market-evidence lab.

This extension is deliberately separate from the official course universe. It
uses public daily adjusted-price data for event-study description only. It does
not alter any of the ten offered funds or claim that film marketing caused a
share-price movement.
"""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "research_extension" / "raw"
TABLE_DIR = ROOT / "results" / "tables"
DATA_DIR = ROOT / "results" / "data"

START_EPOCH = 1577836800  # 2020-01-01 UTC
END_EPOCH = 1704067200  # 2024-01-01 UTC, exclusive

TICKERS = {
    "SONY": "Spider-Man primary studio exposure",
    "DIS": "Spider-Man secondary co-finance/IP context; not primary case ticker",
    "MAT": "Barbie IP-owner and producer exposure",
    "WBD": "Barbie distributor exposure",
    "SPY": "Broad US equity-market benchmark",
}

EVENTS = [
    {
        "film": "Spider-Man: No Way Home",
        "event_stage": "Official teaser trailer",
        "event_date": "2021-08-23",
        "primary_ticker": "SONY",
        "source_id": "S03",
    },
    {
        "film": "Spider-Man: No Way Home",
        "event_stage": "Official trailer",
        "event_date": "2021-11-16",
        "primary_ticker": "SONY",
        "source_id": "S04",
    },
    {
        "film": "Spider-Man: No Way Home",
        "event_stage": "US theatrical release",
        "event_date": "2021-12-17",
        "primary_ticker": "SONY",
        "source_id": "S01",
    },
    {
        "film": "Barbie",
        "event_stage": "Teaser trailer 2",
        "event_date": "2023-04-04",
        "primary_ticker": "MAT",
        "source_id": "S10",
    },
    {
        "film": "Barbie",
        "event_stage": "Main trailer",
        "event_date": "2023-05-25",
        "primary_ticker": "MAT",
        "source_id": "S11",
    },
    {
        "film": "Barbie",
        "event_stage": "US theatrical release",
        "event_date": "2023-07-21",
        "primary_ticker": "MAT",
        "source_id": "S06",
    },
]


def _download_yahoo_chart(ticker: str) -> dict:
    url = (
        "https://query2.finance.yahoo.com/v8/finance/chart/"
        f"{quote(ticker)}?period1={START_EPOCH}&period2={END_EPOCH}"
        "&interval=1d&events=history&includeAdjustedClose=true"
    )
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=60) as response:
        return json.load(response)


def _chart_to_frame(ticker: str, payload: dict) -> pd.DataFrame:
    result = payload["chart"]["result"][0]
    quote_data = result["indicators"]["quote"][0]
    adjusted = result["indicators"].get("adjclose", [{}])[0].get("adjclose")
    if adjusted is None:
        adjusted = quote_data["close"]
    return pd.DataFrame(
        {
            "date": pd.to_datetime(result["timestamp"], unit="s", utc=True)
            .tz_convert(None)
            .normalize(),
            "ticker": ticker,
            "open": quote_data["open"],
            "high": quote_data["high"],
            "low": quote_data["low"],
            "close": quote_data["close"],
            "adjClose": adjusted,
            "volume": quote_data["volume"],
        }
    ).dropna(subset=["adjClose"])


def load_prices() -> pd.DataFrame:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    frames = []
    for ticker in TICKERS:
        cache_path = RAW_DIR / f"yahoo_chart_{ticker}.json"
        if cache_path.exists():
            payload = json.loads(cache_path.read_text(encoding="utf-8"))
        else:
            payload = _download_yahoo_chart(ticker)
            cache_path.write_text(json.dumps(payload), encoding="utf-8")
        frames.append(_chart_to_frame(ticker, payload))
    prices = pd.concat(frames, ignore_index=True).sort_values(["ticker", "date"])
    prices["return"] = prices.groupby("ticker", sort=False)["adjClose"].pct_change()
    return prices


def _relative_position(dates: pd.Series, event_date: pd.Timestamp) -> int:
    positions = np.flatnonzero(dates.to_numpy() >= np.datetime64(event_date))
    if not len(positions):
        raise ValueError(f"No trading date on or after {event_date.date()}")
    return int(positions[0])


def build_event_windows(prices: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    windows = []
    for event in EVENTS:
        event_date = pd.Timestamp(event["event_date"])
        tickers = [event["primary_ticker"], "SPY"]
        event_frames = {}
        for ticker in tickers:
            frame = prices.loc[prices["ticker"].eq(ticker)].reset_index(drop=True)
            event_pos = _relative_position(frame["date"], event_date)
            start = max(0, event_pos - 5)
            end = min(len(frame) - 1, event_pos + 5)
            window = frame.loc[start:end].copy()
            window["relative_trading_day"] = np.arange(start - event_pos, end - event_pos + 1)
            window["film"] = event["film"]
            window["event_stage"] = event["event_stage"]
            window["announced_event_date"] = event_date
            event_frames[ticker] = (frame, event_pos, start, end)
            windows.append(window)

        asset_frame, asset_pos, start, end = event_frames[event["primary_ticker"]]
        benchmark_frame, benchmark_pos, bench_start, bench_end = event_frames["SPY"]
        asset_window_return = (
            asset_frame.loc[end, "adjClose"] / asset_frame.loc[start, "adjClose"] - 1
        )
        benchmark_window_return = (
            benchmark_frame.loc[bench_end, "adjClose"]
            / benchmark_frame.loc[bench_start, "adjClose"]
            - 1
        )
        rows.append(
            {
                **event,
                "mapped_trading_date": asset_frame.loc[asset_pos, "date"],
                "event_day_return": asset_frame.loc[asset_pos, "return"],
                "benchmark_event_day_return": benchmark_frame.loc[
                    benchmark_pos, "return"
                ],
                "event_day_market_adjusted_return": asset_frame.loc[
                    asset_pos, "return"
                ]
                - benchmark_frame.loc[benchmark_pos, "return"],
                "window_start": asset_frame.loc[start, "date"],
                "window_end": asset_frame.loc[end, "date"],
                "eleven_trading_day_return": asset_window_return,
                "benchmark_eleven_day_return": benchmark_window_return,
                "eleven_day_market_adjusted_return": asset_window_return
                - benchmark_window_return,
                "interpretation_limit": (
                    "Descriptive association only; no causal attribution to marketing."
                ),
            }
        )
    return pd.DataFrame(rows), pd.concat(windows, ignore_index=True)


def build_exposure_register() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "film": "Spider-Man: No Way Home",
                "company": "Sony Group Corporation",
                "ticker": "SONY",
                "channel": "Columbia Pictures studio and theatrical economics",
                "course_universe": "No",
                "portfolio_status": "External research-lab primary exposure",
                "evidence_source_ids": "S01;S02",
                "confidence": "High",
            },
            {
                "film": "Spider-Man: No Way Home",
                "company": "The Walt Disney Company",
                "ticker": "DIS",
                "channel": "Marvel/IP and co-finance context",
                "course_universe": "Yes",
                "portfolio_status": "Context only; exposure is not isolated in course data",
                "evidence_source_ids": "S05",
                "confidence": "Medium",
            },
            {
                "film": "Barbie",
                "company": "Mattel, Inc.",
                "ticker": "MAT",
                "channel": "Barbie IP owner and Mattel Films producer",
                "course_universe": "No",
                "portfolio_status": "External research-lab primary exposure",
                "evidence_source_ids": "S06;S07;S08",
                "confidence": "High",
            },
            {
                "film": "Barbie",
                "company": "Warner Bros. Discovery, Inc.",
                "ticker": "WBD",
                "channel": "Worldwide theatrical distribution",
                "course_universe": "No",
                "portfolio_status": "External research-lab secondary exposure",
                "evidence_source_ids": "S09;S10;S11",
                "confidence": "High",
            },
        ]
    )


def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    prices = load_prices()
    event_summary, event_windows = build_event_windows(prices)
    prices.to_csv(DATA_DIR / "movie_lab_external_prices_2020_2023.csv", index=False)
    event_windows.to_csv(DATA_DIR / "movie_lab_event_windows.csv", index=False)
    event_summary.to_csv(TABLE_DIR / "movie_lab_event_summary.csv", index=False)
    build_exposure_register().to_csv(
        TABLE_DIR / "movie_lab_exposure_register.csv", index=False
    )
    print(event_summary.to_string(index=False))


if __name__ == "__main__":
    main()
