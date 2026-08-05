# Setup, from the command line

This is the fast path. You type a few commands, a script does the rest, and
you end up with a conda environment called `dsai` containing everything the
course needs.

If you have never used a terminal before, that is fine. Every command you need
is written out below. Copy one line at a time, press Enter, wait for it to
finish, then move to the next.

If you would rather click through installers, use the illustrated guide in
`../resources/installing-the-tools.md` instead, then come back here.

## Before you start

You need Anaconda and Git installed. Check by running the two commands below.

**Mac:** open Terminal. Press `Command + Space`, type `Terminal`, press Enter.

**Windows:** open **Anaconda Prompt** from the Start menu. Not Command Prompt.
Not PowerShell. Anaconda Prompt.

```
conda --version
git --version
```

Both should print a version number. If either says the command is not found,
install the missing tool first:

- Anaconda: https://www.anaconda.com/download
- Git: https://git-scm.com/downloads

After installing, close the terminal completely and open a new one. The
installers only affect terminals opened afterwards.

## Step 1: Get the repository

Pick a folder you can find again. Your home folder is fine.

**Mac:**

```
cd ~
git clone https://github.com/rejusam/data-science-ai-course.git
cd data-science-ai-course
```

**Windows:**

```
cd %USERPROFILE%
git clone https://github.com/rejusam/data-science-ai-course.git
cd data-science-ai-course
```

`git clone` copies the repository onto your machine. You only do this once.
Later, to pick up new material, you run `git pull` from inside the folder.

## Step 2: Run the setup script

This creates the environment, installs the packages, connects it to Jupyter,
and checks the result.

**Mac:**

```
bash setup/setup-mac.sh
```

**Windows.** There are two Anaconda terminals in your Start menu with almost
the same name, and they need different scripts. Check your prompt first:

| Your prompt looks like | You are in | Run this |
|---|---|---|
| `(base) PS C:\Users\you>` | Anaconda **PowerShell** Prompt | `powershell -ExecutionPolicy Bypass -File setup\setup-windows.ps1` |
| `(base) C:\Users\you>` | Anaconda Prompt (cmd) | `setup\setup-windows.bat` |

**The `PS` is the tell.** If it is there, you are in PowerShell.

Both scripts do exactly the same thing, and either will run in either terminal.
Matching them up just means you get the clearer error messages if something
goes wrong.

It downloads about 1 GB and takes somewhere between 5 and 15 minutes. The
progress display sits still for long stretches. That is normal. Leave it alone
and let it finish.

The script is safe to run again. If the environment already exists it updates
it instead of starting over.

## Step 3: Activate the environment

Installing the environment does not switch you into it. Every new terminal
starts in the `base` environment, so you activate `dsai` each time you sit
down to work:

```
conda activate dsai
```

Your prompt changes to show `(dsai)` at the start of the line. That is how you
know which environment you are in. If you do not see it, you are not in the
course environment, and imports will fail in ways that look mysterious.

To leave it:

```
conda deactivate
```

## Step 4: Check it worked

```
python setup/verify.py
```

It checks three things: the command-line tools (`conda`, `git`, `jupyter`), the
environment you are currently in, and every package the course needs.

`gh` is part of this environment, so it is available whenever `(dsai)` is
active. Git is not, because you need Git before this environment exists in
order to clone the repository at all.

Every line should say `OK`. If anything says `MISSING`, the output tells you
what to run next.

Post that output in Slack when you are done. It tells us you are ready without
you having to explain anything.

## Step 5: Start working

```
jupyter lab
```

This opens Jupyter in your browser. When you create or open a notebook, choose
the kernel named **Python (dsai)**. If you pick a different kernel, the
packages will not be there.

Stop Jupyter with `Ctrl + C` in the terminal, twice.

## What the script actually did

Nothing here is magic, and you will be expected to do it yourself by the end of
the course.

1. Read `setup/environment.yml`, which lists every package the course needs.
2. Ran `conda env create`, which resolved compatible versions of all of them
   and downloaded them into a self-contained environment named `dsai`.
3. Registered that environment with Jupyter, so it shows up as a kernel.
4. Downloaded the spaCy English model and several NLTK corpora, which are data
   rather than code and so are not installed by conda.
5. Ran `verify.py` to import every package and report anything missing.

The reason for a separate environment, rather than installing into `base`, is
that different projects need different versions of the same library. Keeping
each project in its own environment means upgrading one thing does not
silently break another. Employers expect you to work this way.

## Commands worth remembering

| Command | What it does |
|---|---|
| `conda activate dsai` | Switch into the course environment |
| `conda deactivate` | Leave it |
| `conda env list` | Show every environment you have |
| `conda list` | Show packages in the current environment |
| `jupyter lab` | Start Jupyter |
| `git pull` | Fetch new course material |
| `python setup/verify.py` | Re-check your setup |

## When something goes wrong

**`conda: command not found` on Mac.** Quit Terminal completely with
`Command + Q`, not the red button, then open it again. If it still fails,
run `source ~/.zshrc` and try once more.

**`'conda' is not recognized` on Windows.** You are in Command Prompt or
PowerShell. Open **Anaconda Prompt** from the Start menu instead.

**`conda activate` fails on Windows** with a message about your shell not
being initialised. Run `conda init powershell` (or `conda init cmd.exe`),
close the window, open a new Anaconda Prompt, and try again.

**PowerShell refuses to run the script.** That is the execution policy. Use
the exact command given in step 2, which includes `-ExecutionPolicy Bypass`.

**Windows says "Python was not found; run without arguments to install from
the Microsoft Store".** Windows ships a placeholder `python` that opens the
Store, and you are seeing it because the real Python was not found first.

Check whether the environment actually contains Python:

```
conda activate dsai
conda list python
```

If that lists nothing, the environment exists but is empty — usually because a
setup run stopped part way. Rebuild it:

```
conda deactivate
conda env remove -n dsai
conda env create -f setup/environment.yml
```

If Python *is* listed and you still get the Store message, turn off the
placeholder: **Settings → Apps → Advanced app settings → App execution
aliases**, and switch off both `python.exe` and `python3.exe`. Then open a new
terminal.

**The setup script prints the conda version and then stops.** Fixed in August
2026. Run `git pull` to get the corrected script and try again.

**The solve takes forever or fails.** conda is working out a set of package
versions that are all compatible with each other. On a slow connection this is
genuinely slow. If it fails outright, copy the error into Slack rather than
guessing.

**Imports fail inside Jupyter but work in the terminal.** You are on the wrong
kernel. In the notebook, choose **Python (dsai)** from the kernel menu.

**You want to start completely fresh.**

```
conda deactivate
conda env remove -n dsai
conda env create -f setup/environment.yml
```

## Still stuck

Post in Slack with the command you ran and the full error text, and say which
operating system you are on. Paste the text rather than a photo of the screen
where you can, because we can search text.

You can also bring it to the 30 minute support session before class.
