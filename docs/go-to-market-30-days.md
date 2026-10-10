# 30-Day Go-To-Market Plan — QuantEval Cloud

Version 0.1 · 2026-10-10 (Asia/Taipei) · Companion docs: `customer-discovery.md`, `pricing-experiments.md`, `paid-pilot-proposal.md`, `stage-gate-criteria.md`, `first-task-summary.md` §5.

> **Approval gates.** Every step marked 🔒 is externally visible or costs money and requires the founder's explicit approval of the exact recipients, text, or spend **before** it happens. Nothing in this plan has been sent, published, pushed, or purchased. Outreach counts must only include messages actually sent.

## Status
| Item | Status |
|---|---|
| Plan | Completed (draft) |
| Week 1 audit (repos, licenses) | Completed (`repository-audit.md`, `legal-and-licensing-checklist.md`) |
| Sample report from an actual run | Unimplemented (Milestone 1 in progress) |
| Landing page | Unimplemented (plan below) |
| All outreach, posts, publishing | **Blocked** pending approval; 0 sent |
| Lawyer review | **Blocked** pending approval to engage and pay |

Day 1 = the day the founder approves starting GTM (date not fixed).

---

## Week 1 (Days 1–7) — Assets and readiness

| Task | Output | Gate |
|---|---|---|
| Audit technical assets and licenses | Done: audit + legal checklist | — |
| Finish Milestone 1; generate **one sample report from an actual run on synthetic data** | `report.html`, `report.pdf`, `manifest.json`; measured runtime → `unit-economics.md` §2 | Internal |
| Review sample report for compliance language (lint + manual read) | Checklist signed off | Internal |
| Draft landing page (see below) | Static site in repo | 🔒 publish |
| Buy domain (~US$11.17/yr, Cloudflare Registrar; source in `first-task-summary.md` §4) | Domain | 🔒 spend |
| Build qualified prospect list: 60 across categories 1–15 | Private sheet (not in git) | Internal |
| Prepare discovery script + scorecard (`customer-discovery.md`) | Ready | Internal |
| Draft pilot agreement + proposal (`paid-pilot-proposal.md`) | Draft | 🔒 lawyer engagement (spend) |
| Draft Paddle pre-approval inquiry and lawyer questions | Drafts | 🔒 send |
| Prepare open evaluation notebook (synthetic data, MIT) | Repo ready locally | 🔒 push/publish |
| Problem interviews with any warm contacts the founder already has | Scorecards | 🔒 each contact |

**Exit check:** sample report reproduces from its manifest; landing page draft ready; ≥ 60 qualified prospects listed.

## Week 2 (Days 8–14) — Outreach and demos

| Task | Output | Gate |
|---|---|---|
| Contact **30 qualified prospects** (LinkedIn + public business email; Variations A/B in `customer-discovery.md`) | Outreach log (sent only) | 🔒 recipient list + text |
| Publish landing page + sample report link | Live URL | 🔒 publish |
| Post 2 LinkedIn technical posts; publish open notebook to GitHub | Posts, repo | 🔒 each post / push |
| Helpful comments in Kronos/Chronos/TimesFM evaluation threads | Comments | 🔒 each comment |
| Hold short discovery calls (20–30 min); score each | Scorecards | Calls themselves need no approval once booked by the prospect |
| Demonstrate the report workflow on synthetic data (screen share) | Demo notes | — |
| Test pilot pricing verbally (E1, E2 in `pricing-experiments.md`) | Reaction log | — |

**Target (not forecast):** ≥ 8 calls booked.

## Week 3 (Days 15–21) — Pilots and learning

| Task | Output | Gate |
|---|---|---|
| Send pilot proposal to prospects who request it | Proposal | 🔒 each send; ideally after lawyer review |
| Issue PayPal invoice / wire instructions | Invoice | 🔒 each invoice |
| Deliver paid pilots if customers agree | Reports | Delivery to the customer is part of the signed scope |
| Collect structured feedback (3-question survey) | Survey results | 🔒 send survey |
| Log actual inference cost, wall time, and labour hours per report | Cost/time log | Internal |
| Improve the report based on objections (top 3) | Changelog | Internal |
| Follow-ups to week-2 non-responders (one only) | Log | 🔒 |

**Target:** ≥ 1 paid pilot.

## Week 4 (Days 22–30) — Decide

| Task | Output | Gate |
|---|---|---|
| Review demand and economics against `stage-gate-criteria.md` | Decision memo | Internal |
| Decide: continue concierge, pivot segment/offer, or start Stage 3 automation | Recorded decision | Founder |
| Publish a technical case study **only with written customer permission** | Case study | 🔒 customer permission + founder approval |
| Update `unit-economics.md` and `pricing-experiments.md` with measured data | Updated docs | Internal |
| Define next development milestone | Milestone spec | Internal |

## Landing page plan (cheap/free)

| Element | Choice | Cost | Source |
|---|---|---|---|
| Hosting | Cloudflare Pages Free (500 builds/month, 20k files) | US$0 | https://developers.cloudflare.com/pages/platform/limits/ |
| Domain | Cloudflare Registrar .com | ~US$11.17/yr from 2026-11-01 | `first-task-summary.md` §4 |
| Site | Single static HTML page (no framework needed), plus `/sample` (HTML sample report) and `/methodology` | US$0 | — |
| Call booking | Cal.com free link | US$0 | https://cal.com/pricing |
| Lead capture | Mailto + Cal.com; add a form tool only if its free tier is verified | US$0 | — |
| Analytics | Cloudflare Web Analytics (*free tier assumed; verify*) or none | US$0 | *unverified* |
| Legal pages | Privacy notice, terms, "not investment advice" disclaimer — **lawyer review** | lawyer fee | 🔒 |

Page structure (draft copy, no claims beyond evidence):
1. **Headline:** "Independent, reproducible evaluation of financial forecasting models on your data."
2. **Sub-headline:** "Kronos and other time-series foundation models vs. naive and ARIMA baselines, with walk-forward validation, leakage checks, and cost sensitivity."
3. **What you get:** report sections list; link to the synthetic sample report.
4. **Offers:** Reality Check report (US$149) and Team pilot (US$399), both hypotheses. "Invoiced via PayPal or bank wire."
5. **What this is not:** no trading signals, no investment advice, no profitability claims, no live trading.
6. **Methodology and limitations.**
7. **CTA:** "Book a 20-minute call."
8. Footer: disclaimer, privacy notice, contact.

Forbidden on the page: testimonials (none exist), customer logos, "trusted by", performance claims, ticker forecasts.

## Weekly tracking (fill with real numbers only)

| Week | Prospects listed | Messages **sent** | Replies | Calls held | Scorecard ≥ 28 | Pilot requests | Paid pilots | Revenue US$ | Labour h | Compute US$ |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | | | |
| 2 | | | | | | | | | | |
| 3 | | | | | | | | | | |
| 4 | | | | | | | | | | |

## Unverified assumptions
1. 30 personalised messages in week 2 yield ≥ 8 calls (target only).
2. A synthetic-data sample report is credible enough for technical buyers.
3. Lawyer review can be completed before week 3; otherwise the founder must decide whether to take pilots before review (risk in `launch-risk-register.md`).
4. Cloudflare Web Analytics free tier available; Cal.com free plan sufficient.
5. Founder has ~20 h/week for sales + delivery during the 30 days.
