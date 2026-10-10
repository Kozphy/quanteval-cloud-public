"""Generate the synthetic OHLCV sample used for the public sample report.

Fully synthetic: GARCH(1,1)-style daily volatility, small constant drift, 24 intraday sub-steps per bar
to build open/high/low/close, log-normal volume linked to absolute returns. No real market data.

Usage: python examples/synthetic_ohlcv.py --out examples/synthetic_daily.csv [--rows 800 --seed 7]
"""

from __future__ import annotations

import argparse

import numpy as np
import pandas as pd


def generate(rows: int = 800, seed: int = 7, start: str = "2024-01-01") -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    omega, alpha, beta, mu = 2e-6, 0.08, 0.90, 0.0002
    var = omega / (1 - alpha - beta)
    price = 100.0
    out = []
    eps_prev = 0.0
    for i in range(rows):
        var = omega + alpha * eps_prev**2 + beta * var
        sub = rng.normal(mu / 24, np.sqrt(var / 24), 24)
        path = price * np.exp(np.cumsum(sub))
        o = price
        c = float(path[-1])
        h = float(max(o, path.max()))
        lo = float(min(o, path.min()))
        r = np.log(c / o)
        vol = float(np.exp(rng.normal(10 + 25 * abs(r), 0.3)))
        out.append((o, h, lo, c, vol))
        eps_prev = r - mu
        price = c
    ts = pd.date_range(start, periods=rows, freq="D", tz="UTC")
    df = pd.DataFrame(out, columns=["open", "high", "low", "close", "volume"])
    df.insert(0, "timestamp", ts.strftime("%Y-%m-%dT%H:%M:%SZ"))
    df["symbol"] = "SYNTH-GARCH"
    return df


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--rows", type=int, default=800)
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()
    generate(a.rows, a.seed).to_csv(a.out, index=False, float_format="%.6f")
    print(f"wrote {a.out}")
