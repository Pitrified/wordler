from dataclasses import dataclass

import numpy as np

from wordler.constraint import Constraint, ConstraintBank
from wordler.utils import ABC_SPACE_LOW, LET_TO_IDX


@dataclass
class Solver:
    options: np.ndarray
    yellows: np.ndarray

    def __init__(self) -> None:
        self.options = np.ones((5, 26), dtype=int)
        self.yellows = np.zeros(26, dtype=int)

    def apply_constraint_bank(self, cb: ConstraintBank) -> None:
        """Apply a constraint bank to the solver."""
        for lpos, (letter, constraint) in enumerate(cb.zip_norm_constraints()):
            if constraint == Constraint.GREEN:
                self.apply_green(letter, lpos)
            elif constraint == Constraint.YELLOW:
                self.apply_yellow(letter, lpos)
            elif constraint == Constraint.BLACK:
                self.apply_black(letter)
            elif constraint == Constraint.GREY:
                self.apply_grey(letter, lpos)
            else:
                raise ValueError(f"Invalid constraint: {constraint}")

        new_yellows = cb.to_yellow()
        # keep the max of the new and old yellows
        self.yellows = np.maximum(self.yellows, new_yellows)

    def apply_green(self, letter: str, lpos: int) -> None:
        """Apply a green constraint to the solver."""
        lid = LET_TO_IDX[letter]
        # all the other letters in this position are not possible
        self.options[lpos, :] = 0
        self.options[lpos, lid] = 1

    def apply_yellow(self, letter: str, lpos: int) -> None:
        """Apply a yellow constraint to the solver."""
        lid = LET_TO_IDX[letter]
        # the letter in this position is not possible
        self.options[lpos, lid] = 0

    def apply_black(self, letter: str) -> None:
        """Apply a black constraint to the solver."""
        lid = LET_TO_IDX[letter]
        # the letter in any position is not possible
        self.options[:, lid] = 0

    def apply_grey(self, letter: str, lpos: int) -> None:
        """Apply a grey constraint to the solver.

        A grey constraint is a black constraint that occurs after a yellow constraint.
        So if the user guessed `E` twice, both times in the wrong place,
        in a word that has a single `E`,
        the first is a yellow constraint and the second is a grey constraint.
        You learn that the letter is not in that position but it is in the word.
        """
        lid = LET_TO_IDX[letter]
        # the letter in this position is not possible
        self.options[lpos, lid] = 0

    def filter_words(
        self,
        word_vecs: np.ndarray,
        word_yel: np.ndarray,
        word_list: list[str],
    ) -> list[str]:
        """Filter the words based on the constraints."""
        ### check letters

        # mix the word vectors with the options
        let_pos_bit = np.logical_and(word_vecs, self.options)
        # print(f"{let_pos_bit.shape=}")
        # print(let_pos_bit[0].astype(int))

        let_pos_sum = let_pos_bit.sum(axis=(1, 2))
        # print(f"{let_pos_sum.shape=}")
        # print(let_pos_sum[0].astype(int))

        let_val_bit = let_pos_sum == 5
        # print(f"{let_val_bit.shape=}")
        # print(let_val_bit.astype(int))

        #### check yellows

        yel_cnt_bit = self.yellows <= word_yel
        # print(f"{yel_cnt_bit.shape=}")
        # print(yel_cnt_bit[WORD_IDS['alert']].astype(int))

        yel_cnt_sum = yel_cnt_bit.sum(axis=1)
        # print(f"{yel_cnt_sum.shape=}")
        # print(yel_cnt_sum)

        yel_val_bit = yel_cnt_sum == 26
        # print(f"{yel_val_bit.shape=}")
        # print(yel_val_bit.astype(int))

        #### mix the two constraints

        fin_val_bit = np.logical_and(let_val_bit, yel_val_bit)
        # print(f"{fin_val_bit.shape=}")
        # print(fin_val_bit.astype(int))

        # val_ids = np.where(let_pos_sum == 5)[0]
        # val_ids = np.where(let_val_bit)[0]
        fin_val_ids = np.where(fin_val_bit)[0]
        # print(f"{val_ids=}")
        # print(f"{val_ids.shape=}")
        # print(val_ids[0].astype(int))

        # nw = WORD_IDS["abide"]
        # print(f"{WORD_LIST[nw]=}")
        # print(let_pos_bit[nw].astype(int))
        # # print(pos_let[nw].astype(int))
        # print(let_pos_sum[nw].astype(int))

        fin_val_words = [word_list[i] for i in fin_val_ids]
        return fin_val_words

    def print_options(self) -> None:
        """Print the options."""
        print(f"  {ABC_SPACE_LOW}")
        print(self.options.astype(int))

    def print_yellows(self) -> None:
        """Print the yellows."""
        print(f"  {ABC_SPACE_LOW}")
        print(f" {self.yellows}")
