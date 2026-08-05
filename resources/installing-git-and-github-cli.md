# Installing and configuring Git and the GitHub CLI

Windows and Mac. Follow your own operating system, then do the configuration
section, which is the same for everyone.

If you have not installed Anaconda and VS Code yet, do
[`installing-the-tools.md`](installing-the-tools.md) first. This guide assumes
you have a working terminal.

**Which terminal.** On Windows, use **Anaconda Prompt** from the Start menu,
not Command Prompt and not PowerShell. On Mac, use **Terminal**.

**What you get at the end:** `git` for tracking your work, `gh` for talking to
GitHub without pasting passwords, and an authenticated link between your laptop
and your GitHub account.

**Install Git system-wide, not into a conda environment.** You need Git before
the course environment exists, because Git is how you get the repository that
`environment.yml` lives in. `gh` is different — it is listed in
`environment.yml`, so it arrives with the environment, and you only need to
install it by hand if you want it available outside `dsai` as well.

---

## Windows

### 1. Install Git

Pick one.

**Method A — the system installer (recommended).** Open a normal PowerShell or
Command Prompt window and run:

```powershell
winget install --id Git.Git -e --source winget
```

Then **close the terminal completely and open a new one**. Installers only
affect terminals opened afterwards.

**Method B — inside conda.** If `winget` is unavailable or blocked, install
into your conda environment instead:

```powershell
conda install -c conda-forge git
```

Use `conda-forge`, not the `anaconda` channel. This course pins everything to
conda-forge, and mixing channels in one environment causes dependency conflicts
that are unpleasant to unpick.

Check it worked:

```powershell
git --version
```

### 2. Install the GitHub CLI

**Read this before choosing.** Anything installed with `conda install` goes
into **whichever environment is currently active**, and nowhere else. Install
`gh` while you are in `base` and it will disappear the moment you
`conda activate dsai`, with the message:

```
gh : The term 'gh' is not recognized as the name of a cmdlet, function,
script file, or operable program.
```

That is not a broken install. It is the right tool in the wrong environment.

**Method A — system-wide (recommended).** Works in every environment and every
terminal:

```powershell
winget install --id GitHub.cli -e --source winget
```

Then close the terminal and open a new one.

**Method B — into the course environment.** Make sure your prompt shows
`(dsai)` first:

```powershell
conda activate dsai
conda install -c conda-forge gh
```

This works, and it is what to use if `winget` is blocked. Just be aware that
`gh` will then only exist inside `dsai`.

Check it worked:

```powershell
gh --version
```

---

## Mac

### 1. Install Git

Pick one.

**Method A — Apple's own tools (simplest).** Just run:

```bash
git --version
```

If a window appears offering to install the "command line developer tools",
click **Install** and wait. That gives you Git. If you get a version number
instead, Git is already there and you are done.

**Method B — Homebrew.** If you already use Homebrew:

```bash
brew install git
```

**Method C — inside conda.**

```bash
conda install -c conda-forge git
```

### 2. Install the GitHub CLI

```bash
brew install gh
```

or

```bash
conda install -c conda-forge gh
```

Check it worked:

```bash
gh --version
```

---

## If conda fails with an SSL or certificate error

On university, corporate, or some home ISP networks you may see
`CondaSSLError`, `CERTIFICATE_VERIFY_FAILED`, or `SSL certificate verify
failed`.

This happens because the network inspects encrypted traffic using its own
certificate authority, which conda does not know about but your operating
system usually does.

**Try these in order.**

### Fix 1 — use the operating system's certificate store

This is the correct fix and it solves the problem in most cases, because your
IT department has already installed their certificate where the OS can see it.

```bash
conda config --set ssl_verify truststore
```

Then retry the install. Nothing is weakened: conda now trusts exactly what your
computer already trusts.

### Fix 2 — install without conda

Use `winget` on Windows or Homebrew on Mac, as in the sections above. Those use
the operating system's networking and certificate store, so they are usually
unaffected.

### Fix 3 — a different network

A phone hotspot will often work when campus Wi-Fi will not. This costs you
nothing and diagnoses the problem at the same time.

### Last resort, and read this before using it

You may see advice online to run `conda config --set ssl_verify false`. That
switches off certificate checking **completely and permanently**, for every
future conda command, until you switch it back.

It is worth being clear about what that means. Certificate checking is what
proves you are talking to the real server and not something in between. Turning
it off on an untrusted network removes the protection precisely where you most
need it, and the setting is easy to forget about afterwards.

If you have tried the three fixes above and are still stuck, **ask in Slack
before disabling it.** It is usually a five-minute fix with someone looking at
the actual error.

If you have already run it, put it back now and confirm:

```bash
conda config --set ssl_verify true
conda config --show ssl_verify
```

That must print `ssl_verify: True`.

---

## Configuration and authentication

Same on every operating system.

### Step 1: Tell Git who you are

Every commit is stamped with this. Use the email address attached to your
GitHub account, or your commits will not be linked to your profile and your
contribution history will look empty.

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global init.defaultBranch main
```

`init.defaultBranch main` sets the starting branch name for new repositories.
GitHub uses `main`; older Git versions default to `master`, and the mismatch
causes confusion later.

Check it:

```bash
git config --list --global
```

### Step 2: Log in to GitHub

**Check first.** Your login is stored in the operating system's keyring, not
inside a conda environment, so it is shared. If you have authenticated on this
machine before — even from a different environment — you are still logged in:

```bash
gh auth status
```

If that shows a tick and your username, skip to Step 3. Running `gh auth login`
again is harmless but pointless; it will simply tell you
`You were already logged in to this account`.

Otherwise:

```bash
gh auth login
```

Answer with the arrow keys and `Enter`:

| Question | Choose |
|---|---|
| Where do you use GitHub? | **GitHub.com** |
| What is your preferred protocol for Git operations on this host? | **HTTPS** |
| Authenticate Git with your GitHub credentials? | **Yes** |
| How would you like to authenticate GitHub CLI? | **Login with a web browser** |

It then shows a one-time code that looks like `F627-66E9`. Copy it, press
`Enter` to open your browser, paste the code, and click **Authorize**.

You should end with:

```
✓ Authentication complete.
✓ Configured git protocol
✓ Logged in as your-username
```

*Wording is from `gh` 2.97.0 and shifts occasionally between versions. If a
prompt does not match exactly, answer the one that means the same thing.*

Saying **Yes** to "Authenticate Git with your GitHub credentials" is what stops
Git asking for a password every time you push. If you missed it, run it
separately:

```bash
gh auth setup-git
```

### Step 3: Confirm

```bash
gh auth status
```

You should see something like:

```
github.com
  ✓ Logged in to github.com account your-username (keyring)
  - Active account: true
  - Git operations protocol: https
```

The tick and your own username are what matter.

### Step 4: Prove it end to end

Configuration that has never been used is not configuration you can trust.

```bash
gh repo clone rejusam/data-science-ai-course
cd data-science-ai-course
git log --oneline -3
```

If you see three commit messages, everything works: Git is installed,
authenticated, and talking to GitHub.

---

## Troubleshooting

**`git: command not found` or `'git' is not recognized`.** Close the terminal
completely and open a new one. If you installed with conda, check you are in
the right environment — `conda activate dsai`.

**`gh: command not found`, or on Windows `The term 'gh' is not recognized as
the name of a cmdlet`.** Two possible causes, in order of likelihood.

*You are in a different environment from the one you installed it into.* Look
at the start of your prompt. If it says `(dsai)` and you installed `gh` while
in `base`, `gh` is not there. Either install it again inside `dsai`, or install
it system-wide with `winget` so the environment stops mattering:

```powershell
conda activate dsai
conda install -c conda-forge gh
```

*The terminal predates the install.* Close it completely and open a new one.

The same applies to `git` if you installed it with conda rather than the system
installer. This is the most common confusion in the first fortnight, and it is
worth understanding rather than working around: conda environments are isolated
on purpose, and that isolation includes command-line tools, not just Python
packages.

**Browser does not open during `gh auth login`.** Copy the URL from the
terminal into a browser manually. The one-time code stays valid.

**"Authentication failed" when pushing.** Run `gh auth setup-git`, then try
again. If you are being asked for a username and password, Git is not using the
GitHub CLI as its credential helper. GitHub stopped accepting account passwords
for Git operations in 2021, so a password prompt will never succeed.

**Your commits show the wrong name, or are not linked to your profile.** The
email in `git config user.email` does not match an email on your GitHub
account. Fix the config, or add that address to your GitHub account settings.
Existing commits keep the old details.

**Still stuck.** Post in Slack with the command you ran and the full error as
text, and say which operating system you are on. Paste the text rather than a
screenshot where you can, because text is searchable and someone else in the
cohort has probably hit the same thing.

---

## What next

Day-to-day commands are in [`git-cheatsheet.md`](git-cheatsheet.md): the
everyday add-commit-push loop, writing commit messages worth reading, and what
never to commit.
