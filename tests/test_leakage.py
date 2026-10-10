import numpy as np
import pytest

from quanteval.backtest import build_trades
from quanteval.config import Limits, RunConfig
from quanteval.errors import LeakageError
from quanteval.harness import run_evaluation
from quanteval.leakage import LookaheadModel, future_invariance_check, run_negative_control
from quanteval.models.arima import ArimaModel
from quanteval.models.base import ForecastModel
from quanteval.models.naive import DriftModel, NaiveModel
from quanteval.validate import load_ohlcv


@pytest.fixture
def loaded(synth_csv):
    return load_ohlcv(synth_csv, Limits(), min_rows=50)


def test_negative_control_lookahead_is_detected(loaded):
    df, card = loaded
    res = future_invariance_check(LookaheadModel(), df, [200, 300], 5, card)
    assert not res.passed and res.max_abs_diff > 0
    assert run_negative_control(df, [200, 300], 5, card).passed is False


@pytest.mark.parametrize("model", [NaiveModel(), DriftModel(window=64), ArimaModel(order=(1, 1, 1))])
def test_honest_models_are_future_invariant(loaded, model):
    df, card = loaded
    assert future_invariance_check(model, df, [150, 250, 390], 5, card).passed


class OneBarLookahead(ForecastModel):
    """Classic bug: a feature computed with shift(-1) on the whole file."""
    name = "one_bar_lookahead"

    def prepare(self, full_frame):
        self.next_close = full_frame["close"].shift(-1).to_numpy()

    def predict(self, history, horizon, origin, future_timestamps):
        return np.full(horizon, self.next_close[origin])


def test_injected_one_bar_lookahead_aborts_run(synth_csv, tmp_path, monkeypatch):
    import quanteval.harness as h

    monkeypatch.setattr(h, "build_models", lambda names, cfg: [NaiveModel(), OneBarLookahead()])
    cfg = RunConfig(models=["naive"], max_origins=20)
    with pytest.raises(LeakageError, match="one_bar_lookahead"):
        run_evaluation(synth_csv, cfg, tmp_path / "out")


def test_backtest_requires_execution_delay():
    close = np.linspace(100, 120, 50)
    with pytest.raises(LeakageError):
        build_trades(close, np.array([10, 15]), np.array([130.0, 90.0]), 5, delay=0, mode="long_short")
    tt = build_trades(close, np.array([10, 15, 20]), np.array([130.0, 90.0, 130.0]), 5, delay=1, mode="long_short")
    assert np.all(tt.entry > tt.origin) and np.all(tt.entry[1:] >= tt.exit[:-1])
