from itertools import product
from string import ascii_lowercase

import numpy as np

ABC_SPACE_LOW = " ".join(ascii_lowercase)
LET_TO_IDX = {c: i for i, c in enumerate(ascii_lowercase)}


def build_word_vec(word: str) -> np.ndarray:
    """Build a word vector."""
    vec = np.zeros((5, 26), dtype=int)
    for i, letter in enumerate(word):
        vec[i, LET_TO_IDX[letter]] = 1
    return vec


def generate_constraint_strs() -> list[str]:
    """Generate all possible constraint strings."""
    con_letters = "gyb"
    return ["".join(p) for p in product(con_letters, repeat=5)]


CONSTRAINT_STRINGS = generate_constraint_strs()
