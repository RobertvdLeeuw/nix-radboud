from collections import defaultdict
from copy import deepcopy
from functools import partial
from threading import Lock, Thread

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
    start_board: Board,
    n_battles: int,
    data_store: dict = None,
    data_store_lock: Lock = None,
) -> int:
    """
    Makes each possible first move, and tries (p1, p2) + (p2, p1) for each. Returns amount of times player 1 won.
    N rounds = board.width
    """

    if data_store is not None:
        with data_store_lock:
            print(f"{len(data_store) // 2}/{n_battles}", end="\r")

    dummy_player = PlayerController(1, GAME_N, deepcopy(judge))
    tree = Node(start_board, dummy_player).expand_tree(1)
    boards = [
        child.board for i, child in enumerate(tree) if i % 2 == 0
    ]  # Halving so we compute for less time

    p1_wins = 0
    lock = Lock()

    def round(b: Board, p1: PlayerController, p2: PlayerController):
        nonlocal p1_wins

        board = deepcopy(b)
        players = [deepcopy(p1), deepcopy(p2)]
        players[0].player_id = 1
        players[1].player_id = 2

        winner_id = 0
        turn = 0  #  First turn already played in boards definition
        while winner_id == 0:
            turn += 1
            current_player = players[turn % 2]

            # print(f"Round {i}, turn {turn} (player {current_player.player_id})    ", end="\r")

            move = current_player.make_move(board)
            board.play(move, current_player.player_id)

            winner_id = judge.winning(board.get_board_state(), GAME_N)

        winner = p1 if p1.player_id == winner_id else p2
        with lock:
            p1_wins += str(winner) == str(player_1)

    threads = []

    for b in boards:
        t1 = Thread(target=round, args=(b, player_1, player_2))
        t2 = Thread(target=round, args=(b, player_2, player_1))
        threads.extend([t1, t2])

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    if data_store is not None:
        with data_store_lock:
            data_store[(str(player_1), str(player_2))] = p1_wins
            data_store[(str(player_2), str(player_1))] = start_board.width - p1_wins

            print(f"{len(data_store) // 2}/{n_battles}", end="\r")
    return p1_wins


# trial(minimax_1, minimax_2, SimpleHeuristic(GAME_N))
