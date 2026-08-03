# Orientation and the toolchain

Plan label: `Module 0`. Week 1.

## Sessions

| Date | Focus | Lab / activity |
|---|---|---|
| Mon, 3 Aug 2026 | Welcome & orientation; how the 25 weeks work; assessment & attendance (90% min); toolchain: Anaconda/Jupyter, VS Code, Google Colab, Git/GitHub | Guided environment setup; live ice-breaker poll (Slidea); Classroom + Slack + timetable tour |

## What this module covers

- Welcome & orientation
- how the 25 weeks work
- assessment & attendance (90% min)
- toolchain: Anaconda/Jupyter, VS Code, Google Colab, Git/GitHub

## Labs and activities

- Guided environment setup; live ice-breaker poll (Slidea); Classroom + Slack + timetable tour

## How to get the most out of these sessions

- Turn camera on, introduce yourself in Slack, bookmark Classroom + this timetable, install everything tonight - do not fall behind on setup.  make sure you are in a good environment: comfortable, minimal distractions

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

## Notebooks

| Notebook | What it does |
|---|---|
| [`your-cohort-in-data.ipynb`](notebooks/your-cohort-in-data.ipynb) | Takes the session 1 poll export, cleans it, and shows the cohort what it looks like as data |

`your-cohort-in-data.ipynb` is worth running even if you saw it in class. It
goes from a genuinely messy spreadsheet to ten charts, and every step is one
you will learn to do yourself between weeks 2 and 5.

It runs from the tidy CSVs in `data/`, so it works without the original
export. Those CSVs hold aggregate counts only. No names, and no study codes.
