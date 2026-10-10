"""Future timestamp generation from the inferred bar calendar (never from future rows)."""

from __future__ import annotations

import pandas as pd


def future_timestamps(last_ts: pd.Timestamp, horizon: int, frequency: str, bar_seconds: float) -> pd.DatetimeIndex:
    if frequency == "B":
        return pd.bdate_range(last_ts + pd.Timedelta(days=1), periods=horizon, tz=last_ts.tz)
    step = pd.Timedelta(seconds=bar_seconds)
    return pd.DatetimeIndex([last_ts + step * (i + 1) for i in range(horizon)])
