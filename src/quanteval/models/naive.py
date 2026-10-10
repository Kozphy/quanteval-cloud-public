"""Naive baselines. Adapted from Kozphy/ai-quant-strategy-dashboard `forecasting.py`
(naive registry; (c) 2026 Zixsa, used by the copyright holder), extended to multi-step."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .base import ForecastModel


class NaiveModel(ForecastModel):
    name = "naive"
    description = "Random walk: every future close equals the last observed close."

    def predict(self, history, horizon, origin, future_timestamps):
        return np.full(horizon, float(history["close"].iloc[-1]))


class DriftModel(ForecastModel):
    name = "drift"
    description = "Random walk with drift: mean log-return over the lookback window, extrapolated."

    def __init__(self, window: int):
        self.window = window

    def predict(self, history, horizon, origin, future_timestamps):
        close = history["close"].to_numpy(dtype=float)[-(self.window + 1):]
        mu = float(np.mean(np.diff(np.log(close)))) if len(close) > 1 else 0.0
        return close[-1] * np.exp(mu * np.arange(1, horizon + 1))
