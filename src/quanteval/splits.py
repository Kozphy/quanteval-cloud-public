"""Chronological walk-forward folds with explicit leakage assertions.

Leakage guard ideas adapted from Kozphy/ForexTraderWithBloombergAccess-public
`src/forex_quant/backtest.py` (`assert_train_oos_separation`; MIT, (c) 2026 Zixsa).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .errors import LeakageError, QuotaError


@dataclass(frozen=True)
class Fold:
    origin: int          # index of the last bar observable at decision time
    fit_end: int         # last index allowed for parameter estimation (origin - embargo)
    target_start: int    # first evaluated bar (origin + 1)
    target_end: int      # last evaluated bar (origin + horizon), inclusive

    @property
    def target_index(self) -> np.ndarray:
        return np.arange(self.target_start, self.target_end + 1)


def make_folds(n_rows: int, horizon: int, min_history: int, step: int, max_origins: int,
               embargo_bars: int = 0) -> list[Fold]:
    """Expanding-window origins. The last `max_origins` eligible origins are used (most recent data)."""
    first = max(min_history - 1, embargo_bars)
    last = n_rows - 1 - horizon
    if last < first:
        raise QuotaError(
            f"Not enough rows for evaluation: need at least {min_history + horizon} rows, have {n_rows}")
    # Anchor on the most recent origin and walk backwards so the latest data is always evaluated.
    origins = list(range(last, first - 1, -step))[:max_origins]
    origins.reverse()
    folds = [Fold(origin=o, fit_end=o - embargo_bars, target_start=o + 1, target_end=o + horizon) for o in origins]
    assert_folds_valid(folds, horizon, embargo_bars, n_rows)
    return folds


def assert_folds_valid(folds: list[Fold], horizon: int, embargo_bars: int, n_rows: int) -> None:
    prev_end = -1
    for f in folds:
        if f.fit_end > f.origin:
            raise LeakageError(f"fit window end {f.fit_end} after origin {f.origin}")
        if f.target_start <= f.fit_end + embargo_bars:
            raise LeakageError(
                f"evaluation target {f.target_start} <= fit_end {f.fit_end} + embargo {embargo_bars}")
        if f.target_start <= f.origin:
            raise LeakageError(f"target {f.target_start} not strictly after origin {f.origin}")
        if f.target_end - f.target_start + 1 != horizon:
            raise LeakageError("target window length != horizon")
        if f.target_end >= n_rows:
            raise LeakageError("target beyond end of data")
        if f.target_start <= prev_end:
            raise LeakageError("overlapping evaluation windows (step < horizon)")
        prev_end = f.target_end
