"""Assemble the session 3 notebook: NumPy.

    python3 tools/build_02_numpy.py

The notebook is a build artefact. Edit this file, not the .ipynb.

Section 0 finishes the functions material from session 2, which ran out of time
after data structures. It is not optional padding: every section from 5 onward
calls a function, and the closing tasks ask students to write their own.

`ecg_signal.py` is inlined into a setup cell rather than imported, because
Colab cannot see files from the repository. The source is presented as
something to read, not hidden: by the end of session 2 it uses nothing the
students have not been taught.
"""
from pathlib import Path

import nbformat as nbf

REPO = Path(__file__).resolve().parent.parent
MODULE = REPO / "modules" / "01a-programming-fundamentals"
OUTPUT = MODULE / "notebooks" / "02-numpy.ipynb"


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


def ecg_source():
    """ecg_signal.py, with its import line removed (numpy is already loaded)."""
    lines = (MODULE / "ecg_signal.py").read_text().splitlines()
    kept = [line for line in lines if line.strip() != "import numpy as np"]
    # Drop the __main__ block; it would print on import.
    text = "\n".join(kept)
    return text.split('if __name__ == "__main__":')[0].rstrip()


SETUP = '''# ==========================================================
# Setup. Run this once, then carry on.
# Everything below is the contents of ecg_signal.py from the course
# repository, pasted in so this notebook also works in Colab.
# It is worth reading. It uses nothing you were not taught last session.
# ==========================================================
import time

import numpy as np
import matplotlib.pyplot as plt

{}

print("Ready.")
'''


CELLS = [
    md("""
# Session 3 — NumPy

Data Science & AI, Monday 10 August.

Last session you used a Python list to hold five heart-rate readings. Tonight
you will hold two and a half thousand, do arithmetic on all of them at once
without writing a loop, and find every heartbeat in the recording.

NumPy is the foundation everything else in this course sits on. pandas is built
on it. scikit-learn is built on it. Every array of numbers you touch for the
next twenty-four weeks is a NumPy array underneath.
"""),

    md("""
## Before you type anything

**Work on your own copy, not on this file.**

- Jupyter or VS Code: copy this notebook into `notebooks/my-work/` and open
  that copy. The folder is ignored by git, so your work is yours and
  `git pull` will never argue with it.
- Colab: **File → Save a copy in Drive**, then work in the copy.

If you type into the file that came from the repository, the next `git pull`
will refuse to run because your changes would be overwritten. Two minutes now
saves that conversation later.

**Then: Restart & Run All.** Same rule as last week. Your code works when it
runs top to bottom from a fresh start, and nothing less counts.
"""),

    code(SETUP.format(ecg_source())),

    md("""
## 0. Finishing Wednesday: functions  *(slide 15)*

We stopped last session at data structures, which leaves functions unfinished.
Tonight needs them. From section 5 onward everything you call is a function,
and the tasks at the end ask you to write your own.

Twenty minutes, then NumPy.
"""),

    checkpoint("Three quick questions on Wednesday's material, in Slidea. "
               "Answers published straight after."),

    md("""
### Warm-up: put the lines in order

These five lines make a working program that counts how many readings are above
100. They are in the wrong order, and two of them need indenting.

```
        total = total + 1
readings = [68, 60, 72, 91, 105, 58]
print(total)
    if reading > 100:
total = 0
for reading in readings:
```

Type them into the next cell in the right order. Do not run it until you and
your pair agree.
"""),
    code("""
# Your reordered version:

"""),

    md("""
### A function of your own

A function gives a name to a piece of work so you can do it again without
retyping it.
"""),
    code("""
def classify_bpm(bpm, low=60, high=100):
    \"\"\"Return a label for one heart-rate reading.\"\"\"
    if bpm < low:
        return "low"
    if bpm > high:
        return "high"
    return "normal"


print(classify_bpm(48))
print(classify_bpm(72))
print(classify_bpm(130))
"""),

    md("""
Three things to notice.

`def` names the function. `bpm`, `low` and `high` are **parameters**: names
that only exist while the function runs. `return` hands a value back and stops
the function immediately.

`low=60` and `high=100` are **default arguments**. The caller can leave them out
and get the usual thresholds, or pass their own without you editing the
function. That is most of what makes a function reusable rather than a piece of
code with a name stuck on it.
"""),
    predict("What does `classify_bpm(60)` return? "
            "And what does `classify_bpm(60, low=65)` return?"),
    code("""
print(classify_bpm(60))
print(classify_bpm(60, low=65))
"""),

    md("""
Boundaries are where bugs live. `60` is not less than `60`, so the first call
comes back `normal`. The second call moves the threshold to 65 and the same
reading is now `low`. The rule changed, the function did not.

Which of those is correct is a clinical question, not a Python one. The point is
that the code makes the choice visible instead of burying it.
"""),

    md("""
Rather than checking the output by eye, state what you expect and let Python
check it. `assert` says nothing at all when it is right, and fails loudly when
it is not.
"""),
    code("""
assert classify_bpm(48) == "low"
assert classify_bpm(72) == "normal"
assert classify_bpm(130) == "high"
assert classify_bpm(60) == "normal"        # the boundary
assert classify_bpm(60, low=65) == "low"   # a different rule

print("all five checks passed")
"""),

    md("""
### Giving back more than one thing

`return` can hand back several values at once, separated by commas.
"""),
    code("""
def summarise(readings):
    \"\"\"Return the lowest, highest and average of a list of readings.\"\"\"
    return min(readings), max(readings), sum(readings) / len(readings)


lowest, highest, average = summarise([68, 60, 72, 91, 105, 58])

print("lowest  :", lowest)
print("highest :", highest)
print("average : {:.1f}".format(average))
"""),

    md("""
The commas build a **tuple**, an ordered group of values that cannot be changed
afterwards. Splitting it back out into three names in one line is called
unpacking, and you will see it again in about ten minutes when `simulate` hands
back two arrays at once.
"""),

    md("""
### Where a name lives

Names created inside a function exist only inside it. This is **scope**, and it
is the last idea from Wednesday's slides.
"""),
    code("""
def count_high(readings, limit=100):
    total = 0
    for reading in readings:
        if reading > limit:
            total = total + 1
    return total


print(count_high([68, 60, 72, 91, 105, 58]))
"""),

    md("""
#### Deliberate error one

`total` did its job. Now ask for it from outside the function.
"""),
    breaks("""
print(total)
"""),

    md("""
`NameError: name 'total' is not defined`

`total` was created inside `count_high` and stopped existing the moment the
function returned. That is deliberate: a function you can only affect through
its arguments, and only hear from through its return value, is a function you
can reason about on its own.

The traffic goes one way. A function can see names from the main notebook, but
the notebook cannot see inside the function.
"""),

    md("""
## 1. Why NumPy exists  *(slides 23, 44)*

You already have lists. Here is what you gain by giving them up.

We will square a million numbers, first with a loop over a list, then with a
NumPy array.
"""),
    predict("How many times faster do you think the array version will be? "
            "Commit to a number."),
    code("""
numbers = list(range(1_000_000))
array = np.arange(1_000_000)

start = time.perf_counter()
squared_list = [n ** 2 for n in numbers]
list_seconds = time.perf_counter() - start

start = time.perf_counter()
squared_array = array ** 2
array_seconds = time.perf_counter() - start

print("list  : {:.4f} seconds".format(list_seconds))
print("array : {:.4f} seconds".format(array_seconds))
print("NumPy is about {:.0f}x faster".format(list_seconds / array_seconds))
"""),

    md("""
Two reasons for the difference.

A Python list can hold anything, so Python checks the type of every element
every time it touches one. A NumPy array holds **one type only**, stored in a
single continuous block of memory, so the whole operation runs as compiled
code without checking anything.

And `array ** 2` has no Python loop in it at all. That is called
**vectorisation**, and it is the habit to build: if you are writing a loop over
numbers, there is usually an array operation that does it better.
"""),

    md("""
## 2. Making arrays  *(slide 23)*

Four ways you will use constantly.
"""),
    code("""
from_list = np.array([5, 3, 7, 2])
evenly    = np.linspace(0, 1, 5)      # 5 values from 0 to 1 inclusive
counting  = np.arange(0, 10, 2)       # like range(), but an array
empty     = np.zeros(4)

print("from_list :", from_list)
print("evenly    :", evenly)
print("counting  :", counting)
print("empty     :", empty)
"""),

    md("""
`linspace` is the one worth remembering tonight. "Give me *n* points evenly
spaced between here and there" is how you build a time axis, and it is how the
ECG signal below gets its timestamps.
"""),

    md("""
## 3. What an array knows about itself  *(slide 45)*

Every attribute on tonight's method list, on one array.
"""),
    predict("For `np.array([[1, 2, 3], [4, 5, 6]])`, what are `ndim`, "
            "`shape` and `size`?"),
    code("""
grid = np.array([[1, 2, 3],
                 [4, 5, 6]])

print("ndim     :", grid.ndim)       # how many dimensions
print("shape    :", grid.shape)      # rows, columns
print("size     :", grid.size)       # total number of elements
print("dtype    :", grid.dtype)      # the type of every element
print("itemsize :", grid.itemsize)   # bytes per element
print("nbytes   :", grid.nbytes)     # itemsize * size
print("data     :", grid.data)       # the raw block of memory itself
"""),

    md("""
`shape` is a tuple, which is why it prints with brackets. `(2, 3)` means two
rows and three columns.

`dtype` and `itemsize` are the "one type only" claim from section 1, made
concrete: `int64` means every element is an integer taking 8 bytes, so a
6-element array is exactly 48 bytes and NumPy knows where each one sits without
looking. `data` is that block of memory. You will almost never use it directly,
but seeing it once explains why arrays are fast and lists are not.

### Choosing a type  *(slides 24, 25)*

Python has one `int`, which grows as large as you need. NumPy has eleven, and
you pick the size. That is the trade: control and speed, in exchange for having
to think about it.
"""),
    code("""
print("default from whole numbers  :", np.array([1, 2, 3]).dtype)
print("default with a decimal      :", np.array([1.0, 2, 3]).dtype)
print("mixed with text becomes     :", np.array([1, "two", 3]).dtype)
print()

small = np.array([1, 2, 3], dtype=np.int8)     # 1 byte each, -128 to 127
large = np.array([1, 2, 3], dtype=np.float64)  # 8 bytes each

print("int8    :", small.dtype, small.itemsize, "byte per element")
print("float64 :", large.dtype, large.itemsize, "bytes per element")
"""),

    md("""
An `int8` holds one byte, which runs from -128 to 127. So what happens to 300?

### Deliberate error two
"""),
    predict("`np.array([300], dtype=np.int8)` — error, or some other number?"),
    breaks("""
np.array([300], dtype=np.int8)
"""),

    md("""
`OverflowError: Python integer 300 out of bounds for int8`

NumPy refuses, which is the friendly outcome. Now the same idea by a different
route, where it does not refuse.
"""),
    code("""
print("300 converted with astype :", np.array([300]).astype(np.int8)[0])

a = np.array([120], dtype=np.int8)
print("120 + 10 as int8          :", (a + np.int8(10))[0])

print("1.7 and 2.9 to int8       :", np.array([1.7, 2.9]).astype(np.int8))
"""),

    md("""
`44`, `-126`, and `[1 2]`. No error, no warning, three wrong answers.

Asking for the conversion with `astype` means you asserted it was safe, and
arithmetic that runs off the end of a type wraps around rather than complaining.
Converting floats to integers truncates rather than rounding, so 2.9 becomes 2.

That is the cost of choosing a type: it buys speed and memory, and it hands you
the responsibility. It matters when a dataset is large enough that eight bytes
per number is real money, and it is a genuine source of bugs in the wild.

**Missing numbers are a type problem too.** There is no such thing as a missing
integer in NumPy: `np.nan` is a float, so any array with a gap in it becomes a
float array. pandas is built on this, which is why an integer column with one
blank value arrives on Wednesday as `float64`.
"""),
    code("""
print("nan is a          :", type(np.nan).__name__)
print("array with a gap  :", np.array([1, 2, np.nan]).dtype)
print("nan == nan        :", np.nan == np.nan, "  <- use np.isnan(), never ==")
print("isnan             :", np.isnan(np.array([1, 2, np.nan])))
"""),

    md("""
### Axes

**Axis 0 runs down the rows. Axis 1 runs across the columns.** Getting these
the wrong way round is the most common NumPy mistake, and you will meet it
again in pandas on Wednesday.
"""),
    code("""
print("sum of everything :", grid.sum())
print("sum down columns  :", grid.sum(axis=0))   # one result per column
print("sum across rows   :", grid.sum(axis=1))   # one result per row
"""),

    md("""
### Deliberate error two

Asking a one-dimensional array for axis 1.
"""),
    breaks("""
flat = np.array([1, 2, 3, 4])
print(flat.sum(axis=1))
"""),

    md("""
`AxisError: axis 1 is out of bounds for array of dimension 1`

A flat array only has axis 0. This error means "you thought this was a table
and it is a line", which is worth knowing because it usually means your data is
not the shape you assumed.
"""),

    md("""
## 4. Arithmetic without loops  *(slide 44)*

Operations apply to every element at once.
"""),
    predict("What does `np.array([1, 2, 3]) * 2` give? "
            "And what would `[1, 2, 3] * 2` give, as a plain Python list?"),
    code("""
readings = np.array([68, 72, 91, 105, 58])

print("array * 2      :", readings * 2)
print("plain list * 2 :", [68, 72, 91, 105, 58] * 2)
"""),

    md("""
That difference catches people out. `*` on a list means "repeat the list". On
an array it means "multiply every element". Two different operations wearing
the same symbol.
"""),
    code("""
print("minus 60      :", readings - 60)
print("as a fraction :", np.round(readings / 60, 2))
print("two arrays    :", readings + np.array([1, 1, 1, 1, 1]))
"""),

    md("""
### Deliberate error three

Two arrays of different lengths.
"""),
    breaks("""
np.array([1, 2, 3]) + np.array([1, 2])
"""),

    md("""
`ValueError: operands could not be broadcast together with shapes (3,) and (2,)`

**Broadcasting** is NumPy's rule for combining arrays of different shapes. A
single number broadcasts against anything, which is why `readings - 60` works.
Two arrays of different lengths do not, because there is no sensible answer.

Read the shapes in that error message. They tell you exactly what you gave it.
"""),

    checkpoint("Concept check in Slidea before the break: axes, broadcasting, "
               "and what `dtype` buys you."),

    md("""
## 5. A real signal  *(slide 23)*

Now something with more than five numbers in it.

`simulate` builds a synthetic ECG: a heart trace, made of mathematical curves.
It is not recorded from anyone. It gives back two arrays: the time of each
measurement, and the voltage at that time. Two values, one `return`, exactly as
in section 0.
"""),
    code("""
t, signal = simulate(seconds=10, bpm=72)

print("shape       :", signal.shape)
print("ndim        :", signal.ndim)
print("dtype       :", signal.dtype)
print("duration    : {:.1f} seconds".format(t[-1]))
print("sample rate :", int(signal.size / 10), "per second")
"""),

    code("""
plt.figure(figsize=(11, 3))
plt.plot(t[:500], signal[:500], linewidth=1)
plt.xlabel("time (seconds)")
plt.ylabel("mV")
plt.title("Two seconds of a simulated ECG")
plt.show()
"""),

    md("""
The tall spikes are R peaks, one per heartbeat. Counting them over a known
duration is how you measure heart rate, and that is what the rest of this
notebook builds up to.
"""),

    md("""
## 6. Summarising  *(slide 45)*

Every aggregation on tonight's method list, on real data.
"""),
    code("""
print("count   :", signal.size)
print("mean    : {:.4f} mV".format(signal.mean()))
print("std     : {:.4f} mV".format(signal.std()))
print("min     : {:.4f} mV".format(signal.min()))
print("max     : {:.4f} mV".format(signal.max()))
print("sum     : {:.2f}".format(signal.sum()))
"""),

    md("""
The mean sits near zero because an ECG spends most of its time on the baseline
and only briefly spikes. **A mean can describe a signal badly.** Half of
statistics is knowing when a summary is hiding what matters, and this is a
clean example of it.

`cumsum` is the running total: every value is the sum of everything up to that
point.
"""),
    predict("What is `np.cumsum([1, 2, 3, 4])`?"),
    code("""
print(np.cumsum([1, 2, 3, 4]))
"""),

    md("""
## 7. Boolean indexing  *(slide 44)*

This is the most useful idea in NumPy, and it replaces most loops you would
otherwise write, including the one you reordered at the start of tonight.

Comparing an array to a number gives you an array of True and False.
"""),
    predict("Given `arr = np.array([5, 3, 7, 2])`, what does `arr > 3` give? "
            "And what does `arr[arr > 3]` give?"),
    code("""
arr = np.array([5, 3, 7, 2])

print("the mask   :", arr > 3)
print("the values :", arr[arr > 3])
print("how many   :", (arr > 3).sum())     # True counts as 1
"""),

    md("""
Using a mask to index an array returns only the values where it was True.

`(arr > 3).sum()` counting to 2 is a trick worth keeping: True is 1 and False
is 0, so summing a mask counts how many things matched.

Compare it with `count_high` from section 0. Same question, no loop, no
counter, one line. On a million elements it is not close.

On the signal:
"""),
    code("""
high = signal > 0.6

print("samples above 0.6 mV :", high.sum())
print("as a fraction        : {:.2%}".format(high.mean()))
print("largest 5 values     :", np.round(np.sort(signal)[-5:], 3))
"""),

    md("""
## 8. `np.where`, and finding the heartbeats  *(slide 44)*

`np.where` gives the **positions** where a condition is true, rather than the
values. That difference matters here: we want to know *when* each beat
happened, not what its voltage was.
"""),
    code("""
print("values    :", arr[arr > 3])
print("positions :", np.where(arr > 3)[0])
"""),

    md("""
A sample is an R peak if it is above the threshold **and** higher than the
sample before it **and** higher than the one after. That last part is what
stops one wide spike being counted many times.

`r_peaks` is a function with a default argument, like `classify_bpm`. The
threshold is a decision, so it is a parameter rather than a number buried in
the body.
"""),
    code("""
peaks = r_peaks(signal, threshold=0.6)

print("peaks found :", len(peaks))
print("at samples  :", peaks[:6], "...")
print("at times    :", np.round(t[peaks][:6], 2), "seconds")
"""),

    code("""
plt.figure(figsize=(11, 3))
plt.plot(t, signal, linewidth=0.8, label="signal")
plt.plot(t[peaks], signal[peaks], "o", markersize=6, label="detected R peaks")
plt.xlabel("time (seconds)")
plt.ylabel("mV")
plt.title("Ten seconds, with every beat marked")
plt.legend()
plt.show()
"""),

    md("""
## 9. From peaks to a heart rate  *(slide 44)*

The gap between consecutive peaks is one heartbeat. `np.diff` gives the
differences between neighbouring elements.
"""),
    predict("We asked for 72 bpm. What do you expect the estimate to be?"),
    code("""
gaps_in_samples = np.diff(peaks)
gaps_in_seconds = gaps_in_samples / 250          # 250 samples per second

print("gaps (seconds) :", np.round(gaps_in_seconds, 3))
print("mean gap       : {:.3f} s".format(gaps_in_seconds.mean()))
print("estimated rate : {:.1f} bpm".format(60 / gaps_in_seconds.mean()))
"""),

    md("""
You have just measured a heart rate from a raw signal, using nothing but
arithmetic on arrays. No loops.

That is the shape of most signal work: build a mask, find the positions,
measure the gaps.
"""),
    code("""
# Ten seconds at 72 bpm is 12 beats. Let the notebook check its own claim.
assert 11 <= len(peaks) <= 13, "expected about 12 beats, found {}".format(len(peaks))
assert 70 <= 60 / gaps_in_seconds.mean() <= 74

print("the estimate agrees with what we asked for")
"""),

    md("""
### Deliberate error four

Asking for a sample that is not there.
"""),
    breaks("""
print(signal[5000])
"""),

    md("""
`IndexError: index 5000 is out of bounds for axis 0 with size 2500`

The message tells you the size of the thing you indexed. When you meet this in
real work it usually means an off-by-one, or an assumption about length that
was never true.
"""),

    md("""
---

## Your turn  *(slide 45)*

Core tasks first. Work in your pair and swap roles halfway: one explains, the
other types.

For each method, write a comment saying what it does, then code showing it.
Explaining it is the part that makes it stick.
"""),

    code("""
# 1. Make an array of 20 evenly spaced values between 0 and 5 using linspace.
#    Print it, its shape, and its size.

"""),
    code("""
# 2. Generate a 30-second ECG at 90 bpm. Print ndim, shape, size, itemsize
#    and dtype.

"""),
    code("""
# 3. Print the mean, std, min, max and sum of that signal.

"""),
    code("""
# 4. How many samples are above 0.5 mV? Use a boolean mask, not a loop.
#    What fraction of the recording is that?

"""),
    code("""
# 5. Find the R peaks in your 90 bpm signal and check the count is what you
#    would expect from 30 seconds at 90 beats per minute.

"""),
    code("""
# 6. Estimate the heart rate from the peaks. How close is it to 90?

"""),
    code("""
# 7. Print the cumulative sum of the first 10 samples. In one sentence,
#    say what a running total of a signal tells you.

"""),
    code("""
# 8. Now structure it. Write a function
#
#        def describe(bpm, seconds=30):
#
#    that simulates a signal, finds its peaks, and returns three things:
#    the number of peaks, the estimated rate, and the maximum voltage.
#    Call it for 60, 90 and 120 bpm.

"""),

    md("""
### Check your own work

Once task 8 runs, this cell should print one line and complain about nothing.
If it fails, read which `assert` failed. That tells you which part of
`describe` is wrong.
"""),
    code("""
if "describe" not in dir():
    print("Write describe() in task 8 first, then run this cell again.")
else:
    count, rate, tallest = describe(90, seconds=30)

    assert count == len(r_peaks(simulate(seconds=30, bpm=90)[1]))
    assert 88 <= rate <= 92, "rate came back as {}".format(rate)
    assert tallest > 0.6

    print("describe() looks right: {} peaks, {:.1f} bpm".format(count, rate))
"""),

    md("""
### Stretch

Full descriptions are in
[`../stretch-tasks.md`](../stretch-tasks.md). In short: plot the signal with
its peaks marked, break the peak finder by moving the threshold, add noise
until the heart rate estimate fails, and time a loop against a vectorised
operation.

The noise one is the most interesting. Every real measurement has a level of
noise beyond which it stops working, and finding that level yourself is a
genuine experiment rather than an exercise.
"""),

    checkpoint("Pace check in Slidea before you go: green, amber or red."),

    md("""
---

## Before you close the laptop

**Restart & Run All.** It should run clean, top to bottom, apart from the four
cells we broke on purpose.

Attempt the tasks before Wednesday's review, even if you do not finish.
Struggling with a problem first and then seeing the solution is worth several
times more than watching the solution first. That is not motivational talk; it
is the reason the sessions are ordered this way.

Next session: **Wednesday 12 August, pandas**. Tables built on top of the
arrays you just learned.
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
