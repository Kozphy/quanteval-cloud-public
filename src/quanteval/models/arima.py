"""ARIMA baseline on log close (statsmodels, BSD-3).

Adapted from Kozphy/ai-quant-strategy-dashboard `forecasting.py` (ARIMA registry; (c) 2026 Zixsa),
extended to multi-step horizons, an embargo on parameter estimation and a refit stride.
Parameters are estimated on data up to `origin - embargo`; the state is then conditioned on data up to
`origin` (no data after the origin is ever used).
"""

from __future__ import annotations

import warnings

import numpy as np
from statsmodels.tsa.arima.model import ARIMA

from .base import ForecastModel


class ArimaModel(ForecastModel):
    name = "arima"

    def __init__(self, order=(1, 1, 1), refit_stride: int = 1, window: int | None = None, embargo_bars: int = 0):
        self.order = tuple(order)
        self.refit_stride = max(1, int(refit_stride))
        self.window = window
        self.embargo_bars = embargo_bars
        self._params = None
        self._calls = 0
        self.description = f"ARIMA{self.order} on log close, refit every {self.refit_stride} origin(s)"
        self.fit_failures = 0

    def prepare(self, full_frame):
        self._params = None
        self._calls = 0
        self.fit_failures = 0

    def predict(self, history, horizon, origin, future_timestamps):
        y = np.log(history["close"].to_numpy(dtype=float))
        if self.window:
            y = y[-self.window:]
        fit_y = y[: len(y) - self.embargo_bars] if self.embargo_bars else y
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                if self._params is None or self._calls % self.refit_stride == 0:
                    res = ARIMA(fit_y, order=self.order).fit()
                    self._params = res.params
                    if len(fit_y) != len(y):
                        res = res.apply(y)
                else:
                    res = ARIMA(y, order=self.order).filter(self._params)
                fc = np.asarray(res.forecast(horizon), dtype=float)
            except Exception:  # noqa: BLE001 - fall back to naive, but count it
                self.fit_failures += 1
                fc = np.full(horizon, y[-1])
        self._calls += 1
        return np.exp(fc)

    def info(self):
        d = super().info()
        d.update({"order": list(self.order), "refit_stride": self.refit_stride, "fit_failures": self.fit_failures})
        return d
