# Notebook hygiene

One page. Read it once properly and it will save you hours.

## Before you type: work on a copy

Session notebooks come from the course repository, and the course repository
keeps being updated. Copy a notebook into the `my-work/` folder next to it and
work on the copy.

That folder is ignored by git, so your work is never committed and `git pull`
never has to argue with it. In Colab, use **File → Save a copy in Drive**.

Edit the original and the next `git pull` stops with *"Your local changes to the
following files would be overwritten by merge"*. Recoverable, but a nuisance in
the middle of a class.

## The one rule

**Your code works when it runs top to bottom from a fresh start.** Nothing less
counts.

- Jupyter: **Kernel → Restart Kernel and Run All Cells**
- Colab: **Runtime → Restart and run all**
- VS Code: **Restart** in the toolbar, then **Run All**

Do this before you submit anything, before you ask for help, and at the end of
every working session.

## Why, in thirty seconds

A notebook remembers everything you have run, in the order you ran it. Not the
order the cells appear on screen.

That means you can:

- delete a cell and keep using the variable it created
- run cell 10 before cell 4 and get a result nobody else can reproduce
- fix a bug, forget to re-run the cell below it, and see the old answer

The notebook looks fine in all three cases. It is not fine. The person who
finds out is you, usually at the worst moment.

Restart & Run All is how you find out early instead.

## The number in the brackets

`In [7]` means that cell was the seventh thing you ran. Read the numbers down
the page: if they are not in order, your notebook has been run out of order.

`In [ ]` means the cell has not been run at all in this session. `In [*]` means
it is running now, or has hung.

## Which kernel am I on?

Top right of the notebook. It should say **Python (dsai)** for this course.

If imports fail for packages you know you installed, check this before you
check anything else. It is the cause about half the time.

## Habits worth having

**One idea per cell.** Cells are cheap. A cell that does eight things is a cell
you cannot debug.

**Import at the top.** All of them, in the first code cell. Not scattered.

**Restart when things get strange.** If behaviour stops making sense, restart
the kernel before you start doubting yourself. Stale state is far more common
than a mysterious bug.

**Clear outputs before committing to git.** Outputs make diffs unreadable and
can bloat a repository badly. In Jupyter: **Kernel → Restart Kernel and Clear
All Outputs**.

**Never edit a generated notebook.** Some notebooks in this repository are
built by a script in `tools/`. They say so at the top. Edit the script.

## When something is wrong

1. Read the error. The **last line** says what went wrong; the lines above say
   where. Read from the bottom up.
2. Restart & Run All. If the error disappears, it was stale state and you have
   learned something.
3. If it persists, that is a real bug and now you can debug it honestly.
4. Ask, with the full error text pasted as text rather than a screenshot, and
   say what you were trying to do.

## Notebooks are not always the right tool

Notebooks are for exploring: trying things, looking at data, showing your
working.

Once code is something you or someone else will run repeatedly, it belongs in a
`.py` file where it can be imported and tested. We do that in week 2, and the
distinction matters more the further into the course you get.
