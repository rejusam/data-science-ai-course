# Git and GitHub, hands on

One hour. You finish it with your own repository on GitHub, containing your own
work, with at least one commit you made yourself.

This is the exercise sheet. The reference material is elsewhere:
[`installing-git-and-github-cli.md`](installing-git-and-github-cli.md) to get
the tools working, and [`git-cheatsheet.md`](git-cheatsheet.md) for the
commands afterwards.

**Which terminal.** Windows: **Anaconda Prompt** from the Start menu. Mac:
**Terminal**.

**On Colab?** Colab has no repository. Do the exercise on your own machine if
you can. If you genuinely cannot, download your notebook with
**File → Download → .ipynb** and upload it through the GitHub website at step
4, using **Add file → Upload files**. You will miss the command practice, so
pair with someone at a laptop.

---

## 0. Check you are ready (5 minutes)

```
git --version
gh auth status
```

Both must answer. If either does not, stop and fix that first. The guide is
[`installing-git-and-github-cli.md`](installing-git-and-github-cli.md), and one
of the trainers will come to you.

Then check git knows who you are:

```
git config --global user.name
git config --global user.email
```

Empty output means it does not. Set both now, with the email address on your
GitHub account, or your commits will not be credited to you.

---

## 1. The words, once (5 minutes)

| Word | What it means |
|---|---|
| repository | a folder whose history git is tracking |
| commit | a saved point in that history, with a message saying why |
| push | send your commits to GitHub |
| pull | bring GitHub's commits down to your laptop |
| clone | make your own local copy of a repository that already exists |
| fork | make your own copy **on GitHub** of someone else's repository |
| branch | a line of development you can work on without disturbing the main one |
| pull request | a proposal to merge one branch into another, with a discussion attached |

You have already used `clone` and `pull`: that is how you got this course
material and how you have kept it up to date. The rest is new today.

---

## 2. Make a repository (10 minutes)

From your terminal, somewhere outside the course repository. Your home folder
is fine.

```
mkdir ds-practice
cd ds-practice
git init
```

`git init` starts the history. Nothing is tracked yet.

```
git status
```

Read that output. It says which branch you are on and that there is nothing to
commit.

---

## 3. Your first commit (10 minutes)

Put something real in it. Copy in a notebook you have written this fortnight, or
create a file:

```
echo "# My data science practice" > README.md
```

Then the loop you will repeat for the rest of your career:

```
git status          # what changed
git add README.md   # choose what goes in this commit
git commit -m "Start a practice repository"
git status          # clean again
```

**Write the message for someone else.** "Start a practice repository" says why.
"update" and "stuff" say nothing, and you will be reading these back when
something breaks.

Now add your notebook too:

```
git add my-notebook.ipynb
git commit -m "Add the NumPy work from session 3"
```

**Before you commit a notebook, clear its outputs**, with Kernel → Restart Kernel
and Clear All Outputs. Outputs make the diff unreadable and can make the file
enormous.

---

## 4. Put it on GitHub (10 minutes)

```
gh repo create ds-practice --private --source=. --push
```

That creates the repository on GitHub, links it to this folder, and pushes what
you have. Read each flag: `--private` because it is yours, `--source=.` meaning
this folder, `--push` to send it straight away.

```
gh repo view --web
```

Your work, on the internet. That URL is the thing you will put in front of an
employer in six months, so it is worth it being tidy.

Prefer clicking? **New repository** on github.com, then follow the "push an
existing repository" lines it shows you. Same result.

---

## 5. A branch and a pull request (15 minutes)

Branches are how you change something without breaking what already works.

```
git checkout -b add-summary
```

Change a file. Add a few lines to `README.md` saying what you have learned so
far. Then:

```
git add README.md
git commit -m "Describe what the repository contains"
git push -u origin add-summary
```

```
gh pr create --fill
```

Open it in the browser with `gh pr view --web`. That is the review surface: the
diff, the discussion, and the merge button. On a team, someone else reads it
before it merges. On your own repository you are both author and reviewer, which
is still worth doing, because reading your own diff catches things.

Merge it:

```
gh pr merge --squash --delete-branch
git checkout main
git pull
```

---

## 6. An issue (5 minutes)

Issues are the to-do list, kept next to the code rather than in your head.

```
gh issue create --title "Finish the session 3 stretch tasks" --body "The noise experiment"
gh issue list
```

Close it when it is done, from the website or with `gh issue close 1`.

---

## Where this goes next

Every mini project and the capstone lives in a repository like the one you just
made. Nothing about that process changes; there is just more in it.

Two habits from today:

**Commit when something works**, not at the end of the day. A commit is a point
you can get back to, and a working state is the thing worth being able to get
back to.

**Never commit secrets.** API keys, passwords, tokens, patient data. Deleting
one in a later commit does not remove it from the history. It is still there,
and on a public repository it is already scraped. If it happens, tell someone
immediately and rotate the key.

## If it goes wrong

`git status` first, every time. It tells you where you are and usually what to
do next.

Everything except pushing is undoable. Bring the exact error text to Slack or to
the next session, pasted as text rather than as a screenshot so it can be searched.
