"""Leakage checks.

1. Structural: folds must satisfy fit_end < target_start (splits.assert_folds_valid).
2. Future-invariance: a model's forecast at origin t must not change when every bar AFTER t is replaced
   by different values. This catches leakage through dataset-level preprocessing (`prepare`) and any
   accidental access to future rows.
3. Negative control: a deliberately leaky model (uses the realised close h bars ahead) must be flagged;
   if it is not, the detector itself is broken and the run aborts.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .calendar import future_timestamps
from .errors import LeakageError
from .models.base import ForecastModel


class LookaheadModel(ForecastModel):
    """NEGATIVE CONTROL ONLY. Precomputes a 'feature' from future closes on the full file (a classic bug)."""

    name = "negative_control_lookahead"
    description = "Deliberately leaky: precomputes future closes on the whole file."

    def prepare(self, full_frame):
        self._future_close = full_frame["close"].to_numpy(dtype=float)

    def predict(self, history, horizon, origin, future_timestamps):
        return self._future_close[origin + 1: origin + 1 + horizon].copy()


def perturb_future(frame: pd.DataFrame, origin: int, seed: int = 12345) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    out = frame.copy()
    n = len(out) - origin - 1
    if n <= 0:
        return out
    factor = np.exp(np.cumsum(rng.normal(0.0, 0.05, n)))
    for col in ["open", "high", "low", "close"]:
        out.loc[origin + 1:, col] = out.loc[origin + 1:, col].to_numpy() * factor
    if "volume" in out.columns:
        out.loc[origin + 1:, "volume"] = out.loc[origin + 1:, "volume"].to_numpy() * rng.uniform(0.2, 5.0, n)
    return out


@dataclass
class InvarianceResult:
    model: str
    origins_checked: list[int]
    max_abs_diff: float
    passed: bool

    def to_dict(self):
        return self.__dict__.copy()


def _forecast(model: ForecastModel, frame: pd.DataFrame, origin: int, horizon: int, card) -> np.ndarray:
    model.prepare(frame)
    hist = frame.iloc[: origin + 1]
    fts = future_timestamps(hist["timestamp"].iloc[-1], horizon, card.frequency, card.bar_seconds)
    return np.asarray(model.predict(hist, horizon, origin, fts), dtype=float)


def future_invariance_check(model: ForecastModel, frame: pd.DataFrame, origins: list[int], horizon: int,
                            card, tol: float = 0.0) -> InvarianceResult:
    max_diff = 0.0
    for o in origins:
        a = _forecast(model, frame, o, horizon, card)
        b = _forecast(model, perturb_future(frame, o), o, horizon, card)
        max_diff = max(max_diff, float(np.nanmax(np.abs(a - b))))
    model.prepare(frame)  # restore state on the real data
    return InvarianceResult(model.name, list(origins), max_diff, max_diff <= tol)


def run_negative_control(frame: pd.DataFrame, origins: list[int], horizon: int, card) -> InvarianceResult:
    res = future_invariance_check(LookaheadModel(), frame, origins, horizon, card)
    if res.passed:
        raise LeakageError("Leakage detector self-test failed: the deliberately leaky model was not flagged")
    return res
