"""Tests for the Slidea export parser.

These build a small workbook shaped like a real Slidea export rather than
reading a real one. Real exports contain cohort responses, so they are not
committed to this repository and must never be needed to run the tests.
"""
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.slidea import (  # noqa: E402
    confidence_index,
    load_export,
    participation,
    quiz_scores,
)


def _write_workbook(path):
    """A miniature export with one block of each shape we care about."""
    summary = [
        ["Slidea Presentation Analytics Report", None, None],
        [None, None, None],
        ["Presentation:", "Test deck", None],
        [None, None, None],
        [6, 4, 75],
        ["Total Participants", "Total Slides", "Avg Participation"],
    ]

    responses = [
        ["Slidea Audience Response Details", None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        ["MULTIPLE CHOICE: Which operating system?", None, None, None, None, None],
        ["Options", "Response Count", "Percentage", "Status / Details", None, None],
        ["Windows", 4, "66.7%", "Highest Response", None, None],
        ["macOS", 2, "33.3%", None, None, None],
        [None, None, None, None, None, None],
        ["SELECT ANSWER: What is 2 + 2?", None, None, None, None, None],
        ["Options", "Response Count", "Percentage", "Status / Details", None, None],
        ["Four", 5, "83.3%", "Correct Answer", None, None],
        ["Five", 1, "16.7%", None, None, None],
        [None, None, None, None, None, None],
        ["RANKING: Rank these goals", None, None, None, None, None],
        ["Options", "Response Count", "Percentage", "Status / Details", None, None],
        ["Storytelling", 6, "100.0%", "Rank Score Sum: 18", None, None],
        ["Modelling", 6, "100.0%", "Rank Score Sum: 12", None, None],
        [None, None, None, None, None, None],
        ["SCALES: How confident are you TODAY?", None, None, None, None, None],
        ["Options", "Never touched it", "Seen it, cannot do it yet",
         "Can do it with help", "Can do it on my own", "Status / Details"],
        ["Python", 1, 1, 2, 2, "Can do it with help"],
        ["Machine learning", 4, 2, 0, 0, "Never touched it"],
        [None, None, None, None, None, None],
        ["WORD CLOUD: One word", None, None, None, None, None],
        ["Response", "Response Count", "Status / Details", None, None, None],
        ["automation", 2, "Highest Response", None, None, None],
        ["curiosity", 1, None, None, None, None],
    ]

    with pd.ExcelWriter(path) as writer:
        pd.DataFrame(summary).to_excel(writer, sheet_name="Summary Report",
                                       header=False, index=False)
        pd.DataFrame(responses).to_excel(writer, sheet_name="Response Details",
                                         header=False, index=False)
        # Present in real exports, and deliberately never read.
        pd.DataFrame([["Rank", "Participant"], [1, "Some Person"]]).to_excel(
            writer, sheet_name="Leaderboard", header=False, index=False)


@pytest.fixture(scope="module")
def export(tmp_path_factory):
    path = tmp_path_factory.mktemp("slidea") / "export.xlsx"
    _write_workbook(path)
    return load_export(path)


def test_meta_is_read(export):
    assert export.meta["Total Participants"] == 6
    assert export.meta["Total Slides"] == 4
    assert export.meta["Avg Participation"] == 75


def test_all_non_scale_blocks_parsed(export):
    assert len(export.questions) == 4


def test_scale_block_goes_to_scales_not_responses(export):
    assert "How confident are you TODAY?" not in set(export.responses["question"])
    assert export.scales["question"].str.contains("confident").all()


def test_option_counts(export):
    rows = export.question("operating system")
    assert dict(zip(rows["option"], rows["count"])) == {"Windows": 4, "macOS": 2}


def test_percentages_parsed_as_numbers(export):
    rows = export.question("operating system")
    assert rows.loc[rows["option"] == "Windows", "percentage"].iloc[0] == 66.7


def test_correct_answer_flagged(export):
    rows = export.question("2 + 2")
    assert rows.loc[rows["option"] == "Four", "is_correct"].iloc[0]
    assert not rows.loc[rows["option"] == "Five", "is_correct"].iloc[0]


def test_rank_score_extracted(export):
    rows = export.question("Rank these goals")
    scores = dict(zip(rows["option"], rows["rank_score"]))
    assert scores == {"Storytelling": 18, "Modelling": 12}


def test_rank_score_is_none_for_other_questions(export):
    rows = export.question("operating system")
    assert rows["rank_score"].isna().all()


def test_word_cloud_block_uses_response_column(export):
    rows = export.question("One word")
    assert dict(zip(rows["option"], rows["count"])) == {"automation": 2,
                                                        "curiosity": 1}


def test_scales_have_one_row_per_item_and_level(export):
    rows = export.scales
    assert set(rows["item"]) == {"Python", "Machine learning"}
    assert rows["level_index"].max() == 3
    assert len(rows) == 2 * 4


def test_confidence_index_orders_by_strength(export):
    index = confidence_index(export, "confident are you TODAY")
    assert list(index["item"]) == ["Python", "Machine learning"]
    # Python: (0*1 + 1*1 + 2*2 + 3*2) / 6
    assert index.loc[index["item"] == "Python", "index"].iloc[0] == pytest.approx(1.83, abs=0.01)
    assert index.loc[index["item"] == "Machine learning", "index"].iloc[0] == pytest.approx(0.33, abs=0.01)


def test_confidence_index_rejects_unknown_question(export):
    with pytest.raises(KeyError):
        confidence_index(export, "no such question")


def test_quiz_scores_only_covers_graded_questions(export):
    scores = quiz_scores(export)
    assert len(scores) == 1
    row = scores.iloc[0]
    assert row["correct_option"] == "Four"
    assert row["correct_count"] == 5
    assert row["total"] == 6
    assert row["pct_correct"] == pytest.approx(83.3, abs=0.1)


def test_participation_counts_every_question(export):
    counts = participation(export)
    assert len(counts) == 5
    operating_system = counts[counts["question"].str.contains("operating")]
    assert operating_system["respondents"].iloc[0] == 6


def test_question_lookup_is_case_insensitive(export):
    assert len(export.question("OPERATING SYSTEM")) == 2


def test_question_lookup_raises_when_missing(export):
    with pytest.raises(KeyError):
        export.question("favourite biscuit")


def test_leaderboard_sheet_is_never_read(export):
    """Participant names must not appear anywhere in the parsed output."""
    everything = " ".join(
        export.responses.astype(str).to_numpy().ravel().tolist()
        + export.scales.astype(str).to_numpy().ravel().tolist()
    )
    assert "Some Person" not in everything
    assert "Participant" not in everything
