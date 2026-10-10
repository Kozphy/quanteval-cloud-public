"""Model interface.

Every model sees ONLY `history` (rows 0..origin) at prediction time. `prepare(full_frame)` exists
because real pipelines often precompute features on the whole file; the harness's future-invariance
check (see leakage.py) is designed to catch models that leak through that hook.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np
import pandas as pd


class ForecastModel(ABC):
    name: str = "base"
    description: str = ""

    def prepare(self, full_frame: pd.DataFrame) -> None:  # noqa: B027 - optional hook
        """Optional dataset-level preparation. Must not use information after each origin."""

    @abstractmethod
    def predict(self, history: pd.DataFrame, horizon: int, origin: int,
                future_timestamps: pd.DatetimeIndex) -> np.ndarray:
        """Return `horizon` predicted close prices for bars origin+1..origin+horizon."""

    def info(self) -> dict:
        return {"name": self.name, "description": self.description}


def build_models(names: list[str], cfg) -> list[ForecastModel]:
    from .arima import ArimaModel
    from .naive import DriftModel, NaiveModel

    out: list[ForecastModel] = []
    for name in names:
        if name == "naive":
            out.append(NaiveModel())
        elif name == "drift":
            out.append(DriftModel(window=cfg.lookback))
        elif name == "arima":
            out.append(ArimaModel(order=tuple(cfg.arima_order), refit_stride=cfg.arima_refit_stride,
                                  window=None, embargo_bars=cfg.embargo_bars))
        elif name == "kronos_mini":
            from .kronos import KronosMiniModel

            out.append(KronosMiniModel(cfg))
        else:
            raise ValueError(name)
    return out
