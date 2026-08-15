"""Build a separate 2024-current price-only shadow evaluation.

This never overwrites the official 2020-2023 course artifacts. By default it
downloads the fixed 50-equity/10-crypto universe with yfinance. Alternatively,
set SHADOW_PRICE_CSV to a licensed ticker,date,adjClose file.
"""

from __future__ import annotations

import os
import sys
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src import portfolios  # noqa: E402

DATA = ROOT / "results" / "data"
TABLES = ROOT / "results" / "tables"
START_DOWNLOAD = "2023-01-01"
START_LIVE = pd.Timestamp("2024-01-01")
METHODS = ("equal_weight", "min_variance", "risk_parity")


def _fixed_universe() -> tuple[list[str], list[str]]:
    holdings = pd.read_csv(TABLES / "current_holdings.csv")
    tickers = sorted(holdings["ticker"].unique())
    crypto = [ticker for ticker in tickers if ticker.endswith("-USD")]
    equity = [ticker for ticker in tickers if ticker not in crypto]
    if len(equity) != 50 or len(crypto) != 10:
        raise ValueError(f"Expected 50 equities and 10 cryptos; found {len(equity)} and {len(crypto)}")
    return equity, crypto


def _load_external_prices(tickers: list[str]) -> tuple[pd.DataFrame, str]:
    supplied = os.getenv("SHADOW_PRICE_CSV")
    if supplied:
        prices = pd.read_csv(supplied, parse_dates=["date"])
        required = ["ticker", "date", "adjClose"]
        missing = set(required) - set(prices.columns)
        if missing:
            raise ValueError(f"SHADOW_PRICE_CSV is missing columns: {sorted(missing)}")
        return prices[required].copy(), f"user-supplied CSV: {Path(supplied).name}"

    try:
        import yfinance as yf
    except ImportError as exc:
        raise SystemExit(
            "Install requirements-dev.txt or set SHADOW_PRICE_CSV to a licensed "
            "ticker,date,adjClose file. No 2024-current values were invented."
        ) from exc

    end = (date.today() + timedelta(days=1)).isoformat()
    downloaded = yf.download(
        tickers,
        start=START_DOWNLOAD,
        end=end,
        auto_adjust=False,
        progress=False,
        threads=True,
        group_by="column",
    )
    if downloaded.empty:
        raise RuntimeError("The external provider returned no prices")
    field = "Adj Close" if "Adj Close" in downloaded.columns.get_level_values(0) else "Close"
    wide = downloaded[field].copy()
    if isinstance(wide, pd.Series):
        wide = wide.to_frame(tickers[0])
    wide.index.name = "date"
    prices = wide.stack(future_stack=True).rename("adjClose").reset_index()
    prices = prices.rename(columns={prices.columns[1]: "ticker"})
    return prices, "Yahoo Finance via yfinance; research prototype use"


def _returns_wide(prices: pd.DataFrame, tickers: list[str]) -> pd.DataFrame:
    panel = prices[prices["ticker"].isin(tickers)].copy()
    panel = panel.sort_values(["ticker", "date"])
    panel["return"] = panel.groupby("ticker")["adjClose"].pct_change(fill_method=None)
    return panel.pivot(index="date", columns="ticker", values="return").sort_index()


def main() -> None:
    equity, crypto = _fixed_universe()
    all_tickers = equity + crypto
    prices, source = _load_external_prices(all_tickers)
    prices["date"] = pd.to_datetime(prices["date"], errors="coerce")
    prices = prices.dropna(subset=["ticker", "date", "adjClose"])
    prices = prices[prices["date"] >= START_DOWNLOAD]
    coverage = prices.groupby("ticker")["date"].agg(["min", "max", "count"])
    missing = sorted(set(all_tickers) - set(coverage.index))
    if missing:
        raise RuntimeError(f"Provider coverage is incomplete; missing {missing}")

    equity_returns = _returns_wide(prices, equity)
    crypto_returns = _returns_wide(prices, crypto)
    combined_returns = pd.concat(
        [equity_returns, crypto_returns.reindex(equity_returns.index)], axis=1
    )
    universes = {
        "Equity": (equity_returns, 252, 252, 0.20),
        "Crypto": (crypto_returns, 365, 365, 0.30),
        "Combined": (combined_returns, 252, 252, 0.15),
    }
    return_rows: list[pd.DataFrame] = []
    weight_rows: list[pd.DataFrame] = []
    metric_rows: list[dict] = []
    for family, (returns, window, periods, cap) in universes.items():
        for method in METHODS:
            fund = f"{family} {portfolios.METHOD_LABELS[method]}"
            backtest, weights = portfolios.oos_backtest(
                returns,
                method=method,
                estimation_window=window,
                max_weight=cap,
                transaction_cost_bps=10.0,
            )
            backtest = backtest.loc[backtest.index >= START_LIVE]
            weights = weights.loc[weights.index >= START_LIVE]
            if backtest.empty or weights.empty:
                raise RuntimeError(f"Insufficient external history for {fund}")
            decorated = backtest.reset_index()
            decorated.insert(1, "fund", fund)
            decorated.insert(2, "family", family)
            decorated.insert(3, "method", method)
            return_rows.append(decorated)
            long_weights = weights.stack().rename("weight").reset_index()
            long_weights = long_weights.rename(columns={"level_1": "ticker"})
            long_weights.insert(1, "fund", fund)
            long_weights.insert(2, "family", family)
            long_weights.insert(3, "method", method)
            weight_rows.append(long_weights)
            metrics = portfolios.performance_metrics(backtest["net_return"], periods)
            metrics.update(
                {
                    "fund": fund,
                    "family": family,
                    "method": method,
                    "first_live_date": backtest.index.min().date(),
                    "last_live_date": backtest.index.max().date(),
                    "total_turnover": backtest["turnover"].sum(),
                    "transaction_cost_bps": 10.0,
                    "data_source": source,
                    "status": "external price-only shadow; sentiment not extended",
                }
            )
            metric_rows.append(metrics)

    pd.concat(return_rows, ignore_index=True).to_csv(DATA / "shadow_fund_returns.csv", index=False)
    pd.concat(weight_rows, ignore_index=True).to_csv(DATA / "shadow_fund_weights.csv", index=False)
    pd.DataFrame(metric_rows).to_csv(TABLES / "shadow_performance_metrics.csv", index=False)
    coverage.reset_index().assign(data_source=source).to_csv(
        TABLES / "shadow_data_coverage.csv", index=False
    )
    print(f"Shadow evaluation complete through {prices['date'].max().date()} using {source}.")


if __name__ == "__main__":
    main()
