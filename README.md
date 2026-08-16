# poople-engine

An engine to play the word ladder game [poople](https://poople.io/) optimally.

## Word Data Sources

1. [`outparse/english-dictionary-dataset`](https://raw.githubusercontent.com/outparse/english-dictionary-dataset/refs/heads/main/txt/words.txt) in `./data/all_words.txt`

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

4. Use mypy to check type hints.

```bash
uv run mypy .
```

5. Run tests.

```bash
uv run pytest
```
