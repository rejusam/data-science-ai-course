"""Assemble the session 2 notebook: Python basics.

    python3 tools/build_01_python_basics.py

The notebook is a build artefact. Edit this file, not the .ipynb.

Replaces the earlier `lab-1-1-python-basics.ipynb`, which was edited live during
the session and drifted from its build script (a markdown cell became a raw
cell, so it stopped rendering). That file and its build script were removed on
10 Aug 2026, once this one was published.

Content added here that the session ran out of time for, all of it on the deck:
comments (slide 9), `input()` (slide 10), `while` with `break`, `continue` and
`pass` (slide 13), tuples and sets (slide 14), and the rest of functions —
default arguments, several return values, scope (slide 15).

`input()` is shown but never called. Calling it stops a Restart & Run All dead,
waiting for typing that never comes, and this notebook has to run unattended to
be testable.

Cells that are meant to fail carry the `raises-exception` tag, so students see
the real traceback while the notebook still runs top to bottom.
"""
from pathlib import Path

import nbformat as nbf

REPO = Path(__file__).resolve().parent.parent
OUTPUT = (REPO / "modules" / "01a-programming-fundamentals" / "notebooks"
          / "01-python-basics.ipynb")


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


def checkpoint(what):
    return md("""
> **Checkpoint.** {}
""".format(what))


CELLS = [
    md("""
# Session 2 — Python basics

Data Science & AI, Wednesday 5 August.

You ranked "write clean, confident Python" last of the five things you want
from this course. That is a completely reasonable thing to want least, and it
is still the first thing we teach, because everything you ranked above it is
built on it. You cannot tell a convincing story about a model you could not
build.

By the end of this notebook you will have written and run: variables,
conditions, loops, all four data structures, and functions that do something
real.

**How to run a cell:** click it, then press `Shift + Enter`.
"""),

    md("""
## Before you type anything

**Work on your own copy, not on this file.**

- Jupyter or VS Code: copy this notebook into `notebooks/my-work/` and open
  that copy. The folder is ignored by git, so `git pull` will never argue with
  your edits.
- Colab: **File → Save a copy in Drive**, then work in the copy.

## Then: Restart & Run All

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
"""),

    md("""
## 0. What programming actually is  *(slides 4 to 8)*

Programming is writing down a set of instructions precisely enough that a
machine can follow them. The hard part is almost never the typing.

The deck separates two words that get used interchangeably. **Programming** is
working out what the steps are, and it is language-independent. **Coding** is
writing those steps in a particular language. You can be good at one and bad at
the other, and the expensive mistakes live on the programming side.

A program takes an **input** and produces an **output**. Everything in this
course is that shape, from tonight's five-line cell to the capstone.

Slide 7 gives a loop for problems that are not obvious: **define, decompose,
search, verify**. Here it is on something small enough to see all of at once.
"""),

    md("""
**Define.** "Find the unusual readings" is not yet a problem a machine can
solve. What counts as unusual? Say it exactly:

> Given a list of resting heart rates, return the ones below 60 or above 100.

That sentence is the specification. Writing it is programming; everything after
it is coding.

**Decompose.** Three steps, each of which you could do on paper:

1. look at each reading in turn
2. decide whether it is outside the range
3. keep the ones that are

**Search.** Try it.
"""),
    code("""
readings = [68, 72, 91, 105, 58]

unusual = []
for reading in readings:            # 1. each in turn
    if reading < 60 or reading > 100:   # 2. decide
        unusual.append(reading)     # 3. keep it

print("input :", readings)
print("output:", unusual)
"""),

    md("""
**Verify.** Not "it printed something", but "it printed the right something".
Check a case you can work out in your head, including an awkward one.
"""),
    code("""
assert unusual == [105, 58]

# The awkward cases: nothing unusual, and everything unusual.
def find_unusual(values):
    return [v for v in values if v < 60 or v > 100]

assert find_unusual([70, 80, 90]) == []
assert find_unusual([30, 200]) == [30, 200]
assert find_unusual([]) == []

print("verified on four cases, including the empty one")
"""),

    md("""
That is the whole loop, and you will run it hundreds of times over the next
twenty-five weeks. The step people skip is the first one, and skipping it is
what produces code that runs beautifully and answers the wrong question.

The rest of tonight is the coding half: the syntax you need so that the steps
you have worked out can actually be typed.
"""),

    md("""
## 1. Your first cell, and how to leave notes  *(slide 9)*

`print()` displays something. Run this.
"""),
    code("""
print("I am writing Python.")
"""),

    md("""
Anything after a `#` is a **comment**: Python ignores it, people read it. Three
quotes on either side make a block of text that spans several lines, which is
how you describe a whole function or file.

Comments are for whoever maintains the code, including you in six months.
Explain *why*, not *what* — the code already says what.
"""),
    code("""
# A single-line comment.

readings = [68, 72, 91, 105, 58]     # a comment can also sit after code

\"\"\"
Several lines at once.
Used at the top of a file or a function to say what it is for.
\"\"\"

print(readings)
"""),

    md("""
## 2. Variables  *(slide 11)*

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
### Getting something in, getting something out  *(slide 10)*

`print()` is output. `input()` is the other direction: it stops, waits for
someone to type, and hands back what they typed.

```python
age = input("How old is the patient? ")
print("They are", age, "years old")
```

**We are not running that here on purpose.** `input()` waits forever for
typing, which would stop Restart & Run All dead. Try it in a scratch notebook
instead.

One thing to know before you do. `input()` always gives you **text**, even when
the person typed digits. Convert it before doing arithmetic, or you will meet
the `TypeError` from a moment ago.
"""),
    code("""
typed = "54"                 # pretend this came back from input()

print(type(typed))           # str, not int
print(typed + "1")           # joining text: "541"
print(int(typed) + 1)        # convert first, then it is arithmetic: 55
"""),

    md("""
Most of the time in data science you will read from a file rather than ask a
person, so `input()` matters less here than in a first programming course. It
is worth meeting once.
"""),

    md("""
## 3. Operators  *(slide 12)*

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

`and`, `or` and `not` combine conditions.
"""),
    code("""
resting = 72
print(resting > 100)
print(resting == 72)
print(resting != 72)
print(60 <= resting <= 100)               # Python lets you chain these
print(resting > 60 and resting < 100)     # the same thing, spelled out
print(not resting > 100)
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
## 4. Making decisions  *(slide 13)*

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
### Put the lines in order

These five lines make a working program that counts the readings above 100.
They are in the wrong order, and two of them need indenting.

```
        total = total + 1
print(total)
    if reading > 100:
total = 0
for reading in readings:
```

Type them into the next cell in the right order. Agree with your pair before
you run it.
"""),
    code("""
# Your reordered version:

"""),

    md("""
## 5. Repeating things  *(slide 13)*

A `for` loop repeats once for each item in a collection.
"""),
    predict("How many lines does this print, and what is the last one?"),
    code("""
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
### `while`, and three words that steer a loop

A `for` loop runs once per item. A `while` loop runs until a condition stops
being true, which is what you want when you do not know how many turns it will
take.
"""),
    predict("How many lines does this print?"),
    code("""
countdown = 3

while countdown > 0:
    print("beat in", countdown)
    countdown = countdown - 1     # without this line it never stops

print("beat")
"""),

    md("""
**The line that changes the condition is the one people forget.** Leave it out
and the loop runs forever; in Jupyter you would stop it with the square button
in the toolbar.

Three words steer any loop:

| Word | What it does |
|---|---|
| `break` | leave the loop immediately |
| `continue` | skip to the next turn |
| `pass` | do nothing at all, but be a valid block |

`pass` exists because Python needs *something* indented under an `if`. It is a
placeholder for code you have not written yet.
"""),
    code("""
for reading in [58, 68, 72, 91, 105]:
    if reading < 60:
        print("skipping", reading)     # too low to be interesting
        continue                       # straight to the next reading
    if reading > 100:
        print("stopping at", reading)
        break                          # leave the loop, do not finish the list
    print("checked", reading)

for reading in readings:
    if reading == 91:
        pass                           # a decision we have not made yet
    else:
        pass
"""),

    checkpoint("Quick poll before the break: what does `continue` do, and what "
               "does `pass` do?"),

    md("""
## 6. Data structures  *(slide 14)*

Four ways to hold more than one thing.

| Structure | Written as | Ordered | Changeable | Use it for |
|---|---|---|---|---|
| list | `[1, 2, 3]` | yes | yes | a sequence you will add to |
| tuple | `(1, 2)` | yes | **no** | a fixed pair or record |
| set | `{1, 2, 3}` | no | yes | unique values |
| dict | `{"key": "value"}` | yes | yes | labelled fields |

Lists first, since you have been using one.
"""),
    code("""
scores = [5, 3, 7, 2]

scores.append(9)        # add to the end
scores.sort()           # rearrange in place
print(scores)
print("first :", scores[0])       # counting starts at 0
print("last  :", scores[-1])      # negative counts from the end
print("middle:", scores[1:4])     # from 1 up to but not including 4
"""),

    md("""
A **tuple** is a list that cannot be changed after it is made. Use one when the
grouping is fixed: a pair of coordinates, a record with a known shape, or
several values coming back from a function.
"""),
    code("""
reading = (72, "bpm")           # the value and its unit belong together

value, unit = reading           # unpack it into two names
print(value, unit)
"""),

    md("""
### Deliberate error four

Try to change one.
"""),
    breaks("""
reading[0] = 80
"""),

    md("""
`TypeError: 'tuple' object does not support item assignment`

That is the whole point of a tuple. If something must not change, saying so in
the type stops a whole class of bug before it happens.

A **set** holds unique values, unordered. Ask it "have I seen this before" and
it answers instantly, however large it is.
"""),
    predict("How many items are in "
            "`{\"REG-0041\", \"REG-0042\", \"REG-0041\"}`?"),
    code("""
seen = {"REG-0041", "REG-0042", "REG-0041"}

print(seen)
print("how many :", len(seen))
print("is REG-0042 in there?", "REG-0042" in seen)

print("unique readings:", set([68, 72, 68, 91, 72]))
"""),

    md("""
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
print(type(record))
"""),

    md("""
`len` counts the keys, and there are five once `last_visit` has been added.

Ask for a key that is not there and you get a `KeyError`. `.get()` returns
`None` instead of failing, which is what you want when a field is genuinely
optional.
"""),
    code("""
print(record.get("weight_kg"))                  # None, no error
print(record.get("weight_kg", "not recorded"))  # or a value of your choosing
"""),

    md("""
A list of dictionaries is how tabular data looks before it becomes a table.
Next session it becomes a DataFrame, and this is what a DataFrame is made of.
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
## 7. Functions  *(slide 15)*

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

Rather than reading the output and nodding, say what you expect and let Python
check it. `assert` stays silent when it is right and fails loudly when it is
not.
"""),
    code("""
assert classify_rate(105) == "high"
assert classify_rate(52) == "low"
assert classify_rate(72) == "usual"
assert classify_rate(60) == "usual"     # the boundary
assert classify_rate(100) == "usual"    # the other boundary

print("all five checks passed")
"""),

    md("""
### Arguments that have a default

Put a value in the `def` line and the caller can leave that argument out.
"""),
    code("""
def classify(bpm, low=60, high=100):
    \"\"\"The same idea, with the thresholds exposed.\"\"\"
    if bpm > high:
        return "high"
    if bpm < low:
        return "low"
    return "usual"


print(classify(58))                    # the usual thresholds
print(classify(58, low=55))            # a different rule, same function
print(classify(58, 55, 95))            # positionally: low then high
"""),

    md("""
That is what makes a function reusable rather than a piece of code with a name
stuck on it. The rule is now something the caller states, instead of a number
buried inside the body where nobody can see it.

Arguments are matched by position unless you name them. Naming them is worth
the extra characters — `classify(58, 55, 95)` needs you to remember the order,
`classify(58, low=55, high=95)` does not.
"""),

    md("""
### Giving back more than one thing

`return` can hand back several values, separated by commas. That builds a
tuple, which you then unpack.
"""),
    code("""
def summarise_readings(values):
    \"\"\"Return the lowest, highest and average of a list of readings.\"\"\"
    return min(values), max(values), sum(values) / len(values)


lowest, highest, average = summarise_readings(readings)

print("lowest  :", lowest)
print("highest :", highest)
print("average : {:.1f}".format(average))
"""),

    md("""
### Where a name lives

Names created inside a function exist only inside it. This is **scope**.
"""),
    code("""
def count_high(values, limit=100):
    total = 0
    for value in values:
        if value > limit:
            total = total + 1
    return total


print(count_high(readings))
"""),

    md("""
### Deliberate error five

`total` did its job. Now ask for it from outside the function.
"""),
    breaks("""
print(total)
"""),

    md("""
`NameError: name 'total' is not defined`

`total` was created inside `count_high` and stopped existing the moment the
function returned. That is deliberate: a function you can only affect through
its arguments, and only hear from through its return value, is a function you
can reason about on its own.

The traffic goes one way. A function can see names from the main notebook —
`readings` is visible inside `count_high` even though it was never passed in —
but the notebook cannot see inside the function. Relying on that is a bad
habit; pass what you need as an argument and the function keeps working
wherever you move it.
"""),

    md("""
### A function that uses the record structure
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
    assert summarise(person) == summarise_short(person)

print("both versions agree on all", len(cohort), "records")
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

## Your turn  *(slide 33)*

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
    code("""
# 6. Make a set of every study code in `cohort` and print how many unique
#    codes there are.

"""),
    code("""
# 7. Write `oldest_and_youngest(people)` that takes the cohort list and returns
#    two values: the oldest age and the youngest. Unpack them into two names
#    when you call it.

"""),

    md("""
### Check your own work

Run this once tasks 4 and 7 are written. It stays quiet if they are right.
"""),
    code("""
if "is_adult" not in dir() or "oldest_and_youngest" not in dir():
    print("Finish tasks 4 and 7 first, then run this cell again.")
else:
    assert is_adult(18)
    assert not is_adult(17)
    assert is_adult(65)

    oldest, youngest = oldest_and_youngest(cohort)
    assert oldest >= youngest

    print("both functions look right: oldest {}, youngest {}".format(
        oldest, youngest))
"""),

    md("""
### Stretch

Only if the core tasks are done. There is no prize for rushing.

1. Write `average(numbers)` that returns the mean of a list, without using
   `sum()` or `len()`. Use a loop and a counter.
2. Rewrite task 3 with a `while` loop instead of a `for` loop. Which reads
   better, and why?
3. Using `cohort`, print only the people whose rate is not "usual", sorted by
   age, oldest first. Look up `sorted()` and its `key` argument.
"""),

    checkpoint("Pace check before you go: green, amber or red."),

    md("""
---

## Before you close the laptop

**Restart & Run All.** It should run clean from top to bottom, apart from the
five cells we broke on purpose.

Then:

- Re-type one demo from this notebook into a blank notebook, from memory where
  you can. Re-typing is what makes it stick; copying is not.
- Bring one question to Slack or the 30-minute pre-lecture session. One
  question. Not a list, not nothing.

Next: **`02-numpy.ipynb`** — arrays, and why they are much faster than the
lists you just used.
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
