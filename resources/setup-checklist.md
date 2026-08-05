# Setup checklist

Everything you need working, in the order to do it. Tick as you go.

There are several setup guides in this repository and it is not obvious which
comes first. This page is the order. Follow it top to bottom and skip nothing.

**Time:** about 90 minutes in total, most of it waiting for downloads. You can
stop after any stage and pick it up later — each one is complete on its own.

**If you get stuck at any point:** post in Slack with the command you ran and
the full error as text, and say which operating system you are on. Do not sit
on a broken setup. It is a ten-minute problem this week and a serious one by
week four.

---

## Stage 1 — The four tools

Guide: [`installing-the-tools.md`](installing-the-tools.md)
*(the same guide as a printable [PDF](installing-the-tools.pdf))*

- [ ] Anaconda installed
- [ ] VS Code installed
- [ ] Git installed
- [ ] GitHub account created, email confirmed

Check yourself. On Windows use **Anaconda Prompt**; on Mac use **Terminal**:

```
conda --version
git --version
```

Both should print a version number.

> **On a work or shared computer and blocked from installing?** Stop here and
> tell us in Slack. Use Google Colab in the meantime — it runs in the browser
> and needs nothing installed. You will not be left behind, but we need to know.

---

## Stage 2 — The course environment

Guide: [`../setup/README.md`](../setup/README.md)

- [ ] Repository cloned to your machine
- [ ] Setup script run
- [ ] `conda activate dsai` shows `(dsai)` at the start of your prompt
- [ ] `python setup/verify.py` prints `OK` on every line

`verify.py` is the single command that checks everything — the tools, the
environment you are in, and all the packages. Run it any time you are not sure
whether your setup is still intact.

This is the stage that takes longest. The download is around 1 GB and the
progress display sits still for long stretches. That is normal.

> **Post your `verify.py` output in Slack when it passes.** That is how we know
> you are ready, without you having to explain anything. If some lines say
> `MISSING`, post it anyway — that is more useful to us than silence.

---

## Stage 3 — VS Code and Anaconda

Guide: [`vs-code-and-anaconda.md`](vs-code-and-anaconda.md)

- [ ] Python extension installed (by Microsoft)
- [ ] Jupyter extension installed (by Microsoft)
- [ ] Interpreter set to **`dsai`**, not `base`
- [ ] Windows only: `conda init powershell` and execution policy done
- [ ] Terminal in VS Code shows `(dsai)`
- [ ] A notebook opens and its kernel says **Python (dsai)**

The single most common mistake at this stage is selecting `base` instead of
`dsai`. If your imports fail after this, check that first.

---

## Stage 4 — Git and GitHub

Guide: [`installing-git-and-github-cli.md`](installing-git-and-github-cli.md)

- [ ] GitHub CLI (`gh`) installed
- [ ] `git config user.name` and `user.email` set, using your GitHub email
- [ ] `gh auth login` completed
- [ ] `gh auth status` shows a tick and your username
- [ ] You have cloned this repository and can see its commit history

Half the cohort had never heard of Git in week 1, so this stage is expected to
be unfamiliar. It is also the one that pays off most: by week 24 your GitHub
profile is what employers actually look at.

---

## Stage 5 — Ready to work

- [ ] Read [`notebook-hygiene.md`](notebook-hygiene.md). One page, five minutes.
- [ ] Open `modules/01a-programming-fundamentals/notebooks/lab-1-1-python-basics.ipynb`
- [ ] Run **Restart & Run All**. It should complete without stopping.

That notebook contains three cells that are broken on purpose, so you will see
three red tracebacks. That is expected and the notebook keeps running past
them. Reading errors is a skill this course teaches deliberately.

---

## Before every session from now on

```
cd data-science-ai-course
git pull
conda activate dsai
jupyter lab
```

Four commands. `git pull` fetches the new material, `conda activate` puts you
in the right environment. Neither is optional, and forgetting the second is the
cause of most "it was working yesterday" messages.

**You clone once and pull thereafter.** `git clone` creates the folder; running
it again in the same place fails with "destination path already exists", which
is not a problem to fix — it means you already have the repository and should
`cd` into it and `git pull` instead.

---

## Quick diagnosis

| What you see | What it means | Where to look |
|---|---|---|
| `conda: command not found` | Terminal opened before the installer finished, or wrong terminal on Windows | [Stage 1](#stage-1--the-four-tools) |
| `gh` or `git` "not recognized" while `(dsai)` is showing | Tool installed into a different conda environment. They are per-environment | [Git guide](installing-git-and-github-cli.md#troubleshooting) |
| `destination path ... already exists and is not an empty directory` | You have already cloned it. Clone once, `git pull` thereafter | `cd data-science-ai-course && git pull` |
| `git pull` refuses, "local changes would be overwritten" | You edited a file that also changed upstream | Copy your version elsewhere, pull, then merge by hand. Ask in Slack rather than forcing |
| Prompt has no `(dsai)` | Environment not activated | Run `conda activate dsai` |
| `ModuleNotFoundError` in a terminal | Wrong environment | Check `(dsai)` is in your prompt |
| `ModuleNotFoundError` in a notebook | Wrong kernel | [Stage 3](#stage-3--vs-code-and-anaconda), Phase 4 |
| Push asks for a password | Git not using the GitHub CLI for credentials | Run `gh auth setup-git` |
| Code works, then stops working | Cells run out of order | [`notebook-hygiene.md`](notebook-hygiene.md) |
| SSL or certificate error from conda | Network inspects encrypted traffic | [Git guide](installing-git-and-github-cli.md#if-conda-fails-with-an-ssl-or-certificate-error) — try `truststore` first, and do **not** disable verification |
