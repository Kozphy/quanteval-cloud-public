import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples"))

from synthetic_ohlcv import generate  # noqa: E402


@pytest.fixture(scope="session")
def synth_df() -> pd.DataFrame:
    return generate(rows=400, seed=11)


@pytest.fixture
def synth_csv(tmp_path, synth_df) -> Path:
    p = tmp_path / "synth.csv"
    synth_df.to_csv(p, index=False)
    return p


def write(tmp_path, df, name="x.csv"):
    p = tmp_path / name
    df.to_csv(p, index=False)
    return p
