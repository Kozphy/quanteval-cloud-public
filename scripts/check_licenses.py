"""Dependency license gate: fail on GPL/AGPL (non-LGPL) or Commons Clause licenses in the installed environment.

Usage: python scripts/check_licenses.py  (exit code 1 on violation)
Allowlist entries need a written justification.
"""

from __future__ import annotations

import importlib.metadata as md
import re
import sys

ALLOWLIST = {
    # Tri-licensed GPL-2.0+/LGPL-2.1+/MPL-1.1; we elect MPL-1.1. Transitive dependency of WeasyPrint (PDF).
    "pyphen": "tri-licensed; MPL-1.1 elected",
}

BLOCK = [r"\bA?GPL(?!\s*-?\s*compatible)", r"GNU (Affero )?General Public License", r"Commons Clause"]
LGPL = [r"\bLGPL", r"GNU Lesser General Public License", r"GNU Library"]


def license_text(dist: md.Distribution) -> str:
    meta = dist.metadata
    parts = [meta.get("License-Expression") or "", meta.get("License") or ""]
    parts += [c for c in meta.get_all("Classifier") or [] if c.startswith("License ::")]
    return " | ".join(p for p in parts if p)[:2000]


def classify(text: str) -> str:
    stripped = text
    for pat in LGPL:
        stripped = re.sub(pat, "", stripped, flags=re.I)
    if any(re.search(p, stripped, flags=re.I) for p in BLOCK):
        return "blocked"
    if any(re.search(p, text, flags=re.I) for p in LGPL):
        return "review"
    return "ok"


def main() -> int:
    blocked, review = [], []
    for dist in md.distributions():
        name = (dist.metadata.get("Name") or "").lower()
        text = license_text(dist)
        verdict = classify(text)
        if verdict == "blocked" and name not in ALLOWLIST:
            blocked.append((name, text))
        elif verdict == "review" and name not in ALLOWLIST:
            review.append((name, text))
    for name, text in review:
        print(f"REVIEW (LGPL) {name}: {text[:160]}")
    for name, text in blocked:
        print(f"BLOCKED {name}: {text[:160]}")
    print(f"license gate: {len(blocked)} blocked, {len(review)} to review, allowlisted: {sorted(ALLOWLIST)}")
    return 1 if blocked else 0


if __name__ == "__main__":
    sys.exit(main())
