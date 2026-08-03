"""Assemble the 'your cohort in data' notebook.

    python3 tools/build_cohort_notebook.py

The notebook is a build artefact. Edit this file, not the .ipynb.

It runs two ways. With the raw Slidea export present it parses it live, which
is the version shown in class. Without it, it falls back to the tidy CSVs
committed to the repository, so every student can run it. The output is the
same either way.
"""
from pathlib import Path

import nbformat as nbf

REPO = Path(__file__).resolve().parent.parent
OUTPUT = REPO / "modules" / "00-orientation" / "notebooks" / "your-cohort-in-data.ipynb"


def md(text):
    return nbf.v4.new_markdown_cell(text.strip())


def code(text):
    return nbf.v4.new_code_cell(text.strip())


CELLS = [
    md("""
# Your cohort, in data

On Monday night you answered twenty-five poll questions. This notebook takes
that raw export, cleans it, and turns it into something worth looking at.

Two things to notice as we go.

The first is that the data does not arrive tidy. It arrives as a spreadsheet
with twenty-five differently shaped blocks stacked in one sheet. That is not
unusual, it is normal, and dealing with it is most of the job.

The second is that everything here is your own data, collected two days ago,
about you. By about week 12 you will be able to write all of this yourself.
"""),

    code("""
import sys
import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# openpyxl complains that this workbook has no default styling. True, and
# irrelevant to us.
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

# Works whether you opened this notebook from the repository root or from
# the folder it lives in.
ROOT = Path.cwd()
while not (ROOT / "tools").is_dir() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.path.insert(0, str(ROOT))

DATA = ROOT / "modules" / "00-orientation" / "data"

plt.rcParams["figure.figsize"] = (9, 4.5)
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

INK = "#1f3864"
WARM = "#c0504d"
MUTED = "#a6a6a6"

print("Ready. Working from:", ROOT)
"""),

    md("""
## Step 1: What the raw export actually looks like

Before any cleaning. This is the sheet exactly as the polling tool produced it.
"""),

    code("""
from tools.slidea import load_export

# Trainer: point this at the Slidea export to run the live version.
# Students: leave it as None. The tidy CSVs are in the repository and every
# result below is identical either way.
RAW_EXPORT = None

RAW = Path(RAW_EXPORT) if RAW_EXPORT else None
if RAW and not RAW.exists():
    print("RAW_EXPORT is set but that file does not exist:", RAW)
    RAW = None

if RAW:
    raw = pd.read_excel(RAW, sheet_name="Response Details", header=None)
    print("Raw sheet shape:", raw.shape)
    print()
    print(raw.iloc[3:13].fillna("").to_string(max_colwidth=44))
else:
    print("Raw export not present. Using the tidy CSVs instead.")
    print("Nothing below changes; only this cell needs the original file.")
"""),

    md("""
Look at what is wrong with that.

The column headers are not on row 1. The same sheet holds several tables with
different columns. Percentages are text with a `%` on the end, not numbers.
Blank rows separate the blocks. There is no single column that identifies which
question a row belongs to.

None of it is usable in that state.
"""),

    md("""
## Step 2: Reshape it into tidy data

Tidy data means one row per observation and one column per variable. Getting
there is what `tools/slidea.py` does. The point of putting it in a module,
rather than in the notebook, is that it can be tested. It has seventeen tests.
"""),

    code("""
if RAW:
    export = load_export(RAW)
    responses = export.responses[
        ~export.responses["question"].str.contains("study code", case=False)
    ]
    scales = export.scales
    meta = export.meta
else:
    responses = pd.read_csv(DATA / "session1-responses.csv")
    scales = pd.read_csv(DATA / "session1-scales.csv")
    meta = {"Total Participants": 12, "Total Slides": 25, "Avg Participation": 83}

print("participants  :", meta["Total Participants"])
print("slides         :", meta["Total Slides"])
print("participation  :", str(meta["Avg Participation"]) + "%")
print()
responses.head(8)
"""),

    md("""
One row per answer option, with the question, the count, and the percentage as
an actual number. That took one function call, and now everything else is easy.
"""),

    md("""
## Step 3: Who is in this room

Nobody is identified anywhere in this notebook. These are counts.
"""),

    code("""
def chart(question_contains, title=None, colour=INK, source=None):
    \"\"\"Horizontal bar chart of one question, biggest answer at the top.\"\"\"
    table = source if source is not None else responses
    rows = table[table["question"].str.contains(question_contains,
                                                case=False, regex=False)]
    if rows.empty:
        raise KeyError(question_contains)
    rows = rows[rows["count"] > 0].sort_values("count")

    fig, ax = plt.subplots(figsize=(9, 0.55 * len(rows) + 1.6))
    ax.barh(rows["option"], rows["count"], color=colour)
    for y, (value, pct) in enumerate(zip(rows["count"], rows["percentage"])):
        label = " {:.0f}".format(value)
        if pd.notna(pct):
            label += "  ({:.0f}%)".format(pct)
        ax.text(value, y, label, va="center", fontsize=9)
    ax.set_xlim(0, rows["count"].max() * 1.28)
    ax.set_title(title or rows["question"].iloc[0], loc="left", wrap=True)
    ax.set_xlabel("students")
    ax.tick_params(axis="y", labelsize=9)
    plt.tight_layout()
    plt.show()


chart("What best describes where you are right now",
      "Why you are here")
"""),

    code("""
chart("Which operating system will you use",
      "What you will be working on")
chart("can you install software on it",
      "Whether you can install things on it")
"""),

    md("""
That second chart is why Monday's setup session went the way it did.

Two thirds of you are on Windows, and a quarter are on a shared or family
computer. The setup guide in `resources/` is written for both operating
systems for exactly that reason.
"""),

    md("""
## Step 4: What you want, against where you are today

This is the interesting one.

You ranked five things by what you most want to be able to do by week 25. You
also rated your own confidence in five subjects. Putting those two answers side
by side shows the distance you are here to cover.
"""),

    code("""
goals = responses[responses["question"].str.contains("Rank these by what YOU",
                                                     regex=False)]
goals = goals.sort_values("rank_score")

fig, ax = plt.subplots(figsize=(9, 3.4))
ax.barh(goals["option"], goals["rank_score"], color=INK)
for y, value in enumerate(goals["rank_score"]):
    ax.text(value, y, " {:.0f}".format(value), va="center", fontsize=9)
ax.set_xlim(0, goals["rank_score"].max() * 1.2)
ax.set_title("What you most want to be able to do by week 25", loc="left")
ax.set_xlabel("rank score (higher means ranked more important, more often)")
plt.tight_layout()
plt.show()
"""),

    code("""
def confidence(question_contains):
    \"\"\"Average position on a 0 to 4 scale, weighted by how many chose each.\"\"\"
    rows = scales[scales["question"].str.contains(question_contains,
                                                  case=False, regex=False)]
    out = []
    for item, group in rows.groupby("item", sort=False):
        total = group["count"].sum()
        score = (group["level_index"] * group["count"]).sum() / total
        out.append({"item": item, "index": round(score, 2)})
    return pd.DataFrame(out).sort_values("index")


subjects = confidence("confident are you TODAY")

fig, ax = plt.subplots(figsize=(9, 3.4))
colours = [WARM if v < 1 else INK for v in subjects["index"]]
ax.barh(subjects["item"], subjects["index"], color=colours)
for y, value in enumerate(subjects["index"]):
    ax.text(value, y, "  {:.2f}".format(value), va="center", fontsize=9)
ax.set_xlim(0, 4)
ax.set_xticks(range(5))
ax.set_xticklabels(["never\\ntouched it", "seen it", "with\\nhelp",
                    "on my\\nown", "could\\nteach it"], fontsize=8)
ax.set_title("How confident you said you are today", loc="left")
plt.tight_layout()
plt.show()

print("Lowest two, in red, are where most of the course goes.")
"""),

    md("""
Read those two charts together.

Building and evaluating machine learning models is the second most wanted thing
in the room. It is also the second least confident. Generative AI is third most
wanted and the single least confident.

That gap is not a problem. That gap is the course.
"""),

    md("""
## Step 5: When each of those things actually happens

Your top-ranked goals are not evenly spread through the twenty-five weeks. Here
is when each one is taught.
"""),

    code("""
# Weeks come from the course delivery plan. See ../../../SYLLABUS.md
roadmap = pd.DataFrame([
    ("Write clean, confident Python",              1,  2),
    ("Wrangle data with SQL, APIs and pipelines",  6,  8),
    ("Build and evaluate machine learning models", 8, 14),
    ("Deploy models and build with Generative AI",19, 20),
    ("Tell a convincing story with data",         18, 20),
], columns=["goal", "start", "end"])

order = list(goals["option"])
roadmap["rank"] = roadmap["goal"].map({g: i for i, g in enumerate(order)})
roadmap = roadmap.sort_values("rank")

fig, ax = plt.subplots(figsize=(9, 3.4))
ax.barh(roadmap["goal"], roadmap["end"] - roadmap["start"] + 1,
        left=roadmap["start"], color=INK)
for y, row in enumerate(roadmap.itertuples()):
    ax.text(row.end + 0.4, y, "weeks {}-{}".format(row.start, row.end),
            va="center", fontsize=9)
ax.set_xlim(0, 30)
ax.set_xlabel("week of the course")
ax.set_title("When you get what you asked for", loc="left")
plt.tight_layout()
plt.show()
"""),

    md("""
The thing you ranked first, telling a convincing story with data, lands near
the end. That is deliberate. You cannot tell a story about a model you have not
built yet.

The thing you ranked last, writing clean Python, starts on Wednesday of week 1,
because everything else rests on it.
"""),

    md("""
## Step 6: What the room already knows

Four questions on Monday had a right answer. Here is how the room did, hardest
first.
"""),

    code("""
graded = responses[responses["status"].fillna("").str.contains("Correct")]
totals = responses.groupby("question")["count"].sum()

scores = []
for question, group in graded.groupby("question", sort=False):
    # Skip the ice-breaker about the trainer; it is not a knowledge question.
    if "Lead Trainer" in question:
        continue
    correct = group["count"].sum()
    total = totals[question]
    scores.append({
        "question": question,
        "pct": round(correct / total * 100, 1),
        "correct": int(correct),
        "total": int(total),
    })

scores = pd.DataFrame(scores).sort_values("pct")

short = {
    "Quick check: what is the difference between Git and GitHub?": "Git vs GitHub",
    "Quick check: which of these is a SUPERVISED learning problem?": "Supervised learning",
    "Ice cream sales and drowning deaths both rise every summer. What is the safest conclusion?": "Correlation vs causation",
    "Your model is 99% accurate on the data it was trained on. What do you do first?": "Overfitting",
    "Guess: what percentage of a working data scientist's time goes on finding, cleaning and preparing data?": "Time spent cleaning data",
}
scores["label"] = scores["question"].map(short).fillna(scores["question"].str[:40])

fig, ax = plt.subplots(figsize=(9, 3.2))
colours = [WARM if p < 50 else INK for p in scores["pct"]]
ax.barh(scores["label"], scores["pct"], color=colours)
for y, row in enumerate(scores.itertuples()):
    ax.text(row.pct, y, "  {:.0f}%  ({}/{})".format(row.pct, row.correct, row.total),
            va="center", fontsize=9)
ax.axvline(50, color=MUTED, linestyle="--", linewidth=1)
ax.set_xlim(0, 118)
ax.set_xlabel("percent of those who answered, who got it right")
ax.set_title("How the room did on the questions with a right answer", loc="left")
plt.tight_layout()
plt.show()
"""),

    md("""
Two of those are worth dwelling on.

**Correlation and causation.** Half the room got it. A third chose "the
correlation must be a mistake", which is the interesting wrong answer, because
the correlation is completely real. Ice cream sales and drownings do rise
together. Neither causes the other. Hot weather causes both. We spend a whole
session on this in week 6, and it is the single most common way analysts
mislead people, usually without meaning to.

**Supervised learning.** Under a third got it, which is exactly what you would
expect in week 1, and which is why modules 4 and 5 exist.
"""),

    md("""
## Step 7: The guess

One question asked what percentage of a working data scientist's time goes on
finding, cleaning and preparing data.
"""),

    code("""
guesses = responses[responses["question"].str.contains("percentage of a working",
                                                       regex=False)].copy()
guesses["value"] = guesses["option"].str.extract(r"(\\d+)").astype(int)
guesses = guesses.sort_values("value")

values = guesses["value"].repeat(guesses["count"]).tolist()

fig, ax = plt.subplots(figsize=(9, 3))
ax.scatter(values, [1] * len(values), s=190, color=INK, alpha=0.65, zorder=3)
ax.axvline(80, color=WARM, linewidth=2, zorder=2)
ax.text(80, 1.32, " commonly cited answer: 80%", color=WARM, fontsize=10)
median = pd.Series(values).median()
ax.axvline(median, color=MUTED, linestyle="--", linewidth=1.5, zorder=2)
ax.text(median, 0.66, "your median: {:.0f}%".format(median), color="#666666",
        fontsize=10, ha="center")
ax.set_xlim(0, 108)
ax.set_ylim(0.5, 1.6)
ax.set_yticks([])
ax.set_xlabel("percent of time spent finding, cleaning and preparing data")
ax.set_title("Your guesses, and the number the industry usually quotes",
             loc="left")
plt.tight_layout()
plt.show()

print("Guesses ranged from {:.0f} to {:.0f}.".format(min(values), max(values)))
print("Most of the room guessed low.")
"""),

    md("""
The spread matters more than the answer. Guesses ran from 20 to 100, which
means the room genuinely did not know, which is fine in week 1.

The commonly quoted figure is around 80%, and it is the reason this course
spends modules 2 and 3 on getting and cleaning data before it touches a single
model. The modelling is the short part. It is almost always the short part.
"""),

    md("""
## Step 8: In your own words

Two open questions. What might get in the way, and what you are committing to.
"""),

    code("""
def words(question_contains, title, colour=INK):
    rows = responses[responses["question"].str.contains(question_contains,
                                                        case=False, regex=False)]
    rows = rows[rows["count"] > 0].sort_values("count")
    fig, ax = plt.subplots(figsize=(8, 0.42 * len(rows) + 1.4))
    ax.barh(rows["option"], rows["count"], color=colour)
    for y, value in enumerate(rows["count"]):
        ax.text(value, y, " {:.0f}".format(value), va="center", fontsize=9)
    ax.set_xlim(0, rows["count"].max() * 1.25)
    ax.set_title(title, loc="left")
    ax.set_xlabel("students")
    ax.tick_params(axis="y", labelsize=9)
    plt.tight_layout()
    plt.show()


words("most likely to get in the way", "What you said might get in the way", WARM)
words("name ONE habit you will hold", "What you committed to")
"""),

    md("""
Work and time, named by almost everyone. That is not a surprise and it is not a
character flaw, it is what part-time study is.

It does mean the plan has to survive contact with a busy week. Forty-five
focused minutes on a weeknight beats one heroic Sunday, every time, and it is
the difference between finishing and not.
"""),

    md("""
## What just happened

Everything above came out of one messy spreadsheet, and it used exactly the
skills this course teaches, in the order it teaches them.

| What we did | When you learn it |
|---|---|
| Loading a spreadsheet into pandas | Week 2 |
| Reshaping messy data into tidy data | Weeks 4 and 5 |
| Grouping and aggregating | Week 2 |
| Charting to answer a question | Weeks 4 and 5 |
| Writing tested, reusable code | Throughout, starting now |

The parser behind this notebook is `tools/slidea.py`. It is about two hundred
lines and has seventeen tests in `tools/tests/`. Read it whenever you want. By
week 12 none of it will look like magic.

You can run this notebook yourself right now:

```
conda activate dsai
jupyter lab
```
"""),
]


def build():
    notebook = nbf.v4.new_notebook(cells=CELLS)
    notebook.metadata = {
        "kernelspec": {"display_name": "Python (dsai)", "language": "python",
                       "name": "dsai"},
        "language_info": {"name": "python"},
        "colab": {"provenance": []},
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    nbf.write(notebook, str(OUTPUT))
    print("wrote {} cells to {}".format(len(CELLS), OUTPUT))


if __name__ == "__main__":
    build()
