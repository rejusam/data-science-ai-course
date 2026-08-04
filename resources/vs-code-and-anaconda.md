# Connecting VS Code to Anaconda

VS Code does not find your conda environment on its own. This is the step that
makes "I installed the package but the import fails" go away, and it is worth
ten minutes now.

Do this after you have built the course environment with
[`../setup/README.md`](../setup/README.md). You need the `dsai` environment to
exist before you can select it.

---

## Phase 1: Install the two extensions

Both are published by **Microsoft**. There are many extensions with similar
names by other publishers — check the publisher before you install.

1. Open VS Code and click **Extensions** in the left activity bar. The icon is
   four squares with one detached.
2. Search for **Python**. Install the one by Microsoft.
3. Clear the search, search for **Jupyter**. Install the one by Microsoft.

The Python extension gives you interpreter selection, linting and debugging.
The Jupyter extension lets you open and run `.ipynb` notebooks inside VS Code.
This course uses both.

---

## Phase 2: Select the course interpreter

An **interpreter** is the specific Python installation VS Code will use.

1. Open the Command Palette: **Ctrl+Shift+P** on Windows, **Cmd+Shift+P** on
   Mac.
2. Type `Python: Select Interpreter` and press **Enter**.
3. Choose the entry for **`dsai`**. It looks something like
   `Python 3.11.x ('dsai': conda)`.

**Choose `dsai`, not `base`.** `base` is Anaconda's default environment and it
does not have the course packages in it. Selecting `base` is the single most
common reason imports fail for people who have done everything else correctly.

If `dsai` is not in the list, see troubleshooting below.

This setting is per workspace. Opening a different folder means selecting the
interpreter again for that folder.

---

## Phase 3: Windows PowerShell activation

*Windows only. Mac users skip to Phase 4.*

VS Code opens PowerShell by default, and Windows blocks scripts from running in
it until you allow them. The symptom is a terminal that never shows `(dsai)` or
`(base)` at the start of the line.

**1. Let conda work with PowerShell.** Open **Anaconda Prompt** from the Start
menu, outside VS Code, and run:

```powershell
conda init powershell
```

Close that window.

**2. Allow local scripts to run.** Open **Windows PowerShell** and run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Type **Y** and press **Enter**.

You do **not** need administrator rights for this. `-Scope CurrentUser` changes
the setting for your account only, which matters if you are on a shared or
family computer where you are not an administrator.

What it does: `RemoteSigned` allows scripts written on your own machine to run,
while still requiring anything downloaded from the internet to be signed by a
trusted publisher. It is more conservative than the `Unrestricted` you will see
suggested in some forum answers, and it is enough for conda to work.

**3. Restart VS Code completely.** Not just the terminal panel — close the
whole application and reopen it.

---

## Phase 4: Choose the kernel for notebooks

Selecting an interpreter and selecting a notebook kernel are two different
settings, and this catches nearly everyone.

- The **interpreter** is what runs `.py` files and the terminal.
- The **kernel** is what runs the cells in a `.ipynb` notebook.

Open any notebook from this repository. Top right, you will see a kernel
selector. Click it and choose **Python (dsai)**.

If imports work in the terminal but fail inside a notebook, this is almost
always why. Check the kernel before you check anything else.

---

## Phase 5: Verify

Three checks. Do all three.

**1. The terminal shows the environment.**

**Terminal → New Terminal**. The prompt should begin with `(dsai)`:

```
(dsai) C:\Users\you\data-science-ai-course>
```

**2. Python is the one you chose.** In that terminal:

```
python -c "import sys; print(sys.executable)"
```

The path must contain `envs/dsai` (or `envs\dsai` on Windows). If it points at
`anaconda3/bin/python` with no `envs`, you are in `base`.

**3. The course packages import.**

```
python setup/verify.py
```

Every line should say `OK`.

---

## Troubleshooting

**`dsai` is not in the interpreter list.**

The environment may not exist yet. Check:

```
conda env list
```

If `dsai` is missing, go back to [`../setup/README.md`](../setup/README.md) and
create it. If it is listed but VS Code cannot see it, run **Developer: Reload
Window** from the Command Palette, or enter the path by hand using **Enter
interpreter path** at the top of the interpreter list.

**The terminal opens in `base` every time.** VS Code remembers the interpreter
per workspace. Open the folder you are working in as a folder — **File → Open
Folder** — rather than opening loose files.

**`conda: command not found` inside the VS Code terminal on Mac.** VS Code
launched from the Dock does not always inherit your shell configuration. Quit
VS Code fully and reopen it, or open it by running `code .` from Terminal.

**Notebook says "Kernel not found" or "Select Kernel".** Register the
environment with Jupyter:

```
conda activate dsai
python -m ipykernel install --user --name dsai --display-name "Python (dsai)"
```

The setup script does this for you, so if you are here you probably skipped it.

**Everything looks right and imports still fail.** Restart VS Code completely.
Environment changes frequently need a full restart, not just a new terminal.

---

## A note for later in the course

You will create more conda environments as you go — a separate one per project
is good practice and it is what employers expect.

Every time you do, repeat **Phase 2** to point that workspace at the right
interpreter, and **Phase 4** if the project uses notebooks. Environments are
per project, and so is this setting.
