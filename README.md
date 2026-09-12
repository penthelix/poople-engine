# poople-engine

An engine to play the word ladder game [poople](https://poople.io/) optimally.

## Word Data Sources

1. [`outparse/english-dictionary-dataset`](https://raw.githubusercontent.com/outparse/english-dictionary-dataset/refs/heads/main/txt/words.txt) in `./data/all_words.txt` until line 37278.
2. I've added some words that I used during testing that weren't in the first dataset. These begin from line 37279 in `./data/all_words.txt`.

## Dev Setup

1. Clone this repository.
2. Check if you have uv installed. If not, install [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
uv --version
```

3. Create a virtual environment and install dependencies.

```bash
uv sync
```

4. Use basedpyright to check type hints.

```bash
uv run basedpyright
```

5. Run tests.

```bash
uv run pytest
```
