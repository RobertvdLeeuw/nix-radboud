from copy import deepcopy
from functools import partial
from time import perf_counter

import frozenlist
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from board import Board
from heuristics import Heuristic, SimpleHeuristic
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
    def test_n_evals(p: PlayerController, depth: int):
        print(f"Evaluating {p.name} at depth {depth}...         ", end="\r")
        player = deepcopy(p)
        player.heuristic = SimpleHeuristic(GAME_N)
        player.max_depth = depth

        start = perf_counter()
        player.make_move(deepcopy(START_BOARD))
        end = perf_counter()

        return player.heuristic.eval_count, end - start

    results = [[test_n_evals(p, d) for d in depths] for p in players]
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
    def test_time(n: int):
        print(f"Evaluating MCTS with {n} iterations...         ", end="\r")
        player = MCController(
            1, GAME_N, SimpleHeuristic(GAME_N), upper_conf_bound(1), n_iterations=n
        )

        start = perf_counter()
        player.make_move(deepcopy(START_BOARD))
        end = perf_counter()

        return end - start

    plt.title = ("Scaling with iterations (in seconds)",)
    plt.ylabel = ("Seconds",)
    plt.yscale = ("log",)
    plt.xlabel = ("Iterations",)
    plt.plot([test_time(n) for n in Ns])
    print("MC scaling evaluation done.                                                 ")
    plt.savefig("MC-Scaling.png")


plot_MC_iteration_scaling([10, 50, 100])  # , 200, 300, 500, 1000])

# plot_eval_depth_scaling([minimax, abprume, montecarlo], range(1, 8))


from itertools import combinations_with_replacement, product


def plot_battle(players: list[PlayerController], judge: Heuristic, n_rounds: int = 100):
    # No need to compute X vs Y and Y vs X
    trials = {
        frozenset([p1, p2]): trial(p1, p2, judge, n_rounds)
        for p1, p2 in combinations_with_replacement(players, 2)
    }
    results = [[trials[frozenset([p1, p2])] for p2 in players] for p1 in players]

    _, ax = plt.subplots(figsize=(8, 8), layout="constrained")
    ax.matshow(results, cmap="RdYlBu")
    ax.set(
        title=f"Results of {n_rounds} rounds",
        xticks=np.arange(len(players)),
        yticks=np.arange(len(players)),
        xticklabels=players,
        yticklabels=players,
        ylabel="Player 1",
        xlabel="Player 2",
    )

    for (i, j), p1_wins in np.ndenumerate(results):
        ax.text(
            j,
            i,
            f"{players[i].name} wins: {p1_wins} ({round(p1_wins / n_rounds * 100, 2)}%)",
            ha="center",
            va="center",
        )

    plt.savefig("Battles.png")


# plot_battle([minimax, abprune, montecarlo], SimpleHeuristic(GAME_N), 10)
