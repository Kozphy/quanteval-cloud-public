"""Re-run an evaluation from its manifest and compare forecasts and metrics."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from .config import config_from_dict
from .errors import QuantEvalError
from .harness import DETERMINISTIC_MODELS, KRONOS_REPRO_REL_TOL, finalise, run_evaluation
from .validate import sha256_file

TIMING_KEYS = {"latency"}


def _strip(metrics: dict) -> dict:
    return {m: {k: v for k, v in d.items() if k not in TIMING_KEYS} for m, d in metrics.items()}


def reproduce(manifest_path: str | Path, data_path: str | Path, out_dir: str | Path, pdf: bool = False) -> dict:
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    sha = sha256_file(data_path)
    if sha != manifest["data"]["sha256"]:
        raise QuantEvalError(f"Input file hash {sha} does not match manifest {manifest['data']['sha256']}")
    cfg = config_from_dict(manifest["config"])
    result = run_evaluation(data_path, cfg, out_dir)
    new_manifest = finalise(result, out_dir, pdf=pdf)

    orig_pred = pd.read_csv(Path(manifest_path).parent / "predictions.csv")
    new_pred = pd.read_csv(Path(out_dir) / "predictions.csv")
    checks = {}
    ok = True
    for col in [c for c in orig_pred.columns if c.startswith("pred_")]:
        model = col[len("pred_"):]
        a, b = orig_pred[col].to_numpy(float), new_pred[col].to_numpy(float)
        max_abs = float(np.max(np.abs(a - b)))
        max_rel = float(np.max(np.abs(a - b) / np.maximum(np.abs(a), 1e-12)))
        if model in DETERMINISTIC_MODELS:
            passed, rule = max_abs == 0.0, "exact (bitwise-equal floats)"
        else:
            passed, rule = max_rel <= KRONOS_REPRO_REL_TOL, f"max relative diff <= {KRONOS_REPRO_REL_TOL}"
        checks[model] = {"max_abs_diff": max_abs, "max_rel_diff": max_rel, "rule": rule, "passed": passed}
        ok &= passed
    same_actuals = bool(np.array_equal(orig_pred["actual_close"].to_numpy(), new_pred["actual_close"].to_numpy()))
    metrics_equal = _strip(manifest["metrics"]) == _strip(new_manifest["metrics"])
    report = {
        "original_run_id": manifest["run_id"], "reproduced_run_id": new_manifest["run_id"],
        "input_sha256": sha, "predictions_sha256_original": manifest["artefacts"]["predictions.csv"],
        "predictions_sha256_reproduced": new_manifest["artefacts"]["predictions.csv"],
        "predictions_identical": manifest["artefacts"]["predictions.csv"] == new_manifest["artefacts"]["predictions.csv"],
        "actuals_identical": same_actuals, "accuracy_metrics_identical": metrics_equal,
        "per_model": checks, "passed": bool(ok and same_actuals),
        "wall_s_original": manifest["timings"].get("total_wall_s"),
        "wall_s_reproduced": new_manifest["timings"].get("total_wall_s"),
    }
    (Path(out_dir) / "reproducibility.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
