"""Reproduce all Part B models, evidence and app artifacts.

Run from the project root:
    python scripts/run_part_b.py
"""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import matplotlib.pyplot as plt
import pandas as pd

from src import etl, features, fusion, portfolios, sentiment

DATA = ROOT / "results" / "data"
TABLES = ROOT / "results" / "tables"
FIGURES = ROOT / "results" / "figures"
for folder in (DATA, TABLES, FIGURES):
    folder.mkdir(parents=True, exist_ok=True)

COLOURS = {
    "ivory": "#F7F3EA",
    "charcoal": "#242424",
    "oxblood": "#6F1D2C",
    "blue": "#547A92",
    "green": "#35735B",
    "brick": "#B54A42",
    "ochre": "#C7973E",
    "grey": "#8A8A86",
}


def _style():
    plt.rcParams.update(
        {
            "figure.facecolor": COLOURS["ivory"],
            "axes.facecolor": COLOURS["ivory"],
            "axes.edgecolor": COLOURS["grey"],
            "axes.labelcolor": COLOURS["charcoal"],
            "text.color": COLOURS["charcoal"],
            "xtick.color": COLOURS["charcoal"],
            "ytick.color": COLOURS["charcoal"],
            "font.family": "DejaVu Sans",
            "axes.titleweight": "bold",
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


def _fund_name(family: str, method: str) -> str:
    return f"{family} {portfolios.METHOD_LABELS[method]}"


def _long_weights(weights: pd.DataFrame, fund: str, family: str, method: str) -> pd.DataFrame:
    out = weights.stack().rename("weight").reset_index().rename(columns={"level_1": "ticker"})
    out.insert(1, "fund", fund)
    out.insert(2, "family", family)
    out.insert(3, "method", method)
    return out


def _decorate_returns(backtest: pd.DataFrame, fund: str, family: str, method: str) -> pd.DataFrame:
    out = backtest.reset_index()
    out.insert(1, "fund", fund)
    out.insert(2, "family", family)
    out.insert(3, "method", method)
    return out


def _plot_growth(fund_returns: pd.DataFrame):
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.8), sharey=False)
    for ax, family in zip(axes, ["Equity", "Crypto", "Combined"], strict=False):
        subset = fund_returns.loc[fund_returns["family"] == family]
        for fund, group in subset.groupby("fund"):
            ax.plot(
                group["date"], group["growth_of_1"], lw=1.7, label=fund.replace(family + " ", "")
            )
        ax.axhline(1, color=COLOURS["grey"], lw=0.8)
        ax.set_title(family)
        ax.set_xlabel("Live out-of-sample date")
        ax.set_ylabel("Growth of $1")
        ax.legend(frameon=False, fontsize=8)
    fig.suptitle(
        "Out-of-sample growth of $1 after 10 bps transaction costs\nFirst live date follows the initial estimation window; 2020-2023 sample",
        y=1.04,
    )
    fig.tight_layout()
    fig.savefig(FIGURES / "growth_of_one_comparison.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def _plot_drawdowns(fund_returns: pd.DataFrame):
    chosen = fund_returns[fund_returns["method"] == "min_variance"]
    fig, ax = plt.subplots(figsize=(11.5, 5.2))
    for fund, group in chosen.groupby("fund"):
        ax.plot(group["date"], group["drawdown"] * 100, label=fund, lw=1.6)
    ax.axhline(0, color=COLOURS["grey"], lw=0.8)
    ax.set(
        title="Minimum-variance fund drawdowns, live out-of-sample period",
        xlabel="Date",
        ylabel="Drawdown (%)",
    )
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES / "fund_drawdowns.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def _plot_weights(fund_weights: pd.DataFrame):
    subset = fund_weights[
        (fund_weights["family"] == "Combined")
        & (fund_weights["method"].isin(portfolios.METHOD_LABELS))
    ]
    methods = ["equal_weight", "min_variance", "risk_parity"]
    fig, axes = plt.subplots(3, 1, figsize=(12, 11), sharex=True)
    for ax, method in zip(axes, methods, strict=False):
        wide = (
            subset.loc[subset["method"] == method]
            .pivot(index="date", columns="ticker", values="weight")
            .fillna(0)
        )
        leaders = wide.mean().nlargest(8).index
        plotted = wide[leaders].copy()
        plotted["Other"] = wide.drop(columns=leaders).sum(axis=1)
        ax.stackplot(plotted.index, plotted.T, labels=plotted.columns, alpha=0.9)
        ax.set_ylabel("Weight")
        ax.set_title(portfolios.METHOD_LABELS[method])
        ax.legend(ncol=5, fontsize=7, frameon=False, loc="upper left")
    axes[-1].set_xlabel("Rebalance date")
    fig.suptitle(
        "Combined-fund target weights over time\nTop eight average holdings plus Other; monthly walk-forward rebalancing",
        y=0.995,
    )
    fig.tight_layout()
    fig.savefig(FIGURES / "combined_weights_over_time.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def _plot_risk_return(metrics: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10.5, 6))
    colour = {"Equity": COLOURS["blue"], "Crypto": COLOURS["brick"], "Combined": COLOURS["green"]}
    label_settings = {
        "Combined Minimum Variance": ("Combined Min Var", (8, 28), "left"),
        "Equity Minimum Variance": ("Equity Min Var", (8, -30), "left"),
        "Equity Reliability-Gated Sentiment": ("Sentiment Tilt", (8, -7), "left"),
        "Equity Equal Weight": ("Equity Equal Weight", (8, -20), "left"),
        "Equity Risk Parity": ("Equity Risk Parity", (8, -17), "left"),
        "Combined Risk Parity": ("Combined Risk Parity", (8, 28), "left"),
        "Combined Equal Weight": ("Combined Equal Weight", (8, 2), "left"),
    }
    for family, group in metrics.groupby("family"):
        ax.scatter(
            group["annualised_volatility"] * 100,
            group["annualised_return"] * 100,
            s=55 + group["sharpe_ratio"].clip(lower=0).fillna(0) * 50,
            color=colour.get(family, COLOURS["ochre"]),
            label=family,
            alpha=0.85,
        )
        for _, row in group.iterrows():
            default_label = row["fund"].replace(family + " ", "")
            label, offset, horizontal_alignment = label_settings.get(
                row["fund"], (default_label, (4, 4), "left")
            )
            ax.annotate(
                label,
                (row["annualised_volatility"] * 100, row["annualised_return"] * 100),
                xytext=offset,
                textcoords="offset points",
                fontsize=7,
                ha=horizontal_alignment,
            )
    ax.set(
        title="Out-of-sample fund risk and return after transaction costs",
        xlabel="Annualised volatility (%)",
        ylabel="Annualised geometric return (%)",
    )
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES / "risk_return_across_funds.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def _plot_sentiment(index: pd.DataFrame):
    sectors = sorted(index["sector"].unique())
    fig, axes = plt.subplots(5, 2, figsize=(13, 13), sharex=True, sharey=True)
    for ax, sector in zip(axes.flat, sectors, strict=False):
        g = index[index["sector"] == sector]
        smooth = g.set_index("date")["sentiment"].rolling(21, min_periods=5).mean()
        ax.plot(smooth.index, smooth, color=COLOURS["oxblood"], lw=1.3)
        ax.axhline(0, color=COLOURS["grey"], lw=0.7)
        ax.set_title(sector, fontsize=10)
        ax.set_ylabel("21-day mean")
    for ax in axes[-1]:
        ax.set_xlabel("Date")
    fig.suptitle(
        "Finance-augmented VADER sector sentiment\nEqual-weight tickers; no-news ticker-days neutral; 2020-2023",
        y=0.997,
    )
    fig.tight_layout()
    fig.savefig(FIGURES / "sector_sentiment_index.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def _plot_fusion(fund_returns: pd.DataFrame):
    names = ["Equity Minimum Variance", "Equity Reliability-Gated Sentiment"]
    subset = fund_returns[fund_returns["fund"].isin(names)]
    fig, axes = plt.subplots(2, 1, figsize=(11.5, 7.5), sharex=True)
    for fund, g in subset.groupby("fund"):
        axes[0].plot(g["date"], g["growth_of_1"], label=fund, lw=1.8)
        axes[1].plot(g["date"], g["drawdown"] * 100, label=fund, lw=1.5)
    axes[0].set(
        ylabel="Growth of $1", title="Before versus after reliability-gated sentiment fusion"
    )
    axes[1].set(xlabel="Live out-of-sample date", ylabel="Drawdown (%)")
    for ax in axes:
        ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES / "fusion_before_after.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def _plot_crypto_floor_sensitivity(table: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    ax.plot(
        table["crypto_floor_pct"],
        table["sharpe_ratio"],
        color=COLOURS["green"],
        marker="o",
        lw=2,
        label="Sharpe ratio",
    )
    ax.set(
        title="Combined minimum-variance sensitivity to a crypto-sleeve floor",
        xlabel="Minimum total crypto weight (%)",
        ylabel="Out-of-sample Sharpe ratio",
    )
    ax2 = ax.twinx()
    ax2.plot(
        table["crypto_floor_pct"],
        table["maximum_drawdown"] * 100,
        color=COLOURS["brick"],
        marker="s",
        lw=1.8,
        label="Maximum drawdown",
    )
    ax2.set_ylabel("Maximum drawdown (%)", color=COLOURS["brick"])
    lines = ax.get_lines() + ax2.get_lines()
    ax.legend(lines, [line.get_label() for line in lines], frameon=False, loc="best")
    fig.text(
        0.5,
        0.01,
        "Monthly walk-forward; 252-day window; 10 bps one-way turnover costs; 2021-2023 live period",
        ha="center",
        fontsize=8,
    )
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(FIGURES / "crypto_sleeve_floor_sensitivity.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def main():
    _style()
    print("Loading and cleaning all supplied datasets...")
    equities, eq_audit = etl.load_clean_equities()
    crypto, cr_audit = etl.load_clean_crypto()
    news, news_audit = etl.load_clean_news()
    pd.concat([eq_audit, cr_audit, news_audit], ignore_index=True).to_csv(
        TABLES / "carried_forward_integrity_audit.csv", index=False
    )
    features.asset_data_use_register().to_csv(TABLES / "asset_data_use_register.csv", index=False)
    features.asset_liquidity_diagnostics(equities, crypto).to_csv(
        TABLES / "asset_liquidity_diagnostics.csv", index=False
    )

    eq_long = features.daily_returns(equities)
    cr_long = features.daily_returns(crypto)
    eq_wide = features.returns_wide(eq_long)
    cr_wide = features.returns_wide(cr_long)
    combined_wide = pd.concat([eq_wide, cr_wide.reindex(eq_wide.index)], axis=1)

    universes = {
        "Equity": (eq_wide, 252, 252, 0.20),
        "Crypto": (cr_wide, 365, 365, 0.30),
        "Combined": (combined_wide, 252, 252, 0.15),
    }
    methods = ["equal_weight", "min_variance", "risk_parity"]
    return_outputs, weight_outputs, metric_rows = [], [], []
    base_weight_lookup = {}
    for family, (wide, window, periods, cap) in universes.items():
        for method in methods:
            fund = _fund_name(family, method)
            print("Backtesting", fund)
            backtest, weights = portfolios.oos_backtest(
                wide,
                method=method,
                estimation_window=window,
                max_weight=cap,
                transaction_cost_bps=10.0,
            )
            base_weight_lookup[(family, method)] = weights
            return_outputs.append(_decorate_returns(backtest, fund, family, method))
            weight_outputs.append(_long_weights(weights, fund, family, method))
            metrics = portfolios.performance_metrics(backtest["net_return"], periods)
            metrics.update(
                {
                    "fund": fund,
                    "family": family,
                    "method": method,
                    "periods_per_year": periods,
                    "estimation_window": window,
                    "first_live_date": backtest.index.min().date(),
                    "last_live_date": backtest.index.max().date(),
                    "transaction_cost_bps": 10.0,
                    "total_turnover": backtest["turnover"].sum(),
                }
            )
            metric_rows.append(metrics)

    print("Testing minimum crypto-sleeve floors without changing the offered fund menu...")
    crypto_assets = set(cr_wide.columns)
    crypto_floor_rows = []
    for floor in (0.0, 0.10, 0.20, 0.30):
        floor_backtest, floor_weights = portfolios.oos_backtest(
            combined_wide,
            method="min_variance",
            estimation_window=252,
            max_weight=0.15,
            transaction_cost_bps=10.0,
            minimum_group=crypto_assets,
            minimum_group_weight=floor,
        )
        floor_metrics = portfolios.performance_metrics(floor_backtest["net_return"], 252)
        crypto_weight = floor_weights[list(sorted(crypto_assets))].sum(axis=1)
        crypto_floor_rows.append(
            {
                "crypto_floor_pct": floor * 100,
                "annualised_return": floor_metrics["annualised_return"],
                "annualised_volatility": floor_metrics["annualised_volatility"],
                "sharpe_ratio": floor_metrics["sharpe_ratio"],
                "maximum_drawdown": floor_metrics["maximum_drawdown"],
                "ending_value": floor_metrics["ending_value"],
                "total_turnover": floor_backtest["turnover"].sum(),
                "mean_realised_crypto_weight": crypto_weight.mean(),
                "latest_crypto_weight": crypto_weight.iloc[-1],
                "status": "research sensitivity; not an offered fund",
            }
        )
    crypto_floor_table = pd.DataFrame(crypto_floor_rows)
    crypto_floor_table.to_csv(TABLES / "crypto_sleeve_floor_sensitivity.csv", index=False)

    print("Scoring and validating headlines...")
    aligned_news = features.align_headlines_to_trading_days(news, equities["date"])
    sector_lexicon = sentiment.load_sector_lexicon()
    scored, ticker_day = sentiment.score_headlines(aligned_news, sector_lexicon=sector_lexicon)
    ticker_sector = equities[["ticker", "sector"]].drop_duplicates()
    complete_sentiment = sentiment.complete_ticker_day_panel(
        ticker_day, eq_wide.index, ticker_sector
    )
    sector_index = sentiment.sector_sentiment_index(complete_sentiment)
    validation = sentiment.sentiment_validation(scored, sector_index)

    print("Building reliability-gated sentiment extension...")
    base_weights = base_weight_lookup[("Equity", "min_variance")]
    tilted_weights = fusion.apply_sentiment(
        base_weights, complete_sentiment, tilt_strength=0.35, max_weight=0.20
    )
    tilted_backtest = portfolios.returns_from_rebalance_weights(eq_wide, tilted_weights, 10.0)
    tilted_fund = "Equity Reliability-Gated Sentiment"
    return_outputs.append(
        _decorate_returns(tilted_backtest, tilted_fund, "Equity", "sentiment_tilt")
    )
    weight_outputs.append(_long_weights(tilted_weights, tilted_fund, "Equity", "sentiment_tilt"))
    tilted_metrics = portfolios.performance_metrics(tilted_backtest["net_return"], 252)
    tilted_metrics.update(
        {
            "fund": tilted_fund,
            "family": "Equity",
            "method": "sentiment_tilt",
            "periods_per_year": 252,
            "estimation_window": 252,
            "first_live_date": tilted_backtest.index.min().date(),
            "last_live_date": tilted_backtest.index.max().date(),
            "transaction_cost_bps": 10.0,
            "total_turnover": tilted_backtest["turnover"].sum(),
        }
    )
    metric_rows.append(tilted_metrics)

    fund_returns = pd.concat(return_outputs, ignore_index=True)
    fund_weights = pd.concat(weight_outputs, ignore_index=True)
    metrics = pd.DataFrame(metric_rows)[
        [
            "fund",
            "family",
            "method",
            "first_live_date",
            "last_live_date",
            "observations",
            "annualised_return",
            "annualised_volatility",
            "sharpe_ratio",
            "maximum_drawdown",
            "ending_value",
            "total_turnover",
            "transaction_cost_bps",
            "periods_per_year",
            "estimation_window",
        ]
    ].sort_values(["family", "method"])

    fund_returns.to_csv(DATA / "fund_returns.csv", index=False)
    fund_weights.to_csv(DATA / "fund_weights.csv", index=False)
    sector_index.to_csv(DATA / "sector_sentiment_index.csv", index=False)
    complete_sentiment[
        [
            "date",
            "ticker",
            "sector",
            "sentiment",
            "sector_augmented_sentiment",
            "observed_news",
            "article_count",
            "reliability",
            "usable_sentiment_lag1",
            "usable_reliability_lag1",
        ]
    ].to_csv(DATA / "ticker_sentiment_signals.csv", index=False)
    metrics.to_csv(TABLES / "performance_metrics.csv", index=False)
    validation.to_csv(TABLES / "sentiment_validation.csv", index=False)
    pd.DataFrame(
        [
            {
                "term": k,
                "assigned_score": v,
                "status": "transparent student-defined finance extension",
            }
            for k, v in sentiment.FINANCE_LEXICON.items()
        ]
    ).to_csv(TABLES / "finance_lexicon_extension.csv", index=False)
    sector_lexicon.to_csv(TABLES / "sector_sentiment_lexicon.csv", index=False)

    current = (
        fund_weights.sort_values("date")
        .groupby(["fund", "ticker"], as_index=False)
        .tail(1)
        .sort_values(["fund", "weight"], ascending=[True, False])
    )
    current.to_csv(TABLES / "current_holdings.csv", index=False)
    fusion_metrics = metrics[metrics["fund"].isin(["Equity Minimum Variance", tilted_fund])].copy()
    fusion_metrics.to_csv(TABLES / "fusion_comparison.csv", index=False)
    pd.DataFrame(
        [
            {
                "parameter": "Risk-free rate",
                "value": "0%",
                "reason": "Permitted course assumption; used consistently for Sharpe ratios",
            },
            {
                "parameter": "Rebalancing",
                "value": "First observed day of each month",
                "reason": "Monthly implementation with past-only estimation",
            },
            {
                "parameter": "Estimation window",
                "value": "252 equity/combined; 365 crypto observations",
                "reason": "One native-calendar year",
            },
            {
                "parameter": "Constraints",
                "value": "Long-only; 20% equity, 30% crypto, 15% combined cap",
                "reason": "Limits concentration while remaining feasible",
            },
            {
                "parameter": "Transaction costs",
                "value": "10 bps per unit of one-way turnover",
                "reason": "Tests implementation drag beyond the zero-cost baseline",
            },
            {
                "parameter": "No-news rule",
                "value": "Neutral zero; observed-only sensitivity also reported",
                "reason": "Separates absent coverage from measured tone",
            },
            {
                "parameter": "Sentiment timing",
                "value": "One equity trading-day lag",
                "reason": "Prevents same-day headline look-ahead",
            },
        ]
    ).to_csv(TABLES / "model_specification.csv", index=False)

    _plot_growth(fund_returns)
    _plot_drawdowns(fund_returns)
    _plot_weights(fund_weights)
    _plot_risk_return(metrics)
    _plot_sentiment(sector_index)
    _plot_fusion(fund_returns)
    _plot_crypto_floor_sensitivity(crypto_floor_table)
    print(
        f"Complete: {len(metrics)} funds, {len(scored):,} scored headlines, {len(sector_index):,} sector-date index rows"
    )


if __name__ == "__main__":
    main()
