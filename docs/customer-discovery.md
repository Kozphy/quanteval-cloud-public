# Customer Discovery Plan — QuantEval Cloud

Version 0.1 · 2026-10-10 (Asia/Taipei) · Companion docs: `commercial-feasibility.md`, `competitive-landscape.md`, `first-task-summary.md` (15 customer categories), `pricing-experiments.md`, `go-to-market-30-days.md`, `paid-pilot-proposal.md`.

> **Nothing in this document is evidence of demand.** No interviews have been held, no prospect has been contacted, and no message has been sent. Every persona attribute below is a **hypothesis** to be confirmed or killed in discovery calls. Every outreach step needs the founder's explicit approval of the recipient list and the exact text before anything is sent.

## Status
| Item | Status |
|---|---|
| Personas (hypotheses) | Completed (draft) |
| Discovery question bank, scorecard | Completed (draft) |
| Outreach copy, LinkedIn campaign, GitHub strategy | Completed (draft, **not sent**) |
| Prospect list (60 qualified, see GTM week 1) | Unimplemented |
| Interviews | **Blocked**: needs founder approval to contact anyone; 0 held |
| Sample report to show prospects | Unimplemented (depends on Milestone 1 actual run) |

---

## 1. Personas (all fields are hypotheses)

Confidence key: **L** = guess from desk research only; **M** = supported by a cited public signal. No field is **H** yet because no interviews exist.

### Persona 1 — Independent quant researcher ("Ian")
| Field | Hypothesis | Conf. | How to validate |
|---|---|---|---|
| Who | Solo or 2-person researcher; ex-industry or self-taught; may publish research (Substack, GitHub, X) or trade own capital | L | Ask role and income source of research |
| Jobs to be done | "When a new financial foundation model (Kronos, Chronos, TimesFM) appears, I want to know quickly whether it beats my baselines on my instruments, so I don't waste weeks integrating hype." Secondary: "credible evidence I can show my audience." | M — public Kronos evaluation issues exist (https://github.com/shiyu-coder/Kronos/issues/354 , https://github.com/shiyu-coder/Kronos/issues/375) | Q1–Q4 |
| Current workflow | Clone model repo → adapt example notebook → ad-hoc train/test split → eyeball charts → maybe a quick backtest in a personal framework | L | Q3, Q5 |
| Time spent evaluating a new model | 1–3 days per model (author estimate, see `competitive-landscape.md`; **unmeasured**) | L | Q4 (ask for the last real instance) |
| Existing alternatives | DIY notebooks, QuantConnect research, community blog posts and GitHub issues, LLM coding assistants | M (alternatives exist; usage unknown) | Q6 |
| Pain severity (1–5) | 2–3: annoying but solvable alone | L | Scorecard "pain" |
| Budget owner | Self (personal card) | L | Q12 |
| Willingness to pay | Low: perhaps US$0–79 one-off; more likely to want a free sample or open notebook | L | Q13–Q14 (past spending, not hypothetical) |
| Purchase objections | "I can do it myself"; "Your baselines aren't my baselines"; "I won't upload my data"; price | L | Q15, objection log |
| Acquisition channels | GitHub issues and discussions on TSFM repos, r/algotrading-style communities, X/Twitter quant community, Hacker News "Show HN" for an open notebook | L | Track source of every inbound |
| Role in plan | **Feedback and credibility, not primary revenue.** Good for problem interviews and open-notebook reach. | — | — |

### Persona 2 — Small fintech or algorithmic trading startup ("Sofia, CTO / Head of Research")
| Field | Hypothesis | Conf. | How to validate |
|---|---|---|---|
| Who | Seed–Series A, 3–30 staff, 1–5 quants/ML engineers; crypto, FX/CFD, equities analytics, or trading-tool vendor | L | Q1 |
| Jobs to be done | "Decide within a sprint whether to adopt a TSFM in our product/research stack, with evidence I can show my CEO, investors, or a partner." "Get an outside sanity check because my team is too small to build an evaluation harness properly." | L | Q2, Q7 |
| Current workflow | An engineer spends part of a sprint on a notebook comparison; results live in Slack/Notion; methodology varies each time; leakage checks often missing (hypothesis) | L | Q3, Q5, Q8 |
| Time spent | 3–10 engineer-days per serious model evaluation (**assumption**) | L | Q4 |
| Alternatives | Internal notebook; Nixtla `cross_validation`; QuantConnect/LEAN; hiring a freelancer; not evaluating at all | M (tools exist) | Q6 |
| Pain severity | 3–4 when a product or fundraising decision depends on the answer; 1–2 otherwise | L | Q7, Q9 |
| Budget owner | CTO or founder/CEO; tooling budget on company card | L | Q12 |
| WTP | US$149–499 for a one-off report or pilot; US$49–149/mo only if they evaluate models repeatedly | L | Q13, Q14, price test in `pricing-experiments.md` |
| Objections | Data confidentiality; "we'd rather build it ourselves"; vendor is a solo founder in Taiwan (continuity, invoicing); PayPal/wire invoicing friction; report seen as generic | L | Q15 |
| Channels | LinkedIn (CTO/Head of Quant titles), founder communities, GitHub (their public repos using TSFMs), warm intros | L | Track source |
| Role in plan | **Primary target for the first paid pilots (US$399).** | — | — |

### Persona 3 — Financial ML engineering team ("Marcus, ML lead at asset manager, broker, or data vendor")
| Field | Hypothesis | Conf. | How to validate |
|---|---|---|---|
| Who | ML/quant team of 5–50 inside a larger financial or data company | L | Q1 |
| Jobs to be done | "Produce reproducible, auditable evidence for a model-risk or architecture review before adopting an external model." "Benchmark vendor/open models against our internal models with a standard protocol." | L | Q2, Q8 |
| Current workflow | Internal evaluation framework + model-risk documentation; formal review cycles | L | Q3 |
| Time spent | Weeks per model including documentation (**assumption**) | L | Q4 |
| Alternatives | Internal platform; big consultancies; internal model-validation group | L | Q6 |
| Pain severity | Potentially high (documentation burden), but they may already have tools | L | Q7 |
| Budget owner | Head of Quant / ML / Model Risk; procurement involved | L | Q12 |
| WTP | Could be highest, but purchasing needs vendor onboarding, security questionnaire, contract | L | Q12, Q15 |
| Objections | Vendor risk assessment; data cannot leave premises; no SOC 2; solo founder; legal review of terms | L | Q15 |
| Channels | LinkedIn, conference talks, technical blog/case study, warm intros | L | Track source |
| Role in plan | **Learning and pipeline building; unlikely to close in 30 days** for a solo founder. Possible "bring your own predictions" or on-prem CLI variant later. | — | — |

**Explicitly excluded:** retail traders seeking signals or "which stock will go up" (regulatory risk, see `legal-and-licensing-checklist.md` §5; also not a B2B budget).

---

## 2. Discovery question bank (15 questions)

Rules: ask about **past behaviour**, not hypotheticals; never pitch before question 11; don't mention prices until asked or until Q13–Q14; record verbatim quotes. Based on the general "talk about their life, not your idea" interviewing approach (practice, not a cited statistic).

| # | Question | Purpose | Good signal |
|---|---|---|---|
| 1 | "Tell me about your role and what forecasting or trading-research work your team does today." | Context, persona fit | Works with OHLCV forecasting models |
| 2 | "When was the last time you evaluated a new forecasting model, such as a time-series foundation model? Walk me through what happened." | Real recent instance | Specific instance within ~6 months |
| 3 | "What steps did you take, from getting the data to making a decision?" | Current workflow | Multi-step, manual |
| 4 | "Roughly how many hours or days did that take, and who did the work?" | Time cost | ≥ 2 person-days |
| 5 | "How did you set up the train/test split and check for look-ahead or leakage?" | Rigor gap | Uncertain or ad hoc answer |
| 6 | "What tools, libraries, or services did you use? Did you consider anything else?" | Alternatives | Names DIY stack; no dedicated tool |
| 7 | "What happened as a result of that evaluation? What decision did it feed into?" | Stakes | Product, client, or funding decision |
| 8 | "Who else needed to see or trust the results? What did they ask for?" | Audience for report; independence value | Investor, client, committee, manager |
| 9 | "What was the hardest or most frustrating part?" | Pain | Unprompted mention of leakage, baselines, costs, reproducibility |
| 10 | "How often does a model evaluation like this come up? When is the next one?" | Frequency → subscription vs one-off | Monthly or more; a dated next instance |
| 11 | "Have you ever paid for anything to help with model evaluation or validation: tools, data, contractors?" | Past spending | Yes, with an amount |
| 12 | "If you wanted to buy a tool or service for this, who would approve it and how does that usually work?" | Budget owner, process | Card purchase or simple PO |
| 13 | *(After showing the sample report)* "Which parts would you actually use? Which would you ignore?" | Value per section | Points at leakage checks, baselines, reproducibility |
| 14 | "What would you compare this to when deciding whether it's worth it?" | Reference price without leading | Engineer-days, contractor rates |
| 15 | "What would stop you from sending us a dataset next week?" | Objections | Concrete, solvable objections (NDA, data format) |

Closing ask (commitment test, not a question): "Would you like to try this on one of your datasets as a paid pilot at US$399?" or, for Persona 1, "Can I send you the open notebook and get your critique?" Record the answer exactly.

---

## 3. Structured interview scorecard

Fill one per call within 24 h. Store in a private sheet (no customer data in git). Score 0–3 per row.

| Dimension | 0 | 1 | 2 | 3 | Weight |
|---|---|---|---|---|---|
| Recent instance of the problem | None | > 12 months ago | 6–12 months | < 6 months, described in detail | 2 |
| Frequency | Never again | Yearly | Quarterly | Monthly or more | 2 |
| Time cost of current workflow | < 0.5 day | 0.5–2 days | 2–5 days | > 5 person-days | 1 |
| Rigor gap (leakage, baselines, costs) | Has robust internal framework | Minor gaps | Clear gaps admitted | Didn't know about the gaps | 1 |
| Stakes / audience | Curiosity | Personal decision | Team decision | Client, investor, or committee decision | 2 |
| Budget and authority | No budget | Personal money only | Budget exists, needs approval | Interviewee can pay this month | 2 |
| Past spending on similar tools/services | Never | Free tools only | Small paid tools | Paid contractors or vendors | 1 |
| Commitment at close | Declined | "Send me info" | Agreed to demo or data-sharing call | Agreed to paid pilot or to send data | 3 |
| Regulatory fit | Wants signals or advice → disqualify | Retail | Professional individual | B2B entity | gate |

Total = Σ score × weight (max 42). **Interpretation thresholds (hypotheses):** ≥ 28 → hot, offer pilot; 18–27 → nurture with the open notebook; < 18 → learning only. A "Regulatory fit = 0" is an automatic disqualification regardless of score.

Also record: persona, category # (1–15 from `first-task-summary.md`), source channel, verbatim pain quote, objections, price reaction (exact words), next step and date.

---

## 4. Outreach message variations (drafts; **not sent**)

Placeholders in `{braces}`. Each needs founder approval of recipient and final text. Never imply prior relationship, never claim customers or results that don't exist, and never promise trading performance.

### Variation A — Problem-first (Persona 2, LinkedIn or public business email)
> Subject: How do you check whether a time-series foundation model is worth adopting?
>
> Hi {first_name}, I'm Zixsa, an independent quant/ML engineer in Taiwan. I'm researching how small fintech and trading teams decide whether models like Kronos, Chronos, or TimesFM are worth adopting. Public community tests (e.g. https://github.com/shiyu-coder/Kronos/issues/354) suggest simple baselines are often hard to beat, which makes evaluation tricky.
>
> I'm not selling anything on this call. Would you have 20 minutes in the next two weeks to tell me how your team handled the last model evaluation? Happy to share what I learn from other teams (anonymised).
>
> {cal_link}

### Variation B — Artifact-first (after the sample report exists from an actual run)
> Hi {first_name}, I built a reproducible benchmark report that compares Kronos-mini with naive and ARIMA baselines using chronological walk-forward, leakage checks, and cost-sensitivity analysis. The sample uses synthetic data: {sample_report_link}.
>
> I'd value 20 minutes of critique from someone who evaluates forecasting models for real. What's missing, what's wrong, and what would make it useful to your team? No pitch unless you ask.

### Variation C — Peer/technical (Persona 1, GitHub contributors or researchers; only via a channel they publish for contact)
> Hi {first_name}, I read your evaluation of {model} in {public_link}; the {specific detail} was useful. I'm working on an open, reproducible evaluation protocol for financial TSFMs (walk-forward with embargo, pretraining-cutoff check, naive/ARIMA baselines). Would you be willing to review the notebook, or have a 15-minute chat about how you ran yours? Credit in the changelog if you'd like it.

Avoid: "AI that beats the market", "profitable", "signals", "alpha", ticker-specific predictions, fake urgency, and mass-identical blasts.

---

## 5. LinkedIn outreach campaign (plan; not started)

| Element | Plan |
|---|---|
| Goal | 15 discovery conversations within the 30-day window (target, not forecast) |
| Profile prep | Headline describes evaluation work (e.g. "Reproducible evaluation for financial forecasting models"); featured section links to the sample report and open notebook once they exist. Founder edits and publishes. **Approval needed.** |
| Target list | 60 people across categories 1–5, 8, 9, 11 (see `first-task-summary.md` §3); titles: CTO, Head of Research, Head of Quant, ML Lead, Founding Engineer. Qualification criteria from that doc. Built manually from public profiles; **no scraping tools** (LinkedIn's User Agreement restricts automated scraping; *unverified detail, check current terms*). |
| Cadence | 30 personalised connection requests in week 2 (per brief), 10/day max; no automation tools. LinkedIn's exact weekly invitation limit is not published officially (*unverified*), so stay well below anything flagged. |
| Sequence | Day 0: connection note (≤ 300 characters, Variation A, shortened). Day 3 after acceptance: full Variation A or B message. Day 10: one follow-up with a single useful item (e.g. one leakage pitfall). Then stop. |
| Content support | 2 posts per week from week 1: (1) "How we check for look-ahead leakage in foundation-model forecasts" (methods, synthetic data); (2) "What public community tests say about Kronos vs naive baselines" (citing issues #354, #375; no new performance claims of our own unless from actual runs). Founder approves each post. |
| Tracking | Private sheet: name, category, sent date, accepted, replied, call booked, scorecard total, next step. Only rows for messages **actually sent**. |
| Metrics | Acceptance rate, reply rate, call-booked rate, scorecard ≥ 28 rate. No benchmarks claimed; we compare against our own targets only. |
| Cost | US$0 (no Premium or Sales Navigator unless approved; price not sourced). |

---

## 6. GitHub community engagement strategy

Principle: **be useful in public first; never spam issues with product links.**

1. **Publish an open evaluation notebook/repo** (MIT, synthetic data plus a script users run on their own data) showing the protocol: walk-forward with embargo, pretraining-cutoff flag, naive/ARIMA baselines, directional accuracy with CIs. Results only from actual runs. Publishing needs founder approval (push).
2. **Participate in existing evaluation threads** in Kronos (e.g. #354, #375, #204 on training cutoff), Chronos (https://github.com/amazon-science/chronos-forecasting), and TimesFM (https://github.com/google-research/timesfm) issues/discussions **only where we add technical substance**: a reproducible script, a methodology note, a corrected leakage check. No product links unless someone asks for a tool; then link the open repo, not a sales page. Each comment drafted here and posted by the founder after approval.
3. **Contribute upstream** where genuinely useful (e.g. a docs PR clarifying CPU inference, a multi-step evaluation example). Respect each project's CONTRIBUTING guidelines.
4. **Respectful contact:** only contact individuals who publish a contact channel (profile email, website) and whose public work is directly relevant; reference their specific work (Variation C). No bulk email harvesting from commit metadata.
5. **Measure:** stars/forks on the open repo, issues opened by others, inbound messages, and how many discovery calls cite GitHub as source.
6. **Guardrails:** no named-ticker forecast posts; no "Kronos is bad/good" headlines; state limitations and the synthetic-data caveat everywhere.

---

## 7. Paid pilot handoff
Prospects scoring ≥ 28 receive `paid-pilot-proposal.md` (US$399 placeholder, PayPal invoice or wire). The proposal is not sent until the lawyer review item in `legal-and-licensing-checklist.md` §7 is resolved or the founder explicitly accepts that risk.

## Unverified assumptions
1. The three personas exist in reachable numbers through LinkedIn and GitHub.
2. Persona 2 has both the pain and a card-level budget of US$149–499.
3. Persona 3 cannot buy within 30 days (procurement friction).
4. Independence and rigor are valued enough to beat DIY.
5. Time-cost figures (1–3 days DIY; 3–10 engineer-days for startups) are author estimates, not measurements.
6. The scorecard weights and the ≥ 28 "hot" threshold are heuristics to recalibrate after the first 5 calls.
7. LinkedIn invitation limits and scraping rules: exact current terms not verified.
