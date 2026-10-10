"""Transaction-cost-aware RESEARCH backtest of a model-derived direction rule.

This is a historical simulation used to characterise a forecasting model. It is not investment advice
and says nothing about future results.

Adapted from Kozphy/ForexTraderWithBloombergAccess-public `src/forex_quant/backtest.py`
(`realistic_backtest`: execution delay >= 1 bar, turnover-based bps costs) and `metrics.py`
(Sharpe, max drawdown) - MIT, (c) 2026 Zixsa.

Rule per origin t (non-overlapping, step >= horizon):
  exposure = sign(predicted close[t+h] / close[t] - 1)  (long_short)  or  max(sign, 0) (long_flat)
  entered at close[t + delay], exited at close[t + delay + h]; costs = |exposure| * 2 sides * bps.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .errors import LeakageError


@dataclass
class TradeTable:
    origin: np.ndarray
    entry: np.ndarray
    exit: np.ndarray
    exposure: np.ndarray
    gross: np.ndarray


def build_trades(close: np.ndarray, origins: np.ndarray, pred_end: np.ndarray, horizon: int,
                 delay: int, mode: str) -> TradeTable:
    if delay < 1:
        raise LeakageError("delay must be >= 1 bar (same-bar execution is look-ahead)")
    origins = np.asarray(origins)
    entry = origins + delay
    exit_ = entry + horizon
    ok = exit_ <= len(close) - 1
    origins, entry, exit_, pred_end = origins[ok], entry[ok], exit_[ok], np.asarray(pred_end)[ok]
    direction = np.sign(pred_end / close[origins] - 1.0)
    exposure = np.maximum(direction, 0.0) if mode == "long_flat" else direction
    if np.any(entry <= origins):
        raise LeakageError("entry not strictly after decision origin")
    if len(entry) > 1 and np.any(entry[1:] < exit_[:-1]):
        raise LeakageError("overlapping holding periods")
    gross = exposure * (close[exit_] / close[entry] - 1.0)
    return TradeTable(origins, entry, exit_, exposure, gross)


def summarise(tt: TradeTable, cost_bps: float, periods_per_year: float, horizon: int) -> dict:
    cost = np.abs(tt.exposure) * 2.0 * cost_bps / 10_000.0
    net = tt.gross - cost
    active = tt.exposure != 0
    n_active = int(active.sum())
    eq = np.cumprod(1.0 + net)
    peak = np.maximum.accumulate(np.concatenate([[1.0], eq]))[1:]
    dd = float(np.min(eq / peak - 1.0)) if len(eq) else 0.0
    per_year = periods_per_year / horizon
    sd = float(np.std(net, ddof=1)) if len(net) > 1 else 0.0
    sharpe = float(np.mean(net) / sd * np.sqrt(per_year)) if sd > 0 else None
    return {
        "cost_bps_per_side": cost_bps,
        "periods": int(len(net)),
        "active_periods": n_active,
        "exposure_share": float(n_active / len(net)) if len(net) else 0.0,
        "total_return_gross": float(np.prod(1.0 + tt.gross) - 1.0),
        "total_return_net": float(eq[-1] - 1.0) if len(eq) else 0.0,
        "annualised_sharpe_net": sharpe,
        "max_drawdown_net": dd,
        "hit_rate_net": float((net[active] > 0).mean()) if n_active else None,
        "total_cost": float(cost.sum()),
        "equity_net": eq.tolist(),
        "equity_gross": np.cumprod(1.0 + tt.gross).tolist(),
    }


def passive_reference(close: np.ndarray, tt: TradeTable, cost_bps: float) -> dict:
    """Hold long from the first entry to the last exit (one round trip of costs). Reference only."""
    if len(tt.entry) == 0:
        return {}
    gross = close[tt.exit[-1]] / close[tt.entry[0]] - 1.0
    return {"total_return_gross": float(gross),
            "total_return_net": float((1 + gross) * (1 - 2 * cost_bps / 10_000.0) - 1.0)}


def validity(n_active_trades: int, min_trades: int, hard_errors: bool, leakage_ok: bool) -> list[str]:
    reasons = []
    if n_active_trades < min_trades:
        reasons.append(f"only {n_active_trades} non-overlapping active periods (< {min_trades} required)")
    if hard_errors:
        reasons.append("hard data-quality failures")
    if not leakage_ok:
        reasons.append("a leakage check failed")
    return reasons
