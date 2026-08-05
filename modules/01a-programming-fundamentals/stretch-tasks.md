# Stretch tasks

For when the core lab is finished and you want more. There is no prize for
rushing to get here, and no penalty for not reaching it. The core tasks are the
ones that matter.

Each stretch task uses only what the session covered. None of them need
anything you have not been taught.

---

## Lab 1.1 — Python basics

The stretch tasks are at the bottom of the Lab 1.1 notebook, which is
published here after the session.

In short: write an averaging function without `sum()` or `len()`, make
`classify_rate` take optional boundaries with sensible defaults, and filter and
sort the cohort list.

---

## Lab 1.2.1 — NumPy

The session uses a simulated ECG signal. `ecg_signal.py` in this folder
generates it, and it is worth reading — it is about eighty lines and uses only
things you now know.

```python
from ecg_signal import simulate, r_peaks, heart_rate
t, signal = simulate(seconds=10, bpm=72)
```

**1. Plot it.** Use `matplotlib` to plot `signal` against `t`. Then mark the R
peaks on top with a scatter plot, using the indices `r_peaks` gives you. A
signal with its detected peaks marked is a genuinely useful diagnostic picture.

**2. Break the peak finder.** `r_peaks` takes a `threshold`. Find a value that
misses real beats, and one that reports beats that are not there. Then work out
why the default of 0.6 sits where it does.

**3. Add noise until it fails.** `simulate` takes a `noise` argument. Increase
it in steps and find the level at which `heart_rate` stops returning something
close to the bpm you asked for. This is a real question about a real method:
every measurement has a noise level beyond which it stops working.

**4. Vectorise a loop.** Write a loop that squares every element of an array,
then do the same with `signal ** 2`. Time both with `%timeit`. Report the
factor. This is the reason NumPy exists, and seeing the number yourself is
worth more than being told.

**5. Without a loop:** how many samples are above 0.5 mV? What fraction of the
recording is that? Use boolean indexing, not iteration.

---

## Lab 1.2.2 — Pandas

The core lab uses `employee-attrition.csv`.

**1. Ask your own question.** Write down a question about the dataset **before**
you touch it. Then answer it with pandas. Writing the question first is the
habit; it stops the data from leading you somewhere uninteresting.

**2. `loc` versus `iloc`.** Construct one example where `df.loc[1:3]` and
`df.iloc[1:3]` return different numbers of rows. Explain why in a markdown cell,
in your own words. This is the most common pandas confusion and explaining it
is how you stop being confused by it.

**3. Group and compare.** Use `groupby` to compare attrition rates across two
different columns. Which one separates the groups more? Say how you decided.

**4. Missing values.** Find any columns with missing values. For one of them,
argue for a way of handling it, and say what you would lose by doing that.
There is rarely a single right answer, and the reasoning is the assessable part.

**5. Your own dataset.** Load something you actually care about — from your
work, a hobby, a public dataset. Run `head`, `info` and `describe`, and write
three sentences about what you found. The delivery plan asks for fifteen
minutes on your own data this week, and relevance is what makes any of this
stick.
