"""Run configuration and quotas."""

from __future__ import annotations

import dataclasses
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .errors import QuotaError

# Pinned upstream artefacts (see docs/legal-and-licensing-checklist.md)
KRONOS_MINI_ID = "NeoQuasar/Kronos-mini"
KRONOS_MINI_REVISION = "f4e68697d9d5aed55cef5c96aabc3376bcad9f81"
KRONOS_TOKENIZER_ID = "NeoQuasar/Kronos-Tokenizer-2k"
KRONOS_TOKENIZER_REVISION = "26966d0035065a0cae0ebad7af8ece35bc1fb51c"
KRONOS_CODE_COMMIT = "67b630e"
# Stated by the Kronos authors: training cut-off Feb 2024 inclusive (GitHub issue #204);
# arXiv v1 public release 2025-08-02.
KRONOS_TRAINING_CUTOFF = "2024-02-29"
KRONOS_PUBLIC_RELEASE = "2025-08-02"


@dataclass
class Limits:
    max_rows: int = 200_000
    max_file_mb: float = 50.0
    max_lookback: int = 2048  # Kronos-mini context length
    max_horizon: int = 60
    max_origins: int = 500
    timeout_s: float = 1800.0


@dataclass
class KronosConfig:
    enabled: bool = True
    model_id: str = KRONOS_MINI_ID
    model_revision: str = KRONOS_MINI_REVISION
    tokenizer_id: str = KRONOS_TOKENIZER_ID
    tokenizer_revision: str = KRONOS_TOKENIZER_REVISION
    sample_count: int = 5
    temperature: float = 1.0
    top_p: float = 0.9
    threads: int = 4


@dataclass
class BacktestConfig:
    enabled: bool = True
    mode: str = "long_short"  # or "long_flat"
    cost_bps_per_side: float = 5.0
    cost_sensitivity_bps: list[float] = field(default_factory=lambda: [0.0, 5.0, 10.0, 25.0])
    delay_bars: int = 1
    min_trades: int = 30
    periods_per_year: float | None = None  # inferred from data if None


@dataclass
class RunConfig:
    horizon: int = 5
    lookback: int = 256
    min_history: int = 128
    max_origins: int = 150
    step: int | None = None  # defaults to horizon (non-overlapping evaluation windows)
    embargo_bars: int = 0
    seed: int = 42
    models: list[str] = field(default_factory=lambda: ["naive", "drift", "arima", "kronos_mini"])
    arima_order: list[int] = field(default_factory=lambda: [1, 1, 1])
    arima_refit_stride: int = 1
    leakage_check_origins: int = 3
    model_training_cutoff: str = KRONOS_TRAINING_CUTOFF
    model_public_release: str = KRONOS_PUBLIC_RELEASE
    title: str | None = None
    data_provenance: str | None = None
    synthetic_data: bool = False
    kronos: KronosConfig = field(default_factory=KronosConfig)
    backtest: BacktestConfig = field(default_factory=BacktestConfig)
    limits: Limits = field(default_factory=Limits)

    @property
    def effective_step(self) -> int:
        return self.step or self.horizon

    def to_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)

    def validate(self) -> None:
        lim = self.limits
        if not 1 <= self.horizon <= lim.max_horizon:
            raise QuotaError(f"horizon={self.horizon} outside allowed range 1..{lim.max_horizon}")
        if not 16 <= self.lookback <= lim.max_lookback:
            raise QuotaError(f"lookback={self.lookback} outside allowed range 16..{lim.max_lookback}")
        if self.min_history < 16:
            raise QuotaError("min_history must be >= 16")
        if not 1 <= self.max_origins <= lim.max_origins:
            raise QuotaError(f"max_origins={self.max_origins} outside allowed range 1..{lim.max_origins}")
        if self.step is not None and self.step < self.horizon:
            raise QuotaError("step must be >= horizon (overlapping evaluation windows are not allowed)")
        if self.embargo_bars < 0:
            raise QuotaError("embargo_bars must be >= 0")
        if self.backtest.delay_bars < 1:
            raise QuotaError("backtest.delay_bars must be >= 1 (same-bar execution is look-ahead)")
        if self.backtest.mode not in {"long_short", "long_flat"}:
            raise QuotaError("backtest.mode must be long_short or long_flat")
        unknown = set(self.models) - {"naive", "drift", "arima", "kronos_mini"}
        if unknown:
            raise QuotaError(f"unknown models: {sorted(unknown)}")


def _merge(dc_obj: Any, data: dict[str, Any]) -> Any:
    for key, value in data.items():
        if not hasattr(dc_obj, key):
            raise ValueError(f"Unknown config key: {key}")
        current = getattr(dc_obj, key)
        if dataclasses.is_dataclass(current) and isinstance(value, dict):
            _merge(current, value)
        else:
            setattr(dc_obj, key, value)
    return dc_obj


def load_config(path: str | Path | None = None, overrides: dict[str, Any] | None = None) -> RunConfig:
    cfg = RunConfig()
    if path:
        text = Path(path).read_text(encoding="utf-8")
        data = json.loads(text) if str(path).endswith(".json") else yaml.safe_load(text)
        _merge(cfg, data or {})
    if overrides:
        _merge(cfg, {k: v for k, v in overrides.items() if v is not None})
    cfg.validate()
    return cfg


def config_from_dict(data: dict[str, Any]) -> RunConfig:
    cfg = _merge(RunConfig(), data)
    cfg.validate()
    return cfg
