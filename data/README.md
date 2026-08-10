# Shared datasets

Datasets used by more than one module live here. Anything specific to a single
module lives in that module's own `data/` folder instead.

## `employee-attrition.csv`

Ten years of fictitious HR records from a retail chain: one row per employee per
year, marked active or terminated.

| | |
|---|---|
| Source | [kaggle.com/HRAnalyticRepository/employee-attrition-data](https://www.kaggle.com/HRAnalyticRepository/employee-attrition-data) |
| Author | Lyndon Sundmark |
| Licence | CC0: Public Domain |
| Size | 7,318,626 bytes |
| Shape | 49,653 rows, 18 columns |
| Missing values | none |

The dataset page says it is "fictitious/fake data", so nobody in it is real. It is
redistributed here under CC0 so that the course works without a Kaggle account
and without a download, including in Colab and on a locked-down computer.

Used in module 1 (pandas) and again in module 2 (exploratory data analysis).

### Getting it from Kaggle yourself

Worth doing once, because most public data lives behind a page like this one and
reading that page is part of the job.

1. Make a free account at [kaggle.com](https://www.kaggle.com).
2. Open the dataset link above.
3. Read the **Licence** on the right-hand side before anything else. CC0 means
   you can use and redistribute it freely. Not every dataset says that, and the
   licence decides what you are allowed to publish in your own repository.
4. **Download**, unzip, and compare it with the copy here.

### Columns

| Column | What it is |
|---|---|
| `EmployeeID` | identifier, repeats across years; 6,284 people across 49,653 rows |
| `recorddate_key` | the snapshot date this row describes, as text |
| `birthdate_key`, `orighiredate_key`, `terminationdate_key` | dates, as text |
| `age`, `length_of_service` | years |
| `city_name`, `department_name`, `job_title`, `store_name` | where they worked |
| `gender_short`, `gender_full` | the same field twice, in two formats |
| `termreason_desc`, `termtype_desc` | why they left, blank-equivalent while active |
| `STATUS_YEAR` | 2006 to 2015 |
| `STATUS` | `ACTIVE` or `TERMINATED` |
| `BUSINESS_UNIT` | `STORES` or `HEADOFFICE` |

Three things in this file are worth noticing rather than tidying away.

`termreason_desc` says `Resignaton`, missing an `i`, a spelling mistake baked
into the source data.

`terminationdate_key` reads `1/1/1900` on 42,450 of the 48,168 active rows. It
is a placeholder standing in for "no date", not a real date.

The other 5,718 active rows carry a genuine termination date: the file was
assembled after the fact, so a person's eventual leaving date appears on their
earlier active rows too. A model predicting `STATUS` from that column would
score beautifully and be worthless, because the column already contains the
answer. That is called target leakage, and this is a clean example of it.
