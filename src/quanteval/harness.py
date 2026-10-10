"""End-to-end evaluation run: validate -> walk-forward -> metrics -> research backtest -> artefacts."""

from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from . import __version__
from .backtest import build_trades, passive_reference, summarise, validity
from .calendar import future_timestamps
from .config import RunConfig
from .environment import cost_estimate, git_info, hardware, package_versions, peak_rss_gib
from .errors import LeakageError, QuotaError
from .leakage import future_invariance_check, run_negative_control
from .metrics import accuracy_metrics, diebold_mariano, latency_summary
from .models import build_models
from .splits import make_folds
from .validate import Warning_, load_ohlcv, sha256_file

DETERMINISTIC_MODELS = {"naive", "drift", "arima"}
KRONOS_REPRO_REL_TOL = 1e-6


def _periods_per_year(card, cfg: RunConfig) -> float:
    if cfg.backtest.periods_per_year:
        return float(cfg.backtest.periods_per_year)
    if abs(card.bar_seconds - 86400) < 1:
        return 365.0 if card.has_weekend_bars else 252.0
    return 365.0 * 86400.0 / card.bar_seconds


def _subset_metrics(actual, preds, last_obs, mask, names):
    if mask.sum() == 0:
        return None
    out = {}
    for m in names:
        out[m] = accuracy_metrics(actual[mask], preds[m][mask], last_obs[mask])
    return {"n_origins": int(mask.sum()), "models": out}


def run_evaluation(data_path: str | Path, cfg: RunConfig, out_dir: str | Path) -> dict:
    t_start = time.perf_counter()
    deadline = t_start + cfg.limits.timeout_s
    started_at = datetime.now(timezone.utc).isoformat()
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    timings: dict[str, float] = {}

    # 1. Data
    t = time.perf_counter()
    frame, card = load_ohlcv(data_path, cfg.limits, min_rows=cfg.min_history + cfg.horizon + 1)
    timings["load_validate_s"] = time.perf_counter() - t
    warnings: list[Warning_] = list(card.warnings)

    # 2. Folds (+ structural leakage assertions inside make_folds)
    folds = make_folds(len(frame), cfg.horizon, cfg.min_history, cfg.effective_step, cfg.max_origins,
                       cfg.embargo_bars)
    if len(folds) < 30:
        warnings.append(Warning_("EV-FEWORIGINS", "medium", f"Only {len(folds)} evaluation origins.",
                                 "Metrics based on fewer than ~30 independent origins have wide uncertainty."))
    origins = np.array([f.origin for f in folds])
    ts = frame["timestamp"]
    close = frame["close"].to_numpy(dtype=float)

    # 3. Leakage detector self-test (negative control)
    pick = sorted({int(origins[0]), int(origins[len(origins) // 2]), int(origins[-1])})[: cfg.leakage_check_origins]
    t = time.perf_counter()
    neg = run_negative_control(frame, pick, cfg.horizon, card)
    timings["negative_control_s"] = time.perf_counter() - t

    # 4. Models
    t = time.perf_counter()
    models = build_models(cfg.models, cfg)
    timings["model_load_s"] = time.perf_counter() - t

    # 5. Future-invariance leakage check per model
    t = time.perf_counter()
    invariance = []
    for m in models:
        res = future_invariance_check(m, frame, pick, cfg.horizon, card)
        invariance.append(res)
        if not res.passed:
            raise LeakageError(f"Model {m.name} forecast changed when future data changed (max diff {res.max_abs_diff})")
    timings["leakage_checks_s"] = time.perf_counter() - t
    leakage_ok = all(r.passed for r in invariance)

    # 6. Walk-forward
    names = [m.name for m in models]
    preds = {n: np.zeros((len(folds), cfg.horizon)) for n in names}
    lat = {n: [] for n in names}
    actual = np.zeros((len(folds), cfg.horizon))
    last_obs = np.zeros(len(folds))
    t = time.perf_counter()
    for m in models:
        m.prepare(frame)
    for i, f in enumerate(folds):
        if time.perf_counter() > deadline:
            raise QuotaError(f"Timeout: exceeded {cfg.limits.timeout_s:.0f}s after {i} of {len(folds)} origins")
        hist = frame.iloc[: f.origin + 1]
        fts = future_timestamps(hist["timestamp"].iloc[-1], cfg.horizon, card.frequency, card.bar_seconds)
        actual[i] = close[f.target_start: f.target_end + 1]
        last_obs[i] = close[f.origin]
        for m in models:
            t0 = time.perf_counter()
            p = np.asarray(m.predict(hist, cfg.horizon, f.origin, fts), dtype=float)
            lat[m.name].append(time.perf_counter() - t0)
            if p.shape != (cfg.horizon,) or not np.all(np.isfinite(p)):
                raise ValueError(f"{m.name} returned invalid forecast at origin {f.origin}")
            preds[m.name][i] = p
    timings["walk_forward_s"] = time.perf_counter() - t

    # 7. Metrics
    metrics = {n: accuracy_metrics(actual, preds[n], last_obs) for n in names}
    if "naive" in names:
        base_mae = metrics["naive"]["mae"]
        base_end = preds["naive"][:, -1] - actual[:, -1]
        for n in names:
            metrics[n]["rel_mae_vs_naive"] = metrics[n]["mae"] / base_mae if base_mae else None
            metrics[n]["dm_vs_naive"] = (diebold_mariano(preds[n][:, -1] - actual[:, -1], base_end)
                                         if n != "naive" else None)
    for n in names:
        metrics[n]["latency"] = latency_summary(lat[n])

    origin_ts = ts.iloc[origins].reset_index(drop=True)
    target_end_ts = ts.iloc[origins + cfg.horizon].reset_index(drop=True)
    release = pd.Timestamp(cfg.model_public_release, tz="UTC")
    cutoff = pd.Timestamp(cfg.model_training_cutoff, tz="UTC") + pd.Timedelta(days=1)
    post_mask = (origin_ts >= release).to_numpy()
    shadow = {
        "training_cutoff": cfg.model_training_cutoff, "public_release": cfg.model_public_release,
        "origins_total": int(len(folds)),
        "targets_on_or_before_cutoff": int((target_end_ts < cutoff).sum()),
        "origins_before_public_release": int((~post_mask).sum()),
        "origins_after_public_release": int(post_mask.sum()),
        "synthetic_data": bool(cfg.synthetic_data),
    }
    if "kronos_mini" in names and not cfg.synthetic_data:
        if shadow["targets_on_or_before_cutoff"]:
            warnings.append(Warning_("LK-PRETRAIN", "high",
                f"{shadow['targets_on_or_before_cutoff']} evaluation window(s) end on/before Kronos's stated training cut-off ({cfg.model_training_cutoff}).",
                "Kronos may have seen these bars during pre-training; its accuracy there can reflect memorisation."))
        if shadow["origins_before_public_release"]:
            warnings.append(Warning_("LK-SHADOW", "medium",
                f"{shadow['origins_before_public_release']} origin(s) fall between the stated cut-off and the public release ({cfg.model_public_release}).",
                "The model authors could, in principle, have selected checkpoints using this period. Metrics for origins after the public release are reported separately."))
    subset_post = _subset_metrics(actual, preds, last_obs, post_mask, names) if not cfg.synthetic_data else None

    # 8. Research backtest
    ppy = _periods_per_year(card, cfg)
    bt_cfg = cfg.backtest
    backtests = {}
    if bt_cfg.enabled:
        for n in names:
            tt = build_trades(close, origins, preds[n][:, -1], cfg.horizon, bt_cfg.delay_bars, bt_cfg.mode)
            n_active = int((tt.exposure != 0).sum())
            reasons = validity(n_active, bt_cfg.min_trades, hard_errors=False, leakage_ok=leakage_ok)
            entry = {"valid": not reasons, "suppressed_reasons": reasons, "n_periods": int(len(tt.exposure)),
                     "n_active": n_active}
            if not reasons:
                entry["base"] = summarise(tt, bt_cfg.cost_bps_per_side, ppy, cfg.horizon)
                entry["sensitivity"] = [
                    {k: v for k, v in summarise(tt, c, ppy, cfg.horizon).items() if not k.startswith("equity")}
                    for c in bt_cfg.cost_sensitivity_bps]
                entry["passive_long_reference"] = passive_reference(close, tt, bt_cfg.cost_bps_per_side)
                entry["entry_ts"] = [ts.iloc[int(i)].isoformat() for i in tt.entry]
            backtests[n] = entry

    # 9. Predictions artefact
    rows = []
    for i, f in enumerate(folds):
        for s in range(cfg.horizon):
            r = {"origin_index": f.origin, "origin_ts": ts.iloc[f.origin].isoformat(), "step": s + 1,
                 "target_ts": ts.iloc[f.target_start + s].isoformat(), "actual_close": actual[i, s]}
            for n in names:
                r[f"pred_{n}"] = preds[n][i, s]
            rows.append(r)
    pred_df = pd.DataFrame(rows)
    pred_path = out / "predictions.csv"
    pred_df.to_csv(pred_path, index=False, float_format="%.17g")

    wall = time.perf_counter() - t_start
    timings["total_before_report_s"] = wall
    threads = cfg.kronos.threads if "kronos_mini" in names else 1
    result = {
        "schema": "quanteval.manifest/v1",
        "quanteval_version": __version__,
        "run_id": None,
        "started_at_utc": started_at,
        "title": cfg.title or f"Benchmark report: {card.symbol or Path(data_path).name}",
        "config": cfg.to_dict(),
        "data": card.to_dict(),
        "data_provenance": cfg.data_provenance,
        "folds": {"n": len(folds), "first_origin_ts": ts.iloc[origins[0]].isoformat(),
                  "last_origin_ts": ts.iloc[origins[-1]].isoformat(),
                  "last_target_ts": ts.iloc[origins[-1] + cfg.horizon].isoformat(),
                  "step": cfg.effective_step, "embargo_bars": cfg.embargo_bars},
        "models": [m.info() for m in models],
        "leakage": {"structural_fold_checks": "passed",
                    "negative_control": neg.to_dict() | {"detected": not neg.passed},
                    "future_invariance": [r.to_dict() for r in invariance], "all_passed": leakage_ok},
        "pretraining_shadow": shadow,
        "metrics": metrics,
        "metrics_post_release": subset_post,
        "backtest": {"config": cfg.to_dict()["backtest"], "periods_per_year": ppy, "per_model": backtests},
        "warnings": [w.to_dict() for w in warnings],
        "artefacts": {"predictions.csv": sha256_file(pred_path)},
        "environment": {"packages": package_versions(), "hardware": hardware(threads), "git": git_info()},
        "seeds": {"global": cfg.seed, "kronos_per_origin": "seed + origin_index", "perturbation": 12345},
        "timings": timings,
    }
    ident = json.dumps({"data": card.sha256, "config": result["config"],
                        "code": result["environment"]["git"]["commit"], "v": __version__}, sort_keys=True)
    result["run_id"] = hashlib.sha256(ident.encode()).hexdigest()[:16]
    result["_arrays"] = {"origins": origins, "origin_ts": origin_ts, "actual": actual, "preds": preds,
                         "last_obs": last_obs, "close": close, "ts": ts, "lat": lat}
    return result


def finalise(result: dict, out_dir: str | Path, pdf: bool = True) -> dict:
    """Render charts + report, then write manifest with final timings and cost estimate."""
    from .report.render import render_report

    out = Path(out_dir)
    t = time.perf_counter()
    files = render_report(result, out, pdf=pdf)
    result["timings"]["report_render_s"] = time.perf_counter() - t
    total = result["timings"]["total_before_report_s"] + result["timings"]["report_render_s"]
    result["timings"]["total_wall_s"] = total
    peak = peak_rss_gib()
    threads = result["environment"]["hardware"]["torch_threads"] or 1
    result["resources"] = {"peak_rss_gib": round(peak, 3),
                           "cost_estimate": cost_estimate(total, int(threads), peak)}
    for f in files:
        result["artefacts"][Path(f).name] = sha256_file(f)
    manifest = {k: v for k, v in result.items() if not k.startswith("_")}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, default=_json_default), encoding="utf-8")
    return manifest


def _json_default(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (pd.Timestamp,)):
        return o.isoformat()
    raise TypeError(type(o))
