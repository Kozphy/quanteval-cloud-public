# Competitive Landscape

Research date: 2026-10-10. Star counts and licenses come from the GitHub API on that date. Prices are cited where a source was found; anything else is marked *unverified*. No market-size figures are claimed.

## Positioning being tested
"An independent, reproducible **evaluation report** for financial forecasting models, Kronos and other TSFMs included, on *your* OHLCV data. It covers leakage checks, chronological walk-forward against naive and ARIMA baselines, error and directional metrics, latency, and a cost-aware research backtest." It is not a trading platform, a signal service or a model vendor.

## Landscape

| Category | Examples | What they do | Overlap with QuantEval | Gap QuantEval targets | Pricing (source) |
|---|---|---|---|---|---|
| Backtesting / algo platforms | QuantConnect (LEAN, Apache-2.0, ~22k★) | Cloud backtests and live trading, data, research notebooks | High for the backtest part; users can run Kronos signals there (a public blog shows exactly this: https://jiripik.com/2026/08/31/kronos-foundation-model-validation/) | Not a forecasting-model evaluation report; no standard leakage/baseline audit; the user still writes everything | Researcher pack ~US$84/mo, seat US$10/mo (https://www.quantconnect.com/pricing , third-party summary) |
| OSS backtesters | backtrader (GPL-3.0), vectorbt (Commons Clause), nautilus_trader (LGPL), Qlib (MIT, ~49k★) | Libraries | DIY substitute | Require assembly and expertise; no report | Free / vectorbt PRO paid (*unverified*) |
| TSFM benchmarks | GIFT-Eval (Salesforce, Apache-2.0), fev / fev-bench (AutoGluon, Apache-2.0) | Public leaderboards over many generic datasets | Model comparison methodology | Generic domains rather than the customer's own market data or finance-specific checks; no trading-cost lens | Free (https://github.com/SalesforceAIResearch/gift-eval) |
| Finance forecasting benchmarks | FinTSB (GPL-3.0, academic) | Financial TS benchmark with cost-aware backtests | Very close methodologically | Academic and static; doesn't run on customer data; GPL | Free (https://arxiv.org/html/2502.18834) |
| TSFM vendors | Nixtla TimeGPT (+ statsforecast/neuralforecast, Apache-2.0), Amazon Chronos (Apache-2.0), Google TimesFM (Apache-2.0) | Models + cross-validation tooling | Nixtla's `cross_validation` gives DIY rolling evaluation | Vendor-centric; not independent across vendors; no finance leakage/cost audit | TimeGPT on Azure consumption billing (https://www.nixtla.io/blog/timegpt-azure-marketplace); exact price *unverified* |
| ML experiment tracking | Weights & Biases, MLflow (OSS) | Logging and dashboards | Experiment history | No finance-specific evaluation logic | W&B Pro ~US$60/mo per third-party summary (https://wandb.ai/site/pricing/ — *verify*) |
| ML monitoring / eval | Evidently (Apache-2.0 OSS) | Drift and quality reports | Report format, data-quality checks | Not time-series-forecast/trading specific | Cloud plan status conflicting in sources (*unverified*) |
| Data-science competitions | Numerai, Kaggle | Crowd-sourced models on provided data | Evaluation culture | Customer can't bring their own model and data for a private audit | Free |
| RL / finance research libs | FinRL (MIT) | RL trading research | Low | — | Free |
| Community Kronos evals | GitHub issues #354, #355, #375 on Kronos; sumit-ai-ml/kronos-market-eval; blog posts | One-off reproducibility reports | **Direct evidence of demand for exactly this kind of evaluation, and of DIY capability** | One-off, not productised, not on the reader's data | Free |

## What public evidence says about Kronos (cited, not our results)
- Authors claim strong zero-shot RankIC gains (arXiv 2508.02739; AAAI 2026).
- Independent community reports, strictly post-cutoff: Kronos-mini underperforms a persistence baseline on AAPL daily (issue #354, https://github.com/shiyu-coder/Kronos/issues/354); cross-sectional IC +0.022, t=1.39, fails after costs (issue #375, https://github.com/shiyu-coder/Kronos/issues/375); training data is not public and cutoff questions remain (issues #100, #204, #265, #326).
- Implication: there is a credible "verify before you trust" use case, and our sample report must expect Kronos to **lose to naive baselines** on many datasets. That's fine. The product sells evidence, not a winning model.

## Can prospects DIY? (honest assessment)
**Yes, for most competent quants.** All ingredients are free and permissively licensed (Kronos MIT, statsmodels, Nixtla statsforecast, LEAN). A skilled researcher can assemble a walk-forward Kronos-vs-ARIMA comparison in roughly 1–3 days (*estimate, unverified*). Public blogs and issues already give templates.

Where a paid product may still win (all **hypotheses to validate in discovery**):
1. **Time and rigour bundle.** Leakage tests, pretraining-shadow / release-date checks (evaluate only after a model's training cutoff or release), embargoes, cost sensitivity and reproducibility manifests are tedious to get right every time.
2. **Independence and credibility.** A third-party report for an investment committee, a client, a fundraise, or vendor due-diligence on a model.
3. **Repeatability.** The same protocol each time a new TSFM drops (Kronos, Chronos-2, TimesFM-x), on the customer's own universe.
4. **Non-quant buyers** (fintech PMs, ML teams new to finance) who don't know the finance-specific pitfalls.

**Biggest threats**
1. DIY using free OSS and public blog protocols. This is the primary threat.
2. TSFM vendors (Nixtla, AWS, Google) adding finance evaluation templates for free.
3. QuantConnect-style platforms adding "foundation model evaluation" notebooks.
4. Commoditised LLM coding agents that can generate the harness on demand (*assumption*).

## Unverified assumptions
- Buyers value independence and a standard protocol enough to pay instead of DIY.
- There's no existing productised "financial TSFM evaluation report" service. A web search found none, but absence of results doesn't prove absence.
- Third-party pricing summaries (QuantConnect pack, W&B Pro) match current official pricing.
- The DIY time estimate (1–3 days) is the author's estimate and has not been measured.

## Status
- Completed: desk research with sources, license metadata.
- Unimplemented: hands-on trial of competitor products, pricing-page screenshots, customer validation of differentiators.
