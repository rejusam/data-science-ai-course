"""Assemble the session 3 live-coding notebook, Lab 1.2.1 (NumPy).

    python3 tools/build_lab_1_2_1.py

The notebook is a build artefact. Edit this file, not the .ipynb.

`ecg_signal.py` is inlined into a setup cell rather than imported, because
Colab cannot see files from the repository. The source is presented as
something to read, not hidden: by the end of session 2 it uses nothing the
students have not been taught.
"""
from pathlib import Path

import nbformat as nbf

REPO = Path(__file__).resolve().parent.parent
MODULE = REPO / "modules" / "01a-programming-fundamentals"
OUTPUT = MODULE / "notebooks" / "lab-1-2-1-numpy.ipynb"


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
# Lab 1.2.1 — NumPy

Data Science & AI, session 3.

Last session you used a Python list to hold five heart-rate readings. Tonight
you will hold two and a half thousand, do arithmetic on all of them at once
without writing a loop, and find every heartbeat in the recording.

NumPy is the foundation everything else in this course sits on. pandas is built
on it. scikit-learn is built on it. Every array of numbers you touch for the
next twenty-four weeks is a NumPy array underneath.

**Restart & Run All before you start.** Same rule as last week.
"""),

    code(SETUP.format(ecg_source())),

    md("""
## 1. Why NumPy exists

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
## 2. Making arrays

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
## 3. What an array knows about itself

Every attribute Lab 1.2.1 asks about, on one array.
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
"""),

    md("""
`shape` is a tuple, which is why it prints with brackets. `(2, 3)` means two
rows and three columns.

**Axis 0 runs down the rows. Axis 1 runs across the columns.** Getting these
the wrong way round is the most common NumPy mistake, and you will meet it
again in pandas next session.
"""),
    code("""
print("sum of everything :", grid.sum())
print("sum down columns  :", grid.sum(axis=0))   # one result per column
print("sum across rows   :", grid.sum(axis=1))   # one result per row
"""),

    md("""
### Deliberate error one

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
## 4. Arithmetic without loops

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
### Deliberate error two

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

    md("""
## 5. A real signal

Now something with more than five numbers in it.

`simulate` builds a synthetic ECG: a heart trace, made of mathematical curves.
It is not recorded from anyone. It gives back two arrays — the time of each
measurement, and the voltage at that time.
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
The tall spikes are R peaks — one per heartbeat. Counting them over a known
duration is how you measure heart rate, and that is what the rest of this
notebook builds up to.
"""),

    md("""
## 6. Summarising

Every aggregation from the lab list, on real data.
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

`cumsum` is the running total — every value is the sum of everything up to that
point.
"""),
    predict("What is `np.cumsum([1, 2, 3, 4])`?"),
    code("""
print(np.cumsum([1, 2, 3, 4]))
"""),

    md("""
## 7. Boolean indexing

This is the most useful idea in NumPy, and it replaces most loops you would
otherwise write.

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

On the signal:
"""),
    code("""
high = signal > 0.6

print("samples above 0.6 mV :", high.sum())
print("as a fraction        : {:.2%}".format(high.mean()))
print("largest 5 values     :", np.round(np.sort(signal)[-5:], 3))
"""),

    md("""
## 8. `np.where`, and finding the heartbeats

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
## 9. From peaks to a heart rate

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

    md("""
### Deliberate error three

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

## Lab 1.2.1 — your turn

Core tasks first. Work in your pair, swap roles halfway.

The deck asks you to explain each method and give a working example. Do both:
a comment saying what it does, then code showing it.
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

    md("""
---

## Before you close the laptop

**Restart & Run All.** It should run clean, top to bottom.

Attempt the lab before Wednesday's review, even if you do not finish. Struggling
with a problem first and then seeing the solution is worth several times more
than watching the solution first. That is not motivational talk; it is the
reason the labs are scheduled this way.

Next session: **Wednesday 12 August, pandas** — tables built on top of the
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
