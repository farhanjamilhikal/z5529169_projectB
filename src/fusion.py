"""Reliability-gated, look-ahead-safe sentiment fusion."""

from __future__ import annotations

import numpy as np
import pandas as pd


def _capped_normalise(values: pd.Series, cap: float) -> pd.Series:
    w = values.clip(lower=0).astype(float)
    if w.sum() <= 0:
        w[:] = 1.0 / len(w)
    else:
        w /= w.sum()
    for _ in range(20):
        over = w > cap
        if not over.any():
            break
        excess = float((w[over] - cap).sum())
        w.loc[over] = cap
        under = ~over
        room = (cap - w[under]).clip(lower=0)
        if room.sum() <= 0:
            break
        w.loc[under] += excess * room / room.sum()
    return w / w.sum()


def apply_sentiment(
    base_weights: pd.DataFrame,
    ticker_sentiment: pd.DataFrame,
    tilt_strength: float = 0.35,
    max_weight: float = 0.20,
) -> pd.DataFrame:
    """Tilt only at monthly rebalances using the already lagged ticker-day signal."""
    output = []
    signal_panel = ticker_sentiment.copy()
    signal_panel["date"] = pd.to_datetime(signal_panel["date"])
    for date, base in base_weights.sort_index().iterrows():
        today = signal_panel.loc[signal_panel["date"] == pd.Timestamp(date)].set_index("ticker")
        signal = today["usable_sentiment_lag1"].reindex(base.index).fillna(0.0)
        confidence = today["usable_reliability_lag1"].reindex(base.index).fillna(0.0)
        std = signal.std(ddof=0)
        z = ((signal - signal.mean()) / std).clip(-2.0, 2.0) if std > 0 else signal * 0.0
        # A small floor permits the information signal to affect assets assigned zero
        # by a corner solution, while the cap preserves diversification.
        anchored = base.clip(lower=0) + 0.001
        multiplier = np.exp(tilt_strength * z * confidence)
        tilted = _capped_normalise(anchored * multiplier, max_weight)
        tilted.name = date
        output.append(tilted)
    result = pd.DataFrame(output)
    result.index.name = "date"
    return result
