from pathlib import Path

from src.utils import PROJECT_ROOT


def test_main():
    assert isinstance(PROJECT_ROOT, Path)
