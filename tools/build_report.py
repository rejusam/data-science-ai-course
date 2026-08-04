"""Assemble the session 1 storytelling report.

    python3 tools/make_report_charts.py reports/session1/charts
    python3 tools/build_report.py

Charts are generated as SVG and inlined into the template, so the finished
report is one self-contained file with no external requests. Text inside the
charts stays as real text, not paths, so it is selectable and stays crisp.

Chart colours are rewritten to CSS custom properties on the way in. matplotlib
writes fixed hex, which would be unreadable when the page is viewed in dark
mode; routing them through tokens lets the charts follow the page theme.
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REPORT = REPO / "reports" / "session1"
TEMPLATE = REPORT / "report.template.html"
CHARTS = REPORT / "charts"
OUTPUT = REPORT / "index.html"

# matplotlib hex -> the page's theme token
COLOUR_TOKENS = {
    "#12161c": "var(--chart-ink)",
    "#5b6470": "var(--chart-muted)",
    "#c9c6bd": "var(--chart-faint)",
    "#2a78d6": "var(--chart-blue)",
    "#eb6834": "var(--chart-warm)",
}

# Kept as numeric entities so the file renders correctly however it is served,
# including from a server that sends no charset.
ENTITIES = {"—": "&#8212;", "–": "&#8211;"}


def prepare(svg_text):
    """Strip the standalone-document parts and make the SVG themeable."""
    svg = re.sub(r"<\?xml[^>]*\?>\s*", "", svg_text)
    svg = re.sub(r"<!DOCTYPE[^>]*>\s*", "", svg)
    # Drop the fixed pixel size; the viewBox plus CSS handles scaling.
    svg = re.sub(r'(<svg[^>]*?)\s+width="[^"]*"', r"\1", svg, count=1)
    svg = re.sub(r'(<svg[^>]*?)\s+height="[^"]*"', r"\1", svg, count=1)
    for hex_value, token in COLOUR_TOKENS.items():
        svg = svg.replace(hex_value, token)
    for raw, entity in ENTITIES.items():
        svg = svg.replace(raw, entity)
    return svg.strip()


def build():
    html = TEMPLATE.read_text()
    used = []

    for svg_path in sorted(CHARTS.glob("*.svg")):
        token = "{{%s}}" % svg_path.name
        if token not in html:
            print("WARNING unused chart:", svg_path.name)
            continue
        svg = prepare(svg_path.read_text())
        leftover = sorted(set(re.findall(r"#[0-9a-fA-F]{6}", svg)))
        if leftover:
            print("WARNING unmapped colours in {}: {}".format(
                svg_path.name, ", ".join(leftover)))
        html = html.replace(token, svg)
        used.append(svg_path.name)

    unfilled = re.findall(r"\{\{[^}]+\}\}", html)
    if unfilled:
        raise SystemExit("missing charts for: " + ", ".join(unfilled))

    OUTPUT.write_text(html)
    print("inlined {} charts".format(len(used)))
    print("wrote {} ({} KB)".format(OUTPUT, len(html) // 1024))


if __name__ == "__main__":
    build()
