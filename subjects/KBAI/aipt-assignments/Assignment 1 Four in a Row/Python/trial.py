from copy import deepcopy
from functools import partial
from threading import Lock

import numpy as np
from board import Board
from heuristics import Heuristic, SimpleHeuristic
from numba import jit
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

GAME_N = 4
START_BOARD = Board(6, 7)


minimax_1 = MinMaxPlayer(
    1,
    GAME_N,
    4,
    SimpleHeuristic(GAME_N),
)
minimax_2 = MinMaxPlayer(
    2,
    GAME_N,
    2,
    SimpleHeuristic(GAME_N),
)
abprume = AlphaBetaPlayer(
    1,
    GAME_N,
    4,
    SimpleHeuristic(GAME_N),
)
montecarlo = MCController(
    1, GAME_N, SimpleHeuristic(GAME_N), partial(upper_conf_bound, exploration_c=1), time_s=1
)


def trial(
    player_1: PlayerController,
    player_2: PlayerController,
    judge: Heuristic,
    n_rounds: int = 100,
    data_store: dict = None,
    lock: Lock = None,
) -> int:
    """Returns amount of times player 1 won."""

    # print(f"DS: {data_store}, L: {lock}")
    # assert (data_store is None) != (lock is None), "Must pass data store and lock together"

    players = [player_1, player_2]

    player_1.player_id = 1
    player_2.player_id = 2

    def round() -> bool:
        board = Board(6, 7)

        winner = 0
        turn = -1
        while winner == 0:
            turn += 1
            current_player = players[turn % 2]

            # print(f"Round {i}, turn {turn} (player {current_player.player_id})    ", end="\r")

            move = current_player.make_move(board)
            board.play(move, current_player.player_id)

            winner = judge.winning(board.get_board_state(), GAME_N)

        return winner == player_1.player_id

    p1_wins = 0
    for n in range(1, n_rounds + 1):
        p1_wins += round()
        print(f"Round {n}, p1 wins: {p1_wins}    ", end="\r")

    if data_store is None:
        return p1_wins

    with lock:
        data_store[(str(player_1), str(player_2))] = p1_wins


# trial(minimax_1, minimax_2, SimpleHeuristic(GAME_N))
