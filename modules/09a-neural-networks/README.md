# Neural networks

Plan label: `Module 9 Pt 1`. Week 17.

## Sessions

| Date | Focus | Lab / activity |
|---|---|---|
| Mon, 23 Nov 2026 | AI landscape; neural network fundamentals: perceptron, activation functions, backpropagation | Lab NN from scratch |
| Wed, 25 Nov 2026 | TensorFlow and Keras; training aspects: loss, optimisers, epochs, regularisation, callbacks | Lab Keras |

## What this module covers

- AI landscape
- neural network fundamentals: perceptron, activation functions, backpropagation
- TensorFlow and Keras
- training aspects: loss, optimisers, epochs, regularisation, callbacks

## Labs and activities

- Lab NN from scratch
- Lab Keras

## How to get the most out of these sessions

- Build the tiny network by hand before using a framework
- Log every experiment - hyperparameter notes are a professional habit

## AI agents (Module 9 Part 1)

In `notebooks/`:

| Notebook | What it shows | Needs |
|---|---|---|
| `ai-agents.ipynb` | An agent learns a route by Q-learning; then a writer and a reviewer agent, first with Claude, then with a local model | Part 2: an Anthropic API key. Part 3: Ollama |
| `ai-agents-ollama.ipynb` | The writer and reviewer on a free model on your own laptop | Ollama only, no API key |

Setup:
- Ollama, step by step: [`../../resources/ollama-setup.md`](../../resources/ollama-setup.md) (also as a [PDF](../../resources/ollama-setup.pdf))
- Python packages: the Module 9 section of [`../../setup/extras/README.md`](../../setup/extras/README.md)
- An API key goes in a file called `.env` next to the notebook, as `ANTHROPIC_API_KEY=your-key`. The repository ignores `.env`, so the key is never committed. Never paste a key into a notebook.

## Folders

- `notebooks/` — worked examples and lab notebooks
- `data/` — datasets used by this module

## Before you start

Activate the course environment:

```
conda activate dsai
```

Then start Jupyter from the repository root:

```
jupyter lab
```
