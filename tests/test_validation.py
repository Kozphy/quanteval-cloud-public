import pandas as pd
import pytest

from conftest import write
from quanteval.config import Limits
from quanteval.errors import DataValidationError, QuotaError
from quanteval.validate import load_ohlcv

LIM = Limits()


def _err(tmp_path, df, min_rows=50):
    with pytest.raises(DataValidationError) as e:
        load_ohlcv(write(tmp_path, df), LIM, min_rows=min_rows)
    return "\n".join(e.value.errors)


def test_valid_file_passes(synth_csv):
    df, card = load_ohlcv(synth_csv, LIM, min_rows=50)
    assert card.rows == 400 and card.symbol == "SYNTH-GARCH" and len(card.sha256) == 64
    assert list(df.columns)[:5] == ["timestamp", "open", "high", "low", "close"]


def test_unsorted_rejected(tmp_path, synth_df):
    df = synth_df.copy()
    df.iloc[[10, 11]] = df.iloc[[11, 10]].to_numpy()
    assert "not strictly increasing" in _err(tmp_path, df)


def test_duplicate_timestamps_rejected_with_line_numbers(tmp_path, synth_df):
    df = synth_df.copy()
    df.loc[5, "timestamp"] = df.loc[4, "timestamp"]
    msg = _err(tmp_path, df)
    assert "Duplicate timestamps" in msg and "line(s) 6, 7" in msg


def test_high_below_low_rejected(tmp_path, synth_df):
    df = synth_df.copy()
    df.loc[20, "high"] = df.loc[20, "low"] - 1
    assert "high < low" in _err(tmp_path, df)


def test_high_below_open_close_rejected(tmp_path, synth_df):
    df = synth_df.copy()
    df.loc[30, "high"] = min(df.loc[30, "open"], df.loc[30, "close"]) * 0.999
    df.loc[30, "low"] = df.loc[30, "high"] * 0.99
    assert "high < max(open, close)" in _err(tmp_path, df)


def test_non_positive_price_rejected(tmp_path, synth_df):
    df = synth_df.copy()
    df.loc[3, ["open", "high", "low", "close"]] = [0.0, 0.0, 0.0, 0.0]
    assert "Non-positive 'close'" in _err(tmp_path, df)


def test_too_short_rejected(tmp_path, synth_df):
    assert "Too few rows" in _err(tmp_path, synth_df.head(40), min_rows=134)


def test_missing_column_rejected(tmp_path, synth_df):
    assert "Missing required column" in _err(tmp_path, synth_df.drop(columns=["low"]))


def test_unparseable_timestamp_rejected(tmp_path, synth_df):
    df = synth_df.copy().astype({"timestamp": object})
    df.loc[7, "timestamp"] = "not-a-date"
    assert "Unparseable timestamp" in _err(tmp_path, df)


def test_negative_volume_rejected(tmp_path, synth_df):
    df = synth_df.copy()
    df.loc[9, "volume"] = -5
    assert "Negative volume" in _err(tmp_path, df)


def test_multi_symbol_rejected(tmp_path, synth_df):
    df = synth_df.copy()
    df.loc[0, "symbol"] = "OTHER"
    assert "Multiple symbols" in _err(tmp_path, df)


def test_row_quota(tmp_path, synth_df):
    with pytest.raises(QuotaError):
        load_ohlcv(write(tmp_path, synth_df), Limits(max_rows=100), min_rows=50)


def test_file_size_quota(tmp_path, synth_df):
    with pytest.raises(QuotaError):
        load_ohlcv(write(tmp_path, synth_df), Limits(max_file_mb=0.001), min_rows=50)


def test_quality_warnings_gap_and_split(tmp_path, synth_df):
    df = synth_df.drop(index=range(100, 103)).reset_index(drop=True)
    df.loc[200:, ["open", "high", "low", "close"]] *= 0.25  # unadjusted 1:4 split
    _, card = load_ohlcv(write(tmp_path, df), LIM, min_rows=50)
    codes = {w.code for w in card.warnings}
    assert {"DQ-GAP", "DQ-SPLIT", "DQ-EXTREME"} <= codes


def test_naive_timestamps_assumed_utc(tmp_path, synth_df):
    df = synth_df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.tz_localize(None).dt.strftime("%Y-%m-%d")
    _, card = load_ohlcv(write(tmp_path, df), LIM, min_rows=50)
    assert card.timezone_assumed_utc and "DQ-TZ" in {w.code for w in card.warnings}
