"""Kronos-mini zero-shot adapter (CPU).

Model code: vendored from https://github.com/shiyu-coder/Kronos @ 67b630e (MIT, (c) 2025 ShiYu).
Weights: downloaded from Hugging Face at pinned revisions (MIT per model cards); not redistributed.
Future timestamps passed to Kronos are generated from the inferred bar calendar, NOT read from the
data file, so the model never sees future rows (not even their timestamps).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .base import ForecastModel


class KronosMiniModel(ForecastModel):
    name = "kronos_mini"

    def __init__(self, cfg):
        import torch

        from .._vendor.kronos import Kronos, KronosPredictor, KronosTokenizer

        k = cfg.kronos
        self.cfg = cfg
        self.k = k
        self.seed = int(cfg.seed)
        torch.set_num_threads(int(k.threads))
        self.tokenizer = KronosTokenizer.from_pretrained(k.tokenizer_id, revision=k.tokenizer_revision)
        self.model = Kronos.from_pretrained(k.model_id, revision=k.model_revision)
        self.tokenizer.eval()
        self.model.eval()
        self.predictor = KronosPredictor(self.model, self.tokenizer, device="cpu", max_context=int(cfg.lookback))
        self.n_params = int(sum(p.numel() for p in self.model.parameters()))
        self.n_tokenizer_params = int(sum(p.numel() for p in self.tokenizer.parameters()))
        self.description = (f"Kronos-mini zero-shot ({self.n_params:,} params), context {cfg.lookback}, "
                            f"mean of {k.sample_count} samples, T={k.temperature}, top_p={k.top_p}, CPU")

    def predict(self, history, horizon, origin, future_timestamps):
        import torch

        hist = history.iloc[-self.cfg.lookback:]
        cols = ["open", "high", "low", "close"] + [c for c in ("volume", "amount") if c in hist.columns]
        x = hist[cols].reset_index(drop=True).astype(float)
        if "volume" in x.columns:
            x["volume"] = x["volume"].fillna(0.0)
        x_ts = hist["timestamp"].dt.tz_convert("UTC").dt.tz_localize(None).reset_index(drop=True)
        y_ts = pd.Series(pd.DatetimeIndex(future_timestamps).tz_convert("UTC").tz_localize(None))
        # Per-origin seed => results independent of evaluation order and reproducible.
        torch.manual_seed(self.seed + int(origin))
        np.random.seed((self.seed + int(origin)) % (2**32))
        out = self.predictor.predict(df=x, x_timestamp=x_ts, y_timestamp=y_ts, pred_len=horizon,
                                     T=self.k.temperature, top_p=self.k.top_p,
                                     sample_count=self.k.sample_count, verbose=False)
        return out["close"].to_numpy(dtype=float)

    def info(self):
        d = super().info()
        d.update({
            "model_id": self.k.model_id, "model_revision": self.k.model_revision,
            "tokenizer_id": self.k.tokenizer_id, "tokenizer_revision": self.k.tokenizer_revision,
            "params": self.n_params, "tokenizer_params": self.n_tokenizer_params,
            "sample_count": self.k.sample_count, "temperature": self.k.temperature, "top_p": self.k.top_p,
            "threads": self.k.threads, "max_context": self.cfg.lookback,
            "code": "vendored shiyu-coder/Kronos@67b630e (MIT)",
        })
        return d
