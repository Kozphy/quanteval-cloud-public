"""Command-line interface: `quanteval run | reproduce | validate`."""

from __future__ import annotations

import argparse
import json
import sys

from .config import load_config
from .errors import QuantEvalError


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="quanteval", description="Financial forecasting model benchmark (research only)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="run a benchmark and write report.html/report.pdf/manifest.json")
    r.add_argument("--csv", required=True, help="OHLCV CSV (or .parquet)")
    r.add_argument("--out", required=True)
    r.add_argument("--config", help="YAML/JSON config file")
    r.add_argument("--horizon", type=int)
    r.add_argument("--lookback", type=int)
    r.add_argument("--max-origins", type=int, dest="max_origins")
    r.add_argument("--models", help="comma-separated: naive,drift,arima,kronos_mini")
    r.add_argument("--title")
    r.add_argument("--provenance", dest="data_provenance")
    r.add_argument("--no-pdf", action="store_true")

    p = sub.add_parser("reproduce", help="re-run from a manifest and compare results")
    p.add_argument("--manifest", required=True)
    p.add_argument("--csv", required=True)
    p.add_argument("--out", required=True)

    v = sub.add_parser("validate", help="validate a CSV only")
    v.add_argument("--csv", required=True)
    v.add_argument("--config")

    a = ap.parse_args(argv)
    try:
        if a.cmd == "run":
            from .harness import finalise, run_evaluation

            overrides = {"horizon": a.horizon, "lookback": a.lookback, "max_origins": a.max_origins,
                         "title": a.title, "data_provenance": a.data_provenance,
                         "models": a.models.split(",") if a.models else None}
            cfg = load_config(a.config, overrides)
            result = run_evaluation(a.csv, cfg, a.out)
            manifest = finalise(result, a.out, pdf=not a.no_pdf)
            print(json.dumps({"run_id": manifest["run_id"], "out": a.out,
                              "total_wall_s": round(manifest["timings"]["total_wall_s"], 2),
                              "estimated_usd": manifest["resources"]["cost_estimate"]["estimated_usd"]}))
        elif a.cmd == "reproduce":
            from .reproduce import reproduce

            rep = reproduce(a.manifest, a.csv, a.out)
            print(json.dumps(rep, indent=2))
            return 0 if rep["passed"] else 3
        elif a.cmd == "validate":
            from .validate import load_ohlcv

            cfg = load_config(a.config)
            _, card = load_ohlcv(a.csv, cfg.limits, min_rows=cfg.min_history + cfg.horizon + 1)
            print(json.dumps(card.to_dict(), indent=2))
    except QuantEvalError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
