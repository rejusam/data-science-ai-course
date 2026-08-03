# Conda cheat sheet

Conda does two jobs: it installs packages, and it keeps sets of packages
separate from each other. The second job is the one people underestimate.

## Why environments exist

One project needs pandas 1.5, another needs pandas 2.3. Install both into the
same place and one of them breaks. An environment is a self-contained folder
with its own Python and its own packages, so projects cannot interfere with
each other.

This course uses an environment named `dsai`. Your `base` environment should
stay more or less empty.

## Daily use

```
conda activate dsai       # switch into the course environment
conda deactivate          # leave it
```

Your prompt shows the active environment in brackets:

```
(dsai) you@laptop course %
```

If you do not see `(dsai)`, you are not in it, and course packages will look
like they are missing. This is the most common cause of "it worked yesterday".

## Environments

| Command | What it does |
|---|---|
| `conda env list` | List every environment you have |
| `conda create -n name python=3.11` | New empty environment |
| `conda env create -f environment.yml` | Build one from a file |
| `conda env update -f environment.yml --prune` | Update to match the file |
| `conda env remove -n name` | Delete an environment |
| `conda env export > environment.yml` | Write out what you currently have |

`--prune` matters on update: it removes packages that are no longer listed in
the file, rather than leaving them behind.

## Packages

| Command | What it does |
|---|---|
| `conda list` | Everything in the active environment |
| `conda list pandas` | Check one package and its version |
| `conda install -c conda-forge package` | Install from conda-forge |
| `conda remove package` | Uninstall |
| `conda search package` | Which versions exist |

## conda-forge

`-c conda-forge` selects a channel, which is where conda looks for packages.
conda-forge is community maintained, has far more packages than the default
channel, and updates faster. This course uses it throughout.

Mixing channels in one environment causes conflicts that are painful to
diagnose. `environment.yml` pins the channel to conda-forge for exactly that
reason. Stick to it.

## conda and pip together

Some packages are only on PyPI. The rule is: install everything you can with
conda first, then use pip for the rest, and never install the same package
with both.

```
conda activate dsai
pip install some-package
```

`pip` inside an activated environment installs into that environment, not
system-wide. Check with `which pip` on Mac or `where pip` on Windows if you
are unsure.

## Fixing a broken environment

Try updating it to match the file:

```
conda env update -f setup/environment.yml --prune
```

If that does not work, delete and rebuild. This is cheap and reliable, and
nothing of yours lives in the environment:

```
conda deactivate
conda env remove -n dsai
conda env create -f setup/environment.yml
```

## Jupyter kernels

An environment is not automatically visible to Jupyter. Registering it makes
it appear in the kernel list:

```
conda activate dsai
python -m ipykernel install --user --name dsai --display-name "Python (dsai)"
```

The setup script does this for you. If notebooks cannot see your packages,
check which kernel the notebook is using before you check anything else.

## Solving is slow

When you ask conda to install something, it works out a combination of
versions where every package is compatible with every other. That is genuinely
hard, and on a big environment it takes minutes. It is not stuck. Let it run.
