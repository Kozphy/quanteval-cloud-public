# Launch Risk Register — QuantEval Cloud

Version 0.1 · 2026-10-10 (Asia/Taipei) · Review weekly during the 30-day plan. Companion docs: `legal-and-licensing-checklist.md`, `commercial-feasibility.md`, `technical-architecture.md`, `unit-economics.md`.

Scales: **Likelihood** L (low) / M / H; **Impact** L / M / H. Ratings are the author's judgement, not measured probabilities. **Owner:** F = founder; Eng = engineering (founder or agent); Law = Taiwan lawyer (not yet engaged); Acct = accountant (not yet engaged).
Status labels: **Open** (no mitigation in place) · **Mitigating** (work underway) · **Mitigated** (control exists and verified) · **Accepted** (founder explicitly accepts).

> Not legal advice. No regulatory approval is claimed.

## Status of this document
Completed (draft). No risk is marked Mitigated unless a control is verified in this repo. Legal items are **Blocked** on lawyer engagement (needs founder approval to spend).

## Register

| ID | Category | Risk | L | I | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|
| R1 | Legal / regulatory | Taiwan SITCA Art. 4/107: a paid report is characterised as "securities investment consulting" (analysis/recommendations for compensation); criminal penalties (https://law.moj.gov.tw/ENG/LawClass/LawAll.aspx?pcode=G0400121) | M | H | Evaluate the customer's model, not securities; no buy/sell language (CI lint); backtest switchable off and labelled research simulation; B2B only; no published ticker forecasts; **lawyer opinion before first paid pilot** | F + Law | Blocked (lawyer not engaged) |
| R2 | Legal / regulatory | Futures Trading Act (futures consulting) relevant for FX/CFD/futures data — not reviewed | L–M | H | Include in lawyer questions; until then, scope pilots to customer-supplied data with no recommendation language | F + Law | Open |
| R3 | Legal / regulatory | Foreign regimes (US Advisers Act, EU, etc.) — reliance on "not advice about securities" reading is unverified | L | M | Professional-only customers; terms say no advice/no fiduciary; seek counsel if a US/EU customer requests personalised trading guidance | F + Law | Open |
| R4 | Legal / contract | No signed ToS/pilot agreement; liability cap placeholder unreviewed | H (today) | H | `paid-pilot-proposal.md` template; lawyer review of agreement, liability cap, governing law | F + Law | Mitigating (template drafted) |
| R5 | Licensing | Kronos MIT weights trained on vendor data whose terms may not have allowed derived-weight release | L | M | Download from HF at pinned revision, don't redistribute; model-swap path (Chronos/TimesFM Apache-2.0); takedown clause | Eng | Mitigating |
| R6 | Licensing | GPL / Commons Clause dependency enters codebase (backtrader, FinTSB, vectorbt) | M | M | License gate in CI; THIRD_PARTY_NOTICES | Eng | Open (gate is in M1 acceptance criteria; not verified here) |
| R7 | Licensing / data | Sample report or marketing uses data whose terms forbid redistribution (exchange/vendor/yfinance) | M | M | Synthetic data for all public material; aggregate metrics only; no Kronos repo sample data | Eng | Mitigating |
| R8 | Licensing / IP | EvalForge (proprietary) / dashboard (no LICENSE) code reused without founder→company assignment if an entity is formed | L | M | Written IP assignment at incorporation | F + Law | Open |
| R9 | Payment | Stripe unavailable in Taiwan; PayPal fees 4.4 % + US$0.30; not MoR (founder handles tax) | H (certain) | M | PayPal invoice / wire for A/D; price includes fees | F | Accepted (for pilots) |
| R10 | Payment | Paddle rejects or later suspends account under AUP (financial advice, signals, human services) | M | H (for B/C) | Software-first description; pre-approval inquiry before building checkout; keep `PaymentProvider` abstraction | F | Open (inquiry not sent; needs approval) |
| R11 | Payment / tax | Tax treatment of cross-border B2B services in Taiwan unknown; invoicing as individual vs company | M | M | Accountant consult; entity decision | F + Acct | Open |
| R12 | Payment | Chargeback/dispute on PayPal after report delivered | L | M | Signed scope + acceptance step; deliver via logged link | F | Open |
| R13 | Technical | Full walk-forward report runtime on CPU is much longer than expected → SLA/cost miss | M | M | M1 measures runtime; pre-flight cost estimate; caps on origins × samples | Eng | Mitigating (M1 in progress) |
| R14 | Technical | Kronos sampling non-determinism breaks reproducibility claims | M | M | Fixed seeds, documented tolerance, exact reproducibility for naive/ARIMA | Eng | Open (M1 test) |
| R15 | Technical | Upstream Kronos/HF changes or removal | L | M | Pin commit and HF revisions; cache weights in private image | Eng | Mitigating |
| R16 | Scientific | Leakage (look-ahead, overlapping windows) produces flattering results | M | H | Embargo; negative-control test; train/test overlap assertion; pretraining-shadow flag | Eng | Open (M1 tests) |
| R17 | Scientific | Overfitting via repeated config tweaking on the same test window (garden of forking paths) | M | H | Pre-registered config per report; report the number of configs tried; hold-out window not touched during tuning | Eng | Open |
| R18 | Scientific | Small samples → directional accuracy differences reported as meaningful | H | M | Wilson CIs, binomial and DM tests; "not significant" language; ≥ 30-trade gate for backtests | Eng | Open (M1) |
| R19 | Scientific / marketing | Misleading claims ("Kronos wins/loses", "profitable") in reports, posts, landing page | M | H | Forbidden-words lint; no claims beyond actual runs; limitations section; founder approval of all public copy | F | Mitigating |
| R20 | Scientific | Pretraining contamination: evaluation window inside model's training period inflates results | H | M | Release-date / cutoff guard (Kronos cutoff Feb 2024 per issue #204); separate post-release metrics | Eng | Open (M1) |
| R21 | Security | Customer dataset leak (email attachments, logs, shared links) | M | H | Encrypted volume; expiring links; no data in logs/git; 30-day deletion; NDA option | F + Eng | Open |
| R22 | Security | Cross-tenant access once multi-tenant (Stage 6) | L (not built) | H | RLS + org_id from token; tenant isolation test suite as release blocker | Eng | Open (future) |
| R23 | Security | Secrets committed to repo | L | H | gitleaks in CI/pre-commit; `.env` gitignored | Eng | Open (audit found only placeholders) |
| R24 | Security | Malicious CSV (CSV injection, oversized, malformed) | M | M | Strict parser, size/row caps, no formula evaluation, fuzz tests | Eng | Open (M1 validation tests) |
| R25 | Demand | Prospects prefer DIY with free OSS / LLM-generated harnesses | H | H | Discovery calls test independence/rigour wedge; kill thresholds in `pricing-experiments.md` | F | Open |
| R26 | Demand | Target buyers unreachable or unresponsive (low reply rates) | M | H | Multi-channel (LinkedIn, GitHub, warm intros); content-led credibility | F | Open |
| R27 | Demand | Kronos hype fades; buyers stop caring about TSFMs | M | M | Model-agnostic protocol (Chronos, TimesFM, "bring your own predictions") | F | Open |
| R28 | Demand / trust | Buyers distrust a solo vendor in Taiwan (continuity, invoicing, security questionnaires) | M | M | Transparent methodology, reproducible manifests, small low-risk pilot scope | F | Open |
| R29 | Founder capacity | Concierge labour > 4.7 h/report makes Offer A unprofitable at L_rate US$30 (`unit-economics.md` §5) | M | M | Time log; automate slowest steps; raise price | F | Open |
| R30 | Founder capacity | Solo founder splits time across market-data pipeline, QuantEval build, sales → nothing ships | H | H | 30-day plan focused on one sample report + 30 conversations; defer Stage 3 | F | Open |
| R31 | Founder capacity | Illness / unavailability delays customer delivery | L | M | SLA with buffer; status updates; refund policy | F | Accepted |
| R32 | Reputation | Public critique of a model's authors in GitHub threads perceived as hostile or self-promotional | M | M | Technical, reproducible, courteous contributions only; no product links unless asked | F | Open |

## Top 5 to act on first
1. **R1/R4** — engage a Taiwan lawyer (needs spend approval) before the first paid pilot.
2. **R25** — run discovery before building beyond M1.
3. **R16/R18/R20** — make leakage, statistics, and contamination guards part of M1 acceptance (already in criteria).
4. **R30** — keep scope to M1 + discovery for 30 days.
5. **R10** — draft (not send) the Paddle pre-approval inquiry for founder review.

## Unverified assumptions
1. Likelihood/impact ratings are judgement calls, not data.
2. Lawyer and accountant availability and cost unknown.
3. Kronos training cutoff (Feb 2024) taken from a maintainer comment in issue #204, not a formal model card.
