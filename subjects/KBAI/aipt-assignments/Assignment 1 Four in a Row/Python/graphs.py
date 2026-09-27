from copy import deepcopy
from functools import partial
from threading import Lock, Thread
from time import perf_counter

import frozenlist
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from board import Board
from heuristics import Heuristic, SimpleHeuristic
from matplotlib.colors import LinearSegmentedColormap
from players import (
    AlphaBetaPlayer,
    HumanPlayer,
    MCController,
    MCNode,
    MinMaxPlayer,
    Node,
    PlayerController,
    upper_conf_bound,
)
from trial import trial

GAME_N = 4
START_BOARD = Board(6, 7)


minimax = MinMaxPlayer(
    1,
    GAME_N,
    4,
    SimpleHeuristic(GAME_N),
)
abprune = AlphaBetaPlayer(
    2,
    GAME_N,
    4,
    SimpleHeuristic(GAME_N),
)
montecarlo = MCController(1, GAME_N, SimpleHeuristic(GAME_N), upper_conf_bound(1), n_iterations=200)
COLORS = ["orange", "blue", "green", "purple", "red", "yellow"]


def plot_eval_depth_scaling(players: list[PlayerController], depths: list[int]):
    results, lock = dict(), Lock()

    def test_n_evals(p: PlayerController, depth: int):
        # print(f"Evaluating {p.name} at depth {depth}...         ", end="\r")
        player = deepcopy(p)
        player.heuristic = SimpleHeuristic(GAME_N)
        player.max_depth = depth

        start = perf_counter()
        player.make_move(deepcopy(START_BOARD))
        end = perf_counter()

        with lock:
            results[(p, depth)] = player.heuristic.eval_count, end - start

    threads = [Thread(target=test_n_evals, args=(p, d)) for d in depths for p in players]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    results = [[results[(p, d)] for d in depths] for p in players]
    print("Scaling evaluation done.                                                 ")

    fig, evals_ax = plt.subplots(figsize=(8, 12))
    evals_ax.set(
        title="Scaling with search depth (in seconds and evaluations)",
        ylabel="Evaluations (solid)",
        yscale="log",
        xlabel="Search depth",
        xticks=range(max(depths) + 1),
    )
    # plt.tight_layout()

    time_ax = plt.twinx()
    time_ax.set_ylabel("Seconds (dashed)")
    time_ax.yaxis.set_label_position("right")
    time_ax.yaxis.tick_right()

    for p, c, result in zip(players, COLORS, results):
        n_evals, times = zip(*result)
        evals_ax.plot(n_evals, label=p.name, c=c)
        time_ax.plot(times, linestyle="dashed", c=c)

    evals_ax.legend()
    plt.savefig("Scaling.png")


def plot_MC_iteration_scaling(Ns: list[int]):
    results, lock = dict(), Lock()

    def test_time(n: int):
        print(f"Evaluating MCTS with {n} iterations...         ", end="\r")
        player = MCController(
            1, GAME_N, SimpleHeuristic(GAME_N), upper_conf_bound(1), n_iterations=n
        )

        start = perf_counter()
        player.make_move(deepcopy(START_BOARD))
        end = perf_counter()

        with lock:
            results[n] = end - start

    threads = [Thread(target=test_time, args=(n,)) for n in Ns]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    plt.plot(results.keys(), results.values())
    plt.title("MCTS scaling with iterations (in seconds)")
    plt.ylabel("Seconds")
    plt.yscale("log")
    plt.xlabel("Iterations")
    print("MC scaling evaluation done.                                                 ")
    plt.savefig("MC-Scaling.png")


# plot_MC_iteration_scaling([50, 75, 100, 200, 300, 500, 750, 1000])

# plot_eval_depth_scaling([minimax, abprume, montecarlo], range(1, 8))


from itertools import combinations_with_replacement, product


def plot_battle(
    players: list[PlayerController],
    judge: Heuristic,
    n_rounds: int = 100,
    filename: str = "Battles.png",
    labels: list[str] = (),
):
    trials, lock = dict(), Lock()

    # No need to compute X vs Y and Y vs X
    threads = [
        Thread(target=trial, args=(p1, p2, judge, n_rounds, trials, lock))
        for p1, p2 in combinations_with_replacement(players, 2)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    trials.update({(p2, p1): n_rounds - trials[(p1, p2)] for p1, p2 in trials if p1 != p2})

    results = [[trials[(str(p1), str(p2))] for p2 in players] for p1 in players]

    _, ax = plt.subplots(figsize=(12, 12), layout="constrained")

    cmap = LinearSegmentedColormap.from_list(
        "my_gradient", [(0, "red"), (0.5, "white"), (1, "green")]
    )
    ax.matshow(results, cmap=cmap)
    ax.set(
        title=f"Results of {n_rounds} rounds",
        xticks=np.arange(len(players)),
        yticks=np.arange(len(players)),
        xticklabels=labels or players,
        yticklabels=labels or players,
        ylabel="Player 1",
        xlabel="Player 2",
    )

    for (i, j), p1_wins in np.ndenumerate(results):
        ax.text(
            j,
            i,
            f"{labels[i] if labels else players[i].name} wins: {p1_wins}\n({round(p1_wins / n_rounds * 100, 2)}%)",
            ha="center",
            va="center",
        )

    plt.savefig(filename)


# plot_battle([minimax, abprune, montecarlo], SimpleHeuristic(GAME_N), 10)
mc_players = []
mc_labels = []
for c in [0.01, 0.5, 1, 1.5, 2]:
    p = deepcopy(montecarlo)
    p.selection_strat = upper_conf_bound(c)
    p.n_iterations = 800
    mc_players.append(p)
    mc_labels.append(f"MCTS (c={c})")

plot_battle(mc_players, SimpleHeuristic(GAME_N), 20, "MC-battles.png", mc_labels)
