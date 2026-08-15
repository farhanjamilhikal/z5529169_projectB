"""Validate VADER across general review language and optional labelled finance text."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src import sentiment

OUTPUT = ROOT / "results" / "tables" / "dual_domain_sentiment_validation.csv"
LABELS = ("negative", "neutral", "positive")


def polarity_label(compound: float) -> str:
    """Apply VADER's conventional compound-score decision bands."""
    if compound >= 0.05:
        return "positive"
    if compound <= -0.05:
        return "negative"
    return "neutral"


def rating_label(rating: float, maximum: float) -> str:
    """Map ratings to sentiment using predeclared, scale-normalised bands."""
    share = rating / maximum
    if share <= 0.40:
        return "negative"
    if share >= 0.70:
        return "positive"
    return "neutral"


def classification_metrics(actual: list[str], predicted: list[str]) -> dict[str, float]:
    """Return accuracy and macro-F1 without adding a runtime ML dependency."""
    accuracy = sum(a == p for a, p in zip(actual, predicted, strict=True)) / len(actual)
    f1_scores = []
    for label in sorted(set(actual)):
        true_positive = sum(
            a == label and p == label for a, p in zip(actual, predicted, strict=True)
        )
        false_positive = sum(
            a != label and p == label for a, p in zip(actual, predicted, strict=True)
        )
        false_negative = sum(
            a == label and p != label for a, p in zip(actual, predicted, strict=True)
        )
        precision = (
            true_positive / (true_positive + false_positive)
            if true_positive + false_positive
            else 0
        )
        recall = (
            true_positive / (true_positive + false_negative)
            if true_positive + false_negative
            else 0
        )
        f1_scores.append(2 * precision * recall / (precision + recall) if precision + recall else 0)
    return {"accuracy": accuracy, "macro_f1": sum(f1_scores) / len(f1_scores)}


def evaluate_texts(texts: list[str], labels: list[str], domain: str) -> list[dict[str, object]]:
    """Compare standard and finance-augmented VADER on fixed labelled texts."""
    rows = []
    for model, augmented in (("Standard VADER", False), ("Finance-augmented VADER", True)):
        analyser = sentiment._analyser(finance_augmented=augmented)
        predicted = [polarity_label(analyser.polarity_scores(text)["compound"]) for text in texts]
        metrics = classification_metrics(labels, predicted)
        rows.append(
            {
                "domain": domain,
                "model": model,
                "observations": len(labels),
                "accuracy": metrics["accuracy"],
                "macro_f1": metrics["macro_f1"],
                "neutral_prediction_share": predicted.count("neutral") / len(predicted),
                "status": "MEASURED",
                "limitation": "Aggregate benchmark; inspect label and subgroup confusion before use",
            }
        )
    return rows


def nltk_movie_review_rows() -> list[dict[str, object]]:
    """Use NLTK's binary movie-review corpus as a coarse general-domain stress test."""
    try:
        from nltk.corpus import movie_reviews

        file_ids = movie_reviews.fileids()
        texts = [movie_reviews.raw(file_id) for file_id in file_ids]
        labels = [
            "positive" if movie_reviews.categories(file_id)[0] == "pos" else "negative"
            for file_id in file_ids
        ]
    except LookupError:
        return [
            {
                "domain": "Movie reviews (NLTK binary)",
                "model": "Not run",
                "observations": 0,
                "accuracy": pd.NA,
                "macro_f1": pd.NA,
                "neutral_prediction_share": pd.NA,
                "status": "MISSING CORPUS",
                "limitation": "Run nltk.download('movie_reviews'); corpus has no star or platform metadata",
            }
        ]
    rows = evaluate_texts(texts, labels, "Movie reviews (NLTK binary)")
    for row in rows:
        row["limitation"] = (
            "Binary positive/negative labels only; no star rating, platform, franchise, cast or preference metadata"
        )
    return rows


def labelled_csv_rows(path: str, domain: str) -> list[dict[str, object]]:
    """Evaluate a user-supplied labelled CSV without redistributing its text."""
    frame = pd.read_csv(path)
    if "label" in frame:
        labels = frame["label"].astype(str).str.lower().tolist()
    elif {"rating", "rating_max"}.issubset(frame.columns):
        labels = [
            rating_label(rating, maximum)
            for rating, maximum in zip(frame["rating"], frame["rating_max"], strict=True)
        ]
    else:
        raise ValueError(f"{path} needs label or rating and rating_max columns")
    unknown = sorted(set(labels) - set(LABELS))
    if unknown:
        raise ValueError(f"Unknown labels in {path}: {unknown}")
    return evaluate_texts(frame["text"].fillna("").astype(str).tolist(), labels, domain)


def main() -> None:
    rows = nltk_movie_review_rows()
    movie_csv = os.getenv("MOVIE_VALIDATION_CSV")
    finance_csv = os.getenv("FINANCE_VALIDATION_CSV")
    if movie_csv:
        rows.extend(labelled_csv_rows(movie_csv, "Movie reviews (star-labelled)"))
    else:
        rows.append(
            {
                "domain": "Movie reviews (star-labelled)",
                "model": "Not run",
                "observations": 0,
                "accuracy": pd.NA,
                "macro_f1": pd.NA,
                "neutral_prediction_share": pd.NA,
                "status": "AWAITING LEGITIMATE DATA",
                "limitation": "Set MOVIE_VALIDATION_CSV; preferences are subgroup tags, not labels",
            }
        )
    if finance_csv:
        rows.extend(labelled_csv_rows(finance_csv, "Finance (expert-labelled)"))
    else:
        rows.append(
            {
                "domain": "Finance (expert-labelled)",
                "model": "Not run",
                "observations": 0,
                "accuracy": pd.NA,
                "macro_f1": pd.NA,
                "neutral_prediction_share": pd.NA,
                "status": "REQUIRED BEFORE COMMERCIAL USE",
                "limitation": "Set FINANCE_VALIDATION_CSV to a licensed benchmark or student-labelled holdout",
            }
        )
    pd.DataFrame(rows).to_csv(OUTPUT, index=False)
    print(OUTPUT)


if __name__ == "__main__":
    main()
