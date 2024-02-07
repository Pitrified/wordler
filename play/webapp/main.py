from typing import Any
import streamlit as st

from wordler.constraint import Constraint, ConstraintBank
from wordler.const import SOLUTION_FP
from wordler.data import build_word_ids, build_word_vecs, build_word_yel, load_word_list
from wordler.solver import Solver


def apply_constraints():
    widget_value = st.session_state.word_input
    cbs = widget_value.split(" ")[1]
    word_value = widget_value.split(" ")[0]
    print(f"got {widget_value}: {cbs=}")
    # if len(cbs) != 5: return
    cb = ConstraintBank.from_str(word_value, cbs)
    s = st.session_state.solver
    s.apply_constraint_bank(cb)
    s.print_options()
    wl = s.filter_words(**word_data)
    st.session_state.wl = wl
    st.session_state.history.append(cb)
    st.session_state.word_input = ""


def setup_state() -> None:
    if "new_game" in st.session_state:
        ng = st.session_state.new_game
        print(f"new_game: {ng}")
    else:
        print(f"new_game: no state")
        ng = False

    if "solver" not in st.session_state or ng:
        print("new solver")
        st.session_state.solver = Solver()
        s = st.session_state.solver
        s.print_options()

    if "history" not in st.session_state or ng:
        st.session_state.history = []

    if "wl" not in st.session_state or ng:
        st.session_state.wl = []


setup_state()

st.title("Wordle Solver")


@st.cache_data
def load_word_data() -> dict[str, Any]:
    sol_word_list = load_word_list(SOLUTION_FP)[:50000]
    # sol_word_ids = build_word_ids(sol_word_list)
    sol_word_vecs = build_word_vecs(sol_word_list)
    sol_word_yel = build_word_yel(sol_word_vecs)
    return {
        "word_list": sol_word_list,
        "word_vecs": sol_word_vecs,
        "word_yel": sol_word_yel,
    }


word_data = load_word_data()

for cb in st.session_state.history:
    cols = st.columns(15)
    for i, col in enumerate(cols[:5]):
        let = cb.word[i]
        con = cb.cb[i]
        if con == Constraint.GREEN:
            col.markdown(f":green[{let}]")
        elif con == Constraint.YELLOW:
            col.markdown(f":orange[{let}]")
        else:
            col.write(let)

for _ in range(6 - len(st.session_state.history)):
    cols = st.columns(15)
    for i, col in enumerate(cols[:5]):
        col.write("_")

word = st.text_input(
    "Enter your word and the constraints separated by a space",
    key="word_input",
    on_change=apply_constraints,
)

if len(st.session_state.wl) > 0:
    st.write(" ".join(st.session_state.wl))

new_game = st.button("New game", on_click=setup_state, key="new_game")
