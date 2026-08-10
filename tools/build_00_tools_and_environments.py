"""Assemble the tools and environments notebook.

    python3 tools/build_00_tools_and_environments.py

The notebook is a build artefact. Edit this file, not the .ipynb.

Interactive counterpart to deck slides 16 to 22 (developing and running Python,
Jupyter, environments, pip, Anaconda, SciPy) and 34 to 35 (scikit-learn,
statsmodels, BeautifulSoup, NLTK).

Everything here inspects the machine it runs on rather than describing one, so
a student on Colab, on Windows and on a Mac each get a different, correct
answer from the same cell. Nothing installs anything: install commands are
shown as text, because a notebook that pip-installs behind your back is how
environments get broken.
"""
from pathlib import Path

import nbformat as nbf

REPO = Path(__file__).resolve().parent.parent
OUTPUT = (REPO / "modules" / "01a-programming-fundamentals" / "notebooks"
          / "00-tools-and-environments.ipynb")


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
> Put your answer in the chat before we run it.
""".format(question))


CELLS = [
    md("""
# Tools and environments

*Deck slides 16 to 22, and 34 to 35.*

Every cell here asks your computer a question about itself. The answers will
differ between you and the person next to you, and that is the point: most
setup problems are not mysterious, they are a question nobody thought to ask.

Come back to this notebook whenever something "works on their machine".
"""),

    md("""
## Before you type anything

Copy this notebook into `notebooks/my-work/` and work on the copy. On Colab,
**File → Save a copy in Drive**. Then **Restart & Run All**.
"""),

    md("""
## 1. Which Python is this?  *(slide 17)*

You may have several Pythons installed. The system one, the Anaconda one, one
per environment. Only one of them is running this notebook.
"""),
    predict("Will `sys.executable` point at a folder with `dsai` in the name?"),
    code("""
import sys
import platform
from pathlib import Path

print("python version :", sys.version.split()[0])
print("interpreter    :", sys.executable)
print("platform       :", platform.system(), platform.release())
print("machine        :", platform.machine())
"""),

    md("""
`sys.executable` is the single most useful line in this notebook. When an
import fails for a package you are certain you installed, you almost always
installed it into a different interpreter from the one running your code.

The path tells you which environment you are in. If it contains `envs/dsai`,
you are in the course environment. If it says `anaconda3/bin/python` with no
`envs`, you are in `base`, which is the most common cause of a missing package
in this course.
"""),
    code("""
IN_COLAB = "google.colab" in sys.modules

env_name = Path(sys.executable).parent.parent.name

print("environment    :", env_name)
print("running in Colab:", IN_COLAB)

if IN_COLAB:
    print("\\nColab gives you a ready-made environment. conda is not involved,")
    print("and most of this course's packages are already there.")
elif env_name == "dsai":
    print("\\nThis is the course environment. Correct.")
else:
    print("\\nThis is NOT the dsai environment.")
    print("In Jupyter: Kernel > Change Kernel > Python (dsai).")
    print("In VS Code: click the kernel name, top right.")
"""),

    md("""
## 2. What a notebook actually is  *(slide 18)*

A notebook is two things: a document, and a **kernel**, which is a Python
process sitting behind it holding every variable you have made.

The document is a file of cells. The kernel is running memory. Restarting the
kernel throws away the memory and keeps the document, which is why Restart &
Run All is the honest test of whether your code works.

Two pieces of syntax belong to the notebook rather than to Python.
"""),
    code("""
# A line starting with % is a magic: an instruction to the notebook itself.
%config InlineBackend.figure_format = "retina"

# A line starting with ! runs a shell command.
!python --version

# Time a line of code without writing any timing code.
%timeit sum(range(100_000))
"""),

    md("""
Neither `%` nor `!` is Python. Paste a line beginning with either into a `.py`
file and it is a syntax error. That is one of the reasons session 5 moves code
out of notebooks and into modules.
"""),

    md("""
## 3. Environments  *(slide 19)*

An environment is a self-contained set of packages with its own Python.

The problem it solves: project A needs pandas 1.5, project B needs pandas 2.2,
and one computer cannot have both installed globally. Environments give each
project its own shelf instead of one shared pile.

The course environment is called `dsai` and is built from
[`setup/environment.yml`](../../../setup/environment.yml).
"""),
    code("""
import shutil
import subprocess

def run(command):
    \"\"\"Run a shell command and return its output, or a readable message.\"\"\"
    program = command.split()[0]
    if shutil.which(program) is None:
        return "{} is not available here (normal on Colab)".format(program)
    finished = subprocess.run(command.split(), capture_output=True, text=True)
    return (finished.stdout or finished.stderr).strip()


print(run("conda env list"))
"""),

    md("""
The `*` marks the active environment. If you have several, that star is the
answer to "which one am I in".

**The trap:** `conda install` puts a package into whichever environment is
active. Installing into `base` while `dsai` is selected as your kernel gives
you a package you cannot import, with no error to explain it. Activate first,
install second:

```
conda activate dsai
conda install seaborn
```
"""),

    md("""
## 4. Installing packages  *(slide 20)*

`pip` and `conda` both install packages. Prefer `conda` inside a conda
environment, and use `pip` for the few things conda does not carry.

The commands from the slide, none of which we are running here:

```
pip install anypkg                 # install
pip install --upgrade anypkg       # upgrade
pip install anypkg==1.0.4          # a specific version
pip install -r requirements.txt    # everything a project needs
```

**Do not install from inside a notebook** unless you know exactly why. It
installs into whatever interpreter happens to be running, which is how the
"I installed it and it still says ModuleNotFoundError" afternoon begins.

What you can safely do from here is look.
"""),
    code("""
print(run("conda list numpy"))
"""),

    md("""
## 5. What is on this machine  *(slides 22, 23, 26, 27, 34, 35)*

The SciPy ecosystem, plus the libraries the rest of the deck names. Each line
imports the real package and reports its real version, so this doubles as an
install check.
"""),
    code("""
import importlib

LIBRARIES = [
    ("numpy",       "arrays and numerical computing"),
    ("pandas",      "tables, the DataFrame"),
    ("matplotlib",  "plots, the foundation everything else draws on"),
    ("seaborn",     "statistical plots, built on matplotlib"),
    ("scipy",       "scientific computing: statistics, optimisation, signals"),
    ("sklearn",     "machine learning, from module 4 onwards"),
    ("statsmodels", "statistical modelling and R-style formulae"),
    ("bs4",         "reading HTML, for the web scraping in module 3"),
    ("nltk",        "text processing, for module 8"),
]

for name, purpose in LIBRARIES:
    try:
        module = importlib.import_module(name)
        version = getattr(module, "__version__", "installed")
        print("  {:<12} {:<10} {}".format(name, version, purpose))
    except ImportError:
        print("  {:<12} {:<10} {}".format(name, "MISSING", purpose))
"""),

    md("""
Anything reading `MISSING` is worth sorting out before the module that needs
it, not on the night. Post the line in Slack.

Two of those names are not what you would guess: `sklearn` is the import name
for scikit-learn, and `bs4` is the import name for BeautifulSoup. **The name
you install is not always the name you import.**
"""),

    md("""
### Deliberate error

The most common setup error in the course, on purpose.
"""),
    breaks("""
import tensorflow
"""),

    md("""
`ModuleNotFoundError: No module named 'tensorflow'`

Correct, and not a problem. TensorFlow is deliberately left out of `dsai`
because it is large and is not needed until module 9; `setup/extras/` covers
installing it when we get there.

When you meet this error for a package you *do* expect, work through it in this
order:

1. `sys.executable` — which interpreter is this?
2. `conda env list` — is the environment you installed into the active one?
3. Is the notebook's kernel that same environment?

It is almost always step 3.
"""),

    md("""
## 6. The one command that checks everything  *(slide 21)*

The repository has a script that runs the whole check for you, including the
command-line tools this notebook cannot see.

```
conda activate dsai
python setup/verify.py
```

Run it in a terminal whenever something feels wrong. It is faster than
guessing, and its output is the thing to paste into Slack when you ask for
help.

Anaconda Navigator, on slide 21, is the clicking version of everything above:
environments down the left, packages in the middle, and a Launch button for
JupyterLab and VS Code. Nothing is wrong with using it. The commands are worth
knowing because they are what you will find in every answer online.
"""),

    md("""
---

## Your turn

Short, and worth doing once properly.
"""),
    code("""
# 1. Print sys.executable and say, in a comment, which environment it is.

"""),
    code("""
# 2. Print the version of pandas and of numpy that are actually loaded here.

"""),
    code("""
# 3. Use importlib to check whether `plotly` is installed. Print a clear
#    message either way, without letting the cell fail.

"""),
    code("""
# 4. Find out where pandas is installed on disk. Hint: a module has a __file__.

"""),

    md("""
### Check your own work
"""),
    code("""
import pandas as pd

assert pd.__version__.startswith("2."), "this course expects pandas 2.x"
assert Path(pd.__file__).exists()

print("pandas", pd.__version__, "loaded from")
print(" ", Path(pd.__file__).parent)
"""),

    md("""
---

## Before you close the laptop

If any library came back `MISSING`, or your environment is not `dsai`, sort it
out now rather than at the start of the next session. The setup checklist is
[`resources/setup-checklist.md`](../../../resources/setup-checklist.md) and the
support session before each class exists for exactly this.
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
