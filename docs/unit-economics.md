# Unit Economics — QuantEval Cloud

Version 0.1 · 2026-10-10 (Asia/Taipei) · Companion docs: `commercial-feasibility.md` §7, `first-task-summary.md` §4 (budget), `pricing-experiments.md`, `technical-architecture.md`.

> **Runtime and compute cost per report are now measured** (Milestone 1, 2026-10-10; §2). Order volumes, labour hours and the labour rate are still **illustrative inputs, not measurements or forecasts.** Prices are from official pages fetched 2026-10-10 (links inline). No revenue exists.

## Status
| Item | Status |
|---|---|
| Formulas and cost model | Completed |
| Sourced unit prices (compute, storage, payments) | Completed (re-check before any spend) |
| Measured runtime and compute cost per report | **Completed** (M1 actual runs, §2; source `reports/README.md`) |
| Measured founder labour per report | Unimplemented (log during first pilots) |
| Tax / FX / bank-wire fees | Unimplemented (accountant; unverified) |

---

## 1. Formulas

Per job (one report run on one instrument and one config):

```
C_compute = T_wall × (vCPU × p_vcpu_s + GiB × p_gib_s)          # serverless container
C_storage = (S_in + S_out) × retention_months × p_storage_gb_mo   # usually 0 inside free tier
C_egress  = S_out × p_egress_gb                                   # 0 on R2; check worker provider
C_job     = C_compute + C_storage + C_egress
```

Per order (what the customer buys):

```
Fee_pay   = price × fee_pct + fee_fixed
C_labour  = H_founder × L_rate                                     # concierge only, explicitly a cost
COGS      = Σ C_job + Fee_pay + C_labour (+ refunds reserve)
CM        = price − COGS                                           # contribution margin
GM%       = (price − COGS) / price
GM%_exLab = (price − Σ C_job − Fee_pay) / price                     # cash margin, labour excluded
```

Business level:

```
F                 = fixed monthly cost (domain, optional VPS, contingency, …)
Break-even orders = ceil(F / CM_avg)
Labour capacity   = H_available_per_month / H_per_order            # caps concierge throughput
```

## 2. Measured runtime (Milestone 1, actual runs)

Source: `reports/README.md` §Runtime and cost and the run manifests (code commit `d1295a5`, 2026-10-10). Hardware: this box, Intel Xeon vCPU, 8 logical CPUs, torch 2.14.1+cpu, **4 threads**. Config: horizon 5, lookback 256, step 5, seed 42, Kronos-mini sample_count 5, ARIMA(1,1,1) refit every origin, research backtest on; models naive, drift, ARIMA, Kronos-mini.

| Run | Rows / origins | In-process total (manifest) | of which walk-forward | Process wall incl. Python start | Kronos-mini p50 / p95 per forecast | ARIMA p50 / p95 | Peak RSS |
|---|---|---|---|---|---|---|---|
| Synthetic daily (run1, with PDF) | 800 / 134 | **35.80 s** | 30.23 s | **37.73 s** | 166.1 / 277.9 ms | 31.5 / 79.7 ms | **0.52 GiB** |
| Synthetic run2 (reproduce, no PDF) | 800 / 134 | 37.08 s | — | 39.03 s | — | — | — |

Artefact sizes (measured): input CSV ≈ 68 KB; report bundle (HTML + PDF + manifest + predictions + charts) ≈ 1.7–1.9 MB per run.

**Compute cost per report** (Cloud Run Jobs Tier-1 list price; sizing **assumed** 4 vCPU + 1 GiB, enough for the 0.52 GiB peak → US$0.000074 per second):
| Basis | Synthetic |
|---|---|
| Raw (in-process time × rate) | ≈ US$0.0026 |
| **With Cloud Run Jobs 1-minute minimum billing (used in all tables below)** | **US$0.0044** |

A sample on public crypto data exists privately pending data-licensing review.

**Free-tier capacity** (240,000 vCPU-s/month; memory 450,000 GiB-s is not binding at 1 GiB):
- ≈ **1,600 reports/month** at the measured ~37.5 s process wall (240,000 ÷ (4 × 37.5)), as stated in `reports/README.md`.
- ≈ **1,000 reports/month** if every job is billed at the 1-minute minimum (240,000 ÷ 240). Use this more conservative figure for planning.
- Both are arithmetic, not measured on Cloud Run.

**Excluded from these figures:** container cold start and image pull; first download of Kronos weights (~16 MB model + ~16 MB tokenizer; to be baked into the image per `technical-architecture.md`); founder labour (dominant cost, still the US$30/h placeholder below); retries and failed runs; storage and egress (§4).

**Caveats:** one machine, single-instrument daily series with ≤ 800 rows; Cloud Run vCPUs may be faster or slower than this box; larger files (more origins, longer lookback, intraday data, 3 horizons) scale runtime roughly with origins × samples. The Offer D pilot (5 instruments × 2 iterations) is modelled as 10 such jobs. Re-measure when inputs grow beyond ~1,000 rows or when a multi-horizon config is used.

## 3. Unit prices (sourced)

| Item | Price | Source |
|---|---|---|
| Cloud Run Jobs CPU | US$0.000018 / vCPU-s (Tier 1 incl. Taiwan asia-east1) | https://cloud.google.com/run/pricing |
| Cloud Run Jobs memory | US$0.000002 / GiB-s | same |
| Cloud Run Jobs free tier | 240,000 vCPU-s + 450,000 GiB-s / month per billing account | same |
| Modal CPU | US$0.0000131 / physical core-s (= 2 vCPU); memory US$0.00000222 / GiB-s; Starter includes US$30/month compute | https://modal.com/pricing |
| Cloudflare R2 Standard | US$0.015 / GB-month; free 10 GB-month; **egress free** | https://developers.cloudflare.com/r2/pricing/ |
| Neon Postgres Free | 100 CU-hours/project, 1 GB storage, 5 GB egress; Launch US$0.106/CU-h, US$0.35/GB-mo | https://neon.com/pricing |
| GitHub Actions | Public repos free on standard runners; private: 2,000 min/month on Free, then US$0.006/min Linux 2-core | https://docs.github.com/en/billing/concepts/product-billing/github-actions |
| Cloudflare Pages | Free plan: 500 builds/month | https://developers.cloudflare.com/pages/platform/limits/ |
| PayPal (Taiwan, cross-border commercial) | 4.40 % + US$0.30 | https://www.paypalobjects.com/marketing/ua/pdf/TW/en/tw-en-merchant-fees-28-may-2026.pdf |
| Paddle (MoR) | 5 % + US$0.50 | https://www.paddle.com/pricing |
| GCP internet egress (if worker on Cloud Run writes to R2) | **Not fetched (unverified)**; 1 GiB/month free within North America per the Cloud Run page | https://cloud.google.com/run/pricing |

## 4. Cost per job (measured runtime)

| Platform (assumed sizing) | Billing basis | Cost per report |
|---|---|---|
| Cloud Run Jobs, 4 vCPU / 1 GiB | 1-minute minimum | **US$0.0044** (used below) |
| Cloud Run Jobs, 4 vCPU / 1 GiB | raw measured seconds | ≈ US$0.0026 |
| Modal, 2 physical cores (= 4 vCPU) / 1 GiB, US$0.00002842/s | 37.73 s measured wall + default 60 s idle keep-alive (load time not measured) | ≈ US$0.0028 (arithmetic) |

Storage per job (measured sizes): ≈ 0.07 MB input + ≈ 1.9 MB report bundle ≈ **2 MB/job**. 100 jobs ≈ 0.2 GB, far inside R2's 10 GB free tier; R2 egress is free. If the worker runs on Cloud Run and uploads to R2, GCP egress applies (rate unverified; ≈ 2 MB/job is negligible). On Modal, Starter includes 1 TiB/month egress.

**Conclusion (now measured):** compute is **under half a US cent per report** and storage is effectively free at current volumes. Payment fees (~US$7 per US$149 report) are ~1,500× the compute cost, and **founder labour is the dominant cost.** The `commercial-feasibility.md` estimate (< US$1 compute per report) is confirmed for this config.

## 5. Margin per offer

Labour rate `L_rate` = **US$30/hour (assumption: founder opportunity cost placeholder; founder to set)**. Labour hours are hypotheses from `commercial-feasibility.md` (2–6 h per report) and for the pilot from its scope (5 instruments, 2 iterations, 45-min call). Compute uses the **measured US$0.0044 per job** (Cloud Run 1-minute minimum, before free tier; §2). Inside the free tier it is US$0.

### Concierge offers (PayPal invoice)
| Offer | Price | Payment fee | Net after fee | Jobs | Compute | Labour h (hyp.) | Labour cost | **CM** | GM% ex-labour |
|---|---|---|---|---|---|---|---|---|---|
| A — report (low labour) | 149 | 6.86 | 142.14 | 1 | 0.0044 | 2 | 60 | **82.14** | 95.4 % |
| A — report (mid) | 149 | 6.86 | 142.14 | 1 | 0.0044 | 4 | 120 | **22.14** | 95.4 % |
| A — report (high) | 149 | 6.86 | 142.14 | 1 | 0.0044 | 6 | 180 | **−37.86** | 95.4 % |
| D — team pilot (low) | 399 | 17.86 | 381.14 | 10 | 0.044 | 6 | 180 | **201.10** | 95.5 % |
| D — team pilot (high) | 399 | 17.86 | 381.14 | 10 | 0.044 | 12 | 360 | **21.10** | 95.5 % |

GM% ex-labour is now limited almost entirely by the payment fee (PayPal 4.4 % + US$0.30), not compute.

Break-even labour for Offer A at L_rate US$30: 142.14 / 30 ≈ **4.7 hours**. Above that, a US$149 report loses money on a fully-loaded basis. **Delivery must be ≤ 4 h per report or the price must rise** — a key metric for `pricing-experiments.md`.

Range edges (Offer A US$79–199, Offer D US$199–499): PayPal net is US$75.22 / 189.94 (A) and US$189.94 / 476.74 (D).

### Self-serve subscriptions (Paddle, only after pre-approval and automation)
Job quotas are hypotheses from `pricing-experiments.md`; support labour is an assumption.

| Offer | Price/mo | Paddle fee | Net | Jobs/mo (cap) | Compute at cap | Support h (assumption) | **CM** | GM% ex-labour |
|---|---|---|---|---|---|---|---|---|
| B — Starter | 49 | 2.95 | 46.05 | 5 | 0.022 | 0.5 | **31.03** | 93.9 % |
| C — Pro | 149 | 7.95 | 141.05 | 25 | 0.11 | 1.0 | **110.94** | 94.6 % |

Paddle payout minimum is US$100 (`legal-and-licensing-checklist.md` §6), which delays cash at low volume.

## 6. Fixed costs and break-even
Fixed monthly cost F from `first-task-summary.md` §4: **≈ US$16 (no VPS) to ≈ US$23 (with Hetzner)**, of which US$15 is contingency. Lawyer review is a one-off, **unpriced** cost requiring approval.

| CM per order used | Orders to cover F = US$23 |
|---|---|
| Cash basis (labour excluded), Offer A net ≈ US$142 | **1** |
| Offer A fully loaded at 4 h (US$22.14) | **2** |
| Offer D fully loaded at 6 h (US$201.10) | **1** |

Lawyer fee break-even: `ceil(lawyer_fee / CM)`. Example only: a fee of X would need X / 142 cash-basis reports. **X is unknown.**

First-US$1,000 target path (from `commercial-feasibility.md`, a target not a forecast): 2 × D + 2 × A = US$1,096 gross → US$1,046.56 net of PayPal fees.

## 7. 10× demand scenario (illustrative)

Baseline month (hypothesis, not a forecast): 4 Offer A reports + 1 Offer D pilot = 14 jobs. 10× = 40 reports + 10 pilots = 140 jobs.

| Metric | Baseline | 10× |
|---|---|---|
| Net revenue after PayPal fees | US$949.70 | US$9,497.00 |
| Compute, Cloud Run, measured US$0.0044/job, before free tier | US$0.06 | US$0.62 |
| Compute, Cloud Run, with free tier (≈ 1,000 jobs/month at 1-min minimum) | US$0 | US$0 |
| Storage (≈ 2 MB/job measured, 30-day retention) | ≈ 0.03 GB, inside R2 free tier | ≈ 0.28 GB, inside free tier |
| Founder labour (4 h/report, 9 h/pilot) | 25 h | **250 h** |
| Labour cost at US$30/h | US$750 | US$7,500 |

**Finding (compute now measured):** infrastructure scales almost free — even 10× demand (140 jobs) uses ~14 % of the conservative free-tier capacity; **labour does not.** At 10× demand, concierge delivery needs ~250 h/month, beyond a solo founder (assumption: ≤ 80 h/month available for sales and delivery combined, consistent with ~20 h/week in `go-to-market-30-days.md`). The 10× case therefore requires Stage 3 automation (self-serve upload → queued job → automatic report), cutting labour to review only (target ≤ 0.5 h/report, hypothesis). That is the economic trigger for building Stage 3, and only if Stage 9 demand evidence also exists.

## 8. What to measure during pilots (feeds back into this doc)
T_wall and peak memory on production-like hardware and larger/multi-horizon inputs (M1 measured only small daily series on this box); founder hours split into intake/data cleaning, run, review, call, rework; payment fees actually charged; refunds; FX loss on withdrawal (E.SUN; unverified); storage per job.

## Unverified assumptions
1. Runtime measured on this box only (§2); Cloud Run vCPU speed, cold start and weights download not measured; 4 vCPU / 1 GiB sizing is assumed.
2. L_rate US$30/h is a placeholder for founder opportunity cost.
3. Labour hours per offer (2–6 h report; 6–12 h pilot; 0.5–1 h support per subscriber).
4. Job quotas for Offers B/C.
5. Sizes measured for ≤ 800-row daily inputs only (≈ 2 MB/job); larger inputs will produce larger bundles.
6. GCP egress rate and FX/withdrawal costs not sourced.
7. Founder capacity ≤ 80 h/month for sales + delivery.
8. Prices current as of 2026-10-10; providers can change them.
