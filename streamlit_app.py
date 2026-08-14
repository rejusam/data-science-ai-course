"""Session 1 cohort dashboard.

Reads the tidy CSVs produced from the week 1 Slidea poll and presents them as
an explorable dashboard.

Run locally:
    streamlit run streamlit_app.py

The data here is aggregate only. No names, no per-person rows, no study codes.
"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# --------------------------------------------------------------- palette ----
# Values from a validated data-visualisation palette. The five-step confidence
# ramp is a single-hue ordinal scale: it passes lightness monotonicity, step
# gaps, and light-end contrast against this surface.
#
# Deliberately NOT used: a red/green pass-fail encoding. That pair measures
# ΔE 4.1 under deuteranopia, which is indistinguishable for the most common
# form of colour blindness. Correctness is shown with one hue, a threshold
# line, and direct labels instead.

SURFACE = "#fcfcfb"
PLANE = "#f9f9f7"
INK = "#0b0b0b"
INK_2 = "#52514e"
MUTED = "#a6a6a6"
GRID = "#e6e5e1"

SERIES = "#2a78d6"      # categorical slot 1, blue
ACCENT = "#eb6834"      # categorical slot 2, orange — reference marks only
ORDINAL = ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#104281"]

FONT = "system-ui, -apple-system, Segoe UI, Roboto, sans-serif"

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "modules" / "00-orientation" / "data"

st.set_page_config(
    page_title="Cohort in data — Session 1",
    page_icon="📊",
    layout="wide",
)


# ------------------------------------------------------------------ data ----

@st.cache_data
def load():
    responses = pd.read_csv(DATA / "session1-responses.csv")
    scales = pd.read_csv(DATA / "session1-scales.csv")
    return responses, scales


responses, scales = load()

META = {"participants": 12, "slides": 25, "participation": 83}

SHORT_TITLES = {
    "Quick check: what is the difference between Git and GitHub?": "Git vs GitHub",
    "Quick check: which of these is a SUPERVISED learning problem?":
        "Spotting supervised learning",
    "Ice cream sales and drowning deaths both rise every summer. What is the "
    "safest conclusion?": "Correlation vs causation",
    "Your model is 99% accurate on the data it was trained on. What do you do "
    "first?": "Recognising overfitting",
}


def ask(fragment, table=None):
    """Rows for the first question containing `fragment`."""
    source = responses if table is None else table
    hit = source[source["question"].str.contains(fragment, case=False,
                                                 regex=False)]
    if hit.empty:
        raise KeyError(fragment)
    return hit[hit["question"] == hit["question"].iloc[0]]


def base_layout(fig, height, title=None, xtitle=None):
    # Passing title=None leaves plotly.js rendering the string "undefined",
    # so an absent title has to be an empty string.
    fig.update_layout(
        height=height,
        title=dict(text=title or "", x=0, xanchor="left",
                   font=dict(size=15, color=INK, family=FONT)),
        margin=dict(l=8, r=28, t=44 if title else 16, b=36),
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        font=dict(family=FONT, color=INK_2, size=12),
        xaxis=dict(title=xtitle, gridcolor=GRID, zeroline=False,
                   linecolor=GRID, tickfont=dict(color=INK_2)),
        yaxis=dict(gridcolor=GRID, zeroline=False, linecolor=GRID,
                   tickfont=dict(color=INK)),
        showlegend=False,
        hoverlabel=dict(bgcolor=SURFACE, font=dict(family=FONT, color=INK),
                        bordercolor=GRID),
    )
    return fig


def bars(rows, title=None, colour=SERIES, xtitle="students", show_pct=True):
    """Horizontal bars, largest at top, value labelled on each bar."""
    rows = rows[rows["count"] > 0].sort_values("count")
    labels = []
    for _, row in rows.iterrows():
        if show_pct and pd.notna(row.get("percentage")):
            labels.append("{:.0f}  ({:.0f}%)".format(row["count"], row["percentage"]))
        else:
            labels.append("{:.0f}".format(row["count"]))

    fig = go.Figure(go.Bar(
        x=rows["count"], y=rows["option"], orientation="h",
        marker=dict(color=colour, line=dict(width=2, color=SURFACE)),
        text=labels, textposition="outside",
        textfont=dict(color=INK_2, size=11, family=FONT),
        hovertemplate="%{y}<br>%{x} students<extra></extra>",
        width=0.62,
    ))
    height = max(200, 46 * len(rows) + 90)
    base_layout(fig, height, title, xtitle)
    fig.update_xaxes(range=[0, rows["count"].max() * 1.3])
    return fig


def confidence_table(fragment):
    rows = scales[scales["question"].str.contains(fragment, case=False,
                                                  regex=False)]
    out = []
    for item, group in rows.groupby("item", sort=False):
        total = group["count"].sum()
        score = (group["level_index"] * group["count"]).sum() / total
        out.append({"item": item, "index": round(score, 2),
                    "respondents": int(total)})
    return pd.DataFrame(out).sort_values("index")


# ---------------------------------------------------------------- header ----

st.title("Your cohort, in data")
st.markdown(
    "Twenty-five poll questions, answered live in session 1 of a 25-week "
    "Data Science & AI course. Everything here is aggregate — no names, no "
    "individual responses."
)

kpi = st.columns(4)
kpi[0].metric("Participants", META["participants"])
kpi[1].metric("Poll questions", META["slides"])
kpi[2].metric("Average participation", "{}%".format(META["participation"]))
kpi[3].metric("Answers recorded", int(responses["count"].sum() + scales["count"].sum()))

st.divider()

tabs = st.tabs([
    "The headline",
    "Who is here",
    "Goals vs reality",
    "Knowledge check",
    "In their words",
    "Explore the data",
])

# ------------------------------------------------------- tab 1: headline ----

with tabs[0]:
    st.subheader("What the room wants, against what the room can do")
    st.markdown(
        "Both charts are drawn from the same ten people. Read them together."
    )

    left, right = st.columns(2)

    goals = ask("Rank these by what YOU").sort_values("rank_score")
    with left:
        fig = go.Figure(go.Bar(
            x=goals["rank_score"], y=goals["option"], orientation="h",
            marker=dict(color=SERIES, line=dict(width=2, color=SURFACE)),
            text=[" {:.0f}".format(v) for v in goals["rank_score"]],
            textposition="outside",
            textfont=dict(color=INK_2, size=11, family=FONT),
            hovertemplate="%{y}<br>rank score %{x}<extra></extra>",
            width=0.62,
        ))
        base_layout(fig, 330, "What you most want by week 25",
                    "rank score (higher = wanted more)")
        fig.update_xaxes(range=[0, goals["rank_score"].max() * 1.22])
        st.plotly_chart(fig, use_container_width=True)

    subjects = confidence_table("confident are you TODAY")
    with right:
        fig = go.Figure(go.Bar(
            x=subjects["index"], y=subjects["item"], orientation="h",
            marker=dict(color=SERIES, line=dict(width=2, color=SURFACE)),
            text=["  {:.2f}".format(v) for v in subjects["index"]],
            textposition="outside",
            textfont=dict(color=INK_2, size=11, family=FONT),
            hovertemplate="%{y}<br>confidence index %{x:.2f} of 4<extra></extra>",
            width=0.62,
        ))
        base_layout(fig, 330, "How confident you are today", "")
        fig.update_xaxes(
            range=[0, 4.35], tickvals=[0, 1, 2, 3, 4],
            ticktext=["never<br>touched", "seen it", "with<br>help",
                      "on my<br>own", "could<br>teach"],
        )
        st.plotly_chart(fig, use_container_width=True)

    st.info(
        "Building and evaluating machine learning models is the **second most "
        "wanted** thing in the room, and the **second least confident**. "
        "Generative AI is third most wanted and the least confident of all. "
        "That distance is not a problem to fix before starting. It is the course."
    )

    st.subheader("When you get what you asked for")

    roadmap = pd.DataFrame([
        ("Write clean, confident Python", 1, 2),
        ("Wrangle data with SQL, APIs and pipelines", 6, 8),
        ("Build and evaluate machine learning models", 8, 14),
        ("Deploy models and build with Generative AI", 19, 20),
        ("Tell a convincing story with data", 18, 20),
    ], columns=["goal", "start", "end"])
    order = list(goals["option"])
    roadmap["rank"] = roadmap["goal"].map({g: i for i, g in enumerate(order)})
    roadmap = roadmap.sort_values("rank")

    fig = go.Figure(go.Bar(
        x=roadmap["end"] - roadmap["start"] + 1, y=roadmap["goal"],
        base=roadmap["start"], orientation="h",
        marker=dict(color=SERIES, line=dict(width=2, color=SURFACE)),
        text=["weeks {}–{}".format(s, e)
              for s, e in zip(roadmap["start"], roadmap["end"])],
        textposition="outside",
        textfont=dict(color=INK_2, size=11, family=FONT),
        hovertemplate="%{y}<br>weeks %{base}–%{x}<extra></extra>",
        width=0.6,
    ))
    base_layout(fig, 330, None, "week of the course")
    fig.update_xaxes(range=[0, 30], tickvals=[1, 5, 10, 15, 20, 25])
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "Weeks come from the course delivery plan. The top-ranked goal lands "
        "late on purpose — you cannot tell a story about a model you have not "
        "built yet. The lowest-ranked goal starts in week 1, because "
        "everything else rests on it."
    )

# ------------------------------------------------------ tab 2: who is here --

with tabs[1]:
    st.subheader("Who is in the room")
    left, right = st.columns(2)
    with left:
        st.plotly_chart(bars(ask("What best describes where you are right now"),
                             "Why you are here"), use_container_width=True)
        st.plotly_chart(bars(ask("Have you ever used a command line"),
                             "Experience with a terminal"),
                        use_container_width=True)
    with right:
        st.plotly_chart(bars(ask("Which operating system will you use"),
                             "What you will be working on"),
                        use_container_width=True)
        st.plotly_chart(bars(ask("can you install software on it"),
                             "Whether you can install software on it"),
                        use_container_width=True)

    st.caption(
        "Two thirds of the cohort are on Windows and a quarter are on a shared "
        "or family computer. That is why the setup guide is written for both "
        "operating systems, and why nothing in week 1 assumes admin rights."
    )

    st.subheader("Comfort with the toolchain today")
    tools = confidence_table("comfort with each of these tools")
    fig = go.Figure(go.Bar(
        x=tools["index"], y=tools["item"], orientation="h",
        marker=dict(color=SERIES, line=dict(width=2, color=SURFACE)),
        text=["  {:.2f}".format(v) for v in tools["index"]],
        textposition="outside", textfont=dict(color=INK_2, size=11, family=FONT),
        hovertemplate="%{y}<br>comfort %{x:.2f} of 4<extra></extra>",
        width=0.62,
    ))
    base_layout(fig, 300, None, "0 = never used it &nbsp; → &nbsp; 4 = use it confidently")
    fig.update_xaxes(range=[0, 4.35])
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------- tab 3: goals vs real --

with tabs[2]:
    st.subheader("Confidence, answer by answer")
    st.markdown(
        "The headline tab collapses each subject to a single number. This is "
        "the full distribution behind it."
    )

    question = st.radio(
        "Which scale question?",
        sorted(scales["question"].unique()),
        format_func=lambda q: q if len(q) < 70 else q[:67] + "…",
    )

    rows = scales[scales["question"] == question]
    levels = (rows[["level", "level_index"]].drop_duplicates()
              .sort_values("level_index"))
    items = (rows.groupby("item")
             .apply(lambda g: (g["level_index"] * g["count"]).sum() / g["count"].sum(),
                    include_groups=False)
             .sort_values(ascending=False).index.tolist())

    fig = go.Figure()
    for _, level in levels.iterrows():
        subset = rows[rows["level"] == level["level"]].set_index("item")
        fig.add_bar(
            y=items,
            x=[subset["count"].get(item, 0) for item in items],
            name=level["level"],
            orientation="h",
            marker=dict(color=ORDINAL[int(level["level_index"]) % len(ORDINAL)],
                        line=dict(width=2, color=SURFACE)),
            hovertemplate="%{y}<br>" + level["level"] + ": %{x}<extra></extra>",
        )
    fig.update_layout(barmode="stack")
    base_layout(fig, 140 + 62 * len(items), None, "students")
    # A horizontal legend above the plot needs the top margin reserved for it,
    # otherwise it is drawn over the first bar.
    fig.update_layout(
        showlegend=True,
        margin=dict(l=8, r=28, t=58, b=44),
        legend=dict(orientation="h", yanchor="bottom", y=1.04, x=0,
                    font=dict(color=INK_2, size=11),
                    traceorder="normal"),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "Colour runs light to dark with growing confidence — a single hue, so "
        "the order is readable without relying on hue differences."
    )

# -------------------------------------------------- tab 4: knowledge check --

with tabs[3]:
    st.subheader("How the room did on questions with a right answer")

    graded = responses[responses["status"].fillna("").str.contains("Correct")]
    totals = responses.groupby("question")["count"].sum()
    rows = []
    for q, group in graded.groupby("question", sort=False):
        if "Lead Trainer" in q or "percentage of a working" in q:
            continue  # ice-breaker and estimate, not knowledge questions
        correct = int(group["count"].sum())
        total = int(totals[q])
        rows.append({"question": SHORT_TITLES.get(q, q[:44]),
                     "full": q,
                     "pct": round(correct / total * 100, 1),
                     "correct": correct, "total": total})
    quiz = pd.DataFrame(rows).sort_values("pct")

    fig = go.Figure(go.Bar(
        x=quiz["pct"], y=quiz["question"], orientation="h",
        marker=dict(color=SERIES, line=dict(width=2, color=SURFACE)),
        text=["  {:.0f}%   {}/{}".format(p, c, t)
              for p, c, t in zip(quiz["pct"], quiz["correct"], quiz["total"])],
        textposition="outside",
        textfont=dict(color=INK_2, size=11, family=FONT),
        customdata=quiz["full"],
        hovertemplate="%{customdata}<br>%{x:.0f}% correct<extra></extra>",
        width=0.6,
    ))
    base_layout(fig, 300, None, "percent of those answering who were correct")
    fig.update_xaxes(range=[0, 132])
    fig.add_vline(x=50, line=dict(color=MUTED, width=1, dash="dash"))
    fig.add_annotation(x=50, y=1.06, yref="paper", text="half the room",
                       showarrow=False, font=dict(color=MUTED, size=10),
                       xanchor="center")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        "**The interesting wrong answer.** On correlation and causation, only "
        "one person chose *ice cream causes drowning*. Four chose *the "
        "correlation must be a mistake* — but the correlation is completely "
        "real. Ice cream sales and drownings do rise together. Neither causes "
        "the other; hot weather causes both. Dismissing a real correlation is "
        "the more expensive error, and it takes a whole session in week 6."
    )

    st.divider()
    st.subheader("The estimate")
    st.markdown(
        "How much of a working data scientist's time goes on finding, "
        "cleaning and preparing data?"
    )

    guesses = ask("percentage of a working").copy()
    guesses["value"] = guesses["option"].str.extract(r"(\d+)").astype(int)
    spread = guesses["value"].repeat(guesses["count"]).tolist()
    median = pd.Series(spread).median()

    fig = go.Figure(go.Scatter(
        x=spread, y=[1] * len(spread), mode="markers",
        marker=dict(size=19, color=SERIES, opacity=0.62,
                    line=dict(width=2, color=SURFACE)),
        hovertemplate="guessed %{x}%<extra></extra>",
    ))
    fig.add_vline(x=80, line=dict(color=ACCENT, width=2))
    fig.add_annotation(x=80, y=1.36, text="  commonly quoted: 80%",
                       showarrow=False, xanchor="left",
                       font=dict(color=ACCENT, size=12))
    fig.add_vline(x=median, line=dict(color=MUTED, width=1.5, dash="dash"))
    fig.add_annotation(x=median, y=0.68, text="your median {:.0f}%".format(median),
                       showarrow=False, font=dict(color=INK_2, size=11))
    base_layout(fig, 250, None,
                "percent of time spent finding, cleaning and preparing data")
    fig.update_xaxes(range=[0, 110])
    fig.update_yaxes(range=[0.5, 1.6], showticklabels=False, showgrid=False)
    st.plotly_chart(fig, use_container_width=True)

    low, high = min(spread), max(spread)
    st.caption(
        "Guesses ran from {}% to {}%, so the room genuinely did not know, which "
        "is exactly right for week 1. The spread matters more than the answer. "
        "The commonly quoted figure is around 80%, and it is why modules 2 and "
        "3 cover getting and cleaning data before any modelling happens."
        .format(low, high)
    )

# --------------------------------------------------- tab 5: in their words --

with tabs[4]:
    st.subheader("In your own words")
    left, right = st.columns(2)
    with left:
        st.plotly_chart(
            bars(ask("what do you most want to walk away with"),
                 "What you want to walk away with", show_pct=False),
            use_container_width=True)
        st.plotly_chart(
            bars(ask("most likely to get in the way"),
                 "What might get in the way", colour=ACCENT, show_pct=False),
            use_container_width=True)
    with right:
        st.plotly_chart(
            bars(ask("Name any language, database or data tool"),
                 "What you have used before", show_pct=False),
            use_container_width=True)
        st.plotly_chart(
            bars(ask("name ONE habit you will hold"),
                 "What you committed to", show_pct=False),
            use_container_width=True)

    st.caption(
        "Work and time, named by almost everyone. That is what part-time study "
        "is, not a character flaw. It does mean the plan has to survive a busy "
        "week: 45 focused minutes on a weeknight beats one heroic Sunday."
    )

# ------------------------------------------------------- tab 6: explore -----

with tabs[5]:
    st.subheader("Explore any question")
    st.markdown(
        "Every question from the session, with the chart and the numbers "
        "behind it. This is the table view — nothing in this dashboard is "
        "readable only as colour."
    )

    catalogue = (responses[["order", "qtype", "question"]]
                 .drop_duplicates().sort_values("order"))

    kinds = st.multiselect("Filter by poll type",
                           sorted(catalogue["qtype"].unique()),
                           default=sorted(catalogue["qtype"].unique()))
    filtered = catalogue[catalogue["qtype"].isin(kinds)]

    if filtered.empty:
        st.warning("No questions match that filter.")
    else:
        chosen = st.selectbox(
            "Question", filtered["question"].tolist(),
            format_func=lambda q: q if len(q) < 95 else q[:92] + "…")

        rows = responses[responses["question"] == chosen]
        st.caption("Poll type: {}".format(rows["qtype"].iloc[0]))
        st.plotly_chart(bars(rows), use_container_width=True)

        table = rows[["option", "count", "percentage", "status"]].copy()
        table["status"] = table["status"].fillna("")
        table["percentage"] = table["percentage"].map(
            lambda v: "" if pd.isna(v) else "{:.1f}%".format(v))
        table.columns = ["Answer", "Students", "Percent", "Notes"]
        st.dataframe(table.reset_index(drop=True), use_container_width=True,
                     hide_index=True)

    st.divider()
    with st.expander("Download the underlying data"):
        st.markdown(
            "Aggregate counts only. The study-code question is excluded, and "
            "the leaderboard sheet — the only place participant names appear — "
            "is never read by the parser."
        )
        st.download_button("responses.csv", responses.to_csv(index=False),
                           "session1-responses.csv", "text/csv")
        st.download_button("scales.csv", scales.to_csv(index=False),
                           "session1-scales.csv", "text/csv")

# ---------------------------------------------------------------- sidebar ----

with st.sidebar:
    st.header("About")
    st.markdown(
        "Live poll responses from session 1 of a 25-week Data Science & AI "
        "course, parsed from the raw export and presented as a dashboard."
    )
    st.markdown(
        "The export arrives as a single spreadsheet holding twenty-five "
        "stacked blocks in four different shapes, with headers off the first "
        "row and percentages stored as text. The parser that untangles it is "
        "a parser module, and it has seventeen tests."
    )

    st.subheader("Privacy")
    st.markdown(
        "Aggregate counts only. No names, no per-person rows, no study codes. "
        "The parser never opens the leaderboard sheet, and a test asserts that "
        "no name from it can reach the output."
    )

    st.subheader("Accessibility")
    st.markdown(
        "Single-hue ordinal scales rather than red/green pass-fail, which is "
        "unreadable for the most common form of colour blindness. Every chart "
        "is directly labelled, and every question has a table view under "
        "**Explore the data**."
    )

    st.caption("Built with Streamlit, pandas and Plotly.")
