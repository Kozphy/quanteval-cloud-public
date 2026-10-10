# Paid Pilot Proposal — Template

> **Internal header (delete before sending).** Template v0.1, 2026-10-10. Status: **Draft — not sent to anyone.** Sections marked ⚠️ LAWYER REVIEW must be reviewed by a Taiwan-qualified lawyer before use (see `legal-and-licensing-checklist.md` §7 and `launch-risk-register.md` R1, R4). Price is a hypothesis from `pricing-experiments.md` (Offer D). Do not attach testimonials, logos, or performance claims; none exist. Fill `{placeholders}`; each send needs founder approval.

---

# Foundation-Model Reality Check — Team Pilot Proposal

**Prepared for:** {Customer legal name} ("Customer"), attn. {Name, Title}
**Prepared by:** {Founder legal name / entity name}, {city}, Taiwan ("Provider")
**Date:** {YYYY-MM-DD} · **Proposal valid until:** {date + 14 days} · **Reference:** {QE-PILOT-###}

## 1. Purpose
Customer wants independent, reproducible evidence of how a financial time-series forecasting model (Kronos-mini, an open-source MIT-licensed model, by default) performs against simple baselines on Customer's own historical market data. This pilot produces that evidence in a standard, documented format so Customer's team can decide what further research is warranted.

## 2. Scope
| Item | Included |
|---|---|
| Instruments | Up to **5** instruments, one OHLCV series each, supplied by Customer as CSV |
| Bar frequency | One frequency per instrument (e.g. daily, hourly) |
| Forecast horizons | Up to 3 per instrument (e.g. 1, 5, 20 bars) |
| Models compared | Kronos-mini (pinned public weights) vs. naive (last value) and ARIMA baselines |
| Validation protocol | Chronological expanding-window walk-forward with embargo; no shuffling; flag for evaluation windows that overlap the model's documented pretraining period |
| Metrics | MAE, RMSE, MASE, directional accuracy with 95 % confidence intervals, Diebold–Mariano test vs. naive, inference latency (p50/p95) and hardware used |
| Research backtest (optional, Customer may opt out) | Historical simulation of a simple model-derived rule with ≥ 1-bar execution delay and Customer-specified transaction-cost assumptions, with a cost-sensitivity table; omitted with a stated reason when validity checks fail (e.g. fewer than 30 trades) |
| Data-quality and leakage checks | Automated checks with plain-English warnings |
| Iterations | **2** report iterations (e.g. a second run after Customer fixes data or changes horizons) |
| Review call | One **45-minute** results walkthrough by video call |
| Methodology appendix | Written description of protocol, assumptions, and limitations |

**Out of scope:** model training or fine-tuning; Customer's proprietary models (may be quoted separately); live data feeds; live or paper trading; integration work; any recommendation about buying, selling, or holding any security or instrument.

## 3. Deliverables
1. Per-instrument benchmark report in **HTML and PDF**.
2. A cross-instrument summary page.
3. `manifest.json` per run (input file hash, configuration, code version, model revisions, seeds, hardware, wall-clock times) so results can be reproduced.
4. Methodology and limitations appendix.
5. 45-minute review call.

## 4. Timeline (business days, Taipei time)
| Step | When |
|---|---|
| Kick-off call (15 min) and data format confirmation | Day 0 |
| Customer delivers CSV files | Day 0–3 |
| Data validation feedback to Customer | Within 1 business day of receipt |
| Iteration 1 reports delivered | Within {3} business days after valid data |
| Customer feedback / changes | Up to 5 business days |
| Iteration 2 reports delivered | Within {3} business days after feedback |
| Review call | Scheduled within 5 business days after iteration 2 |
| Pilot closes | {Day 15–21} |

## 5. Price and payment
- **Fixed fee: US${399}** for the scope above (placeholder; final price agreed in writing).
- Payment: {100 % on signature | 50 % on signature, 50 % on delivery of iteration 1} by **PayPal invoice** or **bank wire** (details on invoice). Bank charges on wires are borne by the sender unless agreed otherwise.
- Taxes: {to be confirmed with accountant}. ⚠️
- **Refund:** if Provider cannot produce the reports because of a fault in Provider's tooling, Provider refunds the unearned fee in full. No refund is due because a model performs poorly; showing that is a legitimate pilot outcome.

## 6. Customer responsibilities
- Supply data that Customer has the right to share and to have processed for this purpose, in the agreed CSV format.
- Specify transaction-cost assumptions if the research backtest is included (otherwise the documented default is used and labelled as such).
- Nominate one technical contact.
- **Make all investment, trading, and business decisions independently.** Customer is solely responsible for any use of the reports.

## 7. Data handling
| Topic | Commitment |
|---|---|
| Transfer | Via {expiring private upload link / encrypted email attachment}; no public URLs |
| Storage | Encrypted storage controlled by Provider; access limited to Provider |
| Use | Only to perform this pilot; never used to train models; never shared |
| Third parties | Compute may run on {Provider's machines / named cloud provider, e.g. Google Cloud Run, Modal, Cloudflare R2}; list confirmed at kick-off |
| Retention | Customer input files deleted within **30 days** after pilot close unless Customer requests earlier deletion or a longer retention in writing; reports retained {90 days} for support, then deleted |
| Logs, marketing | No Customer data or results in logs, code repositories, sample reports, or marketing. Any case study requires Customer's separate written permission |
| Confidentiality | Mutual confidentiality; NDA available on request ⚠️ LAWYER REVIEW |
| Personal data | Only business contact details; processed under applicable privacy law (Taiwan PDPA; GDPR where applicable) ⚠️ LAWYER REVIEW |

## 8. What this pilot is NOT
- **Not investment advice.** The reports evaluate statistical properties of forecasting models on historical data supplied by Customer. They contain no recommendation to buy, sell, or hold any security, currency, commodity, or other instrument, and no target prices.
- **No profitability claims.** Historical and simulated results do not indicate future results. Transaction costs, slippage, and fills in any research backtest are assumptions.
- **No trading.** Provider does not place trades, connect to brokers, manage money, or provide signals.
- **No fiduciary or advisory relationship** is created.
- **No guarantee** that any model will perform as it did in the evaluation.
- Not a regulatory, audit, or model-risk sign-off.

## 9. Intellectual property
- Customer owns its input data. Customer receives a perpetual, non-exclusive licence to use the delivered reports internally.
- Provider retains ownership of its software, templates, and methodology.
- Open-source components retain their licences (e.g. Kronos, MIT); notices provided on request.
⚠️ LAWYER REVIEW

## 10. Limitation of liability — ⚠️ PLACEHOLDER, LAWYER REVIEW REQUIRED BEFORE USE
> {Placeholder only — not drafted by a lawyer. Intended concept for counsel to review: Provider's total liability limited to the fees paid under this pilot; no liability for indirect, consequential, or trading losses; Customer's sole responsibility for decisions based on the reports; carve-outs as required by applicable law.}

## 11. Governing law and disputes — ⚠️ LAWYER REVIEW
{Governing law and venue to be confirmed by counsel.}

## 12. Acceptance
By signing (or by written email acceptance referencing {QE-PILOT-###}), the parties agree to this proposal {and the attached Pilot Terms ⚠️}.

| | Customer | Provider |
|---|---|---|
| Name | | |
| Title | | |
| Signature | | |
| Date | | |

---

### Internal checklist before sending (delete before sending)
- [ ] Lawyer has reviewed §§ 7, 9, 10, 11 and the "not investment advice" wording (or founder has explicitly accepted the risk in writing).
- [ ] Price, payment split, and timeline filled in and consistent with `pricing-experiments.md`.
- [ ] Prospect qualified (scorecard ≥ 28, regulatory fit ≠ 0) per `customer-discovery.md`.
- [ ] Sample report shown was produced by an actual run.
- [ ] Founder approved recipient and final text.

## Unverified assumptions
1. Turnaround of 3 business days per iteration is achievable (depends on M1 runtime and labour).
2. B2B customers accept PayPal invoice or wire.
3. 30/90-day retention windows are acceptable to customers and compliant (lawyer).
4. The "not investment advice" framing is sufficient under SITCA (lawyer).
