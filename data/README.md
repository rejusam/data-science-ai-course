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

## `penguins_size.csv`

Body measurements of 344 penguins from three islands in the Palmer
Archipelago, Antarctica, one row per bird.

| | |
|---|---|
| Source | [kaggle.com/datasets/parulpandey/palmer-archipelago-antarctica-penguin-data](https://www.kaggle.com/datasets/parulpandey/palmer-archipelago-antarctica-penguin-data) |
| Collected by | Dr Kristen Gorman and the Palmer Station, Antarctica LTER |
| Licence | CC0: Public Domain |
| Cite as | Gorman KB, Williams TD, Fraser WR (2014). Ecological Sexual Dimorphism and Environmental Variability within a Community of Antarctic Penguins (Genus *Pygoscelis*). PLoS ONE 9(3): e90081 |
| Size | 13,519 bytes |
| Shape | 344 rows, 7 columns |

The Kaggle page has a second file, `penguins_lter.csv`, with 17 columns and
longer names. This course uses `penguins_size.csv`.

Used in module 7 (decision trees).

### Columns

| Column | What it is |
|---|---|
| `species` | `Adelie` (152), `Gentoo` (124), `Chinstrap` (68) |
| `island` | `Biscoe`, `Dream` or `Torgersen` |
| `culmen_length_mm`, `culmen_depth_mm` | bill length and depth. The culmen is the top ridge of the bill |
| `flipper_length_mm` | millimetres |
| `body_mass_g` | grams |
| `sex` | `MALE` or `FEMALE` |

Two things in this file are worth noticing rather than tidying away.

Two birds have no measurements at all: all four number columns are empty.

`sex` is empty for 10 birds, and one more has a full stop (`.`) where the
sex should be. That is a gap written as text, so `isna()` does not count it.

## `nz_crashes_2023.csv`

Every crash reported to NZ Police in 2023, one row per crash, with 12 of the
70 fields in the Crash Analysis System (CAS).

| | |
|---|---|
| Source | Waka Kotahi NZ Transport Agency, Crash Analysis System (CAS), [nzta.govt.nz/safety/partners/crash-analysis-system](https://www.nzta.govt.nz/safety/partners/crash-analysis-system/) |
| Licence | CC BY 4.0. Reuse is allowed with credit to Waka Kotahi NZ Transport Agency |
| Downloaded | 19 October 2026, from the public `CAS_Data_Public` ArcGIS layer |
| Size | 2,175,795 bytes |
| Shape | 31,511 rows, 12 columns |
| Missing values | `speedLimit` 169, `NumberOfLanes` 171 |

CAS is updated every month and older records can still change, so a fresh
download will not match this file exactly. This copy is kept fixed so that
everyone gets the same numbers.

Used in module 7 (decision trees workshop).

### Columns

| Column | What it is |
|---|---|
| `crashYear` | 2023 for every row |
| `crashSeverity` | the worst injury: `Fatal Crash` (305), `Serious Crash` (2,086), `Minor Crash` (8,571), `Non-Injury Crash` (20,549) |
| `speedLimit` | km/h, from 5 to 110 |
| `light` | `Bright sun`, `Overcast`, `Twilight`, `Dark` or `Unknown` |
| `weatherA` | `Fine`, `Light rain`, `Heavy rain`, `Mist or Fog`, `Hail or Sleet`, `Snow` or `Null` |
| `roadSurface` | `Sealed`, `Unsealed`, `End of seal` or `Null` |
| `urban` | `Urban` or `Open` (open road) |
| `flatHill` | `Flat`, `Hill Road` or `Null` |
| `NumberOfLanes` | lanes on the road |
| `motorcycle`, `bicycle`, `truck` | how many were involved; 0 means none |

Two things in this file are worth noticing rather than tidying away.

`Null` and `Unknown` are written as text, so `isna()` does not count them.
They mean the police report did not record that detail.

`urban` follows the speed limit exactly: every crash at 70 km/h or below is
`Urban`, every crash at 80 km/h or above is `Open`. The two columns carry the
same information.
