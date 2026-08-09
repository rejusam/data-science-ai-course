# Your work goes here

Copy a session notebook into this folder before you type anything into it, and
work on the copy.

```
cp 02-numpy.ipynb my-work/02-numpy.ipynb
```

In Jupyter or VS Code you can also right-click the notebook in the file browser
and choose **Duplicate**, then drag it in here.

In Colab there is no repository at all: use **File → Save a copy in Drive** and
work on that.

## Why

Everything in this folder except this README is ignored by git. Nothing you put
here is ever committed, and nothing here can be overwritten by a course update.

If you edit the original notebook instead, the next `git pull` stops with:

```
error: Your local changes to the following files would be overwritten by merge
```

Git is protecting your work, but you then have to sort it out before you can
get the new material. Copying first avoids the whole situation.

## If it already happened

Save your edits under a new name first, then take the update:

```
git stash              # put your changes aside
git pull               # get the new material
git stash pop          # put your changes back, or drop them
```

Bring it to a support session if that produces a conflict. It is a five-minute
fix and it is worth seeing once.
