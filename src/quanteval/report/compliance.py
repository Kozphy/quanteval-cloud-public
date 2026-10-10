"""Report language lint: block trade-instruction / promotional wording (see docs/mvp-prd.md section 5)."""

from __future__ import annotations

import html
import re

from ..errors import ComplianceError

FORBIDDEN = [
    r"\bbuy(s|ing)?\b", r"\bsell(s|ing)?\b", r"\bsignals?\b", r"\brecommend\w*", r"\btarget\s+price",
    r"\bguarantee\w*", r"\bprofitable\b", r"\bsure\s+(win|thing)\b", r"\brisk[- ]free\b",
]


def visible_text(markup: str) -> str:
    markup = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", markup, flags=re.S | re.I)
    markup = re.sub(r'src="data:[^"]+"', "", markup)
    return html.unescape(re.sub(r"<[^>]+>", " ", markup))


def find_violations(text: str) -> list[str]:
    hits = []
    for pat in FORBIDDEN:
        for m in re.finditer(pat, text, flags=re.I):
            start = max(0, m.start() - 40)
            hits.append(f"'{m.group(0)}' in: ...{text[start:m.end() + 40].strip()}...")
    return hits


def assert_compliant(markup: str) -> None:
    hits = find_violations(visible_text(markup))
    if hits:
        raise ComplianceError("Report contains disallowed language:\n" + "\n".join(hits[:20]))
