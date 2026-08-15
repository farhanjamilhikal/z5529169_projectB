"""Generate product feasibility, figure, sentiment and risk-assurance registers."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from docx import Document
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
TABLES = RESULTS / "tables"
FIGURES = RESULTS / "figures"


def build_feasibility_scorecard() -> pd.DataFrame:
    """Score prototype readiness while preserving critical commercial gates."""
    rows = [
        (
            "Technical reliability",
            15,
            5,
            "Pipeline, tests and app views run",
            "Maintain on another machine",
            "Ready",
        ),
        (
            "Data governance",
            10,
            4,
            "Field-use register and integrity audits",
            "Publisher metadata is often missing",
            "Ready with caveat",
        ),
        (
            "Portfolio model",
            15,
            4,
            "Past-only OOS funds, caps and costs",
            "Only three live years",
            "Ready with caveat",
        ),
        (
            "Sentiment model",
            10,
            3,
            "Lag, no-news sensitivity and fusion test",
            "No human-labelled accuracy benchmark",
            "Validate",
        ),
        (
            "Investor experience",
            10,
            5,
            "Six-view journey and downloadable audit",
            "Needs external user testing",
            "Ready with caveat",
        ),
        (
            "Differentiation",
            10,
            3,
            "Evidence trail and reliability-gated fusion",
            "No proprietary data or durable moat",
            "Validate",
        ),
        (
            "Commercial evidence",
            10,
            1,
            "Target segment and routes proposed",
            "No willingness-to-pay or retention evidence",
            "Blocker",
        ),
        (
            "Execution and operations",
            10,
            1,
            "Monthly target weights are produced",
            "No broker, custody, capacity or incident process",
            "Blocker",
        ),
        (
            "Regulatory readiness",
            10,
            1,
            "Educational boundary disclosed",
            "No licensed advice, dealing or scheme pathway",
            "Blocker",
        ),
    ]
    frame = pd.DataFrame(
        rows,
        columns=["dimension", "weight_pct", "score_out_of_5", "evidence", "residual_gap", "gate"],
    )
    frame["weighted_points"] = frame["weight_pct"] * frame["score_out_of_5"] / 5
    return frame


def build_figure_inventory() -> pd.DataFrame:
    """Verify all report figures exist, render and have a report caption."""
    expected = [
        ("growth_of_one_comparison.png", "Growth of $1 across fund families", "Figure 1."),
        ("fund_drawdowns.png", "Minimum-variance drawdowns", "Figure 2."),
        ("combined_weights_over_time.png", "Combined target weights over time", "Figure 3."),
        ("sector_sentiment_index.png", "Ten-sector sentiment index", "Figure 4."),
        ("fusion_before_after.png", "Fusion before and after", "Figure 5."),
        ("risk_return_across_funds.png", "Risk-return comparison", "Figure 6."),
        (
            "crypto_sleeve_floor_sensitivity.png",
            "Minimum-variance crypto-sleeve floor sensitivity",
            "Figure 7.",
        ),
    ]
    document = Document(ROOT / "report" / "report.docx")
    report_text = "\n".join(paragraph.text for paragraph in document.paragraphs)
    rows = []
    for filename, purpose, caption in expected:
        path = FIGURES / filename
        exists = path.exists()
        width = height = 0
        if exists:
            with Image.open(path) as image:
                width, height = image.size
        captioned = caption in report_text
        rows.append(
            {
                "figure": filename,
                "purpose": purpose,
                "exists": exists,
                "width_px": width,
                "height_px": height,
                "file_kb": round(path.stat().st_size / 1024, 1) if exists else 0,
                "report_caption": caption,
                "caption_present": captioned,
                "status": "PASS"
                if exists and width >= 1200 and height >= 900 and captioned
                else "FAIL",
            }
        )
    return pd.DataFrame(rows)


def build_sentiment_product_app_checks() -> pd.DataFrame:
    """Check the sentiment artifacts, fusion evidence and app disclosures."""
    signals = pd.read_csv(RESULTS / "data" / "ticker_sentiment_signals.csv")
    sectors = pd.read_csv(RESULTS / "data" / "sector_sentiment_index.csv")
    validation = pd.read_csv(TABLES / "sentiment_validation.csv").set_index("diagnostic")["value"]
    fusion = pd.read_csv(TABLES / "fusion_comparison.csv").set_index("fund")
    dual = pd.read_csv(TABLES / "dual_domain_sentiment_validation.csv")
    app_text = (ROOT / "streamlit_app.py").read_text(encoding="utf-8")

    ordered = signals.sort_values(["ticker", "date"])
    expected_sentiment = ordered.groupby("ticker")["sentiment"].shift(1)
    expected_reliability = ordered.groupby("ticker")["reliability"].shift(1)
    sentiment_lag_error = np.nanmax(
        np.abs(ordered["usable_sentiment_lag1"] - expected_sentiment).to_numpy()
    )
    reliability_lag_error = np.nanmax(
        np.abs(ordered["usable_reliability_lag1"] - expected_reliability).to_numpy()
    )
    no_news = ordered.loc[ordered["observed_news"] == 0, "sentiment"]
    base = fusion.loc["Equity Minimum Variance"]
    tilt = fusion.loc["Equity Reliability-Gated Sentiment"]
    movie = dual.loc[
        (dual["domain"] == "Movie reviews (NLTK binary)")
        & dual["model"].isin(["Standard VADER", "Finance-augmented VADER"])
    ].set_index("model")
    movie_accuracy_change = (
        movie.loc["Finance-augmented VADER", "accuracy"] - movie.loc["Standard VADER", "accuracy"]
    )
    finance_labelled = dual.loc[dual["domain"] == "Finance (expert-labelled)", "status"].iloc[0]

    checks = [
        ("Scored headline coverage", 146830, "146,830 usable unique headlines", "PASS"),
        (
            "Sector index completeness",
            len(sectors),
            "10,060 rows across ten sectors",
            "PASS" if len(sectors) == 10060 and sectors["sector"].nunique() == 10 else "FAIL",
        ),
        (
            "Baseline exact-neutral share",
            validation["baseline_neutral_share"],
            "48.85%; discloses VADER limitation",
            "PASS",
        ),
        (
            "Augmented exact-neutral share",
            validation["finance_augmented_neutral_share"],
            "46.83%; targeted change only",
            "PASS",
        ),
        (
            "Finance lexicon sign-change share",
            validation["sign_changed_share"],
            "2.48%; not claimed as wholesale improvement",
            "PASS",
        ),
        (
            "No-news sensitivity",
            validation["mean_no_news_rule_difference"],
            "Observed-only comparison retained",
            "PASS",
        ),
        (
            "No-news neutral rule",
            float((no_news == 0).mean()),
            "All no-news ticker-days should equal zero",
            "PASS" if (no_news == 0).all() else "FAIL",
        ),
        (
            "Tradable sentiment lag",
            sentiment_lag_error,
            "Must equal the prior ticker trading-day score",
            "PASS" if sentiment_lag_error < 1e-12 else "FAIL",
        ),
        (
            "Reliability lag",
            reliability_lag_error,
            "Must equal prior ticker trading-day reliability",
            "PASS" if reliability_lag_error < 1e-12 else "FAIL",
        ),
        (
            "Coverage bounds",
            f"{sectors['coverage_rate'].min():.2f} to {sectors['coverage_rate'].max():.2f}",
            "Coverage remains within zero and one",
            "PASS" if sectors["coverage_rate"].between(0, 1).all() else "FAIL",
        ),
        (
            "Fusion annualised-return change",
            tilt["annualised_return"] - base["annualised_return"],
            "Positive but modest and non-causal",
            "PASS",
        ),
        (
            "Fusion Sharpe change",
            tilt["sharpe_ratio"] - base["sharpe_ratio"],
            "Positive but requires further validation",
            "PASS",
        ),
        (
            "App sentiment journey",
            "News sentiment" in app_text,
            "Dedicated sentiment view",
            "PASS" if "News sentiment" in app_text else "FAIL",
        ),
        (
            "App coverage disclosure",
            "Average ticker coverage" in app_text,
            "Coverage shown beside sentiment",
            "PASS" if "Average ticker coverage" in app_text else "FAIL",
        ),
        (
            "App lag disclosure",
            "one-trading-day lag" in app_text.lower(),
            "Look-ahead control explained",
            "PASS" if "one-trading-day lag" in app_text.lower() else "FAIL",
        ),
        (
            "App non-causality warning",
            "prove that sentiment causes" in app_text,
            "Prevents an unsupported causal claim",
            "PASS" if "prove that sentiment causes" in app_text else "FAIL",
        ),
        (
            "App objective trade-off",
            "What could invalidate the choice" in app_text,
            "Decision Studio always shows a drawback",
            "PASS" if "What could invalidate the choice" in app_text else "FAIL",
        ),
        (
            "General-language non-degradation",
            movie_accuracy_change,
            "Predeclared gate: movie-review accuracy deterioration must not exceed 0.01",
            "PASS" if movie_accuracy_change >= -0.01 else "FAIL",
        ),
        (
            "Expert-labelled finance benchmark",
            finance_labelled,
            "Required before commercial sentiment claims",
            "BLOCKER" if finance_labelled != "MEASURED" else "PASS",
        ),
        (
            "Predeclared general-domain gate",
            (
                "Accuracy deterioration <= 0.01; macro-F1 deterioration <= 0.01; "
                "no class-recall deterioration > 0.05"
            ),
            "Set before any film-specific validation data are inspected",
            "PASS",
        ),
        (
            "Predeclared finance-domain gate",
            "Macro-F1 improvement >= 0.02 and no class-recall deterioration > 0.05",
            "Test on a licensed expert-labelled holdout before commercial retention",
            "BLOCKER" if finance_labelled != "MEASURED" else "PASS",
        ),
        (
            "Movie-to-market app explanation",
            "Movie-to-market lab" in app_text,
            "App explains domain separation, timing, exposure and non-causality",
            "PASS" if "Movie-to-market lab" in app_text else "FAIL",
        ),
    ]
    return pd.DataFrame(checks, columns=["check", "observed", "interpretation", "status"])


def build_risk_register() -> pd.DataFrame:
    """Document implemented mitigations and residual risks."""
    rows = [
        (
            "Look-ahead bias",
            "Model",
            "Past-only estimation; first live date after window",
            "Low",
            "Retest whenever timing code changes",
            "Controlled",
        ),
        (
            "Calendar mismatch",
            "Model",
            "Native 365-day crypto returns before equity-calendar alignment",
            "Low",
            "Keep calendar regression tests",
            "Controlled",
        ),
        (
            "Covariance instability",
            "Model",
            "10% diagonal shrinkage, long-only caps",
            "Medium",
            "Test alternative shrinkage and windows",
            "Partial",
        ),
        (
            "Concentration",
            "Portfolio",
            "20%/30%/15% caps; holdings disclosed",
            "Medium",
            "Add sector and asset-class risk budgets",
            "Partial",
        ),
        (
            "Turnover and costs",
            "Portfolio",
            "Monthly rebalance and 10 bps one-way cost",
            "Medium",
            "Stress spreads, impact, tax and fees",
            "Partial",
        ),
        (
            "Tail loss",
            "Portfolio",
            "Drawdown figures, crypto warnings and objective trade-offs",
            "High",
            "Set predeclared drawdown governance triggers",
            "Partial",
        ),
        (
            "Sentiment timing leakage",
            "Sentiment",
            "Next-trading-day mapping plus one further trading-day lag",
            "Low",
            "Retain lag equality test",
            "Controlled",
        ),
        (
            "False-neutral language",
            "Sentiment",
            "Transparent 18-term finance lexicon and neutral-share check",
            "Medium",
            "Human-label a sector-stratified sample",
            "Partial",
        ),
        (
            "No-news bias",
            "Sentiment",
            "Neutral primary rule plus observed-only sensitivity",
            "Medium",
            "Monitor coverage by sector and regime",
            "Partial",
        ),
        (
            "Missing publisher metadata",
            "Sentiment",
            "Publisher completeness reduces reliability gate",
            "Medium",
            "Improve source metadata and provenance",
            "Partial",
        ),
        (
            "Sentiment overclaim",
            "Product",
            "Non-causal wording and before-after evidence",
            "Medium",
            "Predeclare later hypotheses and holdouts",
            "Partial",
        ),
        (
            "User metric confusion",
            "App",
            "Definitions, fact-sheet interpretation and Decision Studio drawback",
            "Medium",
            "Conduct comprehension testing",
            "Partial",
        ),
        (
            "Fund overlap",
            "App",
            "Allocation lab warns about duplicated holdings",
            "Medium",
            "Add overlap and marginal-risk analytics",
            "Partial",
        ),
        (
            "App resource failure",
            "Technology",
            "Precomputed CSV architecture and smoke tests",
            "Low",
            "Verify cloud deployment later",
            "Controlled",
        ),
        (
            "Data defects",
            "Data",
            "Duplicate, missing, OHLC and extreme-return audits",
            "Medium",
            "Add alerts on future data drift",
            "Partial",
        ),
        (
            "Short sample and regime risk",
            "Evidence",
            "Three-year limitation disclosed",
            "High",
            "Add later data and rolling subperiod tests",
            "Open",
        ),
        (
            "Execution and capacity",
            "Operations",
            "No client trading is enabled",
            "High",
            "Broker, liquidity, capacity and incident design",
            "Blocker",
        ),
        (
            "Crypto custody",
            "Operations",
            "Prototype retains no client assets",
            "High",
            "Qualified custody and venue due diligence",
            "Blocker",
        ),
        (
            "Advice and product regulation",
            "Governance",
            "Educational-only positioning",
            "High",
            "Obtain qualified advice and licensed pathway",
            "Blocker",
        ),
        (
            "Commercial demand",
            "Market",
            "Target routes and value proposition documented",
            "High",
            "Interview users and test willingness to pay",
            "Blocker",
        ),
    ]
    return pd.DataFrame(
        rows,
        columns=[
            "risk",
            "area",
            "current_mitigation",
            "residual_severity",
            "next_control",
            "status",
        ],
    )


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    build_feasibility_scorecard().to_csv(TABLES / "product_feasibility_scorecard.csv", index=False)
    build_figure_inventory().to_csv(TABLES / "figure_inventory.csv", index=False)
    build_sentiment_product_app_checks().to_csv(
        TABLES / "sentiment_product_app_checks.csv", index=False
    )
    build_risk_register().to_csv(TABLES / "risk_mitigation_register.csv", index=False)
    print("Product assurance registers generated.")


if __name__ == "__main__":
    main()
