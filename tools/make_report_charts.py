"""Generate the report's charts as inline SVG.

Text is kept as text (svg.fonttype = none) so it stays selectable, crisp at
any zoom, and inherits the page's font stack through CSS.
"""
import io
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

REPO = Path("/Users/rsjohn/Projects/data-science-ai-course")
DATA = REPO / "modules" / "00-orientation" / "data"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "reports" / "session1" / "charts"
OUT.mkdir(parents=True, exist_ok=True)

responses = pd.read_csv(DATA / "session1-responses.csv")
scales = pd.read_csv(DATA / "session1-scales.csv")

INK = "#12161c"
MUTED = "#5b6470"
FAINT = "#c9c6bd"
BLUE = "#2a78d6"
DEEP = "#104281"
WARM = "#eb6834"
PAPER = "none"

matplotlib.rcParams.update({
    "svg.fonttype": "none",
    # Fixed salt so element ids are stable between runs. Without it every
    # rebuild rewrites every clip-path id and git shows a large, empty diff.
    "svg.hashsalt": "session1-report",
    "font.family": "sans-serif",
    "font.size": 12,
    "text.color": INK,
    "axes.edgecolor": FAINT,
    "axes.labelcolor": MUTED,
    "xtick.color": MUTED,
    "ytick.color": INK,
    "figure.facecolor": "none",
    "axes.facecolor": "none",
    "savefig.facecolor": "none",
})


def strip(ax, keep_x=True):
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_visible(keep_x)
    ax.tick_params(length=0)
    ax.grid(False)


def save(fig, name):
    buffer = io.StringIO()
    fig.savefig(buffer, format="svg", bbox_inches="tight", transparent=True)
    svg = buffer.getvalue()
    svg = svg[svg.index("<svg"):]
    # matplotlib stamps a generation time into the metadata; drop it so the
    # output only changes when the data or the chart code changes.
    svg = re.sub(r"\s*<dc:date>[^<]*</dc:date>", "", svg)
    # Let CSS drive the type.
    svg = svg.replace("font-family:sans-serif", "font-family:inherit")
    (OUT / name).write_text(svg)
    plt.close(fig)
    print("wrote", name, len(svg) // 1024, "KB")


def ask(fragment):
    hit = responses[responses["question"].str.contains(fragment, case=False,
                                                       regex=False)]
    return hit[hit["question"] == hit["question"].iloc[0]]


def confidence(fragment):
    rows = scales[scales["question"].str.contains(fragment, case=False,
                                                  regex=False)]
    out = []
    for item, group in rows.groupby("item", sort=False):
        total = group["count"].sum()
        out.append({"item": item,
                    "index": (group["level_index"] * group["count"]).sum() / total})
    return pd.DataFrame(out).sort_values("index")


# ------------------------------------------------- 1. want vs confidence ----

goals = ask("Rank these by what YOU").sort_values("rank_score")
subjects = confidence("confident are you TODAY")

PAIRS = {
    "Build and evaluate machine learning models": "Machine learning concepts",
    "Deploy models and build with Generative AI": "Generative AI and LLMs",
    "Write clean, confident Python": "Python programming",
    "Wrangle data with SQL, APIs and pipelines": "SQL and databases",
}

fig, axes = plt.subplots(1, 2, figsize=(11, 4.1), gridspec_kw={"wspace": 0.55})

ax = axes[0]
ax.barh(goals["option"], goals["rank_score"], color=BLUE, height=0.6)
for y, value in enumerate(goals["rank_score"]):
    ax.text(value + 0.8, y, "{:.0f}".format(value), va="center",
            fontsize=11, color=MUTED, family="monospace")
ax.set_xlim(0, 44)
ax.set_title("What they want by week 25", loc="left", fontsize=13,
             color=INK, pad=14)
ax.set_xlabel("rank score", fontsize=10, family="monospace")
strip(ax)
ax.set_xticks([])

ax = axes[1]
colours = [WARM if v < 1 else BLUE for v in subjects["index"]]
ax.barh(subjects["item"], subjects["index"], color=colours, height=0.6)
for y, value in enumerate(subjects["index"]):
    ax.text(value + 0.09, y, "{:.2f}".format(value), va="center",
            fontsize=11, color=MUTED, family="monospace")
ax.set_xlim(0, 4)
ax.set_xticks([0, 1, 2, 3, 4])
ax.set_xticklabels(["never\ntouched", "seen it", "with\nhelp", "on my\nown",
                    "could\nteach"], fontsize=9, family="monospace")
ax.set_title("What they can do today", loc="left", fontsize=13, color=INK,
             pad=14)
strip(ax)
save(fig, "want-vs-can.svg")

# ------------------------------------------------------------ 2. roadmap ----

roadmap = pd.DataFrame([
    ("Write clean, confident Python", 1, 2),
    ("Wrangle data with SQL, APIs and pipelines", 6, 8),
    ("Build and evaluate machine learning models", 8, 14),
    ("Deploy models and build with Generative AI", 19, 20),
    ("Tell a convincing story with data", 18, 20),
], columns=["goal", "start", "end"])
order = list(goals["option"])
roadmap["rank"] = roadmap["goal"].map({g: i for i, g in enumerate(order)})
roadmap = roadmap.sort_values("rank")

fig, ax = plt.subplots(figsize=(11, 3.3))
ax.barh(roadmap["goal"], roadmap["end"] - roadmap["start"] + 1,
        left=roadmap["start"], color=BLUE, height=0.55)
for y, row in enumerate(roadmap.itertuples()):
    ax.text(row.end + 1.0, y, "weeks {}–{}".format(row.start, row.end),
            va="center", fontsize=10.5, color=MUTED, family="monospace")
ax.set_xlim(0, 31)
ax.set_xticks([1, 5, 10, 15, 20, 25])
ax.set_xticklabels([str(w) for w in [1, 5, 10, 15, 20, 25]],
                   family="monospace", fontsize=10)
ax.set_xlabel("week of the course", fontsize=10, family="monospace")
strip(ax)
save(fig, "roadmap.svg")

# -------------------------------------------------------------- 3. guess ----

guesses = ask("percentage of a working").copy()
guesses["value"] = guesses["option"].str.extract(r"(\d+)").astype(int)
spread = guesses["value"].repeat(guesses["count"]).tolist()
median = pd.Series(spread).median()

fig, ax = plt.subplots(figsize=(11, 2.5))
ax.scatter(spread, [1] * len(spread), s=260, color=BLUE, alpha=0.55,
           edgecolors="none", zorder=3)
ax.axvline(80, color=WARM, linewidth=2.4, zorder=2)
ax.text(81.5, 1.34, "commonly quoted: 80%", color=WARM, fontsize=11,
        family="monospace")
ax.axvline(median, color=MUTED, linewidth=1.2, linestyle=(0, (4, 3)), zorder=2)
ax.text(median, 0.62, "their median {:.0f}%".format(median), color=MUTED,
        fontsize=11, ha="center", family="monospace")
ax.set_xlim(5, 108)
ax.set_ylim(0.5, 1.5)
ax.set_yticks([])
ax.set_xticks([20, 40, 60, 80, 100])
ax.set_xticklabels(["20%", "40%", "60%", "80%", "100%"], family="monospace",
                   fontsize=10)
strip(ax)
save(fig, "guess.svg")

# --------------------------------------------------------------- 4. quiz ----

SHORT = {
    "Quick check: what is the difference between Git and GitHub?": "Git vs GitHub",
    "Quick check: which of these is a SUPERVISED learning problem?":
        "Spotting supervised learning",
    "Ice cream sales and drowning deaths both rise every summer. What is the "
    "safest conclusion?": "Correlation vs causation",
    "Your model is 99% accurate on the data it was trained on. What do you do "
    "first?": "Recognising overfitting",
}
graded = responses[responses["status"].fillna("").str.contains("Correct")]
totals = responses.groupby("question")["count"].sum()
rows = []
for question, group in graded.groupby("question", sort=False):
    if question not in SHORT:
        continue
    correct = int(group["count"].sum())
    total = int(totals[question])
    rows.append({"label": SHORT[question],
                 "pct": correct / total * 100,
                 "correct": correct, "total": total})
quiz = pd.DataFrame(rows).sort_values("pct")

fig, ax = plt.subplots(figsize=(11, 2.9))
ax.barh(quiz["label"], quiz["pct"], color=BLUE, height=0.55)
for y, row in enumerate(quiz.itertuples()):
    ax.text(row.pct + 2, y, "{:.0f}%   {}/{}".format(row.pct, row.correct,
                                                     row.total),
            va="center", fontsize=10.5, color=MUTED, family="monospace")
ax.axvline(50, color=FAINT, linewidth=1.2, linestyle=(0, (4, 3)))
ax.text(50, len(quiz) - 0.35, "half the room", color=MUTED, fontsize=9.5,
        ha="center", family="monospace")
ax.set_xlim(0, 122)
ax.set_xticks([])
strip(ax, keep_x=False)
save(fig, "quiz.svg")

print("median guess:", median, "| range:", min(spread), max(spread))
