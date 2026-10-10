"""Matplotlib charts (PNG). Returns {name: path}."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

COLORS = {"naive": "#7f7f7f", "drift": "#2ca02c", "arima": "#1f77b4", "kronos_mini": "#d62728"}


def _save(fig, path: Path) -> str:
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)
    return str(path)


def make_charts(result: dict, out: Path) -> dict[str, str]:
    out.mkdir(parents=True, exist_ok=True)
    a = result["_arrays"]
    names = list(a["preds"].keys())
    h = a["actual"].shape[1]
    origins = a["origins"]
    ts = a["ts"]
    close = a["close"]
    charts: dict[str, str] = {}

    # 1. Out-of-sample forecast paths per model
    lo, hi = int(origins[0]), int(origins[-1] + h)
    fig, axes = plt.subplots(len(names), 1, figsize=(10, 2.4 * len(names)), sharex=True)
    axes = np.atleast_1d(axes)
    for ax, n in zip(axes, names):
        ax.plot(ts.iloc[lo:hi + 1], close[lo:hi + 1], color="black", lw=1.0, label="actual close")
        for i, o in enumerate(origins):
            xs = ts.iloc[o:o + h + 1]
            ys = np.concatenate([[close[o]], a["preds"][n][i]])
            ax.plot(xs, ys, color=COLORS.get(n, "C3"), lw=0.9, alpha=0.8)
        ax.set_title(f"{n}: out-of-sample {h}-bar forecast paths vs actual", fontsize=9)
        ax.tick_params(labelsize=7)
    axes[0].legend(fontsize=7, loc="upper left")
    charts["oos_forecasts"] = _save(fig, out / "oos_forecasts.png")

    # 2. Rolling horizon-end absolute % error
    fig, ax = plt.subplots(figsize=(10, 3))
    win = max(5, min(20, len(origins) // 5))
    for n in names:
        e = np.abs(a["preds"][n][:, -1] / a["actual"][:, -1] - 1) * 100
        ax.plot(a["origin_ts"], pd.Series(e).rolling(win, min_periods=1).mean(), label=n, color=COLORS.get(n))
    ax.set_ylabel(f"abs error % at bar {h}\n(rolling {win} origins)", fontsize=8)
    ax.legend(fontsize=7)
    ax.tick_params(labelsize=7)
    charts["rolling_error"] = _save(fig, out / "rolling_error.png")

    # 3. Error distribution (horizon-end return error, %)
    fig, ax = plt.subplots(figsize=(10, 3))
    for n in names:
        e = (a["preds"][n][:, -1] - a["actual"][:, -1]) / a["last_obs"] * 100
        ax.hist(e, bins=30, histtype="step", lw=1.2, label=n, color=COLORS.get(n))
    ax.set_xlabel(f"forecast minus actual at bar {h}, % of last observed close", fontsize=8)
    ax.legend(fontsize=7)
    ax.tick_params(labelsize=7)
    charts["error_distribution"] = _save(fig, out / "error_distribution.png")

    # 4. Rolling directional hit rate
    fig, ax = plt.subplots(figsize=(10, 3))
    plotted = False
    for n in names:
        p = np.sign(a["preds"][n][:, -1] / a["last_obs"] - 1)
        act = np.sign(a["actual"][:, -1] / a["last_obs"] - 1)
        if np.all(p == 0):
            continue
        hit = pd.Series(np.where((p != 0) & (act != 0), (p == act).astype(float), np.nan))
        ax.plot(a["origin_ts"], hit.rolling(win, min_periods=3).mean(), label=n, color=COLORS.get(n))
        plotted = True
    ax.axhline(0.5, color="black", lw=0.8, ls="--")
    ax.set_ylim(0, 1)
    ax.set_ylabel(f"directional accuracy\n(rolling {win})", fontsize=8)
    if plotted:
        ax.legend(fontsize=7)
    ax.tick_params(labelsize=7)
    charts["directional"] = _save(fig, out / "directional.png")

    # 5. Latency
    fig, ax = plt.subplots(figsize=(10, 2.8))
    data = [np.asarray(a["lat"][n]) * 1000 for n in names]
    ax.boxplot(data, orientation="horizontal", showfliers=True)
    ax.set_yticks(range(1, len(names) + 1), names, fontsize=8)
    ax.set_xscale("log")
    ax.set_xlabel("wall-clock ms per forecast (CPU, log scale)", fontsize=8)
    ax.tick_params(labelsize=7)
    charts["latency"] = _save(fig, out / "latency.png")

    # 6/7. Research backtest charts (valid models only)
    bt = result["backtest"]["per_model"]
    valid = [n for n in names if bt.get(n, {}).get("valid")]
    if valid:
        fig, ax = plt.subplots(figsize=(10, 3))
        for n in valid:
            x = pd.to_datetime(bt[n]["entry_ts"])
            ax.plot(x, bt[n]["base"]["equity_gross"], ls="--", lw=0.9, color=COLORS.get(n), label=f"{n} gross")
            ax.plot(x, bt[n]["base"]["equity_net"], lw=1.2, color=COLORS.get(n), label=f"{n} net")
        ax.axhline(1.0, color="black", lw=0.6)
        ax.set_ylabel("growth of 1.0 (research sim.)", fontsize=8)
        ax.legend(fontsize=7, ncol=2)
        ax.tick_params(labelsize=7)
        charts["research_equity"] = _save(fig, out / "research_equity.png")

        fig, ax = plt.subplots(figsize=(10, 2.8))
        levels = [s["cost_bps_per_side"] for s in bt[valid[0]]["sensitivity"]]
        width = 0.8 / len(valid)
        for j, n in enumerate(valid):
            vals = [s["total_return_net"] * 100 for s in bt[n]["sensitivity"]]
            ax.bar(np.arange(len(levels)) + j * width, vals, width, label=n, color=COLORS.get(n))
        ax.set_xticks(np.arange(len(levels)) + width * (len(valid) - 1) / 2, [f"{lv:g} bps" for lv in levels])
        ax.axhline(0, color="black", lw=0.6)
        ax.set_ylabel("net total return %", fontsize=8)
        ax.legend(fontsize=7)
        ax.tick_params(labelsize=7)
        charts["cost_sensitivity"] = _save(fig, out / "cost_sensitivity.png")
    return charts
