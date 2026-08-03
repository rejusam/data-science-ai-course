# Command line cheat sheet

The commands you actually need for this course. Mac Terminal on the left,
Windows Anaconda Prompt on the right. Where they are the same, only one is
shown.

## Moving around

| What you want | Mac / Linux | Windows |
|---|---|---|
| Where am I? | `pwd` | `cd` |
| List files | `ls` | `dir` |
| List files, with detail | `ls -l` | `dir` |
| List hidden files too | `ls -la` | `dir /a` |
| Go into a folder | `cd foldername` | `cd foldername` |
| Go up one level | `cd ..` | `cd ..` |
| Go to your home folder | `cd ~` | `cd %USERPROFILE%` |
| Clear the screen | `clear` | `cls` |

Folder names with spaces need quotes: `cd "My Documents"`.

## Files and folders

| What you want | Mac / Linux | Windows |
|---|---|---|
| Make a folder | `mkdir name` | `mkdir name` |
| Delete a file | `rm file.txt` | `del file.txt` |
| Delete a folder and contents | `rm -r folder` | `rmdir /s folder` |
| Copy a file | `cp a.txt b.txt` | `copy a.txt b.txt` |
| Move or rename | `mv a.txt b.txt` | `move a.txt b.txt` |
| Show a file's contents | `cat file.txt` | `type file.txt` |

`rm -r` and `rmdir /s` do not use a recycle bin. Deleted is deleted. Check
which folder you are in before running either.

## Shortcuts worth learning

| Key | What it does |
|---|---|
| `Tab` | Completes the file or folder name you started typing |
| Up arrow | Previous command. Press repeatedly to go further back |
| `Ctrl + C` | Stop whatever is running |
| `Ctrl + L` | Clear the screen |

Tab completion is the single biggest time saver here. Type the first few
letters of a folder name and press Tab rather than typing it all out. It also
stops typos, because it will only complete names that actually exist.

## Getting out of things

| Situation | What to press |
|---|---|
| A command is running and you want it to stop | `Ctrl + C` |
| Jupyter is running in the terminal | `Ctrl + C`, twice |
| You are stuck in a text editor you did not mean to open | `Ctrl + X` for nano, `:q!` then Enter for vim |
| The terminal is showing a `>` and will not run anything | You have an unclosed quote. Press `Ctrl + C` |

## Reading a file path

```
/Users/you/data-science-ai-course/modules/04-regression/data/houses.csv
```

Read it left to right as a series of nested folders, ending in a file.

- Mac and Linux separate folders with `/` and start absolute paths with `/`
- Windows uses `\` and starts with a drive letter, like `C:\Users\you\...`

In Python, always use forward slashes or `pathlib`, and both work everywhere:

```python
from pathlib import Path
path = Path("data") / "houses.csv"
```

Two shorthands appear constantly:

- `.` means the folder you are in now
- `..` means the folder above the one you are in
