# Third-Party Notices

QuantEval (c) 2026 Kozphy. This file lists third-party components that QuantEval vendors, adapts or depends on.

## 1. Kronos (vendored model code)
- Source: https://github.com/shiyu-coder/Kronos, commit 67b630e, files `model/{__init__,kronos,module}.py`
- Location: `src/quanteval/_vendor/kronos/` (two import-path lines modified; see VENDORED.md there)
- Weights (not vendored; downloaded at runtime from Hugging Face, MIT per model cards):
  - NeoQuasar/Kronos-mini @ f4e68697d9d5aed55cef5c96aabc3376bcad9f81
  - NeoQuasar/Kronos-Tokenizer-2k @ 26966d0035065a0cae0ebad7af8ece35bc1fb51c
- Citation: Shi et al., "Kronos: A Foundation Model for the Language of Financial Markets", arXiv:2508.02739 (AAAI 2026)

```
MIT License

Copyright (c) 2025 ShiYu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 2. Founder-owned code adapted with attribution
Adapted (not copied verbatim) by the copyright holder; see the module docstrings for exact sources.
- Kozphy/ForexTraderWithBloombergAccess-public (MIT, (c) 2026 Zixsa): leakage guards, delayed-execution cost backtest, data checks, performance metrics.
- Kozphy/Market-Data-Platform-for-Analytics-Execution (MIT, (c) 2026 Zixsa): OHLCV cleaning ideas.
- Kozphy/ai-quant-strategy-dashboard ((c) 2026 Zixsa, no license file; reused by the copyright holder): naive/ARIMA baselines, forecast metrics, latency summary.
- Kozphy/EvalForge (EvalForge Proprietary License, (c) Kozphy; reused by the copyright holder): CI / evidence-manifest patterns.

## 3. Runtime dependencies (installed, not vendored)
| Package | License |
|---|---|
| numpy, pandas, scipy, statsmodels, scikit-learn (transitive), Jinja2 | BSD-3-Clause / BSD |
| torch | BSD-3-Clause-style (with Apache-2.0/MIT/BSL-1.0 components) |
| einops, PyYAML, plotly (not used at runtime), tqdm (MIT + MPL-2.0) | MIT |
| huggingface_hub, safetensors, pyarrow | Apache-2.0 |
| matplotlib | Matplotlib License (PSF-based) |
| WeasyPrint (optional PDF) | BSD-3-Clause; transitive pyphen tri-licensed GPL/LGPL/MPL, MPL-1.1 elected |

`scripts/check_licenses.py` fails CI if a GPL/AGPL (non-LGPL) or Commons Clause package is installed (allowlist with justification only).
