"""Turn a Slidea analytics export into tidy tables.

Slidea exports one Excel sheet containing about twenty-five stacked blocks,
each with its own shape depending on the poll type. That is normal for data
you get handed in the real world, and reshaping it is most of the work in any
analysis.

The end result here is tidy data: one row per observation, one column per
variable, which is the shape every plotting and modelling library expects.

    from tools.slidea import load_export

    export = load_export("session1.xlsx")
    export.responses.head()

Privacy: this module reads only aggregate blocks. It never touches the
Leaderboard sheet, which contains participant display names.
"""
import re
from dataclasses import dataclass

import pandas as pd

RESPONSES_SHEET = "Response Details"
SUMMARY_SHEET = "Summary Report"

# A block starts with a line like "MULTIPLE CHOICE: What best describes ...".
BLOCK_START = re.compile(r"^([A-Z][A-Z ]+):\s*(.+)$")

# Columns that mean "how many people chose this", depending on block shape.
COUNT_COLUMNS = ("Response Count",)
LABEL_COLUMNS = ("Options", "Response")

# Header cells that are not scale levels.
NOT_A_LEVEL = ("Options", "Response", "Status / Details", "Percentage",
               "Response Count")


@dataclass
class SlideaExport:
    """Everything worth having from one Slidea export.

    responses: one row per answer option, for every non-scale question.
    scales:    one row per item and rating level, for scale questions.
    meta:      participants, slide count, average participation.
    """

    responses: pd.DataFrame
    scales: pd.DataFrame
    meta: dict

    @property
    def questions(self):
        """Every question asked, with its type, in the order asked."""
        return (self.responses[["order", "qtype", "question"]]
                .drop_duplicates()
                .sort_values("order")
                .reset_index(drop=True))

    def question(self, needle):
        """Rows for the first question whose text contains `needle`."""
        match = self.responses["question"].str.contains(needle, case=False,
                                                        regex=False)
        if not match.any():
            raise KeyError("no question matching {!r}".format(needle))
        first = self.responses.loc[match, "question"].iloc[0]
        return self.responses[self.responses["question"] == first]


def _clean(value):
    """Excel gives us NaN for blanks. We want a string or None."""
    if value is None:
        return None
    text = str(value).strip()
    if text in ("nan", "NaT", ""):
        return None
    return text


def _to_number(value):
    try:
        return float(str(value).strip().rstrip("%"))
    except (TypeError, ValueError):
        return None


def _find_blocks(raw):
    """Locate every question block: (start_row, type, question_text)."""
    blocks = []
    for index, value in raw[0].items():
        text = _clean(value)
        if not text:
            continue
        match = BLOCK_START.match(text)
        if match:
            blocks.append((index, match.group(1).strip(), match.group(2).strip()))
    return blocks


def _block_rows(raw, start, end):
    """The data rows of one block, and its header row."""
    header = [_clean(v) for v in raw.iloc[start + 1].tolist()]
    rows = []
    for index in range(start + 2, end):
        values = [_clean(v) for v in raw.iloc[index].tolist()]
        if values[0] is None:
            continue
        rows.append(values)
    return header, rows


def _parse_scale_block(header, rows, order, qtype, question):
    """Scale blocks put one rating level per column."""
    levels = [(position, name) for position, name in enumerate(header)
              if name and name not in NOT_A_LEVEL]
    records = []
    for values in rows:
        item = values[0]
        for position, level in levels:
            count = _to_number(values[position]) if position < len(values) else None
            records.append({
                "order": order,
                "qtype": qtype,
                "question": question,
                "item": item,
                "level": level,
                "level_index": [p for p, _ in levels].index(position),
                "count": int(count) if count is not None else 0,
            })
    return records


def _parse_option_block(header, rows, order, qtype, question):
    """Everything that is one row per answer option."""
    label_column = 0
    try:
        count_column = next(position for position, name in enumerate(header)
                            if name in COUNT_COLUMNS)
    except StopIteration:
        count_column = 1

    percentage_column = None
    status_column = None
    for position, name in enumerate(header):
        if name == "Percentage":
            percentage_column = position
        elif name == "Status / Details":
            status_column = position

    records = []
    for values in rows:
        label = values[label_column]
        if label is None or label.upper().startswith("TOTAL"):
            continue
        status = (values[status_column]
                  if status_column is not None and status_column < len(values)
                  else None)
        percentage = (_to_number(values[percentage_column])
                      if percentage_column is not None
                      and percentage_column < len(values) else None)
        count = _to_number(values[count_column]) if count_column < len(values) else None
        records.append({
            "order": order,
            "qtype": qtype,
            "question": question,
            "option": label,
            "count": int(count) if count is not None else 0,
            "percentage": percentage,
            "status": status,
            "is_correct": bool(status and "Correct" in status),
            "rank_score": _rank_score(status),
        })
    return records


def _rank_score(status):
    """Ranking blocks hide the Borda score in the status column."""
    if not status:
        return None
    match = re.search(r"Rank Score Sum:\s*(\d+)", status)
    return int(match.group(1)) if match else None


def _parse_meta(path):
    raw = pd.read_excel(path, sheet_name=SUMMARY_SHEET, header=None)
    meta = {}
    for index in range(len(raw) - 1):
        labels = [_clean(v) for v in raw.iloc[index + 1].tolist()]
        values = [_clean(v) for v in raw.iloc[index].tolist()]
        for label, value in zip(labels, values):
            if label in ("Total Participants", "Total Slides",
                         "Avg Participation"):
                number = _to_number(value)
                meta[label] = int(number) if number is not None else None
    return meta


def load_export(path):
    """Read a Slidea export into tidy tables."""
    raw = pd.read_excel(path, sheet_name=RESPONSES_SHEET, header=None)
    blocks = _find_blocks(raw)
    if not blocks:
        raise ValueError("no question blocks found in {}".format(path))

    option_records = []
    scale_records = []

    for position, (start, qtype, question) in enumerate(blocks, start=1):
        end = blocks[position][0] if position < len(blocks) else len(raw)
        header, rows = _block_rows(raw, start, end)
        if qtype == "SCALES":
            scale_records += _parse_scale_block(header, rows, position, qtype,
                                                question)
        else:
            option_records += _parse_option_block(header, rows, position, qtype,
                                                  question)

    responses = pd.DataFrame(option_records)
    scales = pd.DataFrame(scale_records)
    return SlideaExport(responses=responses, scales=scales,
                        meta=_parse_meta(path))


def participation(export):
    """How many people answered each question, in the order asked."""
    counted = (export.responses.groupby(["order", "qtype", "question"],
                                        as_index=False)["count"].sum()
               .rename(columns={"count": "respondents"}))
    scale_counts = export.scales.groupby(["order", "qtype", "question"])
    if len(export.scales):
        per_item = (scale_counts["count"].sum() /
                    export.scales.groupby(["order", "qtype", "question"])["item"]
                    .nunique())
        scale_frame = per_item.reset_index(name="respondents")
        counted = pd.concat([counted, scale_frame], ignore_index=True)
    return counted.sort_values("order").reset_index(drop=True)


def quiz_scores(export):
    """For questions with a right answer, what share of the room got it."""
    graded = export.responses[export.responses["status"].notna()]
    graded = graded[graded["status"].str.contains("Correct", na=False)]
    if graded.empty:
        return pd.DataFrame(columns=["question", "correct_option",
                                     "correct_count", "total", "pct_correct"])
    totals = export.responses.groupby("question")["count"].sum()
    rows = []
    for question, group in graded.groupby("question", sort=False):
        correct = int(group["count"].sum())
        total = int(totals[question])
        rows.append({
            "question": question,
            "correct_option": " / ".join(group["option"].tolist()),
            "correct_count": correct,
            "total": total,
            "pct_correct": round(correct / total * 100, 1) if total else 0.0,
        })
    return pd.DataFrame(rows).sort_values("pct_correct").reset_index(drop=True)


def confidence_index(export, question_contains="confident are you TODAY"):
    """Turn a scale question into one number per item, from 0 to 4.

    Level 0 is 'never touched it', level 4 is 'could teach it'. The index is
    the average level weighted by how many people chose it.
    """
    rows = export.scales[export.scales["question"].str.contains(
        question_contains, case=False, regex=False)]
    if rows.empty:
        raise KeyError("no scale question matching {!r}".format(question_contains))
    grouped = []
    for item, group in rows.groupby("item", sort=False):
        total = group["count"].sum()
        score = (group["level_index"] * group["count"]).sum() / total if total else 0
        grouped.append({"item": item, "respondents": int(total),
                        "index": round(float(score), 2)})
    return (pd.DataFrame(grouped)
            .sort_values("index", ascending=False)
            .reset_index(drop=True))
