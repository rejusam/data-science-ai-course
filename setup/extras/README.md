# Heavy extras, installed when we reach them

The base environment in `../environment.yml` covers modules 0 through 8. A few
libraries are deliberately left out of it.

They are large, they are slow to resolve, and several of them are fussy about
platform. Installing them in week 1 would mean a longer, more failure-prone
setup for something you will not touch for four months. We install them the
week before they are needed, together, in class.

Activate the environment first:

```
conda activate dsai
```

## Deep learning, from module 9

TensorFlow and Keras. Used from week 17.

```
pip install tensorflow
```

On an Apple Silicon Mac, if the plain install misbehaves, install the two
Apple-maintained packages instead:

```
pip install tensorflow-macos tensorflow-metal
```

Do not run both variants. Pick one.

For anything that needs a GPU, use Google Colab. Colab gives you a GPU for
free, and week 18 has an exercise that compares Colab GPU runtime against your
own machine.

## Transformers and language models, from module 8

Used for the embeddings and LLM work in week 16.

```
pip install transformers sentence-transformers
```

These download model weights the first time you use them, which can be several
hundred megabytes per model.

## AI agents, from module 9

Used in `modules/09a-neural-networks/notebooks/ai-agents.ipynb`.

Part 2 calls Claude. It needs the package and your own API key in a file
called `.env` next to the notebook (the repository ignores `.env`, so the key
is never committed):

```
pip install anthropic
```

Part 3 runs a free model on your own laptop with Ollama. No key, but the
Ollama app and a 2 GB model download come first. Follow
[`../../resources/ollama-setup.md`](../../resources/ollama-setup.md), which ends with:

```
pip install ollama
```

## Cloud and big data, from modules 3 and 10

BigQuery, week 7:

```
pip install google-cloud-bigquery db-dtypes
```

PySpark, week 21. This needs a Java runtime as well as the Python package:

```
conda install -c conda-forge pyspark openjdk
```

## Keeping the record straight

If you install something not listed here and it turns out to be useful, say so
in Slack. Anything the whole cohort ends up needing gets added to
`environment.yml`, and everyone picks it up with:

```
conda env update -f setup/environment.yml --prune
```
