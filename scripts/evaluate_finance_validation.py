import re
from pathlib import Path

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    cohen_kappa_score,
    confusion_matrix,
    precision_recall_fscore_support,
)
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "results" / "tables" / "finance_validation_labels.csv"
SECTOR_LEXICON_PATH = ROOT / "research_extension" / "sector_sentiment_lexicon.csv"
OUT_METRICS = ROOT / "results" / "tables" / "finance_validation_metrics.csv"
OUT_CONFUSION = ROOT / "results" / "tables" / "finance_confusion_matrix.csv"
OUT_ERRORS = ROOT / "results" / "tables" / "finance_error_audit.csv"

LABELS = ["Positive", "Neutral", "Negative"]

FINANCE_LEXICON = {
    "beat": 1.5,
    "upgrade": 1.3,
    "outperform": 1.2,
    "surge": 1.4,
    "strong": 0.8,
    "miss": -1.5,
    "downgrade": -1.3,
    "underperform": -1.2,
    "plunge": -1.6,
    "fraud": -2.5,
    "bankruptcy": -2.7,
    "lawsuit": -1.4,
    "fine": -1.3,
    "penalty": -1.2,
    "guidance cut": -1.6,
    "guidance raise": 1.6,
    "profit warning": -1.8,
    "margin expansion": 1.2,
}


def classify(compound: float) -> str:
    if compound >= 0.05:
        return "Positive"
    if compound <= -0.05:
        return "Negative"
    return "Neutral"


def build_analyser(augmented: bool) -> SentimentIntensityAnalyzer:
    analyser = SentimentIntensityAnalyzer()
    if augmented:
        analyser.lexicon.update(FINANCE_LEXICON)
    return analyser


def score_labels(df: pd.DataFrame, augmented: bool) -> pd.Series:
    analyser = build_analyser(augmented)
    preds = []
    for text in df["headline_text"].fillna(""):
        compound = analyser.polarity_scores(str(text))["compound"]
        preds.append(classify(compound))
    return pd.Series(preds, index=df.index)


def build_sector_matchers(sector_lexicon: pd.DataFrame) -> dict[str, tuple]:
    """One finance-augmented analyser per sector, with that sector's scored
    phrases folded in as placeholder tokens (VADER only scores single words,
    so multi-word phrases need substitution before scoring)."""
    matchers: dict[str, tuple] = {}
    for sector, group in sector_lexicon.groupby("sector"):
        scored = group[group["score"] != 0]
        if scored.empty:
            continue
        phrase_to_token: dict[str, str] = {}
        placeholder_lexicon: dict[str, float] = {}
        for _, row in scored.iterrows():
            phrase = str(row["phrase"]).strip().lower()
            if not phrase or phrase in phrase_to_token:
                continue
            token = "sectorterm_" + re.sub(r"[^a-z0-9]+", "_", phrase).strip("_")
            phrase_to_token[phrase] = token
            placeholder_lexicon[token] = float(row["score"])
        ordered_phrases = sorted(phrase_to_token, key=len, reverse=True)
        pattern = re.compile("|".join(re.escape(p) for p in ordered_phrases), re.IGNORECASE)
        analyser = build_analyser(augmented=True)
        analyser.lexicon.update(placeholder_lexicon)
        matchers[sector] = (pattern, phrase_to_token, analyser)
    return matchers


def score_sector_augmented(df: pd.DataFrame, matchers: dict[str, tuple]) -> pd.Series:
    preds = pd.Series(index=df.index, dtype=object)
    for sector, (pattern, phrase_to_token, analyser) in matchers.items():
        mask = df["sector"] == sector
        if not mask.any():
            continue
        texts = df.loc[mask, "headline_text"].fillna("").astype(str)
        replaced = texts.str.replace(
            pattern, lambda m: f" {phrase_to_token[m.group(0).lower()]} ", regex=True
        )
        preds.loc[mask] = replaced.map(lambda t: classify(analyser.polarity_scores(t)["compound"]))
    unmatched = preds.isna()
    if unmatched.any():
        fallback = build_analyser(augmented=True)
        preds.loc[unmatched] = (
            df.loc[unmatched, "headline_text"]
            .fillna("")
            .astype(str)
            .map(lambda t: classify(fallback.polarity_scores(t)["compound"]))
        )
    return preds


def metric_rows(y_true: pd.Series, y_pred: pd.Series, model_name: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    accuracy = accuracy_score(y_true, y_pred)
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=LABELS, zero_division=0
    )
    rows.append(
        {
            "model": model_name,
            "metric": "accuracy",
            "class": "overall",
            "value": accuracy,
            "support": len(y_true),
        }
    )
    rows.append(
        {
            "model": model_name,
            "metric": "macro_f1",
            "class": "overall",
            "value": float(f1.mean()),
            "support": len(y_true),
        }
    )
    for cls, p, r, f, s in zip(LABELS, precision, recall, f1, support, strict=False):
        rows.extend(
            [
                {"model": model_name, "metric": "precision", "class": cls, "value": p, "support": s},
                {"model": model_name, "metric": "recall", "class": cls, "value": r, "support": s},
                {"model": model_name, "metric": "f1", "class": cls, "value": f, "support": s},
            ]
        )
    return rows


def main() -> None:
    df = pd.read_csv(INPUT)

    required = {
        "headline_id",
        "headline_text",
        "reviewer_1_label",
        "reviewer_2_label",
        "final_label",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df = df.dropna(subset=["headline_text", "final_label"]).copy()
    if df.empty:
        raise ValueError("finance_validation_labels.csv has no labelled rows yet.")

    kappa = cohen_kappa_score(df["reviewer_1_label"], df["reviewer_2_label"], labels=LABELS)

    df["pred_standard"] = score_labels(df, augmented=False)
    df["pred_finance_augmented"] = score_labels(df, augmented=True)

    sector_lexicon = pd.read_csv(SECTOR_LEXICON_PATH)
    sector_matchers = build_sector_matchers(sector_lexicon)
    df["pred_sector_augmented"] = score_sector_augmented(df, sector_matchers)

    metric_data = [
        {
            "model": "reviewer_agreement",
            "metric": "cohens_kappa",
            "class": "overall",
            "value": kappa,
            "support": len(df),
        }
    ]
    metric_data += metric_rows(df["final_label"], df["pred_standard"], "standard_vader")
    metric_data += metric_rows(df["final_label"], df["pred_finance_augmented"], "finance_augmented_vader")
    metric_data += metric_rows(df["final_label"], df["pred_sector_augmented"], "sector_augmented_vader")
    pd.DataFrame(metric_data).to_csv(OUT_METRICS, index=False)

    confusion_rows: list[dict[str, object]] = []
    for model_col, model_name in [
        ("pred_standard", "standard_vader"),
        ("pred_finance_augmented", "finance_augmented_vader"),
        ("pred_sector_augmented", "sector_augmented_vader"),
    ]:
        cm = confusion_matrix(df["final_label"], df[model_col], labels=LABELS)
        for i, actual in enumerate(LABELS):
            for j, predicted in enumerate(LABELS):
                confusion_rows.append(
                    {
                        "model": model_name,
                        "actual": actual,
                        "predicted": predicted,
                        "count": int(cm[i, j]),
                    }
                )
    pd.DataFrame(confusion_rows).to_csv(OUT_CONFUSION, index=False)

    errors: list[pd.DataFrame] = []
    for model_col, model_name in [
        ("pred_standard", "standard_vader"),
        ("pred_finance_augmented", "finance_augmented_vader"),
        ("pred_sector_augmented", "sector_augmented_vader"),
    ]:
        wrong = df[df["final_label"] != df[model_col]].copy()
        wrong["model"] = model_name
        wrong["predicted_label"] = wrong[model_col]
        errors.append(
            wrong[
                [
                    "model",
                    "headline_id",
                    "date",
                    "ticker",
                    "sector",
                    "headline_text",
                    "final_label",
                    "predicted_label",
                    "disagreement_flag",
                    "adjudication_note",
                ]
            ]
        )
    pd.concat(errors, ignore_index=True).to_csv(OUT_ERRORS, index=False)

    print(f"Saved: {OUT_METRICS}")
    print(f"Saved: {OUT_CONFUSION}")
    print(f"Saved: {OUT_ERRORS}")


if __name__ == "__main__":
    main()
