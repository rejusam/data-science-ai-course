"""Assemble the session 4 notebook: pandas and first plots.

    python3 tools/build_03_pandas.py

The notebook is a build artefact. Edit this file, not the .ipynb.

Two datasets, in this order. The cohort's own session 1 poll answers first,
because a table you are inside is easier to reason about than a stranger's, and
then `data/employee-attrition.csv`, which is what the deck prescribes.

The loader looks for the files on disk and falls back to the public repository
over HTTP, so the notebook works from the repository root, from the notebook's
own folder, and in Colab where there is no repository at all.

Covers the deck's method list — read_csv, describe, loc, iloc, index,
sort_index, set_index, sample — plus the plotting slides, which have no other
notebook to live in.
"""
from pathlib import Path

import nbformat as nbf

REPO = Path(__file__).resolve().parent.parent
OUTPUT = (REPO / "modules" / "01a-programming-fundamentals" / "notebooks"
          / "03-pandas.ipynb")


def md(text):
    return nbf.v4.new_markdown_cell(text.strip())


def code(text):
    return nbf.v4.new_code_cell(text.strip())


def breaks(text):
    """A cell we expect to fail. The traceback is the point."""
    cell = nbf.v4.new_code_cell(text.strip())
    cell.metadata["tags"] = ["raises-exception"]
    return cell


def predict(question):
    return md("""
> **Predict first.** {}
>
> Put your answer in the chat before we run it.
""".format(question))


def checkpoint(what):
    return md("""
> **Checkpoint.** {}
""".format(what))


SETUP = '''# ==========================================================
# Setup. Run this once, then carry on.
# The loader looks for each file on disk first, and downloads it from the
# public course repository if it cannot find one. That makes this notebook
# work locally and in Colab without changing a line.
# ==========================================================
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

RAW = "https://raw.githubusercontent.com/rejusam/data-science-ai-course/main/"


def dataset(relative_path):
    """Return a path or URL for a file in the course repository."""
    here = Path.cwd()
    for base in [here] + list(here.parents):
        candidate = base / relative_path
        if candidate.exists():
            return candidate
    return RAW + relative_path


pd.set_option("display.max_columns", 20)
pd.set_option("display.width", 120)

print("pandas     :", pd.__version__)
print("attrition  :", dataset("data/employee-attrition.csv"))
print("poll data  :", dataset("modules/00-orientation/data/session1-responses.csv"))
'''


CELLS = [
    md("""
# Session 4 — pandas and first plots

Data Science & AI, Wednesday 12 August.

Monday you learned arrays: fast, one type, no labels. A **DataFrame** is a
group of arrays with names on the columns and labels on the rows. That is
essentially all it is, and everything else pandas does follows from it.

By the end tonight you will have loaded a real file of fifty thousand rows,
asked it several questions, and drawn three charts that answer them.
"""),

    md("""
## Before you type anything

**Work on your own copy, not on this file.**

- Jupyter or VS Code: copy this notebook into `notebooks/my-work/` and open
  that copy.
- Colab: **File → Save a copy in Drive**.

Then **Restart & Run All**, as always.
"""),

    code(SETUP),

    md("""
## 1. From arrays to tables  *(slides 27, 28)*

A **Series** is one column: an array with an index attached. A **DataFrame** is
several Series sharing one index.
"""),
    code("""
readings = pd.Series([68, 72, 91, 105, 58], name="resting_hr")

print(readings)
print()
print("values are still an array :", type(readings.values).__name__)
print("mean                      :", readings.mean())
print("above 100                 :", readings[readings > 100].tolist())
"""),

    md("""
The values are a NumPy array — `ndarray`, Monday's material — and the mask on
the last line is Monday's boolean indexing, unchanged. What pandas adds is the
index down the left, and names.

Next, several columns at once. A DataFrame can be built from a dictionary: each
key becomes a column name, each list becomes that column's values, and every
list has to be the same length.
"""),
    predict("What will `shape` be for a table built from three columns of "
            "three values?"),
    code("""
cohort = pd.DataFrame({
    "study_code": ["REG-0041", "REG-0042", "REG-0043"],
    "age": [54, 38, 67],
    "resting_hr": [72, 65, 104],
})

print(cohort)
print()
print("shape   :", cohort.shape)
print("columns :", list(cohort.columns))
print("dtypes  :")
print(cohort.dtypes)
"""),

    md("""
That is the list of dictionaries from session 2, with a better interface. Same
data, and now you can ask it questions in one line.
"""),

    md("""
## 2. Your own cohort, as a table  *(slide 29)*

`read_csv` is how nearly every analysis starts. This is the session 1 poll,
your answers.
"""),
    code("""
poll = pd.read_csv(dataset("modules/00-orientation/data/session1-responses.csv"))

print("shape :", poll.shape)
poll.head()
"""),

    md("""
`head()` shows the first five rows. `tail()` shows the last five. Both exist
because the first thing to do with a new file is look at it.

`info()` is the next thing: column names, how many values are present, and what
type each column holds.
"""),
    code("""
poll.info()
"""),

    md("""
Read the middle column. Where the count is lower than the number of rows, values
are missing: `status` and `rank_score` only apply to some question types.

Now one question out of the poll. Five operations are involved, so here they
are one per line, each making a thing with a name you can print.
"""),
    code("""
questions  = poll["question"]                                 # one column
is_ranking = questions.str.contains("Rank these", na=False)   # True / False per row
goals      = poll[is_ranking]                                 # keep matching rows
chosen     = goals[["option", "rank_score"]]                  # keep two columns
ordered    = chosen.sort_values("rank_score", ascending=False)

print("rows in the poll :", len(poll))
print("rows matching    :", is_ranking.sum())
print(ordered.to_string(index=False))
"""),

    md("""
Written as one expression, which is how you will meet it in other people's code:
"""),
    code("""
goals = poll[poll["question"].str.contains("Rank these", na=False)]

print(goals[["option", "rank_score"]].sort_values("rank_score", ascending=False)
      .to_string(index=False))
"""),

    md("""
Same five steps, same output. Nothing is saved between them, so there is nothing
to print when it goes wrong — which is the trade. Write the long version while
you are working it out; the short one is for code that already works.

Four things in there are worth naming.

**`.str` is an accessor.** `poll["question"]` is a Series of strings, but it is
not itself a string, so it has no `.contains`. `.str` is the door through to the
string methods, and it applies them to every row at once. `.str.lower()`,
`.str.startswith()`, `.str.strip()` all work the same way. Forgetting `.str` is
the usual first error here.

**The result is a mask, and it is the same idea as Monday.** `is_ranking` is
123 Trues and Falses, one per row, and `poll[is_ranking]` keeps the rows where it
said True — exactly `arr[arr > 3]` from the NumPy session, with rows instead of
values. `is_ranking.sum()` counts to 5 for the same reason `(arr > 3).sum()`
counted to 2.

**`na=False` decides what a missing value means.** Here it changes nothing:
`question` is filled in on all 123 rows. Point the same code at `status`, which
is missing on 89 of them, and leaving it out gives a mask holding `NaN` rather
than `True` or `False`, and pandas refuses:

`ValueError: Cannot mask with non-boolean array containing NA / NaN values`

Read it as *"is a missing value a match?"* Saying `na=False` answers no.

**Two brackets, not one.** `goals["option"]` is a Series, one column. The inner
brackets in `goals[["option", "rank_score"]]` are an ordinary Python list of
column names, so `goals[["option", "rank_score"]]` is a DataFrame with those two
columns in that order. One name in a list, `goals[["option"]]`, is still a
DataFrame. The brackets, not the number of columns, decide which you get.
"""),

    md("""
`to_string(index=False)` prints the table without the left-hand index. Take it
out and the rows come out numbered 29 to 33, not 0 to 4, because filtering keeps
each row's original label rather than renumbering. That is not a bug and it is
worth seeing now: the index is a label, not a row number. Section 4 is about
exactly this.

Python is bottom of that list and this module is four sessions of it. The chart
in the orientation notebook is this table, drawn.
"""),

    md("""
## 3. A real file  *(slides 29, 31)*

`data/employee-attrition.csv`, ten years of HR records from a retail chain, one
row per employee per year.

It came from Kaggle: **HRAnalyticRepository / employee-attrition-data**, licensed
CC0, and the dataset page states it is fictitious. It is committed to the course
repository so nobody needs an account to follow along, but open the Kaggle page
anyway. Finding data, reading its licence, and deciding whether you may use it is
part of the work, and the licence is the part people skip.
"""),
    predict("Fifty thousand rows of employee records. What fraction of them do "
            "you expect to be marked TERMINATED?"),
    code("""
hr = pd.read_csv(dataset("data/employee-attrition.csv"))

print("shape :", hr.shape)
hr.head()
"""),

    code("""
hr.info()
"""),

    md("""
No missing values anywhere, which is unusual and is a sign the file has been
tidied before publication. Real extracts rarely arrive like this.

`describe()` summarises every numeric column at once.
"""),
    code("""
hr.describe().round(1)
"""),

    md("""
Five numeric columns, and two of them are meaningless as numbers: `EmployeeID`
and `store_name` are labels that happen to be digits. A mean employee ID of
4859.5 is a fact about the data and tells you nothing about the business.

**`describe()` will happily summarise a column that should never be summarised.**
Read the column names, not just the numbers.

For text columns, `value_counts` is the equivalent.
"""),
    code("""
print(hr["STATUS"].value_counts())
print()
print(hr["termreason_desc"].value_counts())
"""),

    md("""
1,485 terminations out of 49,653 rows, which is 3%. Compare that with what you
predicted.

Look at `Resignaton`. That is how it is spelled in the source file, missing an
`i`. You will meet this constantly: the moment you type the correct spelling in
a filter, you get zero rows and conclude nobody ever resigned.

**Read the values, not the values you expected.**
"""),

    checkpoint("Quick poll: what does `describe()` do with the `store_name` "
               "column, and why is that a problem?"),

    md("""
The answer is that it computes a mean store of 27.3, and there is no store 27.3.
Store 46 is not twice store 23; it is a different shop. The numbers are names
that happen to be digits.

So why did pandas do it? Because `store_name` is stored as `int64`, and **a
dtype describes storage, not meaning.** pandas knows how the bytes are laid out.
It has no idea one column is a measurement and the other is a label, and that
judgement is not in the file. It is yours.

Which means you can simply say so.
"""),
    code("""
hr["store_name"] = hr["store_name"].astype("category")
hr["EmployeeID"] = hr["EmployeeID"].astype("category")

hr.describe().round(1)
"""),

    md("""
Three columns now, not five. `age`, `length_of_service` and `STATUS_YEAR` are
the ones that were ever quantities, and `describe()` found them on its own once
the other two stopped claiming to be numbers.

Ask about the cast column directly and you get the summary you actually wanted:
"""),
    code("""
print(hr["store_name"].describe())
"""),

    md("""
`count`, `unique`, `top`, `freq` — 46 stores, and the busiest is store 46 with
4,422 rows. Same method, different question, because the column finally says
what it is.

Two things follow from this.

**Fix the types early, once.** Everything after this point in the notebook now
gets it right for free — `describe()`, `info()`, and any summary you write
later. Correcting a dtype is not tidying-up you do at the end; it is part of
loading the file.

**`category` is also cheaper.** `store_name` drops from about 397 KB to 51 KB,
because pandas stores 46 labels once and keeps a small code per row instead of a
full integer. On this file that is a rounding error; on ten million rows it is
the difference between fitting in memory and not. The reason to cast is meaning,
and the memory is a bonus.
"""),

    md("""
## 4. The index  *(slide 46)*

Every DataFrame has an index down the left. By default it is 0, 1, 2, and you
can put something more useful there.

Start with the one `hr` arrived with.
"""),
    code("""
print("hr.index      :", hr.index)
print("first four    :", list(hr.index[:4]))
print("its name      :", hr.index.name)
"""),

    md("""
`RangeIndex(start=0, stop=49653, step=1)` is pandas saying *"I had nothing to
label these rows with, so I numbered them."* Its name is `None`, because it is
not about anything. It is a row count wearing a label's clothes.

Now a table where the index does mean something. `groupby` is section 7; take
this one line on trust for the moment and watch only the left-hand column.
"""),
    code("""
by_year = hr.groupby("STATUS_YEAR").size()

print(by_year)
"""),

    md("""
The years down the left are the index. Nobody numbered these rows — the years
came out of the data, and each one labels the count beside it.

Put the two side by side:
"""),
    code("""
print("hr      -> index name:", hr.index.name,      "| first four:", list(hr.index[:4]))
print("by_year -> index name:", by_year.index.name, "| first four:", list(by_year.index[:4]))
"""),

    md("""
`None` against `STATUS_YEAR`. That is the whole difference, and it changes how
you get a value out:

```python
by_year[2008]      # 4767, the year 2008
by_year.iloc[0]    # 4579, whichever year happens to be first
by_year[0]         # KeyError: 0 - there is no year 0
```

The last one catches people out constantly. Once the index holds real labels,
`[0]` asks for *the row labelled 0*, not the first row, and there isn't one. The
numbers you saw on `hr` were only ever labels too; they looked like positions
because pandas had counted from zero. Section 5 is `loc` and `iloc`, which exist
to make you say which of the two you meant.

`set_index` moves a column into the index. `reset_index` moves it back out.
`sort_index` sorts by the index, `sort_values` sorts by a column.
"""),
    code("""
small = cohort.set_index("study_code")
print(small)
print()
print("sorted by index:")
print(small.sort_index(ascending=False))
print()
print("back to normal:")
print(small.reset_index())
"""),

    md("""
Once a meaningful index is in place you can look a row up by name, which is what
the next section is about.
"""),

    md("""
## 5. `loc` versus `iloc`  *(slide 46)*

The single most common source of pandas confusion, so we will be slow about it.

- **`loc`** works with **labels**: what is written in the index.
- **`iloc`** works with **integer positions**: where the row physically is.
"""),
    predict("`small.loc[\"REG-0041\":\"REG-0042\"]` and `small.iloc[0:2]` both "
            "return two rows. What does `small.loc[\"REG-0041\":\"REG-0043\"]` "
            "return, and what does `small.iloc[0:3]` return? Careful."),
    code("""
print("loc  REG-0041 to REG-0043 :", len(small.loc["REG-0041":"REG-0043"]), "rows")
print("iloc 0 to 3               :", len(small.iloc[0:3]), "rows")
print("iloc 0 to 2               :", len(small.iloc[0:2]), "rows")
"""),

    md("""
Three rows, three rows, two rows — and `small` only has three rows in total.

`loc` asked for everything from the label REG-0041 to the label REG-0043 and
gave you REG-0043 as well. `iloc[0:3]` asked for positions 0, 1, 2 and stopped
before 3, which happens to be all three rows because there is no position 3.
The two agree by accident. `iloc[0:2]` is the one that shows the rule.

**`loc` includes the end of the range. `iloc` excludes it.** Everywhere else in
Python, ranges exclude the end, so `iloc` is the consistent one and `loc` is the
exception you have to remember.

The reason is that `loc` works on labels, and with labels there is no "one past
the end" to stop at. You asked for everything from this name to that name, so
you get that name too.

The rows themselves, so you can see it rather than count it:
"""),
    code("""
print("loc, by label:")
print(small.loc["REG-0041":"REG-0043"])
print()
print("iloc, by position:")
print(small.iloc[0:2])
"""),
    code("""
print("one row by label    :")
print(small.loc["REG-0042"])
print()
print("one row by position :")
print(small.iloc[1])
print()
print("one cell, by label    :", small.loc["REG-0042", "age"])
print("one cell, by position :", small.iloc[1, 0])
"""),

    md("""
The same 38, reached two ways. `loc` was told *the row called REG-0042, the
column called age*; `iloc` was told *row 1, column 0*. Neither knows what the
other asked for, and they agree here only because that is where the value sits.
"""),

    md("""
### Deliberate error one

Give `iloc` a label and see what it says.
"""),
    breaks("""
small.iloc["REG-0042"]
"""),

    md("""
`TypeError: Cannot index by location index with a non-integer key`

The message names the mistake precisely: `iloc` takes positions, not labels.
When you meet it in your own work, the question to ask is which one you
actually wanted, and it is usually `loc`.
"""),

    md("""
## 6. Selecting and filtering  *(slide 46)*

One column gives a Series. A list of columns gives a DataFrame. This is the
double-bracket rule from section 2, and it is worth seeing the two side by side.
"""),
    code("""
one_column  = hr["age"]                              # a name
two_columns = hr[["age", "department_name"]]         # a list of names

print("hr['age']                     ->", type(one_column).__name__)
print("hr[['age', 'department_name']] ->", type(two_columns).__name__)
print()
print(hr[["age", "length_of_service", "STATUS"]].head())
"""),

    md("""
The inner brackets are an ordinary Python list. That is the only difference, and
it decides whether you get one column on its own or a table with one or more
columns in it.
"""),

    md("""
Filtering is Monday's boolean mask, applied to a table instead of an array.
"""),
    code("""
terminated = hr[hr["STATUS"] == "TERMINATED"]

print("terminated rows :", len(terminated))
print("their mean age  : {:.1f}".format(terminated["age"].mean()))
print("everyone's mean : {:.1f}".format(hr["age"].mean()))
"""),

    md("""
Combine conditions with `&` for and, `|` for or. **Each condition needs its own
brackets**, because `&` binds more tightly than `>` does.
"""),
    code("""
older_leavers = hr[(hr["age"] > 60) & (hr["STATUS"] == "TERMINATED")]

print("terminated and over 60 :", len(older_leavers))
print(older_leavers["termreason_desc"].value_counts())
"""),

    md("""
### Deliberate error two

The same filter with the brackets left out.
"""),
    breaks("""
hr[hr["age"] > 60 & hr["STATUS"] == "TERMINATED"]
"""),

    md("""
`TypeError: Cannot perform 'rand_' with a dtyped [object] array and scalar of
type [bool]`

Without the brackets Python evaluates `60 & hr["STATUS"]` first, which is
nonsense, and the message talks about dtypes rather than about brackets. A
confusing error for a simple cause, which is exactly why it is worth meeting
once here rather than alone at eleven at night.

`sample` takes rows at random, which is useful for eyeballing a big file without the
bias of always looking at the top.
"""),
    code("""
print(hr.sample(5, random_state=0)[["EmployeeID", "age", "department_name",
                                    "STATUS_YEAR", "STATUS"]].to_string())
"""),

    md("""
`random_state=0` fixes the choice so everyone in the room sees the same five
rows and the notebook stays reproducible. Leave it out and you get a different
sample every run.
"""),

    md("""
## 7. Grouping  *(slide 27)*

`groupby` splits the table, applies something to each piece, and puts the
results back together.

It only does the splitting. Ask for the split on its own and look at what comes
back:
"""),
    code("""
print(terminated.groupby("STATUS_YEAR"))
"""),

    md("""
No numbers. `DataFrameGroupBy` is the table sliced into ten piles with nothing
done to them yet — a plan, not a result. **`groupby` never decides what to
work out.** You have to say, and `.size()` is one of the ways of saying it:
*how many rows are in each pile.*

`.mean()`, `.sum()` and `.max()` sit in the same slot and answer different
questions about the same piles.
"""),
    predict("Terminations per year, 2006 to 2015. Do you expect a flat line, a "
            "rising one, or something with a spike in it?"),
    code("""
per_year = terminated.groupby("STATUS_YEAR").size()
print(per_year)
"""),

    md("""
2014 stands out: 253 terminations against a run of 105 to 165 in the years
either side. Anything that breaks a pattern is worth a question, and here the
question is whether something happened in 2014 or whether the data changed.

One aside before we carry on, because it bites later. `.size()` counts **rows**.
Its near neighbour `.count()` counts **values that are not missing**, column by
column, so it hands back a whole DataFrame — seventeen columns wide here, not a
single tally. On this file the two agree, because nothing is missing. On the
poll data they do not: the word cloud answers are 35 rows, of which 5 have a
`status`, so `.size()` says 35 and `.count()` says 5.

Neither is wrong. *How many records* and *how many answers* are different
questions, and the day they disagree is the day it matters which one you asked.
"""),
    md("""
To find out, split each year by *why* people left. Group by two columns instead
of one, and do it in two steps so you can see what each does.
"""),
    code("""
counts = terminated.groupby(["STATUS_YEAR", "termreason_desc"]).size()

print(counts.head(6))
print()
print("rows :", len(counts), "| index levels :", counts.index.nlevels)
"""),

    md("""
Still a Series, but the index has two levels now — year, then reason — and there
are 22 rows, one for each year-and-reason pair that actually happened. Correct,
and hard to read: comparing 2014 with 2013 means hunting up and down a list.

`unstack` lifts the inner level of the index up into columns.
"""),
    code("""
by_reason = counts.unstack(fill_value=0)

print(by_reason)
"""),

    md("""
The same 22 numbers, now a 10 by 3 grid: years down the side, reasons across the
top. Nothing was recalculated. `unstack` only moved a level of the index, and
that is the whole trick — you can read along a row or down a column.

`fill_value=0` fills the pairs that never occurred, like layoffs in 2006. Leave
it out and those cells are `NaN`, and because `NaN` is a float it drags the
whole table with it: every count prints as `12.0` instead of `12`.

There it is. Layoffs happened in exactly two years, 2014 and 2015, and nowhere
else. The 2014 spike is not a hiring or morale story, it is one event, and
splitting a total by a second column is how you find that out.
"""),

    md("""
Every group so far has been counted. `agg` asks for several different summaries
at once and gives each a name. Build up to it — one column, one summary first:
"""),
    code("""
print(hr.groupby("department_name")["age"].mean().round(1).head(4))
"""),

    md("""
`agg` is that, three times over, with names attached. Each line reads
`name_for_the_result=("column to use", "what to do with it")`:
"""),
    code("""
by_dept = hr.groupby("department_name").agg(
    people=("EmployeeID", "nunique"),
    mean_age=("age", "mean"),
    mean_service=("length_of_service", "mean"),
).sort_values("people", ascending=False)

print(by_dept.head(8).round(1))
"""),

    md("""
Three questions about the same 21 piles, answered in one pass, and the names on
the left become the column headings.

**`nunique`, not `size`, and the difference is the whole file.** This table has
one row per employee *per year*, so Customer Service is 7,122 rows but only
1,190 people. `size` would have counted the rows and called it a headcount, and
"Customer Service employs 7,122 people" is the kind of number that reaches a
slide before anybody checks it.

Nothing in the code would have looked wrong. You have to know what a row is.
"""),

    md("""
## 8. Charts  *(slides 26, 30)*

Every chart below answers a question we already asked in numbers. Draw the chart
second, never first: a plot of something you do not understand is decoration.

Every chart cell in this notebook has the same four parts, in the same order:

1. `plt.figure(figsize=(w, h))` — start a new canvas, and say how big in inches.
   Leave it out and your chart lands on top of the previous one.
2. one line that draws — `plt.plot`, `plt.barh`, `plt.hist`. This is the only
   line that changes between charts.
3. the labels — `title`, `xlabel`, `ylabel`. An unlabelled axis is a chart
   nobody else can read.
4. `plt.show()` — draw it and clear the canvas for the next cell.

Read the cells below looking for those four, and the only part you have to think
about is line 2.
"""),
    code("""
plt.figure(figsize=(9, 3.5))                      # 1. canvas

plt.plot(per_year.index, per_year.values,         # 2. draw: x, then y
         marker="o")

plt.title("Terminations per year")                # 3. labels
plt.xlabel("year")
plt.ylabel("people")
plt.grid(alpha=0.3)

plt.show()                                        # 4. show
"""),

    md("""
A **line chart** for something measured over time. Points joined by a line imply
"these are the same thing at different moments", so do not use one for
categories.

`per_year.index` is the years and `per_year.values` is the counts — the index we
spent section 4 on, now doing a job. `plt.plot` always takes x first, then y.

Next, the same four parts with `barh` in slot 2. The extra line at the top is
preparation, not plotting: pick the rows, then sort them.
"""),
    code("""
top = by_dept.head(8)["people"].sort_values()     # 0. prepare the data

plt.figure(figsize=(9, 4))                        # 1. canvas

plt.barh(top.index, top.values,                   # 2. draw: labels, then lengths
         color="#2b6cb0")

plt.title("Largest departments, by number of people")   # 3. labels
plt.xlabel("people")

plt.tight_layout()                                # stop long names being cut off
plt.show()                                        # 4. show
"""),

    md("""
A **bar chart** for categories. Horizontal, because department names read
better across than squashed underneath. Sorted, because an unsorted bar chart
makes the reader do work you could have done for them.
"""),
    predict("Age, across fifty thousand rows. One peak, two peaks, or flat?"),
    code("""
plt.figure(figsize=(9, 3.5))
plt.hist(hr["age"], bins=25, color="#2b6cb0", edgecolor="white")
plt.title("Age distribution")
plt.xlabel("age")
plt.ylabel("rows")
plt.show()
"""),

    md("""
A **histogram** shows the shape of one numeric column: values on the bottom,
how many fall in each bin up the side. This one is broadly flat through the
middle and thins at both ends, which is another sign of generated data: real
workforces are not spread evenly across every age.

Notice the sawtooth. Ages run from 19 to 65, so 47 whole numbers are being
forced into 25 bins: most bins catch two ages and some catch only one, and the
short bars are the ones that caught a single age. Change `bins=` and the shape
changes with it. **A histogram is a claim about your binning as much as about
your data**, which is why you try more than one.

`seaborn` sits on top of matplotlib and gives you the common statistical charts
in one line each. Same four parts; only slot 2 changes, and seaborn takes the
whole DataFrame plus the names of the columns to use rather than raw values.
"""),
    code("""
plt.figure(figsize=(9, 3.5))                      # 1. canvas

sns.boxplot(data=hr, x="age", y="STATUS",         # 2. draw: table, then columns
            color="#2b6cb0")

plt.title("Age, active against terminated")       # 3. labels
plt.tight_layout()
plt.show()                                        # 4. show
"""),

    md("""
A **box plot** is five numbers drawn: the box spans the middle half of the
values, the line inside it is the median, and the whiskers reach out to the rest
with far-out points marked individually.

Read the two medians. Active staff sit at 42, terminated at 60, and the
terminated box is squashed up against the top of the range. That is the same
fact `describe()` would give you, in a form where the difference is obvious
without reading a single number — which is the entire argument for charts.
"""),
    code("""
sample = hr.sample(500, random_state=0)           # 0. 500 rows, not 49,653

sns.pairplot(sample[["age", "length_of_service", "STATUS"]],
             hue="STATUS",                        # colour the points by status
             height=2.4,
             plot_kws={"s": 18, "alpha": 0.6})    # small, see-through dots

plt.show()
"""),

    md("""
`pairplot` builds its own grid of canvases, so there is no `plt.figure` here —
it is the one chart in this notebook that does not follow the four parts.

`alpha=0.6` makes the dots see-through so you can tell one point from fifty
stacked on top of each other. With 49,653 rows every panel would be a solid
block, which is why we sampled 500 first.
"""),

    md("""
`pairplot` draws every numeric column against every other, with the histogram of
each down the diagonal. On two columns it is small; on twenty it is a wall, so
it is a first-look tool, on a sample, not a finished chart.

Terminated people average 51.5 years against 42.1 for everyone, and 11.4 years
of service against 10.4. The age gap is large and the service gap is small.

Before calling that a finding, look at why they left: 885 of the 1,485 retired.
The gap is mostly the shape of retirement, not a story about who leaves. Charts
suggest questions; they do not answer them.
"""),

    md("""
## 9. The deck's own example, and a mistake in it  *(slides 31, 32)*

Slides 31 and 32 use the iris dataset, which ships inside scikit-learn. We used
your data first because a table you are inside is easier to argue with. Now the
slide's version, because there is something wrong with it.

First, look at what `load_iris` actually hands you, before anyone turns it into
a table.
"""),
    code("""
from sklearn.datasets import load_iris

dataset = load_iris()

print("what is in it :", list(dataset.keys()))
print()
print("dataset['data']   :", dataset["data"].shape, "of", dataset["data"].dtype)
print("the first row     :", dataset["data"][0])
print("dataset['target'] :", set(dataset["target"]))
print("target_names      :", dataset["target_names"])
"""),

    md("""
Three things to notice.

**`dataset["data"]` is 150 rows by 4 columns of bare numbers.** A NumPy array,
Monday's material — fast, one type, and **no names anywhere**. The measurements
arrive with nothing saying which is which.

**`dataset["target"]` is 0, 1 and 2**, not species names. Machine learning
libraries want numbers, so the species are stored as codes, and
`target_names` is the lookup that turns a code back into a word.

**The names have to come from somewhere else.** That somewhere is the
`columns=` argument below, and this is where the whole section turns.

Now the slide's code, unchanged. Three steps: build the table, attach the
species codes, swap the codes for names.
"""),
    code("""
# Exactly as the slide writes it.
data = pd.DataFrame(dataset["data"],
                    columns=["Petal length", "Petal Width",
                             "Sepal Length", "Sepal Width"])
data["Species"] = dataset["target"]
data["Species"] = data["Species"].apply(lambda x: dataset["target_names"][x])

print(data.head())
"""),

    md("""
`columns=` matches names to columns **by position, and by nothing else**. The
first name goes on column 0, the second on column 1, and so on. pandas checks
that you supplied four names for four columns — give it three and you get
`ValueError: Shape of passed values is (150, 4), indices imply (150, 3)` — but
it never checks *which* name belongs on *which* column. It counts your labels.
It does not read them.

The last line is `apply` with a `lambda`: run this little function on every
value in the column. The value is a code, `dataset["target_names"][x]` looks the
code up, so 0 becomes setosa. A list comprehension does the same job and you
will see one later in this section.
"""),
    predict("Petals are the coloured inner parts of the flower and sepals are "
            "the green outer ones. Which do you expect to be larger?"),
    code("""
print(data[["Petal length", "Petal Width", "Sepal Length", "Sepal Width"]].mean().round(2))
"""),

    md("""
That says petals are longer than sepals, which is the wrong way round for iris.

Ask the data where its columns actually came from rather than trusting the
labels somebody typed.
"""),
    code("""
for position, name in enumerate(dataset.feature_names):
    print("column", position, "is", name)
"""),

    md("""
The order is sepal length, sepal width, petal length, petal width. The slide
labels them petal, petal, sepal, sepal. **Every column in that frame is
mislabelled**, the numbers are all correct, and nothing errors.

This is the most dangerous class of bug in data work: no traceback, plausible
output, wrong conclusions downstream. The only defence is the one you just
used, which is to check the labels against the source rather than the other way
round.
"""),
    code("""
iris = pd.DataFrame(dataset["data"], columns=dataset.feature_names)
iris["species"] = [dataset["target_names"][i] for i in dataset["target"]]

print(iris.describe().round(2))
"""),

    code("""
sns.pairplot(iris, hue="species", height=1.9, plot_kws={"s": 18})
plt.show()
"""),

    md("""
Now the picture makes sense: setosa separates cleanly on petal measurements,
and the other two overlap. That separation is why iris has been the teaching
dataset for classification since 1936, and you will meet it again in module 5.

Two things to take from this section. `describe()` and `pairplot` are one line
each, exactly as the slide says. And a chart drawn from mislabelled columns
looks just as convincing as a correct one.
"""),

    checkpoint("Pace check before the last stretch."),

    md("""
---

## Your turn  *(slide 47)*

Core tasks first, in your pair. Say what you expect before you run each one.
"""),

    code("""
# 1. Load the attrition file into a DataFrame called `df`, using dataset().
#    Print its shape and the first three rows.

"""),
    code("""
# 2. Print describe() for the numeric columns. In one comment, name a column
#    whose mean should be ignored, and say why.

"""),
    code("""
# 3. Set the index to EmployeeID, then use loc to print the rows for
#    employee 1318. How many rows are there, and why more than one?

"""),
    code("""
# 4. Using iloc, print rows 10 to 14 inclusive, columns 0 to 5.
#    Watch the ends of both ranges.

"""),
    code("""
# 5. Sort the whole table by length_of_service, longest first, and print the
#    top five with sort_values. Then sort by index with sort_index.

"""),
    code("""
# 6. Take a random sample of 10 rows with a fixed random_state. Print the
#    department and status of each.

"""),
    code("""
# 7. How many people resigned, in total? Remember how it is spelled in the
#    file. Then find the mean age of the people who resigned.

"""),
    code("""
# 8. Write a function
#
#        def summary(df, department):
#
#    that returns three values for one department: the number of rows,
#    the mean age, and the number of terminations. Call it for "Meats".

"""),

    md("""
### Check your own work

Run this once tasks 1, 7 and 8 are written.
"""),
    code("""
if "summary" not in dir() or "df" not in dir():
    print("Finish tasks 1 and 8 first, then run this cell again.")
else:
    rows, mean_age, terminations = summary(df, "Meats")

    assert rows == 10269, "expected 10269 rows for Meats, got {}".format(rows)
    assert 50 < mean_age < 55, "mean age came back as {}".format(mean_age)
    assert terminations > 0

    print("summary() looks right: {} rows, mean age {:.1f}, {} terminations".format(
        rows, mean_age, terminations))
"""),

    md("""
### Stretch

1. Terminations per year as a **rate**: divide by the number of people employed
   that year, rather than counting. Does 2014 still stand out?
2. Voluntary against involuntary departures over the ten years, on one chart
   with two lines and a legend.
3. Pick a department and answer one question of your own about it, in numbers
   and then in a chart. Bring the chart on Saturday.
4. `terminationdate_key` reads `1/1/1900` for most active employees, and a real
   date for the rest. Work out why, and why using that column to predict
   `STATUS` would be cheating. The answer is in `data/README.md`, so try it
   first.
"""),

    md("""
---

## Before you close the laptop

**Restart & Run All.** Clean top to bottom, apart from the two cells we broke on
purpose.

`loc` is labels and includes the end. `iloc` is positions and excludes it. If
only one thing survives tonight, that is the one.

Next: **Saturday 15 August**, six hours. Bring broken code of your own, from any
session. The debugging clinic is the most useful hour of this module and it only
works if you bring something.
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
    broken = sum(1 for c in CELLS
                 if "raises-exception" in c.get("metadata", {}).get("tags", []))
    print("wrote {} cells ({} deliberate errors) to {}".format(
        len(CELLS), broken, OUTPUT))


if __name__ == "__main__":
    build()
