#!/usr/bin/env bash
#
# Sets up the course environment on macOS or Linux.
#
#   bash setup/setup-mac.sh
#
# It creates a conda environment called dsai, installs everything the course
# needs, registers the environment with Jupyter, and checks the result.
#
# Safe to run more than once. If the environment already exists it is updated
# rather than rebuilt.

set -euo pipefail

ENV_NAME="dsai"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/environment.yml"

say() {
    printf '\n==> %s\n' "$1"
}

fail() {
    printf '\nERROR: %s\n' "$1" >&2
    exit 1
}

# ---------------------------------------------------------------- checks ----

say "Checking prerequisites"

if ! command -v conda >/dev/null 2>&1; then
    cat >&2 <<'MESSAGE'
ERROR: conda was not found.

Anaconda is not installed, or your terminal cannot see it yet.

  1. Install Anaconda from https://www.anaconda.com/download
  2. Close this terminal window completely and open a new one
  3. Run this script again

If you have just installed Anaconda and this still fails, run:
    source ~/.zshrc
and try once more.
MESSAGE
    exit 1
fi

echo "conda found: $(command -v conda)"
conda --version

[ -f "$ENV_FILE" ] || fail "cannot find $ENV_FILE"
echo "environment file: $ENV_FILE"

# Load conda's shell functions so 'conda activate' works inside this script.
CONDA_BASE="$(conda info --base)"
# shellcheck disable=SC1091
source "$CONDA_BASE/etc/profile.d/conda.sh"

# ------------------------------------------------------------ environment ----

if conda env list | awk '{print $1}' | grep -qx "$ENV_NAME"; then
    say "Environment '$ENV_NAME' already exists, updating it"
    conda env update --name "$ENV_NAME" --file "$ENV_FILE" --prune
else
    say "Creating environment '$ENV_NAME'"
    echo "This downloads about 1 GB and takes 5 to 15 minutes. Leave it running."
    conda env create --file "$ENV_FILE"
fi

say "Activating '$ENV_NAME'"
conda activate "$ENV_NAME"
echo "python: $(command -v python)"

# --------------------------------------------------------- jupyter kernel ----

say "Registering the environment with Jupyter"
python -m ipykernel install --user \
    --name "$ENV_NAME" \
    --display-name "Python (dsai)"
echo "You can now pick 'Python (dsai)' as the kernel in Jupyter and VS Code."

# ------------------------------------------------------------ extra data ----
# These are model and corpus downloads, not packages. They are separate
# because they are large and only needed from module 8 onwards. A failure
# here does not break the rest of the environment.

say "Downloading language data (used from module 8)"

if python -m spacy download en_core_web_sm; then
    echo "spaCy English model installed."
else
    echo "spaCy model download failed. Not fatal. Re-run this later:"
    echo "    conda activate $ENV_NAME && python -m spacy download en_core_web_sm"
fi

if python - <<'PYTHON'
import nltk
for dataset in ("punkt", "stopwords", "wordnet", "vader_lexicon"):
    nltk.download(dataset, quiet=True)
print("NLTK data installed.")
PYTHON
then
    :
else
    echo "NLTK download failed. Not fatal. You can re-run it later."
fi

# ---------------------------------------------------------------- verify ----

say "Checking the environment"
python "$SCRIPT_DIR/verify.py"

cat <<MESSAGE

Done.

Every new terminal starts in the base environment, so before you work on this
course, run:

    conda activate $ENV_NAME

To start Jupyter:

    jupyter lab

MESSAGE
