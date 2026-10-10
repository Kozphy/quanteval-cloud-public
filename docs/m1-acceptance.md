# Milestone 1: acceptance checklist ("Reproducible single-asset benchmark CLI")

Date: 2026-10-10. Code commit for the sample runs: `d1295a5`. Evidence: `reports/README.md`, `reports/test-results.txt`.

| # | Criterion (docs/first-task-summary.md §6) | Result | Evidence |
|---|---|---|---|
| 1 | `pip install -e .` then `quanteval run --csv … --horizon 5 --out out/` gives report.html, report.pdf, manifest.json | **PASS** | `reports/sample-synthetic/run1/`; `tests/test_end_to_end.py::test_cli_run_produces_artefacts_and_reproduces` |
| 2 | Validation rejects unsorted, duplicate, high<low, non-positive and too-short files with explicit messages (≥ 8 tests) | **PASS**: 15 tests, line-referenced messages | `tests/test_validation.py` |
| 3 | Walk-forward with embargo; test asserts no target index ≤ fit end + embargo | **PASS**: parametrised over horizons 1/5/20 and embargo 0/3/10 | `tests/test_splits_config.py` |
| 4 | Injected 1-bar look-ahead triggers a leakage failure | **PASS**: the run aborts with LeakageError, and a negative control runs in every report | `tests/test_leakage.py` |
| 5 | naive, ARIMA and Kronos-mini (pinned f4e68697… / 26966d0…), CPU, fixed seed | **PASS** (plus a drift baseline) | `tests/test_kronos.py`; manifests |
| 6 | MAE, RMSE, MASE, directional accuracy + Wilson CI, DM test vs naive, latency p50/p95, wall time + hardware in manifest | **PASS**, with one deviation: MASE is reported as **MAE relative to naive on the same origins** (scaled by out-of-sample naive error, not in-sample) | manifests, `tests/test_metrics_backtest.py` |
| 7 | Backtest with ≥ 1-bar delay and a bps sensitivity table; suppressed with a reason when < 30 trades | **PASS** | `tests/test_end_to_end.py`, `tests/test_leakage.py::test_backtest_requires_execution_delay` |
| 8 | Re-run from manifest reproduces naive/ARIMA exactly and Kronos within tolerance | **PASS**: all four models bit-identical (synthetic sample here; a second sample on public crypto data was checked privately) | `reports/sample-synthetic/run2/reproducibility.json` |
| 9 | Compliance lint fails the build on forbidden terms | **PASS**: the lint runs on every render, and tests cover it | `src/quanteval/report/compliance.py`, `tests/test_compliance_licenses.py` |
| 10 | THIRD_PARTY_NOTICES with Kronos MIT; license check blocks GPL and Commons Clause | **PASS**: gate reports 0 blocked (pyphen allowlisted as tri-licensed, MPL elected) | `THIRD_PARTY_NOTICES.md`, `scripts/check_licenses.py` |
| 11 | Measured compute time and cost per report recorded in docs/unit-economics.md | **PASS**: measured figures (35.80 s / 37.73 s synthetic, Kronos p50/p95, 0.52 GiB peak, US$0.0044/report at Cloud Run 1-min minimum, free-tier capacity) copied into `docs/unit-economics.md` §2, and margin, break-even and 10× tables recomputed with measured compute | `docs/unit-economics.md` §2, §4–§7; `reports/README.md` §Runtime and cost |

Tests: **80 passed** (15 validation, 19 splits/config/quotas, 6 leakage, 8 metrics/backtest, 23 compliance/licenses, 6 end-to-end, 3 Kronos-mini CPU).

Quotas enforced (config.Limits): max_rows 200,000; max_file_mb 50; lookback 16–2048; horizon 1–60; max_origins 500; timeout 1,800 s; step ≥ horizon; delay ≥ 1.

## Not done or known gaps
- CI (`.github/workflows/ci.yml`) runs on GitHub Actions (Linux, Python 3.12). At M1 sign-off, tests had been run locally only.
- No shuffled-target sanity check (in the PRD, not in the M1 criteria).
- One instrument per run; no "bring your own predictions" mode; no web upload, auth, queue or billing.
- ARIMA order is fixed (1,1,1); no AIC search.
- Statistical tests are not corrected for multiple comparisons.
- Kronos bitwise reproducibility was verified on one machine only.
- A sample on public crypto data exists privately pending data-licensing review.
- WeasyPrint warns that HarfBuzz-Subset is missing; the PDF still renders, but fonts aren't subset (larger file).
