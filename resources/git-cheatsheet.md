# Git and GitHub cheat sheet

Git records the history of your work. GitHub stores a copy online and is where
employers will look at what you have built.

## One-time setup

Tell git who you are. This is stamped on every commit you make.

```
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Use the same email address as your GitHub account, otherwise your commits will
not be linked to your profile.

## Getting this course repository

```
git clone https://github.com/rejusam/data-science-ai-course.git
cd data-science-ai-course
```

Then, before each session:

```
git pull
```

That fetches new material. Do it often.

## Starting your own project

```
mkdir my-project
cd my-project
git init
```

Then create a matching repository on GitHub and connect them:

```
git remote add origin https://github.com/YOUR-USERNAME/my-project.git
git branch -M main
git push -u origin main
```

## The everyday loop

Four commands, in this order, every time you finish a piece of work.

```
git status                    # what has changed
git add .                     # stage everything changed
git commit -m "Add EDA notebook for bikeshare data"
git push                      # send it to GitHub
```

| Command | What it does |
|---|---|
| `git status` | What is changed, staged, or untracked |
| `git add file` | Stage one file |
| `git add .` | Stage everything in this folder and below |
| `git commit -m "message"` | Record the staged changes |
| `git push` | Upload commits to GitHub |
| `git pull` | Download commits from GitHub |
| `git log --oneline` | History, one line per commit |
| `git diff` | What changed, line by line |

## Writing commit messages

Describe what changed and why, in a way that makes sense to you in three
months. "Update" and "fix" tell you nothing.

Reasonable:

```
Add K-Means clustering notebook for module 6
Fix train/test split leaking target into features
Drop rows with missing sale price, document why in README
```

Not reasonable:

```
stuff
asdf
final FINAL v2
```

## Undoing things

| Situation | Command |
|---|---|
| Unstage a file you added | `git restore --staged file` |
| Throw away changes to a file | `git restore file` |
| Change the last commit message | `git commit --amend -m "New message"` |
| See what a file looked like before | `git log -p file` |

`git restore file` discards your edits permanently. Be sure.

If you are lost, stop. Do not run commands you found online that contain
`--force` or `reset --hard`. Ask in Slack, and say what you were trying to do.
Git very rarely loses committed work, but force-pushing can.

## What not to commit

- Datasets over about 50 MB. GitHub rejects files over 100 MB.
- API keys, passwords, credentials of any kind.
- `.env` files.
- Anything containing personal data about real people.

A `.gitignore` file lists things git should skip. This repository has one.

If you commit a secret by accident, treat it as leaked: rotate the key
immediately. Deleting the file in a later commit does not remove it from the
history, and the history is public.

## Making your repositories worth looking at

By week 24 you will be sending these links to employers. What separates a
repository that helps from one that does not:

- A README that says what the project does, what data it uses, and what you
  found. Written for someone who has never seen it.
- Commits spread over time, telling the story of how it was built.
- Notebooks that run top to bottom without errors on a fresh clone.
- No commented-out dead code, no `Untitled12.ipynb`.

Recruiters spend well under a minute per repository. The README is what they
read.
