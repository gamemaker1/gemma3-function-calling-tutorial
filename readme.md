# Offline, Multimodal Function Calling with Gemma: A Tutorial

> This repository contains the source code for the tutorial on function calling with Gemma 3.

The tutorial is a single Python Notebook, [`tutorial.ipynb`](tutorial.ipynb). It uses helper functions from the [`toolkit`](toolkit/). The best way to learn is to do: please follow the below instructions on getting started so you can change, run and experiment with the code in the notebook as you read.

### Getting Started

This tutorial assumes you have basic knowledge of Python. In addition, this tutorial uses the following tools:

- [`ollama`](https://ollama.com) to run the models locally on your computer
- [`uv`](https://docs.astral.sh/uv/getting-started/) to run python code and manage dependencies.

If you haven't already, please follow this links above to get them set up.

First, let's make sure everything is installed correctly. Open your terminal and check the versions:

```bash
uv --version
ollama --version
```

Next, start `ollama` by running the following command:

```bash
ollama serve
```

In another terminal, clone this repository and open the notebook by running:

```bash
git clone https://github.com/gamemaker1/gemma3-function-calling-tutorial.git
cd gemma3-function-calling-tutorial/
uv run --with jupyter jupyter lab tutorial.ipynb
```

This should open this tutorial notebook in your browser so you can follow along!
