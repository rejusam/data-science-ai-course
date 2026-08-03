# Data Science & AI

Course materials for a 25 week, part time Data Science and AI programme, taken
from zero programming experience to a deployed capstone project.

Maintained by Dr Reju Sam John. The repository grows as the course runs, so
run `git pull` before each session.

## Start here

If you are a student joining the course, do these three things in order.

**1. Install the tools.** Anaconda, VS Code, Git, and a GitHub account.

- Comfortable with a terminal, or willing to be: [`setup/README.md`](setup/README.md)
- Prefer clicking through installers: [`resources/installing-the-tools.md`](resources/installing-the-tools.md)

**2. Build the environment.** One command, once.

```
git clone https://github.com/rejusam/data-science-ai-course.git
cd data-science-ai-course
bash setup/setup-mac.sh              # macOS or Linux
```

On Windows, open **Anaconda Prompt** and run:

```
setup\setup-windows.bat
```

**3. Check it worked.**

```
conda activate dsai
python setup/verify.py
```

Every line should say `OK`. If not, the output tells you what to do, and
[`setup/README.md`](setup/README.md) has a troubleshooting section.

## What is in here

| Folder | Contents |
|---|---|
| [`setup/`](setup) | Environment definition, install scripts, verification |
| [`modules/`](modules/README.md) | Teaching material, one folder per module, in course order |
| [`labs/`](labs) | Lab exercises |
| [`projects/`](projects) | Mini project and capstone briefs |
| [`resources/`](resources) | Cheat sheets, glossary, further reading |
| [`SYLLABUS.md`](SYLLABUS.md) | Every session, date, topic and due date |

## The shape of the course

Twenty-five weeks, running 3 August 2026 to 6 February 2027. Sixty teaching
sessions: Monday and Wednesday evenings, plus a full-day Saturday intensive
every second week.

The path through the material:

1. **Programming and maths** — Python, NumPy, pandas, then the linear algebra,
   calculus and statistics that machine learning is built on.
2. **Getting and understanding data** — exploratory analysis, SQL, APIs, cloud
   data platforms.
3. **Modelling** — regression, classification, clustering, trees and ensembles.
4. **Language and deep learning** — NLP, transformers, neural networks, CNNs.
5. **Shipping** — generative AI applications, deployment, MLOps, and a capstone
   you present and can show an employer.

Three mini projects along the way, each ending in a public GitHub repository
with a README. See [`SYLLABUS.md`](SYLLABUS.md) for dates and due dates.

## How to work in this repository

Activate the environment before you do anything:

```
conda activate dsai
```

Your prompt will show `(dsai)`. If it does not, packages will appear to be
missing.

Start Jupyter from the repository root, so notebook paths to `data/` folders
work as written:

```
jupyter lab
```

Inside a notebook, choose the kernel named **Python (dsai)**.

Pull new material before each session:

```
git pull
```

If `git pull` complains that your local changes would be overwritten, it is
because you edited a file that has since changed upstream. Copy your work
somewhere safe first, then ask in Slack. Do not force anything.

Keep your own work in a folder named `scratch/`. It is ignored by git, so it
will never conflict with course updates.

## A note on using AI tools

You will use large language models in this course, and module 10 is about
building with them. Two rules make the difference between using them well and
using them badly.

Write the code yourself first, then ask for a review. If you generate code you
cannot explain line by line, you have not learned anything, and it will show in
an interview.

Check what they tell you. Language models produce confident, well-formatted,
wrong answers, particularly about library APIs and version-specific behaviour.
Run the code. Read the actual documentation.

## The cohort dashboard

An interactive dashboard built from the session 1 poll data lives in
[`streamlit_app.py`](streamlit_app.py). Six tabs, ten charts, a table view for
every question, and a download of the underlying data.

Run it locally:

```
conda activate dsai
pip install streamlit plotly
streamlit run streamlit_app.py
```

`requirements.txt` at the repository root exists for Streamlit Community
Cloud, which installs with pip and does not use conda. It is deliberately
separate from `setup/environment.yml`, which is the coursework environment.

## Licence

Course materials are released under [CC BY-NC-SA 4.0](LICENSE). Code samples
and scripts in this repository may be reused under the MIT terms noted in the
same file.
