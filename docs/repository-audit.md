# Repository Audit — Kozphy QuantEval Cloud

Audit date: 2026-10-10 (Asia/Taipei). Auditor: Grok Bot (automated, read-only).
Method: public shallow→full clones into `_audit/` (gitignored, not committed), license file review, dependency manifest review, test execution in isolated Python 3.12 venvs (uv), regex secret scan of the working tree plus a full-history scan with gitleaks v8.21.2 (redacted output).
Nothing was pushed, published or modified upstream.

## Status legend
- **Completed** — done and evidenced below
- **Blocked** — could not be done; reason given
- **Unimplemented** — deliberately out of scope for this phase

## Summary table

| Repo | HEAD (date) | License | Lang / key deps | Tests (this audit) | Secrets (full history) | Bloomberg dependency | Reuse verdict |
|---|---|---|---|---|---|---|---|
| Kozphy/ForexTraderWithBloombergAccess-public | c911ee7 (2026-09-15) | MIT (© 2026 Zixsa) | Python ≥3.11; numpy, pandas, scipy, PyYAML | **29 passed** | none found | None in public mirror (only a doc comment about ticker mapping); Bloomberg adapters live in a private repo that was **not audited** | **Reuse**: leakage guards, cost-aware backtest, data contracts, evidence/report writer |
| Kozphy/ai-quant-strategy-dashboard | ea91838 (2026-08-24) | **No LICENSE file** (all rights reserved by default; sole author Zixsa) | Python ≥3.10: numpy, pandas, scikit-learn, statsmodels, streamlit, plotly; Next.js 16 / React 19 front-end | **15 passed** | none found | None | **Reuse**: rolling-origin forecasting + baseline registry (naive/ARIMA), forecast metrics, latency p50/p95, experiment manifest. Add a LICENSE before any public reuse. |
| Kozphy/Market-Data-Platform-for-Analytics-Execution | 6503187 (2026-07-15) | MIT (© 2026 Zixsa) | Python ≥3.10: httpx, pandas, pyarrow, psycopg; Airflow, Postgres via Docker | **4 passed** (only 4 tests) | 1 gitleaks hit: `.env.example` (see below) | None | **Partial reuse**: OHLCV normalisation/cleaning, missing-bar detection, Parquet storage. Airflow/Postgres stack is too heavy for the MVP. |
| Kozphy/EvalForge | 4fcec3b (2026-10-10) | **EvalForge Proprietary License** (© 2026 Kozphy, all rights reserved) | Python: FastAPI, pydantic, scikit-learn, jsonschema, httpx, optional torch/OpenAI | **96 passed, 1 skipped** | none found (test fixtures contain obvious dummy values) | None | **Reuse patterns**: evidence bundle with SHA-256 hashes, bootstrap CIs, policy gate, report writer. Domain is LLM finance Q&A, not time-series, so reuse is structural not drop-in. Owner may relicense to self. |
| shiyu-coder/Kronos (upstream) | 67b630e (2026-04-13) | MIT (© 2025 ShiYu) | Python: torch ≥2.0, einops, huggingface_hub, safetensors, pandas | **4 passed** (`tests/test_kronos_regression.py`, CPU, needs `PYTHONPATH=.`); `finetune/qlib_test.py` errors on collection (needs qlib; not relevant) | none found | None | **Use as pinned dependency** (vendored copy of `model/` or git-pinned), not a fork. |

All four Kozphy repos have a single commit author (Zixsa / public-mirror-bot), so there are no third-party contributor IP issues for the founder reusing their own code (**Completed**, from `git shortlog`).

## Per-repo notes

### ForexTraderWithBloombergAccess-public (MIT)
- Structure: `src/forex_quant/{data,backtest,metrics,research,features,signals,regimes,policy,evidence,experiment,pipeline,control_plane,institutional}.py`, `tests/` (5 files: leakage, data contracts, research core, harness, institutional controls), `configs/` (synthetic).
- Reusable for MVP:
  - `backtest.py`: `realistic_backtest` (execution delay ≥1 bar enforced, turnover-based bps costs, liquidity cap), `assert_no_lookahead_positions`, `assert_train_oos_separation` (embargo), `inject_lookahead_leakage` (negative test helper).
  - `data.py`: `validate_golden_schema` (tz-aware timestamps, duplicates, positive close, `available_at ≥ timestamp`), `fingerprint_frame` (SHA-256 dataset fingerprint), missing-data policies.
  - `metrics.py`: Sharpe, Sortino, max drawdown, CAGR, Calmar, hit rate, exposure.
  - `evidence.py`: Markdown report + JSON artifact writer.
- Gaps: schema expects `asset`/`close`/`available_at`, not full OHLCV; needs an OHLCV adapter (high ≥ max(open,close), low ≤ min(open,close), volume ≥ 0).
- README states Bloomberg adapters and secrets are only in the private repo, synced by a force-push workflow. **The private repo was not audited (Blocked: not public / no access requested).** The MVP must not depend on it.

### ai-quant-strategy-dashboard (no license file)
- Structure: `src/quant_dashboard/{forecasting,backtest,metrics,latency,experiment,features,modeling,llm_signals}.py`, Streamlit `app.py`, plus a Next.js UI (`app/`, `components/`, uses `@vercel/analytics`).
- Reusable for MVP:
  - `forecasting.py`: rolling-origin evaluation with naive, moving average, SES, AR/MA/ARMA/ARIMA(2,1,2)/SARIMA/ETS registry; `forecast_metrics` (MAE, RMSE, MAPE).
  - `latency.py`: `benchmark_call` → p50/p95/throughput.
  - `experiment.py`: deterministic `ExperimentManifest` ID (dataset/model/code SHA).
- Gaps (important for MVP):
  - `_rolling_origin` raises `NotImplementedError` for horizon ≠ 1. Multi-step horizons must be added.
  - ARIMA is refit on every step; cost on long series is unmeasured and may be slow. Needs a refit stride.
  - No directional-accuracy metric.
- Action: add a LICENSE (e.g., keep proprietary or MIT) before public reuse; as the sole author, the founder can reuse it privately now.

### Market-Data-Platform-for-Analytics-Execution (MIT)
- Structure: ingestion (Binance), transformation (cleaning, features), storage (Parquet, Postgres), orchestration (Airflow DAG, DQ checks), quant (threshold backtester, Sharpe/MDD), streaming alerts.
- Reusable: `transformation/cleaning.py` (`normalize_ohlcv_frame`, `fill_missing_bars`, `clean_ohlcv_frame`), Parquet helpers. The DQ checks are Postgres-bound and not reusable as-is.
- Test coverage is thin (4 tests).
- **Secret finding (low severity):** `.env.example` (commit d919d38) contains a syntactically valid Airflow Fernet key `AIRFLOW__CORE__FERNET_KEY=...` and default credentials (`admin/admin`, `change_me_local_only`, `dev_webserver_secret_change_me`). These are documented placeholders for local Docker, not production credentials. Recommendation: replace the Fernet key with an empty value plus a generation command, and never reuse it anywhere real. Not copied into this project.

### EvalForge (Proprietary, © Kozphy)
- Structure: `finance_eval/` (154-item synthetic finance/accounting golden set, graders, judge, policy, evidence, report), `app/` (FastAPI control plane + operator UI), `research/`, 22 test files, Docker, CI.
- Reusable patterns: evidence bundle (`sha256_file`, manifest), `bootstrap_ci`, PASS/WARN/FAIL policy gate, report writer, async run model (relevant later for the job queue).
- The license forbids use by anyone without written permission. The copyright holder (founder) can reuse it; if QuantEval is ever incorporated as a separate legal entity, a written license/assignment from the founder to the company is needed (**Unverified assumption**: entity structure unknown).

### Kronos (MIT; upstream)
- Model zoo (README and HF cards): Kronos-mini 4.1M params, context 2048, tokenizer Kronos-Tokenizer-2k; Kronos-small 24.7M / 512; Kronos-base 102.3M / 512; Kronos-large 499.2M is **not released**.
- Measured on this audit box (count from loaded weights): Kronos-mini **4,108,032** params; Kronos-Tokenizer-2k **3,958,042** params.
- Regression tests pin `Kronos-small` and `Kronos-Tokenizer-base` HF revisions and passed on CPU (4/4, ~34 s incl. download).
- **Informal CPU smoke measurement (not a benchmark):** Kronos-mini @ revision f4e6869, tokenizer-2k @ 26966d0, torch 2.14.1+cpu, 4 threads, generic Intel Xeon vCPU, `pred_len=24`, `sample_count=1`, 3 runs each: context 256 → 0.32–0.36 s per forecast; context 512 → 0.54–0.58 s per forecast. Shows CPU-only inference is feasible; the real per-report cost must be measured in Milestone 1 with the actual walk-forward settings (many forecast origins × samples).
- Repo contains third-party market data samples (`finetune_csv/data/HK_ali_09988_kline_5min_all.csv`, 5.6 MB; `tests/data/regression_input.csv`; `examples/yuce/*.json`; `webui/prediction_results/*.json`). Provenance/licensing of these data files is not stated. **Do not reuse them in sample reports or marketing.**
- Example scripts use `akshare`/`qlib` data sources (Chinese A-share). Not needed for the MVP.
- Pretraining data: authors state it is from licensed vendors (WIND, Tsanghi, Binance, etc.) and cannot be shared (issue #100 comment: https://github.com/shiyu-coder/Kronos/issues/100#issuecomment-3310349963). Training cutoff stated as Feb 2024 inclusive, OOS from June 2024 (issue #204).

## Secret scan results (Completed)
- gitleaks full history: EvalForge 0, ForexTrader-public 0, Kronos 0, ai-quant-strategy-dashboard 0, Market-Data-Platform 1 (placeholder Fernet key in `.env.example`, above).
- Regex scan of working trees: only placeholders and test fixtures (`api_key="test-key"`, `"abc123"`).
- No `.env` files with real values committed. `.env.example` files exist in EvalForge (empty keys) and Market-Data-Platform.
- No licensed Bloomberg data or credentials found in any public repo.

## Reuse plan for the MVP (proposed, not yet implemented)
| MVP need | Source | Action |
|---|---|---|
| OHLCV schema + quality checks | ForexTrader `data.py` + MDP `cleaning.py` | Port + extend to full OHLCV invariants |
| Leakage guards / embargo | ForexTrader `backtest.py` | Port as-is + tests |
| Naive / ARIMA baselines, MAE/RMSE | dashboard `forecasting.py` | Port, add multi-step horizon, refit stride, directional accuracy |
| Latency p50/p95 | dashboard `latency.py` | Port as-is |
| Cost-aware research backtest | ForexTrader `backtest.py` + `metrics.py` | Port; single-asset mode |
| Experiment manifest + hashes | dashboard `experiment.py` + EvalForge `evidence.py` | Merge |
| Kronos-mini adapter | Kronos `model/` (MIT) | Pin commit + HF revisions; keep MIT notice |
| Report HTML/PDF | ForexTrader `evidence.py` pattern | New Jinja2 template; PDF via WeasyPrint (BSD) |

## Unverified assumptions
- The private `Kozphy/ForexTraderWithBloombergAccess` repo does not leak into the public mirror beyond what was scanned (only the public mirror was audited).
- Test pass results reflect Python 3.12 on Linux; other OS/versions not tested. The CI configs were not executed.
- The Next.js front-end of the dashboard was not built or run.
- Kronos latency numbers above come from one shared box and are not representative of production hardware.

## Status
- Completed: clone, license review, dependency review, tests for all 5 repos, secret scans, reuse mapping, Kronos-mini CPU smoke run.
- Blocked: private ForexTrader repo audit (no access, out of scope).
- Unimplemented: porting/refactoring code (Milestone 1).
