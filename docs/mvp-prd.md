# Concierge MVP PRD — Financial Model Benchmark Report

Version 0.1 · 2026-10-10 · Status: **Spec only (Unimplemented)**

## 1. Problem (hypothesis, to be validated)
Teams considering financial time-series foundation models (Kronos, Chronos, TimesFM…) lack a fast, leakage-safe, reproducible way to tell whether a model beats simple baselines on *their* instruments after costs. Public evidence, such as Kronos GitHub issues #354 and #375, suggests naive baselines are often hard to beat. That makes an independent check valuable, if buyers agree.

## 2. Users and delivery mode
- Buyer: fintech CTO / head of research / quant researcher (B2B).
- Delivery: **concierge**. The customer sends a CSV (email or a private upload link). The founder runs a CLI job (admin-triggered) and delivers an HTML + PDF report and a manifest within an agreed SLA (target ≤ 3 business days; *assumption*).
- No customer-facing web app in v0. One CLI plus a report template.

## 3. Scope (must have)
| # | Capability | Spec |
|---|---|---|
| 1 | **CSV upload + validation** | Columns: `timestamp, open, high, low, close[, volume][, amount][, symbol]`. One symbol per run in v0. Timezone-aware or declared tz. Limits: ≤ 50 MB, ≤ 500k rows (*assumption*). Hard checks: parseable, monotonic increasing, no duplicate timestamps, positive prices, `high ≥ max(open, close)`, `low ≤ min(open, close)`, `volume ≥ 0`, min rows = context + test window. Soft checks (warnings): gaps vs inferred frequency, zero-volume runs, stale prices (repeated close), extreme returns (> k·MAD), suspected splits/adjustments, weekend bars for equities. |
| 2 | **Forecast horizon** | `h ∈ {1, 5, 10, 20}` bars (config). Target: close; secondary: log-return. |
| 3 | **Chronological validation** | Expanding-window walk-forward: `n_origins` (default 50, *assumption*), step = h, embargo ≥ h bars between the fit window end and the evaluation target. No shuffling. Optional fixed train/test split for small data. **Release-date guard:** flag any evaluation window before the model's documented training cutoff (Kronos: Feb 2024 per issue #204) or public release (2025-08-02, arXiv v1) as "inside pretraining shadow", and report post-release metrics separately. |
| 4 | **Models** | (a) Naive last value (random walk). (b) Seasonal/drift naive (optional). (c) ARIMA via statsmodels: fixed order (default (1,1,1)) or small AIC grid, refit every `refit_stride` origins. (d) **Kronos-mini** zero-shot (HF revisions pinned), context ≤ 512 default (max 2048), `sample_count` configurable (default 5, *assumption*), seed fixed; report mean path plus sample spread. |
| 5 | **Metrics** | MAE, RMSE (price and return space), MASE vs naive, directional accuracy (sign of h-step return) with Wilson CI and a binomial test vs 50%, Diebold–Mariano test vs naive. **Inference latency**: p50/p95 per forecast and total wall time, with hardware recorded. |
| 6 | **Cost-aware research backtest (when valid)** | Rule: sign of predicted h-step return → position in {−1, 0, +1} (or long/flat), executed with ≥ 1-bar delay, non-overlapping holding of h bars. Costs: user-specified bps per side (default 5 bps; plus a sensitivity table at 0/5/10/25 bps). Output: gross/net return, Sharpe, max DD, turnover, hit rate, vs buy-and-hold and naive-signal rules. **Validity gates (backtest is suppressed with an explanation if any fail):** ≥ 30 non-overlapping trades; no hard data-quality failures; no leakage-test failure; costs supplied or default acknowledged. Labelled "historical research simulation, not investment advice". |
| 7 | **Charts** | Out-of-sample actual vs forecast (per model) with origin markers; error distribution; rolling MAE; directional hit-rate over time; equity curve gross vs net (if backtest valid); cost-sensitivity bar chart; latency histogram. |
| 8 | **Leakage and data-quality warnings** | Automated tests: shuffled-target sanity check, future-shift negative control (inject 1-bar look-ahead, which must be detected), train/test overlap assertion, pretraining-shadow flag, survivorship note (single symbol can't be checked, so the report states it). Each warning has a plain-English explanation and severity. |
| 9 | **Report** | Self-contained HTML (Plotly inline) + PDF (WeasyPrint). Sections: Executive summary (which model won on what, with uncertainty); Data card; Protocol; Results tables; Charts; Backtest (or suppression reason); Warnings; Limitations and disclaimers; Reproducibility appendix. |
| 10 | **Experiment manifest** | `manifest.json`: run_id (hash), created_at UTC, input file SHA-256, row count, detected frequency, config, code git SHA, package versions, model IDs + HF revisions, seeds, hardware, wall times, metric outputs, warnings. Re-running with the same manifest must reproduce metrics within tolerance (naive/ARIMA exactly; Kronos within a stated tolerance given sampling). |

## 4. Non-goals (v0)
Multi-asset or cross-sectional ranking; fine-tuning; GPU; custom customer models (v0.2 candidate: "bring predictions CSV"); auth, billing, multi-tenancy; live data feeds; live or paper trading; any buy/sell recommendation.

## 5. Report language rules (compliance-by-design)
- Allowed: "Model X's 5-bar directional accuracy was 51.2% (95% CI 47–55%), not significantly different from 50%."
- Forbidden: "buy", "sell", "signal", "target price", "expected profit", "recommend", forward-looking return claims.
- Mandatory footer: research evaluation of a forecasting model on historical data supplied by the customer; not investment advice; past simulated performance does not indicate future results; costs and fills are assumptions.

## 6. Data handling (concierge)
- Customer data is stored on an encrypted volume, used only for that job, and deleted within 30 days of delivery unless the customer asks otherwise (*policy to confirm in pilot agreement*).
- No customer data in git, logs, sample reports or marketing.
- Report shared via an expiring link or email attachment. No public URLs.

## 7. Acceptance criteria for v0 (testable)
1. `quanteval run --csv data.csv --horizon 5 --out out/` completes on a 2,000-row daily CSV on CPU, producing `report.html`, `report.pdf`, `manifest.json`.
2. Invalid CSVs (unsorted, duplicate, high<low, negative price) fail with explicit, line-referenced errors (unit tests).
3. Future-shift negative control is detected (test).
4. Naive and ARIMA metrics are bit-for-bit reproducible from the manifest. Kronos metrics are reproducible within the documented tolerance with a fixed seed.
5. Backtest is suppressed with a reason when < 30 trades.
6. Report contains none of the forbidden words (automated lint test).
7. Measured wall time and compute cost per report recorded in the manifest.
8. Sample report generated **only from actual executions** on synthetic or redistributable public data.

## 8. Metrics to track during concierge
Report turnaround time; founder labour hours per report; compute cost per report; customer follow-up questions; customer-perceived value (post-delivery 3-question survey); repeat requests.

## Unverified assumptions
SLA ≤ 3 business days; 50 MB limit; default 50 origins and 5 Kronos samples fit CPU time budgets; customers can supply clean OHLCV CSVs; 30-trade validity threshold suitable (heuristic, not a statistical guarantee).

## Status
Spec: Completed (draft). Implementation: Unimplemented (see first-task-summary.md Milestone 1).
