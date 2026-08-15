"""Headline sentiment, no-news treatment and equal-ticker sector indices."""

from __future__ import annotations

import numpy as np
import pandas as pd

FINANCE_LEXICON = {
    "beat": 1.5,
    "beats": 1.5,
    "upgrade": 1.8,
    "upgraded": 1.8,
    "outperform": 1.6,
    "surge": 1.7,
    "surges": 1.7,
    "record": 1.3,
    "miss": -1.5,
    "misses": -1.5,
    "downgrade": -1.8,
    "downgraded": -1.8,
    "underperform": -1.6,
    "plunge": -2.0,
    "plunges": -2.0,
    "bankruptcy": -2.5,
    "fraud": -2.5,
    "layoffs": -1.4,
}


def _analyser(finance_augmented: bool = True):
    import nltk
    from nltk.sentiment import SentimentIntensityAnalyzer

    try:
        analyser = SentimentIntensityAnalyzer()
    except LookupError:
        nltk.download("vader_lexicon", quiet=True)
        analyser = SentimentIntensityAnalyzer()
    if finance_augmented:
        analyser.lexicon.update(FINANCE_LEXICON)
    return analyser


def score_headlines(aligned_headlines: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Score the original headline string with baseline and finance-augmented VADER."""
    frame = aligned_headlines.copy()
    base = _analyser(finance_augmented=False)
    finance = _analyser(finance_augmented=True)
    titles = frame["title"].fillna("").astype(str)
    frame["vader_compound"] = titles.map(lambda text: base.polarity_scores(text)["compound"])
    frame["finance_vader_compound"] = titles.map(
        lambda text: finance.polarity_scores(text)["compound"]
    )
    frame["publisher_observed"] = frame["publisher"].fillna("").str.strip().ne("").astype(int)
    frame["url_observed"] = frame["url"].fillna("").str.strip().ne("").astype(int)

    ticker_day = (
        frame.groupby(["aligned_date", "ticker", "sector"], as_index=False)
        .agg(
            sentiment=("finance_vader_compound", "mean"),
            baseline_sentiment=("vader_compound", "mean"),
            article_count=("title", "size"),
            publisher_completeness=("publisher_observed", "mean"),
            url_completeness=("url_observed", "mean"),
            unique_publishers=(
                "publisher",
                lambda x: x.dropna().astype(str).str.strip().replace("", np.nan).nunique(),
            ),
        )
        .rename(columns={"aligned_date": "date"})
    )
    coverage_strength = np.minimum(1.0, np.log1p(ticker_day["article_count"]) / np.log(6.0))
    ticker_day["reliability"] = coverage_strength * (
        0.5 + 0.5 * ticker_day["publisher_completeness"]
    )
    ticker_day["observed_news"] = 1
    return frame, ticker_day


def complete_ticker_day_panel(
    ticker_day: pd.DataFrame,
    equity_calendar: pd.DatetimeIndex,
    ticker_sector: pd.DataFrame,
) -> pd.DataFrame:
    """Neutral-fill no-news ticker-days and lag the usable signal by one trading day."""
    universe = ticker_sector[["ticker", "sector"]].drop_duplicates()
    grid = (
        pd.MultiIndex.from_product(
            [
                pd.DatetimeIndex(equity_calendar).sort_values().unique(),
                sorted(universe["ticker"].unique()),
            ],
            names=["date", "ticker"],
        )
        .to_frame(index=False)
        .merge(universe, on="ticker", how="left")
    )
    panel = grid.merge(ticker_day, on=["date", "ticker", "sector"], how="left")
    panel["observed_news"] = panel["observed_news"].fillna(0).astype(int)
    for col in [
        "sentiment",
        "baseline_sentiment",
        "article_count",
        "publisher_completeness",
        "url_completeness",
        "unique_publishers",
        "reliability",
    ]:
        panel[col] = panel[col].fillna(0.0)
    panel = panel.sort_values(["ticker", "date"]).reset_index(drop=True)
    panel["usable_sentiment_lag1"] = panel.groupby("ticker")["sentiment"].shift(1)
    panel["usable_reliability_lag1"] = panel.groupby("ticker")["reliability"].shift(1)
    return panel


def sector_sentiment_index(complete_panel: pd.DataFrame) -> pd.DataFrame:
    """Equal-weight tickers; expose neutral-fill and observed-only sensitivity."""
    rows = []
    for (date, sector), group in complete_panel.groupby(["date", "sector"], sort=True):
        observed = group.loc[group["observed_news"] == 1, "sentiment"]
        rows.append(
            {
                "date": date,
                "sector": sector,
                "sentiment": group["sentiment"].mean(),
                "observed_only_sentiment": observed.mean() if len(observed) else np.nan,
                "coverage_rate": group["observed_news"].mean(),
                "article_count": group["article_count"].sum(),
                "ticker_count": group["ticker"].nunique(),
            }
        )
    out = pd.DataFrame(rows).sort_values(["sector", "date"]).reset_index(drop=True)
    out["usable_sentiment_lag1"] = out.groupby("sector")["sentiment"].shift(1)
    return out


def sentiment_validation(
    scored_headlines: pd.DataFrame, sector_index: pd.DataFrame
) -> pd.DataFrame:
    base_zero = scored_headlines["vader_compound"].eq(0).mean()
    finance_zero = scored_headlines["finance_vader_compound"].eq(0).mean()
    disagreement = (
        np.sign(scored_headlines["vader_compound"])
        .ne(np.sign(scored_headlines["finance_vader_compound"]))
        .mean()
    )
    no_news_sensitivity = (
        (sector_index["sentiment"] - sector_index["observed_only_sentiment"]).abs().mean()
    )
    return pd.DataFrame(
        [
            {
                "diagnostic": "baseline_neutral_share",
                "value": base_zero,
                "interpretation": "Share of headlines scored exactly zero by standard VADER",
            },
            {
                "diagnostic": "finance_augmented_neutral_share",
                "value": finance_zero,
                "interpretation": "Share scored zero after the transparent finance lexicon",
            },
            {
                "diagnostic": "sign_changed_share",
                "value": disagreement,
                "interpretation": "Share whose sign changes after finance augmentation",
            },
            {
                "diagnostic": "mean_no_news_rule_difference",
                "value": no_news_sensitivity,
                "interpretation": "Mean absolute sector-index difference: neutral-fill versus observed-only",
            },
        ]
    )
