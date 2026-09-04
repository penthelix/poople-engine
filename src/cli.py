import typer

from src.graph import Graph, build_graph
from src.utils import (
    CORPUS_FILE,
    DATA_FOLDER,
    filter_words_by_length,
    lnum_to_word,
    sanitize_word,
    word_to_lnum,
)


def main(start_word: str, target_word: str = "poop"):
    start_word = sanitize_word(start_word)
    word_len: int = len(start_word)
    _, word_len_file = filter_words_by_length(
        in_path=CORPUS_FILE, out_dir=DATA_FOLDER, word_length=word_len
    )

    graph: Graph = build_graph(word_len_file)
    graph.calculate_shortest_paths()
    path: list[str] = [
        lnum_to_word(idx, word_len_file)
        for idx in graph.get_shortest_path_idx(
            word_to_lnum(start_word, word_len_file),
            word_to_lnum(target_word, word_len_file),
        )
    ]

    print("Poople Engine")
    print(" -> ".join(path))


if __name__ == "__main__":
    typer.run(main)
