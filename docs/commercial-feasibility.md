# Commercial Feasibility — Stage 0

Date: 2026-10-10. Scope: can a solo founder in Taiwan legally and economically sell a financial-model evaluation report to international B2B buyers for under US$100/month in costs? Companion docs: `repository-audit.md`, `legal-and-licensing-checklist.md`, `competitive-landscape.md`.

> Not legal or tax advice. No regulatory approval is claimed. No customer interviews have happened yet, so every demand statement below is a **hypothesis**.

## Verdict (provisional)
**Conditionally feasible. Proceed to customer validation, not to SaaS build.**
- Licensing: ✅ green-amber. Kronos code and all public weights are MIT; core deps are BSD/Apache/MIT. Residual risk: weights were trained on vendor-licensed data the authors cannot share.
- Payments from Taiwan: ✅ workable, with caveats. Stripe isn't available; Paddle (MoR) supports Taiwan sellers but its AUP bans financial advice, trading signals and pure human services, so get explicit pre-approval. Use PayPal invoice or bank wire for concierge pilots.
- Regulatory: ⚠️ amber. Taiwan SITCA Art. 4 defines paid "analysis, opinions or recommendations" on securities broadly, and Art. 107 carries criminal penalties. Mitigate through product design (evaluate models, never recommend securities), B2B-only, and a lawyer review before the first paid pilot.
- Demand: ❓ unknown. Public GitHub issues show people *are* independently evaluating Kronos. That's a signal of interest, not of willingness to pay.
- DIY threat: 🔴 high. Every ingredient is free and permissively licensed.

## 1. Kronos source and model licenses
| Asset | License | Commercial use | Notes |
|---|---|---|---|
| Kronos code (github.com/shiyu-coder/Kronos @ 67b630e) | MIT | Yes | Keep notice |
| Kronos-mini (HF rev f4e6869), Tokenizer-2k (rev 26966d0) | MIT (model card) | Yes | Not gated |
| Kronos-small / base / Tokenizer-base | MIT | Yes | |
| Kronos-large | unreleased | — | Can't be offered |
| Pretraining data | Vendor-licensed (WIND, Tsanghi, Binance…), not shared | n/a | Provenance can't be audited; issue #100 |

CPU feasibility: Kronos-mini has 4.1M params (measured 4,108,032) plus a 3.96M-param tokenizer and a 2048 context (README). In an informal smoke run on this box (4 CPU threads) one 24-step forecast took ~0.3–0.6 s (context 256–512). CPU-only, scale-to-zero inference looks plausible; a full walk-forward report's cost is **unmeasured** and is the first thing Milestone 1 must measure.

## 2. Dependency commercial compatibility
Fine: torch, numpy, pandas, scipy, statsmodels, scikit-learn, plotly, matplotlib, Jinja2, WeasyPrint, pyarrow (see checklist). Avoid as dependencies: backtrader and FinTSB (GPL-3.0), vectorbt (Commons Clause "no right to Sell").

## 3. Taiwan-compatible payment options (ranked for this business)
| Rank | Option | Use for | Why | Key risk | Source |
|---|---|---|---|---|---|
| 1 | **PayPal Business invoice** (+ bank wire for ≥US$500) | Concierge pilots (Offers A, D) | Available in Taiwan; invoices for services; withdraw via E.SUN | 4.40% + US$0.30 cross-border fee; not MoR (founder handles tax) | https://www.paypalobjects.com/marketing/ua/pdf/TW/en/tw-en-merchant-fees-28-may-2026.pdf |
| 2 | **Paddle** (MoR) | Self-serve subscriptions (Offers B, C) once software-delivered | Supports Taiwan sellers; handles global VAT; 5% + 50¢; payout by wire/Payoneer, US$100 min | AUP bans investment advice/signals, regulated financial products, and pure human services. Needs pre-approval | https://www.paddle.com/pricing ; https://www.paddle.com/help/start/intro-to-paddle/what-am-i-not-allowed-to-sell-on-paddle |
| 3 | Gumroad | One-off digital "sample/methodology pack" | TWD bank payout, min NT$800 | Not designed for B2B SaaS; fee level unverified | https://gumroad.com/help/article/13-getting-paid |
| 4 | Lemon Squeezy | — (not recommended now) | Taiwan bank payouts supported | Bans services; migrating merchants to Stripe Managed Payments, which doesn't support Taiwan | https://docs.lemonsqueezy.com/help/getting-started/supported-countries ; https://www.lemonsqueezy.com/blog/2026-update |
| 5 | ECPay / NewebPay | Taiwan domestic B2B only | Local cards; ECPay takes foreign cards in TWD | Needs a TW business registration; no foreign VAT handling | https://www.ecpay.com.tw/Business/payment_fees?type=p |
| — | Stripe | Not available | Taiwan isn't a supported country | US LLC route adds cost and complexity; defer | https://stripe.com/global |

**Recommendation:** collect the first US$1,000 through PayPal invoices or bank wire under a signed pilot agreement. Apply to Paddle in parallel (with approval) using a software-first product description, so subscriptions are ready if demand appears.

## 4. Regulatory boundary (summary; details in checklist)
- **Taiwan:** SITCA Art. 4 and Art. 107 (https://law.moj.gov.tw/ENG/LawClass/LawAll.aspx?pcode=G0400121). Main risk: a paid report that a regulator reads as "analysis or recommendations on trading securities". Mitigations: evaluate the customer's *model* on the customer's *data*; no buy/sell language; no named-ticker forecasts published; B2B/professional only; no live trading; lawyer opinion before revenue.
- **US:** publisher exclusion (*Lowe v. SEC*, 472 U.S. 181) covers impersonal, bona fide publications. Our report is personalised to a client's model. We rely instead on the argument that it isn't advice about securities at all (**unverified**).
- **Biggest legal risk:** a Taiwan SITCA characterisation of the paid backtest section ("trading utility"). Mitigations: allow switching the backtest section off, label it as research simulation, and get counsel review.

## 5. Customer segments with budget and urgency (hypotheses, unvalidated)
| Segment | Urgent problem (hypothesis) | Budget owner | Budget signal | Confidence |
|---|---|---|---|---|
| Small fintech / algo-trading startups evaluating TSFMs | Must decide quickly whether Kronos/Chronos/TimesFM is worth integrating; no in-house eval protocol | CTO / Head of Research | Tooling spend of tens to hundreds of US$/mo is common (*assumption*) | Medium-low |
| Financial ML teams at asset managers, brokers, data vendors | Model-risk/validation evidence for new models; independent review | Head of Quant / Model Risk | Larger budgets but long procurement (*assumption*) | Low for a solo founder in 30 days |
| Independent quant researchers / prop traders | Want to know if a hyped model works on their instruments | Self | Low WTP, price-sensitive (*assumption*) | Low for revenue, high for feedback |
| TSFM/model builders (startups, academics) | Need credible third-party benchmark for their model's finance performance | Founder / PI | Marketing or grant budget (*assumption*) | Unknown; worth testing |
| Data vendors / alt-data providers | Show their data improves forecasts | Product / Sales | Sales-enablement budget (*assumption*) | Unknown |

## 6. Competition and DIY (summary)
See `competitive-landscape.md`. Prospects **can** reproduce this themselves. The paid wedge must be standardised rigour, independence and speed. Validate that wedge before building.

## 7. Unit-economics sketch (estimates only)
- Direct compute per report: expected under US$1 on CPU (*estimate*). To be measured in Milestone 1.
- Founder labour per concierge report: 2–6 h initially (*estimate*). This is the dominant cost.
- At Offer A US$149 with 4.4% + US$0.30 PayPal fee → ~US$142 net per report before labour (arithmetic on the cited fee).
- First US$1,000: e.g. 2 team pilots at US$399 + 2 reports at US$149 = US$1,096 gross. **This is a target, not a forecast.**

## 8. Go / no-go gates for this stage
Proceed past concierge only if Stage 9 thresholds are met (15 genuine discovery calls, ≥3 pilot/demo requests, ≥2 paying pilots, ≥1 repeat signal, measured positive contribution margin).

## Unverified assumptions
1. Target buyers will pay for an independent report rather than DIY.
2. A model-evaluation report is outside SITCA "securities investment consulting".
3. Paddle approves the product under its AUP.
4. Report compute stays under US$1 on CPU.
5. Founder labour per report is 2–6 h.
6. B2B buyers accept PayPal or wire invoicing from an individual or small Taiwan entity.
7. Kronos MIT weights carry no enforceable upstream vendor claims.

## Status
- Completed: license audit, dependency review, payment-provider research, regulatory desk research, competitive desk research.
- Blocked: legal opinion (requires a paid lawyer, which needs the founder's approval to spend); customer validation (requires outreach approval).
- Unimplemented: Paddle pre-approval inquiry, pilot agreement drafting, entity decision.
