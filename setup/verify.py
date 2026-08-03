"""Check that the course environment is working.

Run it after creating the environment:

    conda activate dsai
    python setup/verify.py

Every line should say OK. Anything that says MISSING needs fixing before
class. Copy the whole output into Slack if you need help.
"""
import importlib
import platform
import sys
import warnings

# Some libraries emit deprecation warnings simply for being imported, or for
# being asked their version. Those are not your problem and printing them here
# only makes a working setup look broken.
warnings.filterwarnings("ignore")

# (import name, what we use it for)
PACKAGES = [
    ("numpy", "arrays and numerical work"),
    ("pandas", "tables and data wrangling"),
    ("scipy", "scientific computing"),
    ("matplotlib", "plotting"),
    ("seaborn", "statistical plots"),
    ("plotly", "interactive plots"),
    ("statsmodels", "statistical models and tests"),
    ("sklearn", "machine learning"),
    ("imblearn", "class imbalance"),
    ("xgboost", "gradient boosting"),
    ("graphviz", "drawing decision trees"),
    ("jupyterlab", "notebook interface"),
    ("ipykernel", "notebook kernel"),
    ("sqlalchemy", "talking to databases"),
    ("requests", "calling web APIs"),
    ("bs4", "web scraping"),
    ("nltk", "natural language toolkit"),
    ("spacy", "natural language processing"),
    ("flask", "serving a model"),
    ("fastapi", "serving a model"),
    ("dotenv", "keeping secrets out of code"),
    ("kmodes", "clustering categorical data"),
    ("openpyxl", "reading Excel files"),
    ("pytest", "running tests"),
]

MIN_PYTHON = (3, 9)


def version_of(module):
    for attribute in ("__version__", "VERSION", "version"):
        value = getattr(module, attribute, None)
        if isinstance(value, str):
            return value
    return "installed"


def check_python():
    print("Python")
    print("  version    : {}".format(platform.python_version()))
    print("  executable : {}".format(sys.executable))
    print("  platform   : {} ({})".format(platform.system(), platform.machine()))
    if sys.version_info < MIN_PYTHON:
        print("  WARNING: this course expects Python {}.{} or newer".format(*MIN_PYTHON))
        return False
    return True


def check_environment():
    """Warn if the base environment is active instead of the course one."""
    prefix = sys.prefix
    name = prefix.rstrip("/\\").split("/")[-1].split("\\")[-1]
    print("  conda env  : {}".format(name))
    if name != "dsai":
        print()
        print("  WARNING: you do not appear to be in the 'dsai' environment.")
        print("  Run 'conda activate dsai' and try again.")
        return False
    return True


def check_packages():
    print()
    print("Packages")
    missing = []
    for import_name, purpose in PACKAGES:
        try:
            module = importlib.import_module(import_name)
        except ImportError:
            print("  MISSING  {:<14} {}".format(import_name, purpose))
            missing.append(import_name)
        else:
            print("  OK       {:<14} {:<12} {}".format(
                import_name, version_of(module), purpose))
    return missing


def main():
    print("=" * 68)
    print("COURSE ENVIRONMENT CHECK")
    print("=" * 68)
    python_ok = check_python()
    env_ok = check_environment()
    missing = check_packages()

    print()
    print("=" * 68)
    if not missing and python_ok and env_ok:
        print("Everything is working. You are ready for class.")
        return 0

    if missing:
        print("{} package(s) missing: {}".format(len(missing), ", ".join(missing)))
        print()
        print("Try this first:")
        print("    conda env update -f setup/environment.yml --prune")
        print()
        print("If that does not fix it, delete the environment and start again:")
        print("    conda deactivate")
        print("    conda env remove -n dsai")
        print("    conda env create -f setup/environment.yml")
    print()
    print("Still stuck? Copy everything above into Slack.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
