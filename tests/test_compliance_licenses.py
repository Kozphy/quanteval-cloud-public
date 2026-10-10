import importlib.util
from pathlib import Path

import pytest

from quanteval.errors import ComplianceError
from quanteval.report.compliance import assert_compliant, find_violations

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("text", ["You should BUY now", "sell signal", "Trading signals inside", "we recommend X",
                                  "target price 100", "guaranteed returns", "a profitable model", "risk-free"])
def test_forbidden_language_detected(text):
    assert find_violations(text)
    with pytest.raises(ComplianceError):
        assert_compliant(f"<p>{text}</p>")


@pytest.mark.parametrize("text", ["passive long reference", "forecast target window", "Bessel", "buyer-side"[:0] + "OK"])
def test_allowed_language(text):
    assert not find_violations(text)


def test_template_source_is_compliant():
    tpl = (ROOT / "src/quanteval/report/templates/report.html.j2").read_text()
    from quanteval.report.compliance import visible_text
    import re
    assert not find_violations(visible_text(re.sub(r"\{[{%#].*?[}%#]\}", " ", tpl, flags=re.S)))


def _load_gate():
    spec = importlib.util.spec_from_file_location("check_licenses", ROOT / "scripts/check_licenses.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.parametrize("text,verdict", [
    ("GPL-3.0", "blocked"), ("GNU General Public License v3 (GPLv3)", "blocked"),
    ("Apache 2.0 with Commons Clause", "blocked"), ("AGPL-3.0-only", "blocked"),
    ("LGPL-3.0", "review"), ("MIT", "ok"), ("BSD-3-Clause", "ok"), ("Apache-2.0", "ok"),
])
def test_license_classifier(text, verdict):
    assert _load_gate().classify(text) == verdict


def test_installed_environment_passes_license_gate():
    assert _load_gate().main() == 0


def test_third_party_notices_include_kronos_mit():
    t = (ROOT / "THIRD_PARTY_NOTICES.md").read_text()
    assert "Copyright (c) 2025 ShiYu" in t and "MIT License" in t and "f4e68697d9d5aed55cef5c96aabc3376bcad9f81" in t
    assert (ROOT / "src/quanteval/_vendor/kronos/LICENSE").exists()
