# Tools

Small, tested utilities used by the course notebooks.

| File | What it does |
|---|---|
| `slidea.py` | Parses a Slidea poll export into tidy DataFrames |
| `build_cohort_notebook.py` | Generates `modules/00-orientation/notebooks/your-cohort-in-data.ipynb` |
| `build_01_python_basics.py` | Generates the session 2 notebook |
| `build_02_numpy.py` | Generates the session 3 notebook |
| `build_03_pandas.py` | Generates the session 4 notebook |
| `build_04_code_quality.py` | Generates the session 5 notebook |
| `tests/` | Tests for the above |

Every notebook in `modules/` is a build artefact. **Edit the script, never the
`.ipynb`.** Each build script holds the same content as its notebook, so a
notebook and its script are published together or held back together.

```
python3 -m pytest tools/tests -q
```

## About slidea.py

A Slidea export is one Excel sheet holding about twenty-five stacked blocks,
each shaped differently depending on the poll type: multiple choice, ranking,
scales, word cloud, open ended. Column headers are not on the first row,
percentages are text, and blank rows separate the blocks.

`load_export()` turns that into two tidy frames, `responses` and `scales`,
plus a `meta` dictionary. Everything downstream is then straightforward.

It is worth reading if you want to see what real data cleaning looks like
before the course gets there formally in modules 2 and 3.

## Privacy

`slidea.py` reads the `Summary Report` and `Response Details` sheets only. It
never reads `Leaderboard`, which contains participant display names. A test
asserts that no name from the Leaderboard can appear in parsed output.

Raw exports are not committed to this repository. The CSVs under
`modules/00-orientation/data/` are aggregate counts only, with the study-code
question removed.

## Regenerating the notebook

The notebook is a build artefact. Edit `build_cohort_notebook.py`, then:

```
python3 tools/build_cohort_notebook.py
```
