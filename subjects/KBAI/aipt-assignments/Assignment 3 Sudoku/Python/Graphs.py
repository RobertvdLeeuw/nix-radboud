from copy import deepcopy
from glob import glob

import matplotlib.pyplot as plt
import pandas as pd
from Game import EvalLimit, Game, get_eval_count
from Sudoku import Sudoku

HEURISTICS = ("mrv", "finalized", "degree", "lcv")
sudokus = [(path, Sudoku(path)) for path in glob("./Sudokus/*.txt", recursive=False)]


def get_sudoku_type(filepath: str) -> str:
    if "complete" in filepath:
        return "Complete, Invalid" if "wrong" in filepath else "Complete, Valid"

    return "Incomplete, Invalid" if "wrong" in filepath else "Incomplete, Valid"


n_evals = []
for path, s in reversed(sudokus):
    for heuristics in (
        [],
        *[HEURISTICS[:i] + HEURISTICS[i + 1 :] for i in range(len(HEURISTICS))],
        HEURISTICS,
    ):
        name = path.split("/")[-1].replace(".txt", "")

        if len(heuristics) == len(HEURISTICS):
            heuristics_formatted = "all"
        elif len(heuristics) == 0:
            heuristics_formatted = "none"
        else:
            missing = [h for h in HEURISTICS if h not in heuristics][0]
            heuristics_formatted = "all but " + missing

        print(f"---------- {name} ({heuristics_formatted}) start ----------")

        try:
            g = Game(deepcopy(s)).solve(**{h: True for h in heuristics})
        except EvalLimit:
            pass
        except:
            raise

        print(f"---------- {name} ({heuristics_formatted}) end ------------")

        n_evals.append((name, heuristics_formatted, get_eval_count()))


def heuristic_key(label: str) -> tuple[int, str]:
    if label == "none":
        return (0, "")
    return (label.count("+") + 1, label)


# grouped barplot: Y = eval count, X ticks = name, X-group = heuristics
df = pd.DataFrame(n_evals, columns=["sudoku", "heuristics", "evals"])
pivot = df.pivot(index="sudoku", columns="heuristics", values="evals")
pivot = pivot[sorted(pivot.columns, key=heuristic_key)]

ax = pivot.plot(kind="bar", figsize=(12, 6), width=0.8)
ax.set(xlabel="Sudoku", ylabel="Evaluation count", yscale="log")
ax.legend(title="Heuristics")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("./graphs/bar-eval-missing-1.png")

print(df)
