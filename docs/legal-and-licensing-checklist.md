# Legal and Licensing Checklist

> **Not legal, tax or regulatory advice.** This is a founder working checklist built from public sources on 2026-10-10. Nothing here is regulatory approval or a legal opinion. Before taking payment, have a Taiwan-qualified lawyer and accountant review the items marked ⚠️.

Status legend: **Completed** (checked against a cited source) · **Blocked** · **Unimplemented** (to do) · ⚠️ needs professional review

## 1. Model and code licenses

| Item | Finding | Source | Status |
|---|---|---|---|
| Kronos code | MIT License, © 2025 ShiYu. Commercial use, modification and SaaS hosting allowed; keep copyright + license notice. | `LICENSE` in https://github.com/shiyu-coder/Kronos ; GitHub API reports `mit` | Completed |
| Kronos-mini weights | HF model card `license: mit`, not gated. Revision used: `f4e68697d9d5aed55cef5c96aabc3376bcad9f81` | https://huggingface.co/NeoQuasar/Kronos-mini | Completed |
| Kronos-Tokenizer-2k weights | MIT, not gated. Rev `26966d0035065a0cae0ebad7af8ece35bc1fb51c` | https://huggingface.co/NeoQuasar/Kronos-Tokenizer-2k | Completed |
| Kronos-small / base, Tokenizer-base | MIT, not gated | https://huggingface.co/NeoQuasar/Kronos-small , /Kronos-base , /Kronos-Tokenizer-base | Completed |
| Kronos-large | Not released; cannot be offered | Kronos README model zoo | Completed |
| Non-commercial clauses | None found in code license or HF cards | as above | Completed |
| Kronos pretraining data | From licensed vendors (WIND, Tsanghi, Binance, etc.); not redistributable; authors cannot share | https://github.com/shiyu-coder/Kronos/issues/100#issuecomment-3310349963 | Completed (finding) ⚠️ |
| Residual risk: weights trained on vendor data | The MIT grant comes from the authors. Whether their vendor agreements permitted releasing derived weights is unknown. MIT gives no warranty or indemnity. Treat as low-to-moderate, unquantified risk. Mitigation: don't redistribute weights yourself (download from HF at runtime), keep a model-swap path (Chronos/TimesFM are Apache-2.0), add a takedown clause to ToS. | inference | ⚠️ Unverified |
| Kronos sample data in repo | HK Alibaba 5-min CSV, regression CSVs, example JSON. Provenance not stated. **Do not reuse.** | repo tree | Completed |
| Attribution | Ship `THIRD_PARTY_NOTICES` with the MIT texts for Kronos plus the deps below; cite the paper (arXiv 2508.02739) in reports | — | Unimplemented |

## 2. Dependency licenses (installed versions in audit venv, via pip-licenses)

| Package | License | Commercial SaaS OK? |
|---|---|---|
| torch 2.14.1 | BSD-style / Apache-2.0 mix | Yes |
| numpy 2.5.3, pandas 2.2.2, scipy 1.18.1, scikit-learn 1.9.1 | BSD-3 (numpy: BSD-3 + 0BSD/MIT/Zlib/CC0 parts) | Yes |
| statsmodels 0.15.0 (ARIMA) | BSD-3 | Yes |
| einops, safetensors (Apache-2.0), huggingface_hub (Apache-2.0) | MIT / Apache-2.0 | Yes |
| matplotlib 3.9.3 | PSF-style (matplotlib license) | Yes |
| plotly 7.1.0 | MIT | Yes |
| Jinja2 | BSD | Yes |
| WeasyPrint 70.0 (PDF) | BSD | Yes. Transitive `pyphen` is GPL/LGPL/MPL tri-licensed; elect MPL-1.1. ⚠️ confirm |
| pyarrow | Apache-2.0 | Yes |
| tqdm | MIT + MPL-2.0 | Yes (MPL file-level copyleft only on modified tqdm files) |

Avoid as runtime dependencies in a closed SaaS without review: **backtrader (GPL-3.0)**, **FinTSB (GPL-3.0)**, **vectorbt (Apache-2.0 + Commons Clause: "does not grant ... the right to Sell")**, nautilus_trader (LGPL-3.0, generally OK if unmodified and dynamically linked ⚠️). Sources: GitHub license metadata and https://raw.githubusercontent.com/polakowo/vectorbt/master/LICENSE.md . **Status: Completed (check), Unimplemented (automated license gate in CI).**

## 3. Founder's own repositories
- ForexTrader-public, Market-Data-Platform: MIT, sole author. Reuse OK.
- ai-quant-strategy-dashboard: **no LICENSE file**. Sole author, so private reuse is OK; add a license before others can legally reuse it. Unimplemented.
- EvalForge: proprietary, © Kozphy. Owner reuse OK. If a company is formed, sign an IP assignment or license from founder to company. ⚠️ Unimplemented.

## 4. Data
- MVP uses only customer-uploaded CSVs and **public or synthetic** sample data. Customers must warrant they have the rights to upload and process their data (ToS clause). Unimplemented.
- Sample report data: generate it synthetically, or use a source whose terms allow redistribution of derived charts. Exchange and vendor terms (Binance, Yahoo/yfinance, TWSE, Polygon, Alpha Vantage) restrict redistribution in different ways and have **not been reviewed**. ⚠️ Default to synthetic data plus aggregate metrics only. Unimplemented.
- No Bloomberg data or credentials anywhere in the product. Completed (audit).
- Personal data: B2B contact details only. Taiwan Personal Data Protection Act and GDPR (if EU customers) apply: privacy notice, retention, deletion. ⚠️ Unimplemented.

## 5. Regulatory boundary: software evaluation vs investment advice

### Taiwan
- Securities Investment Trust and Consulting Act (SITCA) **Art. 4**: "securities investment consulting" means providing analysis, opinions, or recommendations on investment in or trading of securities, securities-related products, or other FSC-approved items **for compensation**. It requires FSC permission. **Art. 107**: operating it without permission can bring up to 5 years' imprisonment and a NT$1M–50M criminal fine. Source: https://law.moj.gov.tw/ENG/LawClass/LawAll.aspx?pcode=G0400121 . Completed (text retrieved).
- FSC FinTech FAQ (search summary, not fully read): a pure technology provider to licensed institutions that does not face investors or provide advisory or trading services generally does not need a securities license, while software that delivers recommendations or signals for a fee to investors may. Source: https://www.fsc.gov.tw/websitedowndoc?file=chfsc%2F202210031521410.pdf&filedisplay=%E7%9B%A3%E7%90%86%E9%96%80%E8%A8%BAFAQ%E7%AC%AC%E5%85%AD%E7%89%88.pdf ⚠️ Read in full and confirm.
- Futures Trading Act (futures consulting) may matter for FX/CFD/futures data. **Not reviewed.** ⚠️

### United States
- Investment Advisers Act §202(a)(11)(D) publisher exclusion as read in *Lowe v. SEC*, 472 U.S. 181 (1985): impersonal, bona fide, general and regular circulation. https://supreme.justia.com/cases/federal/us/472/181/ . Personalised advice is not covered. A model-evaluation report on a customer's own model and data is arguably not "advice as to the value of securities" at all. That reading is **unverified**. ⚠️

### Design guardrails (product rules, not legal conclusions)
1. Evaluate **models**, not securities. Reports state statistical properties of a forecasting model on the customer's data. No buy/sell/hold language, no "signals", no target prices, no ranking of securities to buy.
2. The backtest is labelled "historical research simulation of a model-derived rule, gross and net of assumed costs", with mandatory disclaimers. No forward-looking performance claims.
3. Customers are B2B or professional (researchers, fintech teams). No retail marketing and no "make money trading" positioning.
4. No live trading, broker connections, order routing or custody.
5. Don't publish recurring forecasts for named tickers (e.g., "Kronos says TSMC up next week"). That is the most likely way to slide into advice.
6. ToS: no investment advice; no fiduciary relationship; customer is responsible for decisions; data rights warranty; limitation of liability; governing law. ⚠️ Lawyer drafts or reviews.

## 6. Payments and tax
- **Stripe**: not available for Taiwan-based businesses; Taiwan is absent from https://stripe.com/global (third-party confirmations dated 2026-10). The workaround is a US LLC + EIN + US bank (cost and time not budgeted). Completed (finding).
- **Paddle** (MoR, 5% + 50¢; https://www.paddle.com/pricing): Taiwan sellers are not on the unsupported list (https://www.paddle.com/help/start/intro-to-paddle/which-countries-are-supported-by-paddle); payout by wire or Payoneer, US$100 minimum (https://www.paddle.com/help/manage/get-paid/when-and-how-do-i-get-paid). ⚠️ **The AUP prohibits "Investment or financial advice, including trading signals and strategies", "regulated financial products in any jurisdiction", and pure human or consulting services** (https://www.paddle.com/help/start/intro-to-paddle/what-am-i-not-allowed-to-sell-on-paddle). QuantEval must present itself as ML-evaluation software, and a hand-delivered concierge report may count as a "human service". Ask Paddle for pre-approval before relying on it.
- **Lemon Squeezy**: Taiwan is listed for bank payouts (https://docs.lemonsqueezy.com/help/getting-started/supported-countries), but it **prohibits "Services of any kind ... consulting"** (https://docs.lemonsqueezy.com/help/getting-started/prohibited-products), and the company is steering merchants to Stripe Managed Payments, which does not support Taiwan sellers (https://www.lemonsqueezy.com/blog/2026-update). This is a platform-continuity risk.
- **Gumroad**: Taiwan bank payouts in TWD, minimum NT$800 (https://gumroad.com/help/article/13-getting-paid). It suits one-off digital report sales; its fee (~10% per third-party comparison) is unverified on the official site.
- **PayPal Business (Taiwan)**: cross-border commercial receipts 4.40% + fixed fee (USD 0.30); withdrawal to Taiwan via E.SUN (https://www.paypalobjects.com/marketing/ua/pdf/TW/en/tw-en-merchant-fees-28-may-2026.pdf). It works for invoicing paid pilots (a service), and **it is not a merchant of record**, so the founder handles tax.
- **ECPay / NewebPay**: Taiwan gateways. ECPay accepts foreign cards but settles in TWD (https://www.ecpay.com.tw/Business/payment_fees?type=p). They need a Taiwan business registration and are not MoR for foreign VAT. Suitable for Taiwan B2B customers only.
- **B2B bank wire** (SWIFT to a Taiwan bank) for pilots ≥ US$500: lowest fee, manual. Unverified on fees.
- Tax: Taiwan income tax on the founder or entity; whether cross-border B2B services are zero-rated for Taiwan VAT is **unverified**. Foreign B2C digital VAT/GST is handled by an MoR (Paddle) and **not** by PayPal or wire. ⚠️ Accountant.

## 7. Open items before first paid pilot
| # | Item | Owner | Status |
|---|---|---|---|
| 1 | Decide entity: sole proprietorship vs Taiwan company (affects ECPay, invoices, Paddle KYC) | Founder + accountant | Unimplemented ⚠️ |
| 2 | Lawyer review of SITCA boundary for "model evaluation report" positioning | Taiwan lawyer | Unimplemented ⚠️ |
| 3 | ToS, Privacy Policy, Pilot Agreement (with no-advice, data-rights, liability cap, deletion clauses) | Lawyer / template | Unimplemented ⚠️ |
| 4 | Paddle pre-approval inquiry (product description + sample report) | Founder | Unimplemented (do not send without approval) |
| 5 | THIRD_PARTY_NOTICES + license gate in CI (block GPL/Commons Clause deps) | Eng | Unimplemented |
| 6 | Sample data: synthetic generator + documented provenance | Eng | Unimplemented |

## Unverified assumptions
- MIT weights are legally clean for commercial hosting despite vendor-sourced training data.
- An evaluation report about a customer's model on the customer's data is not "securities investment consulting" under SITCA Art. 4.
- Paddle will accept a model-evaluation SaaS under its AUP.
- PayPal invoices are acceptable to target B2B buyers' procurement.
- Fees cited from third-party pages (Gumroad ~10%, Lemon Squeezy fee stack) match the providers' current official pricing.
