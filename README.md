# poople-engine

An engine to play the word ladder game [poople](https://poople.io/) optimally.

Poople is a silly word ladder game. The goal is to transform a starting word into the word 'poop', changing one letter a time. To explore the game better, I wrote an engine to play it optimally. It works by creating a graph of all words of a given length and finds the shortest path from the initial word to the final word.

Though initially motivated by poople, this engine works for any variant and allows you to specify a starting and ending word of any length (assuming both are of the same length).

As of now, the engine is very inefficient. It generates the graph of words at every run. Future iterations will implement caching. The words dataset is also lacking.

## Word Data Sources

1. [`outparse/english-dictionary-dataset`](https://raw.githubusercontent.com/outparse/english-dictionary-dataset/refs/heads/main/txt/words.txt) in `./data/all_words.txt` until line 37278.
2. I've added some words that I used during testing that weren't in the first dataset. These begin from line 37279 in `./data/all_words.txt`.

## Installation

1. Download the latest release from [GitHub Releases](https://github.com/penthelix/poople-engine/releases).
2. Run the engine.

```bash
./poople <start_word> # Use --target-word to specify an optional target word
```

3. Optionally, you can move the executable to a directory in your PATH to run it from anywhere.

## Tech Stack

- Python 3
- [Typer](https://typer.tiangolo.com/) for CLI

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

4. Run the engine.

```bash
uv run poople <start_word> # Use --target-word to specify an optional target word
```

5. Run tests with pytest and use basedpyright for type checking.

```bash
uv run pytest
uv run basedpyright
```
