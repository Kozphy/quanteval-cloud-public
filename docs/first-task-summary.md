# First Task Summary — QuantEval Cloud

Date: 2026-10-10 (Asia/Taipei). Inputs: `repository-audit.md`, `commercial-feasibility.md`, `competitive-landscape.md`, `legal-and-licensing-checklist.md`, `mvp-prd.md`.
Rules followed: no code pushed, no outreach sent, no money spent, no customers or results invented. Numbers without a source are labelled *estimate* or *assumption*.

---

## 1. Minimum sellable offer
**"Foundation-Model Reality Check": an independent benchmark report**
- What the customer gets: Kronos-mini vs naive vs ARIMA on **their** OHLCV CSV (1 instrument, up to 3 horizons). Chronological walk-forward with embargo, release-date/pretraining-shadow check, MAE/RMSE/MASE, directional accuracy with CIs, latency, cost-sensitivity research backtest when valid, leakage and data-quality warnings, HTML + PDF + reproducibility manifest, and a 30-minute walkthrough call.
- Price hypothesis: **US$149 one-time** (inside the brief's Offer A range of US$79–199). **Team pilot US$399** (Offer D): up to 5 instruments, 2 report iterations, a 45-minute review call, and a written methodology appendix.
- Delivery: concierge, admin-triggered CLI, target ≤ 3 business days (*assumption*).
- Payment: PayPal Business invoice or bank wire against a short pilot agreement (Paddle later, after pre-approval).
- Guarantee: refund if the report can't be produced because of a tool fault (not because the model under-performs).
- Explicitly **not**: trading signals, recommendations, or a promise that any model is profitable.

## 2. Smallest implementation scope
One Python package plus a CLI. No web app, auth, billing or queue.
- `quanteval/validate.py`: OHLCV contract and quality checks (port of ForexTrader `data.py` + MDP `cleaning.py`).
- `quanteval/splits.py`: expanding walk-forward with embargo and release-date flag (port of ForexTrader leakage guards).
- `quanteval/models/{naive,arima,kronos}.py`: Kronos-mini adapter, pinned HF revisions, CPU (port of dashboard `forecasting.py`, extended to multi-step).
- `quanteval/metrics.py`: MAE, RMSE, MASE, directional accuracy and CI, DM test, latency (port of dashboard `latency.py`).
- `quanteval/backtest.py`: single-asset delayed-execution cost backtest with validity gates (port of ForexTrader `backtest.py`).
- `quanteval/report/`: Jinja2 HTML + WeasyPrint PDF + `manifest.json`.
- `tests/`: validation, leakage negative controls, reproducibility, forbidden-word lint.
- `examples/synthetic_ohlcv.py`: generates the public sample dataset (no third-party data).

## 3. First 15 customer categories and outreach qualification criteria
These are **categories to test**, not identified customers. No one has been contacted.

| # | Category | Why they might care (hypothesis) | Qualify if… |
|---|---|---|---|
| 1 | Seed–Series A algo-trading / quant fintech startups | Deciding whether to integrate TSFMs | Public eng/research team ≥ 2; mentions ML forecasting; non-sanctioned jurisdiction |
| 2 | Crypto market-making / quant trading firms (small) | Many instruments, fast model churn | Hiring ML/quant roles; uses OHLCV models |
| 3 | Robo-advisor / wealthtech ML teams | Need model-risk evidence | Has data-science team; B2B or licensed entity |
| 4 | Market-data / alt-data vendors | Prove their data improves forecasts | Sells to quants; has a "research" or "use case" page |
| 5 | TSFM / forecasting-model startups | Want third-party finance benchmark | Published model; finance claims in marketing |
| 6 | University fintech / quant labs (PIs, grant-funded) | Reproducible evaluation for papers | Recent papers on financial TSFMs; has budget line |
| 7 | Independent quant researchers selling research (Substack, etc.) | Credibility for their audience | Publishes model-based research; ≥ 1k followers |
| 8 | Prop-trading firms' research desks (small) | Screening new models cheaply | Public evidence of systematic trading; ≤ 50 staff |
| 9 | Broker / exchange innovation or data-science teams (APAC) | Evaluating AI features for clients | Has public AI initiatives; Taiwan / HK / SG / JP |
| 10 | Fintech consultancies / ML agencies serving finance | Outsource rigorous eval for their clients | Lists finance ML projects; could white-label |
| 11 | Trading-tool / charting platforms adding AI forecasts | Need evidence before shipping AI features | Announced or teasing AI forecast features |
| 12 | Family offices with in-house quants | Independent check on vendor models | Has quant hire; reachable via LinkedIn |
| 13 | Model-risk / validation consultants | Tooling to speed TS model validation | Practice includes model validation |
| 14 | Open-source contributors evaluating Kronos/Chronos on GitHub | Already doing this work manually | Opened/commented on evaluation issues (e.g., Kronos #354/#375) — **public engagement only, no scraping or spam** |
| 15 | Quant education / bootcamp providers | Teaching material on honest evaluation | Runs paid quant ML courses |

**Universal qualification criteria** (all required before outreach): business or professional context, not retail; a plausible budget owner identified; a recent public signal of interest in ML forecasting; a jurisdiction not on Paddle's unsupported list; no need for live trading or recommendations; contact through a legitimate channel (LinkedIn connection, public business email, GitHub discussion). Disqualify: retail traders seeking signals; anyone asking "which stock will go up"; requests needing licensed data we can't use.

## 4. Realistic monthly operating budget (target under US$100)
| Item | Choice | Monthly cost (USD) | Source / basis |
|---|---|---|---|
| Domain (.com) | Cloudflare Registrar | ~0.93 (US$11.17/yr from 2026-11-01) | https://domainnamewire.com/2026/10/09/time-is-running-out-com-prices-go-up-on-november-1/ ; https://www.cloudflare.com/application-services/products/registrar/buy-com-domains/ |
| Landing page | Cloudflare Pages (free) | 0 | https://developers.cloudflare.com/pages/functions/pricing/ |
| Report/file storage | Cloudflare R2 free tier (10 GB-month, free egress) | 0 | https://developers.cloudflare.com/r2/pricing/ |
| Compute (report jobs) | Run on founder machine first; then Cloud Run Jobs free tier (240k vCPU-s, 450k GiB-s/mo) | 0 (est.) | https://cloud.google.com/run/pricing |
| Optional always-on box | Hetzner CX23 (2 vCPU, 4 GB) €5.99 incl. IPv4 | ~7 (FX *estimate*) | https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/ |
| Error monitoring | Sentry Developer (free, 5k errors) | 0 | https://sentry.io/pricing/ |
| Scheduling | Cal.com free | 0 | https://cal.com/pricing |
| Payments | PayPal 4.40% + US$0.30 per cross-border receipt; Paddle 5% + 50¢ (no monthly fee) | variable only | PayPal TW fee PDF; https://www.paddle.com/pricing |
| Code hosting | GitHub (existing account) | 0 (*assumption*: current free plan suffices) | — |
| Contingency (overage, misc SaaS) | — | 15 (*estimate*) | — |
| **Total recurring** | | **≈ US$23 / month** (≈ 16 without Hetzner) | |

Not in the monthly budget (each needs explicit approval before spending): a one-off lawyer review of SITCA positioning and the pilot agreement (cost unknown, *unverified*), LinkedIn Premium or Sales Navigator (price not sourced), and a US LLC for Stripe (not recommended now).

## 5. 30-day validation plan
Every outreach step requires the founder's explicit approval of the recipients and message text before anything is sent.

| Week | Goals | Concrete outputs | Exit check |
|---|---|---|---|
| 1 (Days 1–7) | Audit ✅ (this doc set); build Milestone 1; generate **one sample report from an actual run on synthetic data**; landing page draft; discovery script; pilot agreement draft; lawyer and Paddle questions drafted | Sample report (HTML/PDF), landing page (not published without approval), prospect list of 60 across categories 1–15 with qualification notes | Sample report reproducible from manifest |
| 2 (8–14) | With approval: contact 30 qualified prospects; book discovery calls; demo the report workflow; test US$149 / US$399 pricing verbally | Outreach log (actually sent only), call notes with interview scorecard | ≥ 8 calls booked (*target*) |
| 3 (15–21) | Deliver paid pilots if any customer agrees; collect structured feedback; measure labour hours and compute cost per report; fix top objections | Pilot reports, time and cost log, objection list | ≥ 1 paid pilot (*target*) |
| 4 (22–30) | Review demand and economics against the Stage 9 gates; decide to continue concierge, pivot segment or offer, or automate; publish a technical case study only with customer permission | Decision memo, updated pricing hypotheses, next milestone | Go/no-go recorded honestly |

Leading indicators tracked: reply rate, discovery-to-demo, demo-to-paid, price objections, perceived value score, hours per report, compute US$ per report, refunds.

## 6. First incremental coding milestone — M1: "Reproducible single-asset benchmark CLI"
**Goal:** produce, from a real execution, the sample report used in sales, with no web stack.

**Acceptance criteria** (all must pass in CI on Linux, CPU only):
1. `pip install -e .` then `quanteval run --csv examples/synthetic_daily.csv --horizon 5 --out out/` produces `report.html`, `report.pdf` and `manifest.json`.
2. Validation rejects unsorted, duplicate-timestamp, `high < low`, non-positive-price and too-short files with explicit messages (≥ 8 unit tests).
3. A walk-forward split with an embargo is used; a test asserts no evaluation target index ≤ the fit window end + embargo.
4. A negative control works: injecting a 1-bar look-ahead feature/forecast triggers a leakage failure (test).
5. Models: naive, ARIMA (statsmodels) and Kronos-mini (HF revision pinned to `f4e68697…`, tokenizer `26966d0…`). Kronos runs on CPU with a fixed seed.
6. Metrics: MAE, RMSE, MASE, directional accuracy with Wilson CI, DM test vs naive, latency p50/p95, and total wall time with hardware info written to the manifest.
7. The backtest runs with ≥ 1-bar delay and a bps-cost sensitivity table, and is suppressed with a reason when < 30 trades.
8. Reproducibility: re-running from `manifest.json` reproduces naive/ARIMA metrics exactly and Kronos metrics within the documented tolerance (test).
9. A compliance lint test fails the build if the report contains forbidden terms (buy/sell/signal/recommend/target price/guaranteed).
10. `THIRD_PARTY_NOTICES` includes the Kronos MIT license, and the dependency license check blocks GPL and Commons Clause packages.
11. Measured compute time and estimated cost per report for the sample are recorded in `docs/unit-economics.md` (to be created in M1) from actual runs only.

Estimated effort: 4–6 focused days (*estimate*). Out of scope for M1: web upload, auth, billing, queue, multi-asset.

---

## Status board
| Item | Status |
|---|---|
| Repository audit | Completed |
| Commercial feasibility, competitive landscape, legal checklist | Completed (desk research; legal review **Blocked** pending founder approval to engage and pay counsel) |
| Concierge MVP spec | Completed (draft) |
| Customer discovery, outreach | **Blocked** (needs founder approval; nothing sent) |
| Payment provider setup (PayPal / Paddle) | Unimplemented (needs founder action and approval) |
| Benchmark prototype, sample report | Completed (Milestone 1; see `docs/m1-acceptance.md` and `reports/README.md`; the published sample is synthetic) |
| Remaining brief docs: `customer-discovery.md`, `technical-architecture.md`, `unit-economics.md` (runtime section pending M1), `pricing-experiments.md`, `go-to-market-30-days.md`, `launch-risk-register.md`, `paid-pilot-proposal.md`, `stage-gate-criteria.md` | Completed (draft, v0.1, 2026-10-10) |

## Unverified assumptions (consolidated)
1. Buyers will pay US$149–399 instead of DIY.
2. The report positioning stays outside SITCA "securities investment consulting" (lawyer needed).
3. Paddle accepts the product under its AUP.
4. CPU compute per report is under US$1, and founder labour is 2–6 h.
5. A 3-business-day SLA is acceptable.
6. FX conversion for the Hetzner price (€→US$).
7. GitHub free plan suffices.
