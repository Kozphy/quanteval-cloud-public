import pytest

from quanteval.config import RunConfig, load_config
from quanteval.errors import LeakageError, QuotaError
from quanteval.splits import Fold, assert_folds_valid, make_folds


@pytest.mark.parametrize("embargo", [0, 3, 10])
@pytest.mark.parametrize("horizon", [1, 5, 20])
def test_no_target_index_within_fit_window_plus_embargo(horizon, embargo):
    folds = make_folds(n_rows=600, horizon=horizon, min_history=128, step=horizon, max_origins=500,
                       embargo_bars=embargo)
    assert folds
    for f in folds:
        assert f.target_index.min() > f.fit_end + embargo
        assert f.target_index.min() > f.origin
        assert len(f.target_index) == horizon
    ends = [f.target_end for f in folds]
    starts = [f.target_start for f in folds]
    assert all(s > e for s, e in zip(starts[1:], ends[:-1]))  # non-overlapping windows
    assert folds[-1].target_end == 599  # most recent data evaluated


def test_overlapping_windows_rejected():
    folds = [Fold(200, 200, 201, 205), Fold(203, 203, 204, 208)]
    with pytest.raises(LeakageError):
        assert_folds_valid(folds, 5, 0, 600)


def test_target_inside_fit_window_rejected():
    with pytest.raises(LeakageError):
        assert_folds_valid([Fold(200, 200, 200, 204)], 5, 0, 600)
    with pytest.raises(LeakageError):
        assert_folds_valid([Fold(200, 198, 199, 203)], 5, 0, 600)


def test_not_enough_rows():
    with pytest.raises(QuotaError):
        make_folds(n_rows=100, horizon=5, min_history=128, step=5, max_origins=10)


@pytest.mark.parametrize("override", [{"horizon": 0}, {"horizon": 61}, {"lookback": 4096},
                                      {"max_origins": 10_000}, {"step": 2, "horizon": 5}, {"models": ["lstm"]}])
def test_config_quotas(override):
    with pytest.raises(QuotaError):
        load_config(None, override)


def test_backtest_delay_must_be_positive():
    cfg = RunConfig()
    cfg.backtest.delay_bars = 0
    with pytest.raises(QuotaError):
        cfg.validate()
