# Programming fundamentals

Plan label: `Module 1 Pt 1`. Weeks 1-2.

## Sessions

| Date | Focus | Lab / activity |
|---|---|---|
| Wed, 5 Aug 2026 | Programming fundamentals: Python syntax, types, control flow, functions, notebooks workflow | Lab 1.1 Python basics; pair-programming in breakouts |
| Mon, 10 Aug 2026 | NumPy: arrays, vectorisation, broadcasting, random numbers | Lab 1.2.1 NumPy |
| Wed, 12 Aug 2026 | Pandas: Series/DataFrame, indexing, merge/join, groupby, reshaping | Lab 1.2.2 Pandas (employee-attrition.csv) |
| Sat, 15 Aug 2026 | Consolidation clinic: Python/NumPy/Pandas walkthrough + Q&A; start Maths & Stats for DS (linear algebra basics) | Lab review & debugging clinic; Training Plan workshop; prework check |

## What this module covers

- Programming fundamentals: Python syntax, types, control flow, functions, notebooks workflow
- NumPy: arrays, vectorisation, broadcasting, random numbers
- Pandas: Series/DataFrame, indexing, merge/join, groupby, reshaping
- Consolidation clinic: Python/NumPy/Pandas walkthrough + Q&A
- start Maths & Stats for DS (linear algebra basics)

## Labs and activities

- Lab 1.1 Python basics; pair-programming in breakouts
- Lab 1.2.1 NumPy
- Lab 1.2.2 Pandas (employee-attrition.csv)
- Lab review & debugging clinic; Training Plan workshop; prework check

## How to get the most out of these sessions

- Re-type every demo yourself rather than copying; bring 1 question to the 30-min post-lecture support
- Attempt the lab before the review session - struggle first, then watch the solution
- Use your own dataset of interest for 15 min of practice - relevance drives retention
- Complete your Training Plan with concrete goals and book a 1:1 - students with a written plan finish the capstone

## Folders

- `notebooks/` — worked examples and lab notebooks
- `data/` — datasets used by this module

## Before you start

Activate the course environment:

```
conda activate dsai
```

Then start Jupyter from the repository root:

```
jupyter lab
```

## Notebooks and materials

| File | What it is |
|---|---|
| [`notebooks/lab-1-1-python-basics.ipynb`](notebooks/lab-1-1-python-basics.ipynb) | Session 2 live-coding notebook and Lab 1.1 |
| [`notebooks/lab-1-2-1-numpy.ipynb`](notebooks/lab-1-2-1-numpy.ipynb) | Session 3 live-coding notebook and Lab 1.2.1 |
| [`ecg_signal.py`](ecg_signal.py) | Generates the simulated ECG signal used in the NumPy session |
| [`stretch-tasks.md`](stretch-tasks.md) | Extra work for all three labs, for when the core is done |

Read [`../../resources/notebook-hygiene.md`](../../resources/notebook-hygiene.md)
before the first lab. It is one page and it prevents the most common source of
confusion with notebooks.

`ecg_signal.py` is worth reading rather than only importing. It is about eighty
lines and, by the end of session 2, uses nothing you have not been taught. The
signal is entirely synthetic, built from mathematical curves. No patient data
is used anywhere in this course.
