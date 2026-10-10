import json

import pandas as pd
import pytest

from quanteval.cli import main
from quanteval.config import RunConfig
from quanteval.errors import QuotaError
from quanteval.harness import run_evaluation
from quanteval.reproduce import reproduce

BASELINES = "naive,drift,arima"


def test_cli_run_produces_artefacts_and_reproduces(synth_csv, tmp_path):
    out = tmp_path / "run1"
    rc = main(["run", "--csv", str(synth_csv), "--out", str(out), "--horizon", "5", "--models", BASELINES,
               "--max-origins", "40"])
    assert rc == 0
    for f in ["report.html", "report.pdf", "manifest.json", "predictions.csv", "charts/oos_forecasts.png"]:
        assert (out / f).exists(), f
    m = json.loads((out / "manifest.json").read_text())
    assert m["data"]["sha256"] and m["config"]["horizon"] == 5 and m["seeds"]["global"] == 42
    assert m["environment"]["packages"]["statsmodels"] and m["timings"]["total_wall_s"] > 0
    assert m["leakage"]["negative_control"]["detected"] and m["leakage"]["all_passed"]
    assert m["resources"]["cost_estimate"]["estimated_usd"] > 0
    rep = reproduce(out / "manifest.json", synth_csv, tmp_path / "run2")
    assert rep["passed"] and rep["predictions_identical"] and rep["accuracy_metrics_identical"]
    for model in ["naive", "drift", "arima"]:
        assert rep["per_model"][model]["max_abs_diff"] == 0.0


def test_cli_rejects_bad_csv_with_exit_code(tmp_path, synth_df, capsys):
    df = synth_df.copy()
    df.loc[10, "high"] = df.loc[10, "low"] - 1
    p = tmp_path / "bad.csv"
    df.to_csv(p, index=False)
    assert main(["run", "--csv", str(p), "--out", str(tmp_path / "o"), "--models", "naive"]) == 2
    assert "high < low" in capsys.readouterr().err


def test_backtest_suppressed_when_too_few_trades(synth_csv, tmp_path):
    cfg = RunConfig(models=["naive", "drift"], max_origins=20)
    r = run_evaluation(synth_csv, cfg, tmp_path / "o")
    bt = r["backtest"]["per_model"]
    assert not bt["drift"]["valid"] and "required" in bt["drift"]["suppressed_reasons"][0]
    assert not bt["naive"]["valid"]


def test_backtest_shown_when_enough_trades(synth_csv, tmp_path):
    cfg = RunConfig(models=["naive", "drift"], max_origins=60)
    r = run_evaluation(synth_csv, cfg, tmp_path / "o")
    assert r["backtest"]["per_model"]["drift"]["valid"]
    assert len(r["backtest"]["per_model"]["drift"]["sensitivity"]) == 4


def test_timeout_quota(synth_csv, tmp_path):
    cfg = RunConfig(models=["arima"], max_origins=50)
    cfg.limits.timeout_s = 0.0
    with pytest.raises(QuotaError, match="Timeout"):
        run_evaluation(synth_csv, cfg, tmp_path / "o")


def test_predictions_cover_only_out_of_sample(synth_csv, tmp_path):
    cfg = RunConfig(models=["naive"], max_origins=30)
    run_evaluation(synth_csv, cfg, tmp_path / "o")
    p = pd.read_csv(tmp_path / "o" / "predictions.csv")
    assert (pd.to_datetime(p["target_ts"]) > pd.to_datetime(p["origin_ts"])).all()
