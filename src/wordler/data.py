from pathlib import Path

import numpy as np

from wordler.utils import build_word_vec


def load_word_list(w_fp: Path) -> list[str]:
    """Load words, one per line."""
    with open(w_fp, "r") as f:
        return f.read().splitlines()


def build_word_ids(word_list: list[str]) -> dict[str, int]:
    """Build word ids."""
    return {word: i for i, word in enumerate(word_list)}


def build_word_vecs(word_list: list[str]) -> np.ndarray:
    """Build word vectors."""
    return np.array([build_word_vec(word) for word in word_list], dtype=int)


def build_word_yel(word_vecs: np.ndarray) -> np.ndarray:
    """Build word yellow counts."""
    return word_vecs.sum(axis=1, dtype=int)
