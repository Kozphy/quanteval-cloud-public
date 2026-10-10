"""OHLCV loading and validation.

Hard checks raise DataValidationError with CSV line references; soft checks become warnings.
Adapted in part from Kozphy/ForexTraderWithBloombergAccess-public `src/forex_quant/data.py`
(`validate_golden_schema`, `fingerprint_frame`; MIT, (c) 2026 Zixsa) and
Kozphy/Market-Data-Platform-for-Analytics-Execution `transformation/cleaning.py` (MIT, (c) 2026 Zixsa).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

from .config import Limits
from .errors import DataValidationError, QuotaError

REQUIRED = ["timestamp", "open", "high", "low", "close"]
OPTIONAL = ["volume", "amount"]
ALIASES = {"timestamps": "timestamp", "date": "timestamp", "datetime": "timestamp", "time": "timestamp"}
MAX_LISTED = 5


@dataclass
class Warning_:
    code: str
    severity: str  # info | low | medium | high
    message: str
    explanation: str

    def to_dict(self) -> dict:
        return {"code": self.code, "severity": self.severity, "message": self.message, "explanation": self.explanation}


@dataclass
class DataCard:
    path: str
    sha256: str
    file_bytes: int
    rows: int
    start: str
    end: str
    frequency: str
    bar_seconds: float
    has_weekend_bars: bool
    symbol: str | None
    columns: list[str]
    timezone_assumed_utc: bool
    warnings: list[Warning_] = field(default_factory=list)

    def to_dict(self) -> dict:
        d = {k: v for k, v in self.__dict__.items() if k != "warnings"}
        d["warnings"] = [w.to_dict() for w in self.warnings]
        return d


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _lines(mask: pd.Series) -> str:
    # CSV line number = 0-based row index + 2 (header is line 1)
    idx = list(np.flatnonzero(mask.to_numpy()))
    shown = ", ".join(str(i + 2) for i in idx[:MAX_LISTED])
    more = f" (+{len(idx) - MAX_LISTED} more)" if len(idx) > MAX_LISTED else ""
    return f"line(s) {shown}{more}"


def load_ohlcv(path: str | Path, limits: Limits, min_rows: int) -> tuple[pd.DataFrame, DataCard]:
    path = Path(path)
    if not path.exists():
        raise DataValidationError([f"File not found: {path}"])
    size = path.stat().st_size
    if size > limits.max_file_mb * 1024 * 1024:
        raise QuotaError(f"File is {size / 1e6:.1f} MB; limit is {limits.max_file_mb} MB")

    try:
        if path.suffix.lower() == ".parquet":
            raw = pd.read_parquet(path)
        else:
            raw = pd.read_csv(path)
    except Exception as exc:  # noqa: BLE001
        raise DataValidationError([f"Could not parse file: {exc}"]) from exc

    if len(raw) > limits.max_rows:
        raise QuotaError(f"File has {len(raw)} rows; limit is {limits.max_rows}")

    raw.columns = [ALIASES.get(str(c).strip().lower(), str(c).strip().lower()) for c in raw.columns]
    errors: list[str] = []
    missing = [c for c in REQUIRED if c not in raw.columns]
    if missing:
        raise DataValidationError([f"Missing required column(s): {missing}. Required: {REQUIRED}"])

    df = raw.copy()
    ts = pd.to_datetime(df["timestamp"], errors="coerce", utc=False)
    bad_ts = ts.isna()
    if bad_ts.any():
        errors.append(f"Unparseable timestamp at {_lines(bad_ts)}")
    tz_assumed = False
    if not bad_ts.any():
        if getattr(ts.dt, "tz", None) is None:
            ts = ts.dt.tz_localize("UTC")
            tz_assumed = True
        else:
            ts = ts.dt.tz_convert("UTC")
    df["timestamp"] = ts

    for col in ["open", "high", "low", "close"] + [c for c in OPTIONAL if c in df.columns]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in ["open", "high", "low", "close"]:
        nan = df[col].isna()
        if nan.any():
            errors.append(f"Missing/non-numeric '{col}' at {_lines(nan)}")
        nonpos = df[col] <= 0
        if nonpos.any():
            errors.append(f"Non-positive '{col}' at {_lines(nonpos)}")
    if "volume" in df.columns:
        neg = df["volume"] < 0
        if neg.any():
            errors.append(f"Negative volume at {_lines(neg)}")

    hl = df["high"] < df["low"]
    if hl.any():
        errors.append(f"high < low at {_lines(hl)}")
    tol = 1e-9
    hi_bad = df["high"] + tol * df["high"].abs() < df[["open", "close"]].max(axis=1)
    if hi_bad.any():
        errors.append(f"high < max(open, close) at {_lines(hi_bad)}")
    lo_bad = df["low"] - tol * df["low"].abs() > df[["open", "close"]].min(axis=1)
    if lo_bad.any():
        errors.append(f"low > min(open, close) at {_lines(lo_bad)}")

    if not bad_ts.any():
        dup = df["timestamp"].duplicated(keep=False)
        if dup.any():
            errors.append(f"Duplicate timestamps at {_lines(dup)}")
        backwards = df["timestamp"].diff() <= pd.Timedelta(0)
        backwards = backwards & ~dup
        if backwards.any():
            errors.append(
                f"Timestamps not strictly increasing at {_lines(backwards)} "
                "(sort the file chronologically; QuantEval does not reorder data silently)"
            )

    if len(df) < min_rows:
        errors.append(f"Too few rows: {len(df)} < required minimum {min_rows} (min_history + horizon + 1)")

    if errors:
        raise DataValidationError(errors)

    keep = REQUIRED + [c for c in OPTIONAL if c in df.columns]
    symbol = None
    if "symbol" in df.columns and df["symbol"].nunique() == 1:
        symbol = str(df["symbol"].iloc[0])
    elif "symbol" in df.columns and df["symbol"].nunique() > 1:
        raise DataValidationError(["Multiple symbols in one file; v0 supports one instrument per run"])
    df = df[keep].reset_index(drop=True)

    deltas = df["timestamp"].diff().dropna().dt.total_seconds()
    bar_seconds = float(deltas.median())
    has_weekend = bool((df["timestamp"].dt.weekday >= 5).any())
    if abs(bar_seconds - 86400) < 1 and not has_weekend:
        freq = "B"  # business-day calendar (equities)
    else:
        freq = f"{int(bar_seconds)}s"

    card = DataCard(
        path=str(path), sha256=sha256_file(path), file_bytes=size, rows=len(df),
        start=df["timestamp"].iloc[0].isoformat(), end=df["timestamp"].iloc[-1].isoformat(),
        frequency=freq, bar_seconds=bar_seconds, has_weekend_bars=has_weekend, symbol=symbol,
        columns=list(df.columns), timezone_assumed_utc=tz_assumed,
    )
    card.warnings = quality_warnings(df, card)
    return df, card


def quality_warnings(df: pd.DataFrame, card: DataCard) -> list[Warning_]:
    out: list[Warning_] = []
    if card.timezone_assumed_utc:
        out.append(Warning_("DQ-TZ", "low", "Timestamps had no timezone; UTC was assumed.",
                            "If bars are in exchange-local time, session alignment and calendar features may be off."))
    deltas = df["timestamp"].diff().dt.total_seconds()
    expected = card.bar_seconds
    if card.frequency == "B":
        bdays = pd.bdate_range(df["timestamp"].iloc[0].normalize(), df["timestamp"].iloc[-1].normalize())
        missing = len(bdays) - len(df)
        if missing > 0:
            out.append(Warning_("DQ-GAP", "info", f"{missing} business day(s) without a bar (holidays or gaps).",
                                "Exchange holidays are expected; unexplained gaps can distort multi-step horizons."))
    else:
        gaps = deltas > 1.5 * expected
        if gaps.any():
            out.append(Warning_("DQ-GAP", "medium", f"{int(gaps.sum())} gap(s) longer than 1.5x the median bar spacing.",
                                "Missing bars mean an h-step forecast may span more calendar time than intended."))
    if "volume" in df.columns:
        zero = (df["volume"] == 0)
        if zero.any():
            out.append(Warning_("DQ-ZEROVOL", "low", f"{int(zero.sum())} bar(s) with zero volume.",
                                "Zero-volume bars often indicate stale or synthetic quotes."))
        if df["volume"].isna().any():
            out.append(Warning_("DQ-VOLNAN", "low", "Volume has missing values; they are filled with 0 for Kronos.",
                                "Kronos uses volume as an input feature."))
    else:
        out.append(Warning_("DQ-NOVOL", "low", "No volume column; Kronos receives zeros for volume/amount.",
                            "Kronos was pre-trained with volume; omitting it may reduce forecast quality."))
    close = df["close"]
    stale = (close.diff() == 0).astype(int)
    runs = stale.groupby((stale == 0).cumsum()).cumsum()
    if (runs >= 3).any():
        out.append(Warning_("DQ-STALE", "medium", "Close unchanged for 4+ consecutive bars at least once.",
                            "Repeated prices suggest stale data or an illiquid instrument."))
    logret = np.log(close).diff().dropna()
    med = logret.median()
    mad = (logret - med).abs().median() or 1e-12
    extreme = (logret - med).abs() > 12 * 1.4826 * mad
    if extreme.any():
        out.append(Warning_("DQ-EXTREME", "medium",
                            f"{int(extreme.sum())} extreme bar-to-bar move(s) (> 12 robust std devs).",
                            "Could be genuine market events, unadjusted splits/dividends, or bad ticks. Check before trusting metrics."))
    if (logret.abs() > np.log(1.8)).any():
        out.append(Warning_("DQ-SPLIT", "high", "A bar-to-bar move larger than +80%/-44% was found.",
                            "This is typical of an unadjusted split or a data error; forecast errors around it will dominate."))
    return out
