# Pricing Experiments — QuantEval Cloud

Version 0.1 · 2026-10-10 (Asia/Taipei) · Companion docs: `unit-economics.md`, `customer-discovery.md`, `stage-gate-criteria.md`, `paid-pilot-proposal.md`.

> Every price here is a **hypothesis**. No customer has seen a price yet and no revenue exists. **No unlimited plans** until per-job cost is measured (`unit-economics.md` §2) and quotas are proven safe.

## Status
| Item | Status |
|---|---|
| Offer definitions A–D (hypotheses) | Completed (draft) |
| Experiment design, metrics, thresholds | Completed (draft) |
| Running experiments | **Blocked**: needs outreach approval and a sample report from an actual M1 run |
| Paddle checkout for B/C | **Blocked**: Paddle pre-approval not requested (needs founder approval); PayPal invoice only for A/D |

---

## 1. Offers (hypotheses)

| Offer | Price hypothesis | What's included (draft) | Payment rail | Launch timing |
|---|---|---|---|---|
| **A — One-time report** ("Foundation-Model Reality Check") | **US$149 anchor**, test range US$79–199 | 1 instrument, up to 3 horizons; Kronos-mini vs naive vs ARIMA; leakage + DQ warnings; cost-sensitivity research backtest when valid; HTML + PDF + manifest; 30-min walkthrough | PayPal invoice | Week 2 (with approval) |
| **B — Starter** | US$49/month | Self-serve upload; **5 evaluation jobs/month** (hypothesis), ≤ 100k rows/job, 1 model set; email support | Paddle (after approval) | Only after Stage 3 automation **and** Stage 9 gate |
| **C — Pro** | US$149/month | **25 jobs/month** (hypothesis), ≤ 500k rows/job, multi-horizon, experiment history, priority support | Paddle (after approval) | Same as B |
| **D — Team pilot** | **US$399 anchor**, test range US$199–499 | Up to 5 instruments, 2 report iterations, 45-min review call, methodology appendix, 2–3 week window | PayPal invoice or wire | Week 2–3 (with approval) |

Rules: no "unlimited" anything; overage = buy another report (A) or upgrade; annual discounts not offered until retention is measured; refunds only for tool fault (not model under-performance), per `first-task-summary.md` §1.

## 2. Metrics (definitions)

| Metric | Definition | Source |
|---|---|---|
| Discovery-to-trial conversion | # prospects who send data for a free sample or paid pilot ÷ # discovery calls held | Scorecard sheet |
| Trial-to-paid conversion | # paid orders ÷ # prospects who received a trial/demo on their data | Invoice log |
| Average revenue per customer (ARPC) | Gross revenue ÷ paying customers (period) | Invoice log |
| Usage cost per job | Measured `C_job` (`unit-economics.md` §1) | Worker logs |
| Gross margin | (Revenue − payment fees − compute − storage − delivery labour) ÷ revenue | `unit-economics.md` |
| Customer acquisition cost (CAC) | (Paid spend + founder sales hours × L_rate) ÷ new paying customers | Time log |
| Retention / repeat | % customers with a second order (A/D) or month-2 renewal (B/C) | Invoice log |
| Refund requests | # and US$ refunded, with reason | Invoice log |
| Report completion time | Data received → report delivered (business hours) | Job log |
| Customer-perceived value | Post-delivery survey: (1) usefulness 1–5, (2) "would you pay again at this price?" Y/N, (3) "what would you remove/add?" | Survey |

## 3. Experiment design

Small numbers mean these are **directional, not statistically significant** tests. Decisions use pre-set thresholds, not p-values.

### E1 — Price anchoring in discovery (weeks 2–3)
- **Hypothesis:** Persona 2 accepts US$399 for a pilot without strong objection.
- **Method:** in qualified calls (scorecard ≥ 28), after Q13–Q14, present Offer D at US$399. Alternate the order in which A and D are mentioned by call number (odd: D first, even: A first). Record exact reaction words.
- **Sample:** all qualified calls in window (expect < 15).
- **Success:** ≥ 2 paid pilots at ≥ US$299 (matches Stage 9 gate).

### E2 — Report price point (Offer A)
- **Hypothesis:** US$149 is not the main objection.
- **Method:** quote US$149 by default. If ≥ 3 prospects in a row say price is the blocker *and* otherwise score ≥ 28, test US$99 for the next 3. If 3 consecutive accept US$149 without negotiation, test US$199 for the next 3.
- **Guardrail:** never below fully loaded break-even (≈ US$142 net ÷ labour hours; see `unit-economics.md` §5) unless explicitly framed as a design-partner discount with a written feedback commitment.

### E3 — Paid vs free first report
- **Hypothesis:** offering a free first report on synthetic or customer data does not convert better than a paid pilot with refund-on-tool-fault.
- **Method:** free sample only for Persona 1 (feedback value); Persona 2/3 get paid offers only. Compare engagement depth (follow-up questions, survey scores).

### E4 — Subscription intent (no checkout yet)
- **Hypothesis:** ≥ 30 % of paying pilot customers expect ≥ 1 new model evaluation per month (Q10).
- **Method:** ask Q10 and "if this were a monthly product with N jobs, what N would you need?" Record answers; **do not** sell B/C until automation exists.
- **Output:** job-quota calibration for B/C.

### E5 — Value metric
- **Hypothesis:** customers think in "evaluations" (model × instrument × horizon) rather than seats.
- **Method:** ask which unit they would expect to pay by; tally.

## 4. Kill / continue thresholds (end of day 30)

| Signal | Continue | Adjust | Kill or pivot |
|---|---|---|---|
| Paid pilots (D) | ≥ 2 | 1 | 0 after ≥ 15 genuine calls |
| Price objections | < 50 % of qualified calls cite price as main blocker | 50–70 % → test lower anchor or narrower scope | > 70 % and DIY cited as alternative → problem not worth paying for in this segment |
| Delivery labour (Offer A) | ≤ 4 h median | 4–6 h → automate the slowest step or raise price | > 6 h median → current price is unprofitable |
| Perceived value | Median usefulness ≥ 4/5 and ≥ 1 "would pay again" | Median 3 | Median ≤ 2 |
| Refunds | 0 | 1 | ≥ 2 (quality issue) |
| Repeat signal | ≥ 1 repeat order or explicit renewal request | Verbal interest only | None and Q10 shows "rarely" for most |

A "kill" result triggers reassessment of segment, positioning, and offer **before** building more features (brief Stage 9).

## 5. Tracking table (fill only with real events)

| Date | Prospect ID (private) | Persona | Offer quoted | Price quoted | Reaction (verbatim) | Outcome | Paid US$ | Labour h | Compute US$ | Survey |
|---|---|---|---|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — | — | — | — | — |

## Unverified assumptions
1. Prospects will tell the truth about price objections in calls.
2. Quotas of 5 and 25 jobs/month are placeholders until E4 data and M1 runtime exist.
3. US$49/US$149 subscriptions are viable only after self-serve automation; concierge labour would make B unprofitable (see `unit-economics.md` §5).
4. PayPal invoicing is acceptable to B2B buyers for A/D.
5. Paddle approval will be granted (not yet requested).
