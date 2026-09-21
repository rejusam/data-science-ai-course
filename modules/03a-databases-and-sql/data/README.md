# `bikeshare.db` — the SQL practice database

A single SQLite file, **2.2 MB, 19,478 rows across 7 tables and 1 view.**
Built by `tools/build_practice_database.py` in the course repo.

Use it with `15-sql-practice.ipynb` (21 self-marking exercises) or on its
own with any SQLite tool.

## Opening it — four ways, all free, none needing an account

| | How |
|---|---|
| **Python** | `sqlite3.connect("data/bikeshare.db")` — the `sqlite3` module is in the standard library |
| **DB Browser for SQLite** | Free desktop app, <https://sqlitebrowser.org/>. Open the file, use the *Execute SQL* tab |
| **VS Code** | Install the "SQLite" or "SQLite Viewer" extension, then click the file |
| **Browser only** | <https://sqliteonline.com/> → *File* → *Open DB* → pick the file. Nothing installed |

You do **not** need to install SQLite from sqlite.org, and you do **not**
need a Mode or ThoughtSpot account.

## Where the data comes from

Every row is real. Nothing is generated.

| Table | Source |
|---|---|
| `rides_daily`, `rides_hourly` | UCI Bike Sharing Dataset (Fanaee-T & Gama) — Capital Bikeshare, Washington D.C., 2011–2012 |
| `weather`, `season`, `year_lookup` | Code definitions transcribed verbatim from that dataset's `Readme.txt` |
| `stations` | A real Capital Bikeshare GBFS `station_information` feed, 858 stations |
| `housing` | The Boston housing dataset — the same file notebook 12 and Lab 2.2.2 use |

**On the `housing` table's `B` column:** it is derived from the
proportion of Black residents by town and was built into a model of house
price. scikit-learn removed its `load_boston` loader in version 1.2 for
exactly this reason. It is included because the labs use this dataset; do
not model with it. That a famous teaching dataset can carry an ethical
defect is itself part of the course.

## Schema

### `rides_daily` — 731 rows, one per day

`dteday` **PK** (TEXT, `'YYYY-MM-DD'`)

| Column | Type | Notes |
|---|---|---|
| `season_id` | INTEGER | → `season` |
| `year_id` | INTEGER | → `year_lookup` (0 = 2011, 1 = 2012) |
| `mnth` | INTEGER | 1–12 |
| `holiday`, `workingday` | INTEGER | 0 or 1 |
| `weekday` | INTEGER | 0–6 |
| `weather_id` | INTEGER | → `weather` |
| `temp`, `atemp`, `hum`, `windspeed` | REAL | **normalised** — see below |
| `casual`, `registered`, `cnt` | INTEGER | `casual + registered = cnt`, always |

### `rides_hourly` — 17,379 rows, one per hour

Same columns plus `hr` (0–23). **Composite primary key `(dteday, hr)`** —
a date alone is not unique here. `dteday` is a foreign key to
`rides_daily`.

### `stations` — 858 rows

| Column | Type | Notes |
|---|---|---|
| `station_id` | TEXT **PK** | GBFS UUID |
| `name` | TEXT | e.g. "Reston Town Center Metro South" |
| `short_name` | TEXT | |
| `region_id` | INTEGER | **NULL for 54 stations** — see below |
| `capacity` | INTEGER | 7 to 55 |
| `lat`, `lon` | REAL | |
| `has_kiosk` | INTEGER | 0 or 1 |

### `housing` — 506 rows

`town_id` **PK**, then the 14 standard Boston columns: `CRIM`, `ZN`,
`INDUS`, `CHAS`, `NOX`, `RM`, `AGE`, `DIS`, `RAD`, `TAX`, `PTRATIO`,
`B`, `LSTAT`, `MEDV`.

### Lookups

`weather` (4 rows), `season` (4), `year_lookup` (2). The weather
descriptions are the dataset's own wording:

| `weather_id` | `label` | `description` |
|---|---|---|
| 1 | Clear | Clear, Few clouds, Partly cloudy, Partly cloudy |
| 2 | Mist | Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist |
| 3 | Light rain or snow | Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds |
| 4 | Heavy rain or snow | Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog |

`season`: 1 Spring, 2 Summer, 3 Fall, 4 Winter. *(The source readme
writes "springer" for 1 — that is its own typo.)*

### `daily_summary` — a VIEW, 731 rows

Joins `rides_daily` to all three lookups and converts temperature to
Celsius, so you can see what a view buys before you write the joins
yourself. Slide 66 covers views.

```sql
SELECT * FROM daily_summary LIMIT 5;
```

## Two things about the data worth knowing before you start

**1. Weather code 4 never appears in `rides_daily`.** It exists in the
`weather` lookup and it does appear in `rides_hourly` (223 rides), but
no whole day was classified as heavy rain or snow.

This makes `INNER JOIN` and `LEFT JOIN` genuinely differ on real data:

```sql
-- 3 rows: code 4 vanishes
SELECT w.label, COUNT(d.dteday) FROM weather w
JOIN rides_daily d ON w.weather_id = d.weather_id GROUP BY w.label;

-- 4 rows: code 4 appears, with a count of 0
SELECT w.label, COUNT(d.dteday) FROM weather w
LEFT JOIN rides_daily d ON w.weather_id = d.weather_id GROUP BY w.label;
```

**2. 54 of the 858 stations have `region_id = NULL`.** That is how the
source feed ships. It is not a loading error, and it is there so you can
practise on real missing data:

```sql
SELECT COUNT(*) FROM stations WHERE region_id IS NULL;   -- 54
SELECT COUNT(*) FROM stations WHERE region_id = NULL;    -- 0, always
```

The second query returns nothing no matter what the data holds, because
nothing is ever `= NULL`. Use `IS NULL`.

There are no region *names* in this database. The GBFS feed we have
carries only IDs; the file that maps them to names
(`system_regions.json`) was not captured, so no name table has been
invented.

## The normalised columns

Four columns are pre-scaled by the original dataset's authors. To read
them as real units:

| Column | Multiply by | To get |
|---|---|---|
| `temp` | 41 | degrees Celsius |
| `atemp` | 50 | "feels like" Celsius |
| `hum` | 100 | % humidity |
| `windspeed` | 67 | the source's wind speed units |

```sql
SELECT dteday, ROUND(temp * 41, 1) AS celsius FROM rides_daily LIMIT 5;
```

## Integrity guarantees

The build script asserts all of these before the file is written. Every
one passed:

- `rides_daily` and `rides_hourly` both sum to **3,292,679** rides.
- `casual + registered = cnt` in every row of both tables — 0 violations.
- Every `rides_hourly.dteday` exists in `rides_daily` — 0 orphans.
- `PRAGMA foreign_key_check` returns nothing.
- Row counts: 731 / 17,379 / 858 / 506 / 4 / 4 / 2.

Foreign keys, `CHECK` constraints and two indexes are declared in the
schema. **Remember that SQLite only enforces foreign keys when you ask
it to** — per connection:

```sql
PRAGMA foreign_keys = ON;
```

Notebook 14 §5 covers why that is off by default and what else SQLite
does not enforce.

## Breaking it safely

It is a file. Copy it and wreck the copy:

```python
import shutil
shutil.copy("data/bikeshare.db", "my-sandbox.db")
```

Then try `UPDATE` with no `WHERE`, `DELETE FROM rides_daily`, or an
`INSERT` that violates a `CHECK`. You cannot damage anything, and the
error messages are the lesson.

## Rebuilding

```bash
python3 tools/build_practice_database.py
```

Needs `bikeshare-day.csv`, `bikeshare-hour.csv`,
`capitalbikeshare-stations.json` and `housing.data` in `data/`. It
verifies 17 properties and refuses to produce a file if any fail.
