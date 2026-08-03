# Sets up the course environment on Windows.
#
# Open Anaconda PowerShell Prompt from the Start menu, change to the repo
# folder, and run:
#
#     powershell -ExecutionPolicy Bypass -File setup\setup-windows.ps1
#
# It creates a conda environment called dsai, installs everything the course
# needs, registers the environment with Jupyter, and checks the result.
#
# Safe to run more than once. If the environment already exists it is updated
# rather than rebuilt.

$ErrorActionPreference = "Stop"

$EnvName = "dsai"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$EnvFile = Join-Path $ScriptDir "environment.yml"

function Say($message) {
    Write-Host ""
    Write-Host "==> $message" -ForegroundColor Cyan
}

function Fail($message) {
    Write-Host ""
    Write-Host "ERROR: $message" -ForegroundColor Red
    exit 1
}

# ---------------------------------------------------------------- checks ----

Say "Checking prerequisites"

if (-not (Get-Command conda -ErrorAction SilentlyContinue)) {
    Write-Host @"
ERROR: conda was not found.

You are probably in the wrong terminal. This course uses Anaconda Prompt,
not Windows PowerShell and not Command Prompt.

  1. Click Start
  2. Type: Anaconda PowerShell Prompt
  3. Open it, change to this folder, and run this script again

If Anaconda Prompt is not in your Start menu, Anaconda is not installed.
Install it from https://www.anaconda.com/download
"@ -ForegroundColor Red
    exit 1
}

Write-Host "conda found: $((Get-Command conda).Source)"
conda --version

if (-not (Test-Path $EnvFile)) { Fail "cannot find $EnvFile" }
Write-Host "environment file: $EnvFile"

# ------------------------------------------------------------ environment ----

$existing = conda env list | ForEach-Object { ($_ -split '\s+')[0] }

if ($existing -contains $EnvName) {
    Say "Environment '$EnvName' already exists, updating it"
    conda env update --name $EnvName --file $EnvFile --prune
} else {
    Say "Creating environment '$EnvName'"
    Write-Host "This downloads about 1 GB and takes 5 to 15 minutes. Leave it running."
    conda env create --file $EnvFile
}
if ($LASTEXITCODE -ne 0) { Fail "conda could not build the environment" }

Say "Activating '$EnvName'"
conda activate $EnvName
if ($LASTEXITCODE -ne 0) {
    Fail "could not activate '$EnvName'. Run 'conda init powershell', close this window, open a new one, and try again."
}

# --------------------------------------------------------- jupyter kernel ----

Say "Registering the environment with Jupyter"
python -m ipykernel install --user --name $EnvName --display-name "Python (dsai)"
Write-Host "You can now pick 'Python (dsai)' as the kernel in Jupyter and VS Code."

# ------------------------------------------------------------ extra data ----
# Model and corpus downloads, not packages. Only needed from module 8. A
# failure here does not break the rest of the environment.

Say "Downloading language data (used from module 8)"

python -m spacy download en_core_web_sm
if ($LASTEXITCODE -eq 0) {
    Write-Host "spaCy English model installed."
} else {
    Write-Host "spaCy model download failed. Not fatal. Re-run later with:" -ForegroundColor Yellow
    Write-Host "    conda activate $EnvName; python -m spacy download en_core_web_sm"
}

python -c "import nltk; [nltk.download(d, quiet=True) for d in ('punkt','stopwords','wordnet','vader_lexicon')]; print('NLTK data installed.')"
if ($LASTEXITCODE -ne 0) {
    Write-Host "NLTK download failed. Not fatal. You can re-run it later." -ForegroundColor Yellow
}

# ---------------------------------------------------------------- verify ----

Say "Checking the environment"
python (Join-Path $ScriptDir "verify.py")

Write-Host @"

Done.

Every new Anaconda Prompt starts in the base environment, so before you work
on this course, run:

    conda activate $EnvName

To start Jupyter:

    jupyter lab

"@
