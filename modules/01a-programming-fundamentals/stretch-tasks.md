# Stretch tasks

For when the core work is finished and you want more. There is no prize for
rushing to get here, and no penalty for not reaching it. The core tasks are the
ones that matter.

Each stretch task uses only what the session covered. None of them need
anything you have not been taught.

---

## Session 2 — Python basics

The stretch tasks are at the bottom of `notebooks/01-python-basics.ipynb`.

In short: write an averaging function without `sum()` or `len()`, rewrite a
counting loop as a `while` loop and argue which reads better, and filter and
sort the cohort list.

---

## Session 3 — NumPy

The session uses a simulated ECG signal. `ecg_signal.py` in this folder
generates it, and it is worth reading: it is about eighty lines and uses only
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

## Session 4 — pandas

The core work uses `data/employee-attrition.csv`.

**1. Ask your own question.** Write down a question about the dataset **before**
you touch it. Then answer it with pandas. Writing the question first is the
habit; it stops the data from leading you somewhere uninteresting.

**2. `loc` versus `iloc`.** Construct one example where `df.loc[1:3]` and
`df.iloc[1:3]` return different numbers of rows. Explain why in a markdown cell,
in your own words. This is the most common pandas confusion and explaining it is
how you stop being confused by it.

**3. Rates, not counts.** Terminations per year is a count, and counts follow
headcount. Divide by the number of people employed each year and plot the rate
instead. Does 2014 still stand out?

**4. Missing values that are not missing.** `info()` reports no nulls at all,
and the file still has gaps in it. They are just wearing a disguise.
`termreason_desc` says `Not Applicable`, and `terminationdate_key` says
`1/1/1900`. Find every value in this file that means "no value", say how you
would represent each one, and say what you would lose by converting it to `NaN`.

**5. Your own dataset.** Load something you actually care about, from your
work, a hobby, a public dataset. Run `head`, `info` and `describe`, and write
three sentences about what you found. The delivery plan asks for fifteen
minutes on your own data this week, and relevance is what makes any of this
stick.

---

## Session 5 — code quality and testing

**1. Your own module.** Move the `Patient` class into `patient.py` next to the
pytest demo, write `test_patient.py` with four tests, and make them pass.

**2. The edge case nobody wrote.** Add a test for `summarise` on a list with one
item. Decide what it *should* do before you check what it *does*.

**3. A threshold that moves.** `heart_rate.py` has no test for `count_unusual`
with non-default thresholds. Write one.

**4. Refactor something of your own.** Take any cell you wrote in sessions 2 to
4 that repeats itself, turn the repetition into a function, and prove the
results are unchanged with an `assert` before and after. That proof is the
difference between refactoring and hoping.

**5. Noise, again, with a test.** The noisy recording in session 5 reports about
387 bpm for a 72 bpm signal, and nothing errors. Write a test that would have
caught it: a rate outside 30 to 200 is not a plausible resting heart rate. Then
decide where that check belongs: in `r_peaks`, in the rate calculation, or in
the caller.
