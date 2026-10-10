import numpy as np
import pytest

from quanteval.backtest import build_trades, summarise, validity
from quanteval.metrics import accuracy_metrics, diebold_mariano, directional, wilson_ci


def test_wilson_ci_known_value():
    lo, hi = wilson_ci(50, 100)
    assert lo == pytest.approx(0.4038, abs=1e-3) and hi == pytest.approx(0.5962, abs=1e-3)


def test_directional_accuracy_counts():
    last = np.array([100.0, 100, 100, 100])
    actual = np.array([101.0, 99, 101, 100])  # last one: no move -> excluded
    pred = np.array([102.0, 98, 99, 105])
    d = directional(actual, pred, last)
    assert d["n"] == 3 and d["hits"] == 2 and d["accuracy"] == pytest.approx(2 / 3)


def test_directional_undefined_for_flat_forecast():
    d = directional(np.array([101.0, 99]), np.array([100.0, 100]), np.array([100.0, 100]))
    assert d["accuracy"] is None and d["n"] == 0


def test_mae_rmse():
    actual = np.array([[1.0, 2.0], [3.0, 4.0]])
    pred = np.array([[2.0, 2.0], [3.0, 6.0]])
    m = accuracy_metrics(actual, pred, np.array([1.0, 3.0]))
    assert m["mae"] == pytest.approx(0.75) and m["rmse"] == pytest.approx(np.sqrt(5 / 4))


def test_dm_negative_when_model_better():
    rng = np.random.default_rng(0)
    base = rng.normal(0, 2, 200)
    better = base * 0.5
    r = diebold_mariano(better, base)
    assert r["stat"] < 0 and r["p_value"] < 0.01


def test_backtest_costs_and_values():
    close = np.array([100, 100, 110, 110, 110, 121, 121, 121, 121, 121], dtype=float)
    # origin 0: predict up -> enter close[1]=100, exit close[3]=110 (+10%); origin 2: predict down -> enter close[3]=110 exit close[5]=121 (-10%)
    tt = build_trades(close, np.array([0, 2]), np.array([150.0, 50.0]), horizon=2, delay=1, mode="long_short")
    assert tt.gross == pytest.approx([0.10, -0.10])
    s0 = summarise(tt, 0.0, 252, 2)
    s10 = summarise(tt, 10.0, 252, 2)
    assert s0["total_return_gross"] == pytest.approx(1.1 * 0.9 - 1)
    assert s10["total_return_net"] == pytest.approx((1 + 0.10 - 0.002) * (1 - 0.10 - 0.002) - 1)
    assert s10["total_cost"] == pytest.approx(0.004)


def test_long_flat_mode():
    close = np.linspace(100, 110, 20)
    tt = build_trades(close, np.array([0, 5]), np.array([50.0, 200.0]), 3, 1, "long_flat")
    assert list(tt.exposure) == [0.0, 1.0]


def test_validity_gate():
    assert validity(29, 30, False, True)
    assert validity(30, 30, False, True) == []
    assert validity(100, 30, False, False)
