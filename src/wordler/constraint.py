from dataclasses import dataclass
from enum import Enum
from typing import Iterator, Self

import numpy as np

from wordler.utils import LET_TO_IDX


class Constraint(Enum):
    """Enum for constraint."""

    GREEN = "G"
    YELLOW = "Y"
    BLACK = "B"
    GREY = "K"

    @classmethod
    def from_code(cls, c: str):
        c = c.upper()
        if c == "G":
            return cls.GREEN
        elif c == "Y":
            return cls.YELLOW
        elif c == "B":
            return cls.BLACK
        elif c == "K":
            return cls.GREY
        else:
            raise ValueError(f"Invalid constraint: {c}")

    def __repr__(self) -> str:
        return self.value


ConstraintList = list[Constraint]


@dataclass
class ConstraintBank:
    word: str
    cb: ConstraintList

    @classmethod
    def from_str(cls, word: str, cb_str: str) -> Self:
        return cls(word, [Constraint.from_code(c) for c in cb_str])

    @property
    def cb_norm(self) -> ConstraintList:
        """Normalize the constraint list, placing `K` in place of `B` if needed."""
        seen_yellow = []
        cb_norm = []
        for letter, constraint in self.zip_constraints():
            if constraint in (Constraint.YELLOW, Constraint.GREEN):
                seen_yellow.append(letter)
            elif constraint == Constraint.BLACK:
                if letter in seen_yellow:
                    constraint = Constraint.GREY
            cb_norm.append(constraint)
        return cb_norm

    def zip_constraints(self) -> Iterator[tuple[str, Constraint]]:
        return zip(self.word, self.cb)

    def zip_norm_constraints(self) -> Iterator[tuple[str, Constraint]]:
        return zip(self.word, self.cb_norm)

    def __repr__(self) -> str:
        return f"{self.word} {self.cb} {self.cb_norm}"

    def to_yellow(self) -> np.ndarray:
        """Return the count of minimal occurrences for each letter."""
        yel = np.zeros(26, dtype=int)
        for letter, constraint in self.zip_constraints():
            if constraint == Constraint.YELLOW or constraint == Constraint.GREEN:
                yel[LET_TO_IDX[letter]] += 1
        return yel
