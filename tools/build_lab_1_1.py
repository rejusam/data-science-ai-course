"""Assemble the session 2 live-coding notebook, Lab 1.1.

    python3 tools/build_lab_1_1.py

The notebook is a build artefact. Edit this file, not the .ipynb.

Cells that are meant to fail carry the `raises-exception` tag, so students see
the real traceback while the notebook still runs top to bottom. That matters:
the errors are the lesson, and a notebook that halts on the first one cannot be
tested.
"""
from pathlib import Path

import nbformat as nbf

REPO = Path(__file__).resolve().parent.parent
OUTPUT = (REPO / "modules" / "01a-programming-fundamentals" / "notebooks"
          / "lab-1-1-python-basics.ipynb")


def md(text):
    return nbf.v4.new_markdown_cell(text.strip())


def code(text):
    return nbf.v4.new_code_cell(text.strip())


def breaks(text):
    """A cell we expect to fail. The traceback is the point."""
    cell = nbf.v4.new_code_cell(text.strip())
    cell.metadata["tags"] = ["raises-exception"]
    return cell


def predict(question):
    return md("""
> **Predict first.** {}
>
> Put your answer in the chat before we run it. Being wrong here is useful and
> costs nothing.
""".format(question))


CELLS = [
    md("""
# Lab 1.1 — Python basics

Data Science & AI, session 2.

You ranked "write clean, confident Python" last of the five things you want
from this course. That is a completely reasonable thing to want least, and it
is still the first thing we teach, because everything you ranked above it is
built on it. You cannot tell a convincing story about a model you could not
build.

By the end of tonight you will have written and run: variables, conditions,
loops, a data structure, and a function that does something real.

**How to run a cell:** click it, then press `Shift + Enter`.
"""),

    md("""
## Before anything else: Restart & Run All

A notebook remembers everything you have run, in the order you ran it. That is
convenient and it is also the single biggest source of confusion for people new
to notebooks.

You can delete a cell and still use the variable it created. You can run cells
out of order and get a result that nobody else can reproduce. The notebook
looks fine. It is not fine.

**The rule for this course:** your code works when it runs top to bottom from a
fresh start. Nothing less counts.

From the menu: **Kernel → Restart Kernel and Run All Cells**. In Colab:
**Runtime → Restart and run all**.

Do it now, before we start. Get in the habit tonight and you will save yourself
hours in week nine.
"""),

    md("""
## 1. Your first cell

`print()` displays something. Run this.
"""),
    code("""
print("I am writing Python.")
"""),

    md("""
## 2. Variables

A variable is a name for a value. You make one with `=`.

Read `=` as "gets" rather than "equals" — it is an instruction, not a
statement of fact.
"""),
    code("""
heart_rate = 72
temperature = 38.4
patient_id = "REG-0041"
is_flagged = False

print(heart_rate)
print(temperature)
print(patient_id)
print(is_flagged)
"""),

    md("""
Every value has a **type**. Python tracks it for you, but you need to know
what it is, because types decide what operations are allowed.
"""),
    code("""
print(type(heart_rate))
print(type(temperature))
print(type(patient_id))
print(type(is_flagged))
"""),

    md("""
Those four are the ones you will use constantly. The table is in the same
order as the output above.

| Type | What it holds | Our example |
|---|---|---|
| `int` | whole number | `heart_rate = 72` |
| `float` | number with a decimal point | `temperature = 38.4` |
| `str` | text | `patient_id = "REG-0041"` |
| `bool` | true or false | `is_flagged = False` |

`38.4` is a float because it has a decimal point. `72` is an int because it
does not. That is the whole distinction, and it matters more than it looks:
dividing two ints in Python gives you a float, which surprises people coming
from other languages.
"""),

    predict("What will `print(\"5\" + 5)` do?"),

    md("""
### Our first deliberate error

The cell below is broken on purpose. Read the error before you read the
explanation.

**Read tracebacks from the bottom up.** The last line tells you what went
wrong. The lines above tell you where.
"""),
    breaks("""
print("5" + 5)
"""),

    md("""
`TypeError: can only concatenate str (not "int") to str`

`"5"` is text and `5` is a number. `+` means "join together" for text and
"add" for numbers, and Python will not guess which one you meant.

Fix it by converting, and being explicit about which you wanted.
"""),
    code("""
print("5" + str(5))     # text: "55"
print(int("5") + 5)     # number: 10
"""),

    md("""
## 3. Operators

Arithmetic works how you would expect, with two worth noting: `**` is power
and `%` is remainder.
"""),
    predict("What are the values of `17 / 5`, `17 // 5` and `17 % 5`?"),
    code("""
print(17 / 5)      # true division
print(17 // 5)     # whole part only
print(17 % 5)      # remainder
print(2 ** 10)     # 2 to the power of 10
"""),

    md("""
Comparisons produce a `bool`. Note the double `==` for "is equal to": a single
`=` assigns, a double `==` asks.
"""),
    code("""
resting = 72
print(resting > 100)
print(resting == 72)
print(resting != 72)
print(60 <= resting <= 100)   # Python lets you chain these
"""),

    md("""
### Deliberate error two

A single `=` inside a condition. This one is a `SyntaxError`, which means
Python could not even understand the line, let alone run it.
"""),
    breaks("""
if resting = 72:
    print("resting rate is 72")
"""),

    md("""
`SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?`

Modern Python guesses what you meant, which is kind of it. Older versions just
said `invalid syntax` and left you to work it out.
"""),

    md("""
## 4. Making decisions

`if` runs a block when a condition is true. `elif` and `else` handle the other
cases.

The **indentation is not decoration**. It is how Python knows which lines
belong to the block. Four spaces, consistently.
"""),
    predict("With `resting = 72`, which line prints?"),
    code("""
resting = 72

if resting > 100:
    print("tachycardia range")
elif resting < 60:
    print("bradycardia range")
else:
    print("within the usual resting range")
"""),

    md("""
### Deliberate error three

The most common error a beginner meets. The indentation is missing.
"""),
    breaks("""
if resting > 60:
print("this line should be indented")
"""),

    md("""
`IndentationError: expected an indented block after 'if' statement`

Python is telling you exactly what it wants. Most error messages are this
helpful once you are in the habit of reading them.
"""),

    md("""
## 5. Repeating things

A `for` loop repeats once for each item in a collection.
"""),
    predict("How many lines does this print, and what is the last one?"),
    code("""
readings = [68, 72, 91, 105, 58]

for reading in readings:
    print("reading:", reading)
"""),

    md("""
Combine a loop with a condition and you have something genuinely useful: you
are now filtering data, which is most of what data work is.
"""),
    code("""
unusual = []

for reading in readings:
    if reading > 100 or reading < 60:
        unusual.append(reading)

print("unusual readings:", unusual)
print("how many:", len(unusual))
"""),

    md("""
## 6. Data structures

Four ways to hold more than one thing.

| Structure | Written as | Ordered | Changeable | Use it for |
|---|---|---|---|---|
| list | `[1, 2, 3]` | yes | yes | a sequence you will add to |
| tuple | `(1, 2)` | yes | **no** | a fixed pair or record |
| set | `{1, 2, 3}` | no | yes | unique values |
| dict | `{"key": "value"}` | yes | yes | labelled fields |

The dictionary is the one you will use most. It stores labelled values, which
is exactly what a record is.
"""),
    code("""
# One record from a registry. Real registries hold thousands of these.
record = {
    "study_code": "REG-0041",
    "age": 54,
    "resting_hr": 72,
    "consented": True,
}

print(record["study_code"])
print(record["age"])

record["last_visit"] = "2026-07-14"     # add a field
print(record)
"""),

    predict("What does `len(record)` return, and why?"),
    code("""
print(len(record))
print(list(record.keys()))
"""),

    md("""
A list of dictionaries is how tabular data looks before it becomes a table.
Next week it becomes a DataFrame, and this is what a DataFrame is made of.
"""),
    code("""
cohort = [
    {"study_code": "REG-0041", "age": 54, "resting_hr": 72},
    {"study_code": "REG-0042", "age": 38, "resting_hr": 65},
    {"study_code": "REG-0043", "age": 67, "resting_hr": 104},
]

for person in cohort:
    print(person["study_code"], "->", person["resting_hr"])
"""),

    md("""
## 7. Functions

A function is a named piece of code you can run again with different inputs.

Write one as soon as you notice you are about to copy and paste. That is the
signal, and it is reliable.
"""),
    code("""
def classify_rate(bpm):
    \"\"\"Return a plain-English description of a resting heart rate.\"\"\"
    if bpm > 100:
        return "high"
    elif bpm < 60:
        return "low"
    else:
        return "usual"


print(classify_rate(72))
print(classify_rate(105))
print(classify_rate(52))
"""),

    md("""
Three things to notice.

`def` names the function and lists what goes in. The line ending in `:` starts
an indented block, exactly like `if`. `return` sends a value back to whoever
called it — a function without `return` gives you `None`.
"""),

    predict("What does `classify_rate(60)` return? Careful with the boundary."),
    code("""
print(classify_rate(60))
print(classify_rate(100))
"""),

    md("""
Boundaries are where bugs live. `60` is not less than `60`, so it comes back
as "usual". Whether that is correct depends on the definition you were given,
and checking the boundary cases is the difference between code that works and
code that looks like it works.

Now a function that uses the record structure from earlier.
"""),
    code("""
def summarise(record):
    \"\"\"One line describing a person in the registry.\"\"\"

    # Step 1: take each field out of the dictionary and give it a name.
    study_code = record["study_code"]
    age = record["age"]
    resting_hr = record["resting_hr"]

    # Step 2: use the function we already wrote.
    category = classify_rate(resting_hr)

    # Step 3: build the sentence.
    sentence = f"{study_code} is {age} years old, resting rate {resting_hr} ({category})"

    # Step 4: hand it back to whoever called this function.
    return sentence


for person in cohort:
    print(summarise(person))
"""),

    md("""
Notice the `f` before the opening quote. That makes it an **f-string**, and
anything inside `{ }` is replaced by its value. It is the clearest way to build
text out of variables, and you will use it constantly.

Written out like that, every step has a name and you can read it top to bottom.
That is worth something while you are learning, and it is worth something again
in six months when you have forgotten how it works.
"""),

    md("""
### The same function, written shorter

Once you are comfortable, you will often skip the intermediate names and read
straight from the dictionary.
"""),
    predict("Will this print exactly the same lines as the version above?"),
    code("""
def summarise_short(record):
    \"\"\"The same thing, without the intermediate variables.\"\"\"
    category = classify_rate(record["resting_hr"])
    return f"{record['study_code']} is {record['age']} years old, resting rate {record['resting_hr']} ({category})"


for person in cohort:
    print(summarise_short(person))
"""),

    code("""
# Prove they agree, rather than assuming it.
for person in cohort:
    print(summarise(person) == summarise_short(person))
"""),

    md("""
Same output, half the lines. Two things to take from the comparison.

**Watch the quotes.** Inside an f-string written with double quotes, the
dictionary keys have to use single quotes — `record['age']`, not
`record["age"]`. Matching quotes end the string early, and the error you get
does not obviously point at the cause.

**Shorter is not automatically better.** The long version is easier to read,
easier to debug, and easier to change. The short version is quicker to write
and fine once the logic is settled. Professional code contains both, and
choosing between them is a judgement, not a rule.

Rewriting working code into a clearer or shorter form, without changing what it
does, is called **refactoring**. You have just done it, and the check above is
how you know you did it safely: the behaviour is identical.
"""),

    md("""
---

## Lab 1.1 — your turn

Work in your breakout pair. One of you types, the other explains what to type.
Swap halfway. If you are the more confident one, take the explaining role
first: you will learn more from it than from typing.

Everything you need is above.

### Core tasks

Finish these before the session ends.
"""),

    code("""
# 1. Make a list called `ages` holding the ages 54, 38, 67, 29, 71.
#    Print how many there are.

"""),
    code("""
# 2. Loop over `ages` and print each one, labelled, like:
#        age: 54

"""),
    code("""
# 3. Count how many people in `ages` are over 60. Print the count.

"""),
    code("""
# 4. Write a function `is_adult(age)` that returns True if age is 18 or over.
#    Test it with 17, 18 and 65.

"""),
    code("""
# 5. Add a new person to the `cohort` list: study code REG-0044, age 45,
#    resting heart rate 88. Then print a summary of every person using the
#    `summarise` function.

"""),

    md("""
### Stretch

Only if the core tasks are done. There is no prize for rushing.

1. Write `average(numbers)` that returns the mean of a list, without using
   `sum()` or `len()`. Use a loop and a counter.
2. Make `classify_rate` take an optional `low` and `high` boundary, so it can
   be used for something other than heart rate. Default them to 60 and 100 so
   existing calls keep working.
3. Using `cohort`, print only the people whose rate is not "usual", sorted by
   age, oldest first. Look up `sorted()` and its `key` argument.
"""),

    md("""
---

## Before you close the laptop

**Restart & Run All.** If it runs clean from top to bottom, your work is
genuinely finished. If it does not, that is worth knowing now rather than on
Monday.

Then:

- Re-type one demo from tonight into a blank notebook, from memory where you
  can. Re-typing is what makes it stick; copying is not.
- Bring one question to Slack or the 30-minute pre-lecture session on Monday.
  One question. Not a list, not nothing.

Next session: **Monday 10 August, NumPy** — arrays, and why they are much
faster than the lists you just used.
"""),
]


def build():
    notebook = nbf.v4.new_notebook(cells=CELLS)
    notebook.metadata = {
        "kernelspec": {"display_name": "Python (dsai)", "language": "python",
                       "name": "dsai"},
        "language_info": {"name": "python"},
        "colab": {"provenance": []},
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    nbf.write(notebook, str(OUTPUT))
    broken = sum(1 for c in CELLS
                 if "raises-exception" in c.get("metadata", {}).get("tags", []))
    print("wrote {} cells ({} deliberate errors) to {}".format(
        len(CELLS), broken, OUTPUT))


if __name__ == "__main__":
    build()
