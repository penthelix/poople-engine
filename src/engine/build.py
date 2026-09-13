import os

from PyInstaller.__main__ import run


def main() -> None:
    data_arg: str = f"data/all_words.txt{os.pathsep}data"
    run(["src/engine/cli.py", "--add-data", data_arg, "--name", "poople"])
