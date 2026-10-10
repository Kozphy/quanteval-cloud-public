"""Forecast accuracy metrics and latency summaries.

Latency helpers adapted from Kozphy/ai-quant-strategy-dashboard `latency.py` ((c) 2026 Zixsa).
Bootstrap/CI ideas from Kozphy/EvalForge `finance_eval/metrics.py` (proprietary, (c) Kozphy; owner reuse).
"""

from __future__ import annotations

import math

import numpy as np
from scipy import stats


def wilson_ci(successes: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (centre - half, centre + half)


def directional(actual_end: np.ndarray, pred_end: np.ndarray, last_obs: np.ndarray) -> dict:
    a = np.sign(actual_end / last_obs - 1.0)
    p = np.sign(pred_end / last_obs - 1.0)
    mask = (a != 0) & (p != 0)
    n = int(mask.sum())
    if n == 0:
        return {"n": 0, "hits": 0, "accuracy": None, "ci_low": None, "ci_high": None, "p_value_vs_50pct": None,
                "note": "model forecasts no change, so direction is undefined"}
    hits = int((a[mask] == p[mask]).sum())
    lo, hi = wilson_ci(hits, n)
    pval = float(stats.binomtest(hits, n, 0.5).pvalue)
    return {"n": n, "hits": hits, "accuracy": hits / n, "ci_low": lo, "ci_high": hi, "p_value_vs_50pct": pval}


def diebold_mariano(e_model: np.ndarray, e_base: np.ndarray, h: int = 1) -> dict:
    """DM test on squared horizon-end errors (non-overlapping origins, so lag-0 variance;
    Harvey-Leybourne-Newbold small-sample correction with h=1). Negative stat => model better."""
    d = e_model**2 - e_base**2
    n = len(d)
    if n < 3 or np.allclose(d, 0):
        return {"stat": None, "p_value": None, "n": n}
    dbar = d.mean()
    var = d.var(ddof=0) / n
    if var <= 0:
        return {"stat": None, "p_value": None, "n": n}
    dm = dbar / math.sqrt(var)
    hh = 1  # non-overlapping origins => treat as one-step-ahead loss series
    k = math.sqrt((n + 1 - 2 * hh + hh * (hh - 1) / n) / n)
    stat = dm * k
    p = 2 * (1 - stats.t.cdf(abs(stat), df=n - 1))
    return {"stat": float(stat), "p_value": float(p), "n": n}


def accuracy_metrics(actual: np.ndarray, pred: np.ndarray, last_obs: np.ndarray) -> dict:
    """actual/pred: shape (n_origins, horizon) in price units."""
    err = pred - actual
    end_err = err[:, -1]
    return {
        "mae": float(np.mean(np.abs(err))),
        "rmse": float(np.sqrt(np.mean(err**2))),
        "mape_pct": float(np.mean(np.abs(err) / np.abs(actual)) * 100),
        "mae_end": float(np.mean(np.abs(end_err))),
        "rmse_end": float(np.sqrt(np.mean(end_err**2))),
        "return_mae_end_pct": float(np.mean(np.abs(pred[:, -1] / last_obs - actual[:, -1] / last_obs)) * 100),
        "directional": directional(actual[:, -1], pred[:, -1], last_obs),
    }


def latency_summary(seconds: list[float]) -> dict:
    arr = np.asarray(seconds, dtype=float) * 1000.0
    if arr.size == 0:
        return {"n": 0}
    return {
        "n": int(arr.size),
        "p50_ms": float(np.percentile(arr, 50)),
        "p95_ms": float(np.percentile(arr, 95)),
        "mean_ms": float(arr.mean()),
        "max_ms": float(arr.max()),
        "total_s": float(arr.sum() / 1000.0),
    }
