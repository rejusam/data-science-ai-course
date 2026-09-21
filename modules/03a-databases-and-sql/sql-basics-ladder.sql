-- =====================================================================
-- SQL FROM ZERO — 22 steps, each adding ONE new idea
--
-- For teaching the first session, and for learning it yourself.
-- Open data/bikeshare.db in DB Browser for SQLite -> "Execute SQL" tab.
-- Paste this file in. Select ONE step, press Cmd+Return (Ctrl+Return on
-- Windows). DB Browser runs only what you selected.
--
-- Every result below was produced by running the query on 9 Sep 2026.
--
-- Steps 1-8    reading rows
-- Steps 9-14   maths over many rows
-- Steps 15-18  putting tables together
-- Steps 19-22  the things that catch everyone
-- =====================================================================


-- =====================================================================
-- FIRST, THE THREE WORDS
--
--   TABLE   a grid of data. Like one sheet in Excel.
--   ROW     one record going across. One day. One station.
--   COLUMN  one field going down. Every day's temperature.
--
-- A query asks: WHICH ROWS, and WHICH COLUMNS OF THEM?
-- That is the whole of SELECT. Everything else is detail.
-- =====================================================================


-- ---------------------------------------------------------------------
-- STEP 1.  Show me everything.
--
--   SELECT = "give me these columns"
--   *      = "all of them"
--   FROM   = "out of this table"
--   LIMIT 5= "only the first 5 rows, I do not want all 731"
--
-- ALWAYS put LIMIT on your first look at a table. Always.
-- ---------------------------------------------------------------------
SELECT * FROM rides_daily LIMIT 5;


-- ---------------------------------------------------------------------
-- STEP 2.  Ask for the columns you actually want.
--
-- Instead of *, name them, separated by commas.
-- Result: 5 rows, 3 columns.
-- ---------------------------------------------------------------------
SELECT dteday, cnt, temp
FROM rides_daily
LIMIT 5;


-- ---------------------------------------------------------------------
-- STEP 3.  Rename a column for the reader, with AS.
--
-- The table is unchanged. This only renames it in the OUTPUT.
-- Result headers read: date | rides
-- ---------------------------------------------------------------------
SELECT dteday AS date,
       cnt    AS rides
FROM rides_daily
LIMIT 5;

SELECT dteday AS date,
       cnt    AS rides, temp
FROM rides_daily
LIMIT 5;

SELECT dteday AS date, cnt    AS rides, temp FROM rides_daily LIMIT 5;
select dteday as date, cnt    as rides, temp from rides_daily limit 5;
-- ---------------------------------------------------------------------
-- STEP 4.  Pick rows with a condition: WHERE.
--
-- "Only the rows where this is true."
-- Result: 12 rows. Every day busier than 8000 rides.
-- ---------------------------------------------------------------------
SELECT dteday, cnt
FROM rides_daily
WHERE cnt > 8000;

--   >   greater than        <   less than
--   >=  greater or equal    <=  less or equal
--   =   equal to            !=  not equal to

SELECT COUNT(*)
FROM rides_daily
WHERE cnt > 8000;

SELECT COUNT(*) AS days_over_8000
FROM rides_daily
WHERE cnt > 8000;
-- It ignores all NULL (missing) values
SELECT COUNT(windspeed) FROM rides_daily WHERE cnt > 8000;

SELECT COUNT(*) cnt FROM rides_daily;
-- If you add the word DISTINCT before a column name, SQL will only count the unique
SELECT COUNT(DISTINCT cnt) cnt FROM rides_daily;


-- ---------------------------------------------------------------------
-- STEP 5.  Text goes in single quotes. Numbers do not.
--
-- Result: 1 row -> 2012-09-15, 8714 rides. One row, because this table
-- holds exactly one row per date. (rides_hourly would give you 24.)
-- ---------------------------------------------------------------------
SELECT dteday, cnt
FROM rides_daily
WHERE dteday = '2012-09-15';

-- Careful: this is a common beginner error - quotes around a number.
-- It happens to work in SQLite, but do not rely on it.
--     WHERE cnt = '8714'      <- wrong habit
--     WHERE cnt = 8714        <- right


-- ---------------------------------------------------------------------
-- STEP 6.  Two conditions: AND (both true) / OR (either true).
--
-- Result: 12 rows. year_id 1 means 2012.
-- ---------------------------------------------------------------------
SELECT dteday, cnt
FROM rides_daily
WHERE year_id = 1
  AND cnt > 8000;

SELECT dteday, cnt
	FROM rides_daily
		WHERE year_id = 0
			AND cnt > 6000;

-- ---------------------------------------------------------------------
-- STEP 7.  Shortcuts: BETWEEN and IN.
--
-- BETWEEN is inclusive at BOTH ends - 6 AND 8 means 6, 7 and 8.
-- Result: 5 rows shown, 92 underneath (June 30 + July 31 + August 31).
-- ---------------------------------------------------------------------
SELECT dteday, mnth, cnt
FROM rides_daily
WHERE year_id = 1
  AND mnth BETWEEN 6 AND 8
LIMIT 5;

SELECT COUNT(*) AS total_summer_rides
FROM rides_daily
WHERE year_id = 1
  AND mnth BETWEEN 6 AND 8


-- IN = "is it any of these?" - shorter than mnth=6 OR mnth=7 OR mnth=8
-- Result: identical to the query above. Same 92 rows underneath.
SELECT dteday, mnth, cnt
FROM rides_daily
WHERE year_id = 1
  AND mnth IN (6, 7, 8)
LIMIT 5;

SELECT COUNT(*) AS total_summer_rides
FROM rides_daily
WHERE year_id = 1
  AND mnth IN (6, 7, 8);

-- ---------------------------------------------------------------------
-- STEP 8.  Sort with ORDER BY. Add DESC for biggest-first.
--
-- Result: busiest day first -> 2012-09-15, 8714 rides.
-- ---------------------------------------------------------------------
SELECT dteday, cnt
FROM rides_daily
ORDER BY cnt DESC
-- ORDER BY cnt ASC
LIMIT 5;

-- Without DESC it sorts smallest-first.
-- Result: 2012-10-29, 22 rides. (That is Hurricane Sandy.)
SELECT dteday, cnt
FROM rides_daily
ORDER BY cnt
LIMIT 5;


-- =====================================================================
-- Steps 9-14: from "show me rows" to "work something out"
-- =====================================================================

-- ---------------------------------------------------------------------
-- STEP 9.  COUNT - how many rows?
--
-- Result: 731. One number, one row. That is still a table.
-- ---------------------------------------------------------------------
SELECT COUNT(*) AS how_many_days
FROM rides_daily;

-- COUNT respects WHERE, like everything else. Result: 12
SELECT COUNT(*) AS busy_days
FROM rides_daily
WHERE cnt > 8000;


-- ---------------------------------------------------------------------
-- STEP 10.  SUM, AVG, MIN, MAX - the other four.
--
-- These "aggregate": many rows in, ONE number out.
-- Result: 3292679 | 4504.3489... | 22 | 8714
-- ---------------------------------------------------------------------
SELECT SUM(cnt) AS total_rides,
       AVG(cnt) AS average_per_day,
       MIN(cnt) AS quietest,
       MAX(cnt) AS busiest
FROM rides_daily;


-- ---------------------------------------------------------------------
-- STEP 11.  ROUND, so the average is readable.
--
-- ROUND(number, how_many_decimals)
-- Result: 4504.3
-- ---------------------------------------------------------------------
SELECT ROUND(AVG(cnt), 1) AS average_per_day
FROM rides_daily;


-- ---------------------------------------------------------------------
-- STEP 12.  Do arithmetic in SELECT.
--
-- temp is stored divided by 41. Multiply it back to get Celsius.
-- Result: 2011-01-01 -> 14.1 C
-- ---------------------------------------------------------------------
SELECT dteday,
       temp,
       ROUND(temp * 41, 1) AS celsius
FROM rides_daily
LIMIT 5;


-- ---------------------------------------------------------------------
-- STEP 13.  GROUP BY - the big one. Aggregate PER SOMETHING.
--
-- Step 10 gave ONE total for all 731 days.
-- This gives one total PER weather type.
--
-- Read it as: "make a pile for each weather_id, then count each pile."
-- Result: 3 rows -> 1:463 days, 2:247 days, 3:21 days
-- ---------------------------------------------------------------------
SELECT weather_id,
       COUNT(*) AS days,
       SUM(cnt) AS total_rides
FROM rides_daily
GROUP BY weather_id;

-- The rule that makes GROUP BY click:
--   every column in SELECT must either be
--     (a) in the GROUP BY, or
--     (b) inside an aggregate like COUNT/SUM/AVG.
--   Because: what would "the dteday of 463 days" even mean?
-- Wrong:
SELECT weather_id, temp
FROM rides_daily
GROUP BY weather_id;

-- ---------------------------------------------------------------------
-- STEP 14.  DISTINCT - "show me the different values".
--
-- Great for meeting a new column. Result: 1, 2, 3
-- ---------------------------------------------------------------------
SELECT DISTINCT weather_id
FROM rides_daily;

-- Result: 4 rows -> 1, 2, 3, 4. The hourly table has a code the
-- daily table never uses. Worth noticing.
SELECT DISTINCT weather_id
FROM rides_hourly;


-- =====================================================================
-- Steps 15-18: two tables at once
-- =====================================================================

-- ---------------------------------------------------------------------
-- STEP 15.  The problem JOIN solves.
--
-- rides_daily says weather_id = 1. What is 1?
-- The answer lives in a different table.
-- ---------------------------------------------------------------------
SELECT * FROM weather;
--   1 Clear | 2 Mist | 3 Light rain or snow | 4 Heavy rain or snow


-- ---------------------------------------------------------------------
-- STEP 16.  JOIN - glue the two together.
--
--   JOIN weather   =  also bring in the weather table
--   ON  ... = ...  =  match them up using THIS pair of columns
--
-- Result: 5 rows, now with a readable word instead of a code.
-- ---------------------------------------------------------------------
SELECT rides_daily.dteday,
       rides_daily.cnt,
       weather.label
FROM rides_daily
JOIN weather ON rides_daily.weather_id = weather.weather_id
LIMIT 5;


-- ---------------------------------------------------------------------
-- STEP 17.  Nicknames, so it is not so long to type.
--
-- "rides_daily d" means "call it d from now on". Same query as step 16.
-- Everyone does this. Get used to reading it.
-- ---------------------------------------------------------------------
SELECT d.dteday, d.cnt, w.label
FROM rides_daily d
JOIN weather w ON d.weather_id = w.weather_id
LIMIT 5;


-- ---------------------------------------------------------------------
-- STEP 18.  JOIN and GROUP BY together. This is real work.
--
-- Result: Clear 2257952 | Mist 996858 | Light rain or snow 37869
-- ---------------------------------------------------------------------
SELECT w.label,
       COUNT(*)   AS days,
       SUM(d.cnt) AS total_rides
FROM rides_daily d
JOIN weather w ON d.weather_id = w.weather_id
GROUP BY w.label
ORDER BY total_rides DESC;


-- =====================================================================
-- Steps 19-22: the four that catch everyone, including me
-- =====================================================================

-- ---------------------------------------------------------------------
-- STEP 19.  WHERE filters ROWS. HAVING filters GROUPS.
--
-- This FAILS: "misuse of aggregate: SUM()"
-- Because WHERE runs BEFORE the groups are made. At that moment,
-- SUM(cnt) does not exist yet.
-- ---------------------------------------------------------------------
SELECT weather_id, SUM(cnt) AS total
FROM rides_daily
WHERE SUM(cnt) > 1000000
GROUP BY weather_id;

-- This works. HAVING runs AFTER the groups exist.
-- Result: 1 row -> weather_id 1, total 2257952
SELECT weather_id, SUM(cnt) AS total
FROM rides_daily
GROUP BY weather_id
HAVING SUM(cnt) > 1000000;


-- ---------------------------------------------------------------------
-- STEP 20.  Empty cells are NULL, and NULL is not zero.
--
-- 54 stations have no region recorded.
-- Result: 858 | 804 | 54
--
-- COUNT(*)         counts ROWS.
-- COUNT(region_id) counts rows where region_id HAS a value.
-- ---------------------------------------------------------------------
SELECT COUNT(*)          AS all_stations,
       COUNT(region_id)  AS have_a_region,
       COUNT(*) - COUNT(region_id) AS missing
FROM stations;


-- ---------------------------------------------------------------------
-- STEP 21.  To find NULLs you must say IS NULL.
--
-- Result: 54 | 0
--
-- The second is not a mistake in the data. "= NULL" can never be true,
-- ever, in any database. NULL means "unknown", and "unknown = unknown"
-- is not true - it is unknown. So use IS NULL.
-- ---------------------------------------------------------------------
SELECT (SELECT COUNT(*) FROM stations WHERE region_id IS NULL) AS with_is_null,
       (SELECT COUNT(*) FROM stations WHERE region_id =  NULL) AS with_equals;


-- ---------------------------------------------------------------------
-- STEP 22.  Whole numbers divided give whole numbers.
--
-- Result: 0 | 0.336
--
-- The first column is NOT rounded. 331/985 in whole-number arithmetic
-- is 0, because SQL threw the remainder away. Multiply by 1.0 first
-- and it becomes decimal arithmetic.
-- ---------------------------------------------------------------------
SELECT casual,
       cnt,
       casual / cnt                 AS whole_number_division,
       ROUND(casual * 1.0 / cnt, 3) AS proper_division
FROM rides_daily
LIMIT 3;


-- =====================================================================
-- THE ORDER YOU WRITE IT IN
--
--   SELECT    which columns          (5th to actually run)
--   FROM      which table            (1st)
--   JOIN      ...and which other     (1st)
--   WHERE     which rows             (2nd)
--   GROUP BY  make piles             (3rd)
--   HAVING    which piles            (4th)
--   ORDER BY  sort it                (6th)
--   LIMIT     just the top few       (7th)
--
-- You WRITE it in that order, top to bottom.
-- The database RUNS it in the numbered order.
--
-- That mismatch explains step 19 completely: WHERE runs 2nd, the piles
-- are not made until 3rd, so WHERE cannot possibly see a pile's total.
-- =====================================================================


-- =====================================================================
-- YOUR FIRST FIVE QUERIES — write these yourself, no copying
--
--  1. The 10 quietest days, with their dates.
SELECT dteday, cnt 
FROM rides_daily 
ORDER BY cnt ASC 
LIMIT 10;
--  2. How many stations have a capacity of 20 or more?
SELECT COUNT(*) as station_count 
FROM stations 
WHERE capacity >= 20;
--  3. Total rides per month in 2012, busiest month first.
SELECT d.mnth, SUM(d.cnt) as total_rides 
FROM rides_daily d 
JOIN year_lookup y ON d.year_id = y.year_id 
WHERE y.calendar_year = 2012 
GROUP BY d.mnth 
ORDER BY total_rides DESC;
--  4. Every station with no region, listed by name.
SELECT name 
FROM stations 
WHERE region_id IS NULL;
--  5. Average rides per season, using the season table so the output
--     says "Summer" and not "2".
SELECT s.label as season, AVG(d.cnt) as average_rides 
FROM rides_daily d 
JOIN season s ON d.season_id = s.season_id 
GROUP BY s.label;
--
-- Answers are exercises 1-12 in 15-sql-practice.ipynb, which marks
-- them for you.
-- =====================================================================


CREATE TABLE cars (car TEXT, maker TEXT);
CREATE TABLE trucks (truck TEXT, maker TEXT);

INSERT INTO cars (car, maker) VALUES 
('car-aaa', 'aaa'), ('car-bbb', 'bbb'), ('car-ccc', 'ccc'),
('car-ddd', 'ddd'), ('car-eee', 'eee'), ('car-fff', 'fff');

INSERT INTO trucks (truck, maker) VALUES 
('truck-aaa', 'aaa'), ('truck-xxx', 'xxx'), ('truck-ccc', 'ccc'),
('truck-yyy', 'yyy'), ('truck-eee', 'eee'), ('truck-fff', 'fff');