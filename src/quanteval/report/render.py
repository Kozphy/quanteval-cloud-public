"""HTML (+ optional PDF) report rendering."""

from __future__ import annotations

import base64
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .charts import make_charts
from .compliance import assert_compliant


def _fmt(v, nd=4):
    if v is None:
        return "n/a"
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, (int,)):
        return f"{v:,}"
    if isinstance(v, float):
        if v != v:
            return "n/a"
        if abs(v) >= 1000:
            return f"{v:,.2f}"
        if v != 0 and abs(v) < 1e-3:
            return f"{v:.3g}"
        return f"{v:.{nd}f}"
    return str(v)


def _pct(v, nd=1):
    return "n/a" if v is None else f"{v * 100:.{nd}f}%"


def summary_lines(result: dict) -> list[str]:
    m = result["metrics"]
    names = list(m.keys())
    h = result["config"]["horizon"]
    n = result["folds"]["n"]
    lines = []
    best = min(names, key=lambda k: m[k]["mae"])
    lines.append(f"Across {n} non-overlapping out-of-sample origins and a {h}-bar horizon, the lowest MAE "
                 f"(price units, all steps) came from <b>{best}</b> ({_fmt(m[best]['mae'])}).")
    for k in names:
        if k == "naive":
            continue
        rel = m[k].get("rel_mae_vs_naive")
        dm = m[k].get("dm_vs_naive") or {}
        d = m[k]["directional"]
        rel_txt = f"MAE {_fmt(rel, 3)}x the naive random walk" if rel is not None else "MAE vs naive n/a"
        dm_txt = (f"Diebold-Mariano p={dm['p_value']:.3f} at bar {h}" if dm.get("p_value") is not None else "DM test n/a")
        if d.get("accuracy") is not None:
            sig = "different from" if d["p_value_vs_50pct"] < 0.05 else "not statistically different from"
            dir_txt = (f"directional accuracy {_pct(d['accuracy'])} (95% CI {_pct(d['ci_low'])}-{_pct(d['ci_high'])}, "
                       f"n={d['n']}), {sig} 50%")
        else:
            dir_txt = "directional accuracy undefined"
        lines.append(f"<b>{k}</b>: {rel_txt} ({dm_txt}); {dir_txt}.")
    lines.append("Forecast-accuracy results (this section) are reported separately from the research backtest "
                 "(section 6); a model can be more accurate without producing a better simulated outcome, and vice versa.")
    return lines


def render_report(result: dict, out: Path, pdf: bool = True) -> list[str]:
    charts = make_charts(result, out / "charts")
    embedded = {k: base64.b64encode(Path(p).read_bytes()).decode() for k, p in charts.items()}
    env = Environment(loader=FileSystemLoader(Path(__file__).parent / "templates"),
                      autoescape=select_autoescape(["html", "j2"]))
    env.filters["fmt"] = _fmt
    env.filters["pct"] = _pct
    tpl = env.get_template("report.html.j2")
    html = tpl.render(r=result, charts=embedded, summary=summary_lines(result))
    assert_compliant(html)
    files = []
    html_path = out / "report.html"
    html_path.write_text(html, encoding="utf-8")
    files.append(str(html_path))
    files.extend(charts.values())
    if pdf:
        try:
            from weasyprint import HTML

            pdf_path = out / "report.pdf"
            HTML(string=html, base_url=str(out)).write_pdf(str(pdf_path))
            files.append(str(pdf_path))
            result.setdefault("notes", []).append("PDF rendered with WeasyPrint")
        except Exception as exc:  # noqa: BLE001
            result.setdefault("notes", []).append(f"PDF not rendered: {exc}")
    return files
