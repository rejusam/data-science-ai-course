# Run an AI model on your laptop with Ollama

**What this gives you:** a free AI language model that runs on your own
computer. No API key, no payment, and nothing you type leaves your laptop.
We use it in Part 3 of
`modules/09a-neural-networks/notebooks/ai-agents.ipynb`.

**What you need:**
- about 3 GB of free disk space (the model alone is 2.0 GB)
- 8 GB of memory (RAM) or more is comfortable. With less, see "Slow
  laptop?" at the end.
- 15 to 30 minutes, mostly waiting for downloads

There are four steps. Do them in order.

---

## Step 1. Install Ollama

1. Go to **https://ollama.com/download**
2. Choose **Windows** or **macOS** and download the installer.
3. Open the downloaded file and follow the installer, like any other app.
4. When it finishes, Ollama runs quietly in the background. You will see a
   small llama icon:
   - Windows: in the system tray (bottom right, near the clock; you may need
     to click the ^ arrow)
   - Mac: in the menu bar (top right)

## Step 2. Download the model

Open a terminal:
- **Windows:** press the Windows key, type `cmd`, press Enter
  (Command Prompt).
- **Mac:** press Cmd + Space, type `Terminal`, press Enter.

Type this and press Enter:

```
ollama pull llama3.2
```

It downloads about 2 GB. Wait until you see `success`.

## Step 3. Check that the model works

In the same terminal, type:

```
ollama run llama3.2
```

When you see `>>>`, type a question, for example `What is a neural
network?`, and press Enter. The model answers.

To leave the chat, type `/bye` and press Enter.

## Step 4. Install the Python package

This step is in your course environment.

- **Windows:** open **Anaconda Prompt** (not Command Prompt).
- **Mac:** use Terminal.

Type these two lines, pressing Enter after each:

```
conda activate dsai
pip install ollama
```

**Done.** Open `ai-agents.ipynb` in VS Code or Jupyter. Run the cell that
sets `WRITER`, `REVIEWER` and `TASK` in Part 2 (it needs no API key), then
run the Part 3 cells.

---

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `'ollama' is not recognized` (Windows) or `command not found: ollama` (Mac) | The terminal was opened before Ollama was installed | Close the terminal, open a new one, try again. If it still fails, repeat Step 1. |
| `ConnectionError: Failed to connect to Ollama` (in the notebook) | The Ollama app is not running | Start Ollama from the Start menu (Windows) or Applications (Mac), then run the cell again. |
| `model 'llama3.2' not found (status code: 404)` | The model was not downloaded | Do Step 2 again. |
| `ModuleNotFoundError: No module named 'ollama'` | Step 4 was skipped, or done in the wrong environment | Do Step 4 again. Make sure the notebook uses the `dsai` kernel. |
| The answer takes more than a minute | Your laptop is short of memory | See "Slow laptop?" below. |

## Slow laptop?

Use the smaller version of the same model (1.3 GB instead of 2.0 GB):

1. In a terminal: `ollama pull llama3.2:1b`
2. In the notebook, find the line `MODEL = "llama3.2"` and change it to
   `MODEL = "llama3.2:1b"`

The smaller model is faster but makes more mistakes.

## Good to know

- The first question after starting Ollama is the slowest, because the model
  has to load into memory. Later questions are quicker.
- The model's answers change each time you ask. That is normal.
- A small model like this one is weaker than Claude or ChatGPT. It sometimes
  ignores instructions or gets facts wrong. Always check what it says.
- To free the disk space later: `ollama rm llama3.2`
