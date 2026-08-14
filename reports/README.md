# Reports

Written analysis of the cohort's own data. Where the dashboard is for looking
things up, a report makes an argument and commits to it.

| Report | What it covers |
|---|---|
| [`session1/`](session1/index.html) | What twelve people said on the first night: what they want, what they can do today, and the distance between the two |

## Reading one

Open `index.html` in a browser. Each report is a single self-contained file
with no external requests, so it works offline and can be emailed as-is.

## Building one

Reports are generated, not hand-edited. Prose lives in `report.template.html`
with `{{chart-name.svg}}` placeholders; charts are generated separately and
inlined at build time.

The two build steps run from the trainer's copy of the course tooling, which is
not published in this repository.

Both steps are deterministic: rerunning them without changing the data or the
code produces a byte-identical file, so git diffs only show real changes.

## Why the charts are SVG

Text inside them stays as text rather than being flattened to paths, so it is
selectable, searchable, and crisp at any zoom. Their colours are rewritten to
CSS custom properties during the build, which lets the charts follow the
page's light and dark themes instead of being fixed to one background.

## Structure worth copying

If you write your own report for a mini project, this shape travels well:

1. **The short version** — the finding, before the evidence. If a reader stops
   after this section they should still have the point.
2. **Findings** — one claim per section, each earning its chart.
3. **What changed because of this** — a report that ends at "interesting" was
   not worth writing.
4. **What this cannot tell you** — sample size, self-report bias, non-response,
   and anything you quoted but did not establish yourself. Stating the limits
   of your evidence is what separates analysis from advertising.
