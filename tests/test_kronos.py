"""Kronos-mini on CPU (downloads pinned weights from Hugging Face on first run)."""

import json

import numpy as np
import pytest

from quanteval.cli import main
from quanteval.config import RunConfig
from quanteval.reproduce import reproduce

pytestmark = pytest.mark.kronos


@pytest.fixture(scope="module")
def kronos_model():
    from quanteval.models.kronos import KronosMiniModel

    cfg = RunConfig(lookback=128)
    cfg.kronos.sample_count = 2
    return KronosMiniModel(cfg)


def test_kronos_pinned_and_param_count(kronos_model):
    info = kronos_model.info()
    assert info["model_revision"].startswith("f4e68697") and info["tokenizer_revision"].startswith("26966d0")
    assert info["params"] == 4_108_032


def test_kronos_deterministic_and_future_invariant(kronos_model, synth_csv):
    from quanteval.config import Limits
    from quanteval.leakage import future_invariance_check
    from quanteval.validate import load_ohlcv

    df, card = load_ohlcv(synth_csv, Limits(), min_rows=50)
    res = future_invariance_check(kronos_model, df, [200, 350], 3, card)
    assert res.passed and res.max_abs_diff == 0.0


def test_kronos_end_to_end_with_reproduction(synth_csv, tmp_path):
    cfg = {"horizon": 3, "lookback": 128, "max_origins": 8, "kronos": {"sample_count": 2}}
    cfg_path = tmp_path / "cfg.json"
    cfg_path.write_text(json.dumps(cfg))
    out = tmp_path / "k1"
    assert main(["run", "--csv", str(synth_csv), "--out", str(out), "--config", str(cfg_path), "--no-pdf"]) == 0
    m = json.loads((out / "manifest.json").read_text())
    assert m["metrics"]["kronos_mini"]["latency"]["n"] == 8
    assert m["models"][-1]["model_revision"].startswith("f4e68697")
    rep = reproduce(out / "manifest.json", synth_csv, tmp_path / "k2")
    assert rep["passed"], rep
    assert rep["per_model"]["kronos_mini"]["max_rel_diff"] <= 1e-6
