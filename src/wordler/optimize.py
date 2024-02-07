from copy import deepcopy
from time import perf_counter
import numpy as np
import pandas as pd
from tqdm import tqdm
from wordler.constraint import ConstraintBank
from wordler.solver import Solver
from wordler.utils import CONSTRAINT_STRINGS


def compute_cleaning(
    word: str,
    s: Solver,
    word_vecs: np.ndarray,
    word_yel: np.ndarray,
    word_list: list[str],
    # ) -> float:
) -> tuple[float, pd.DataFrame]:
    new_lens = []
    perf_ls = []
    for cbs in CONSTRAINT_STRINGS[:]:
        t0 = perf_counter()
        cb = ConstraintBank.from_str(word, cbs)
        t1 = perf_counter()
        ss = deepcopy(s)
        t2 = perf_counter()
        ss.apply_constraint_bank(cb)
        t3 = perf_counter()
        # ss.print_options()
        new_wl = ss.filter_words(word_vecs, word_yel, word_list)
        t4 = perf_counter()
        # print(cbs, new_wl)
        if len(new_wl) > 1:
            new_lens.append(len(new_wl))
        perf_ls.append(
            {
                "cb": t1 - t0,
                "copy": t2 - t1,
                "apply": t3 - t2,
                "filter": t4 - t3,
                "word": word,
                "cbs": cbs,
                "new_wl": len(new_wl),
            }
        )
    # print(new_lens)
    if len(new_lens) == 0:
        avg_len = 0
    else:
        avg_len = sum(new_lens) / len(new_lens)
    perf_df = pd.DataFrame(perf_ls)
    # print(perf_df)
    return avg_len, perf_df


def sort_word_list(
    s: Solver,
    word_vecs: np.ndarray,
    word_yel: np.ndarray,
    word_list: list[str],
    word_list_possible: list[str],
    # ) -> list[str]:
) -> tuple[list[str], pd.DataFrame]:
    new_lens = []
    all_perf_dfs = []
    for word in tqdm(word_list_possible[:]):
        # print(word)
        # word = word.lower()
        cleaning, perf_df = compute_cleaning(word, s, word_vecs, word_yel, word_list)
        new_lens.append((word, cleaning))
        all_perf_dfs.append(perf_df)
    # new_lens.sort(key=lambda x: x[1], reverse=True)
    new_lens.sort(key=lambda x: x[1])
    # print(new_lens)
    all_perf_df = pd.concat(all_perf_dfs, ignore_index=True)
    # return [x[0] for x in new_lens], all_perf_df
    return new_lens, all_perf_df
