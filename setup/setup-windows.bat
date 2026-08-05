@echo off
REM Sets up the course environment on Windows, for people using Anaconda
REM Prompt (the Command Prompt flavour rather than the PowerShell one).
REM
REM Open Anaconda Prompt from the Start menu, change to the repo folder,
REM and run:
REM
REM     setup\setup-windows.bat
REM
REM There are two Anaconda terminals in the Start menu. This one is for
REM Anaconda Prompt, whose prompt looks like:  (base) C:\Users\you>
REM If yours shows PS  --  (base) PS C:\Users\you>  --  you are in Anaconda
REM PowerShell Prompt, and setup-windows.ps1 is the better fit. Either script
REM works in either terminal.
REM
REM Safe to run more than once. If the environment already exists it is
REM updated rather than rebuilt.

setlocal

set ENV_NAME=dsai
set SCRIPT_DIR=%~dp0
set ENV_FILE=%SCRIPT_DIR%environment.yml

echo.
echo ==^> Checking prerequisites

where conda >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: conda was not found.
    echo.
    echo You are probably in the wrong terminal. This course uses Anaconda
    echo Prompt, not Command Prompt and not PowerShell.
    echo.
    echo   1. Click Start
    echo   2. Type: Anaconda Prompt
    echo   3. Open it, change to this folder, and run this script again
    echo.
    echo If Anaconda Prompt is not in your Start menu, Anaconda is not
    echo installed. Get it from https://www.anaconda.com/download
    echo.
    exit /b 1
)

REM `call` is required on every conda command. On Windows conda is conda.bat,
REM and invoking one batch file from another without `call` hands over control
REM and never returns, so the rest of this script would silently not run.
call conda --version

if not exist "%ENV_FILE%" (
    echo ERROR: cannot find %ENV_FILE%
    exit /b 1
)
echo environment file: %ENV_FILE%

echo.
echo ==^> Building the environment
echo This downloads about 1 GB and takes 5 to 15 minutes. Leave it running.

call conda env list | findstr /b /c:"%ENV_NAME% " >nul
if errorlevel 1 (
    call conda env create --file "%ENV_FILE%"
) else (
    echo Environment "%ENV_NAME%" already exists, updating it.
    call conda env update --name %ENV_NAME% --file "%ENV_FILE%" --prune
)
if errorlevel 1 (
    echo ERROR: conda could not build the environment.
    exit /b 1
)

echo.
echo ==^> Activating %ENV_NAME%
call conda activate %ENV_NAME%
if errorlevel 1 (
    echo ERROR: could not activate %ENV_NAME%.
    echo Run "conda init cmd.exe", close this window, open a new Anaconda
    echo Prompt, and try again.
    exit /b 1
)

REM If the environment exists but has no Python in it, `python` falls through
REM to the Microsoft Store stub and every later step fails confusingly.
call python -c "import sys; print(sys.executable)" >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python is not available inside "%ENV_NAME%".
    echo.
    echo The environment exists but looks empty, which usually means an
    echo earlier run of this script stopped part way through.
    echo.
    echo Remove it and build it again:
    echo     conda deactivate
    echo     conda env remove -n %ENV_NAME%
    echo     conda env create -f setup\environment.yml
    echo.
    exit /b 1
)

echo.
echo ==^> Registering the environment with Jupyter
call python -m ipykernel install --user --name %ENV_NAME% --display-name "Python (dsai)"

echo.
echo ==^> Downloading language data (used from module 8)
call python -m spacy download en_core_web_sm
if errorlevel 1 (
    echo spaCy model download failed. Not fatal. Re-run it later.
)
call python -c "import nltk; [nltk.download(d, quiet=True) for d in ('punkt','stopwords','wordnet','vader_lexicon')]; print('NLTK data installed.')"
if errorlevel 1 (
    echo NLTK download failed. Not fatal. You can re-run it later.
)

echo.
echo ==^> Checking the environment
call python "%SCRIPT_DIR%verify.py"

echo.
echo Done.
echo.
echo Every new Anaconda Prompt starts in the base environment, so before you
echo work on this course, run:
echo.
echo     conda activate %ENV_NAME%
echo.
echo To start Jupyter:
echo.
echo     jupyter lab
echo.

endlocal
