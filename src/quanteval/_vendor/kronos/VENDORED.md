# Vendored: Kronos model code

- Upstream: https://github.com/shiyu-coder/Kronos
- Commit: 67b630e (2026-04-13)
- Files: `model/__init__.py`, `model/kronos.py`, `model/module.py`
- License: MIT, Copyright (c) 2025 ShiYu (see `LICENSE` in this directory)
- Local modification: `kronos.py` import changed from `from model.module import *` to the
  relative `from .module import *` so the code works as a sub-package, and the
  `sys.path.append("../")` line is commented out. No other changes.
- Weights are NOT vendored; they are downloaded from Hugging Face at pinned revisions
  (see `quanteval/models/kronos.py`).
