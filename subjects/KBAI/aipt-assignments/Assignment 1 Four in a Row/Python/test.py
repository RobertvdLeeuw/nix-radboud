from copy import deepcopy
from functools import partial

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
    flip_player_turn,
    upper_conf_bound,
)

GAME_N = 4
WIDTH, HEIGHT = 7, 6
START_BOARD = Board(WIDTH, HEIGHT)
DUMMY_PLAYER = PlayerController(1, GAME_N, SimpleHeuristic(GAME_N))


def test_tree():
    print("Testing tree...", end="\r")
    tree_root = Node(START_BOARD, DUMMY_PLAYER)

    assert len(tree_root.expand_tree(1).children) == WIDTH, (
        f"Expected {START_BOARD.width} nodes on root expansion, got {len(tree_root.children)}"
    )
    assert tree_root.is_fully_expanded, "Expanding root tree didn't occur fully"

    one_col_full = Board(START_BOARD)
    cur_turn = 1
    for _ in range(HEIGHT):
        one_col_full.play(0, cur_turn)
        cur_turn = flip_player_turn[cur_turn]

    one_col_full_node = Node(one_col_full, DUMMY_PLAYER)
    assert len(one_col_full_node.expand_tree(1).children) == WIDTH - 1, (
        f"Expected {START_BOARD.width} nodes on 1 column full expansion, got {len(tree_root.children)}"
    )
    assert one_col_full_node.is_fully_expanded, "Expanding 1 col full tree didn't occur fully"

    print("Tree passed tests")


test_tree()


def sanity_check_player(player: PlayerController):
    print(f"Sanity checking player {player.name}...", end="\r")
    # Column
    for deciding_col in range(WIDTH):
        one_to_win, one_to_lose = np.zeros((WIDTH, HEIGHT)), np.zeros((WIDTH, HEIGHT))

        col, row = np.indices((WIDTH, HEIGHT))

        winner_mask = ((HEIGHT - row) < GAME_N) & (col == deciding_col)

        one_to_win[winner_mask] = player.player_id
        one_to_lose[winner_mask] = flip_player_turn[player.player_id]

        one_to_win, one_to_lose = Board(one_to_win), Board(one_to_lose)

        move = player.make_move(one_to_win)
        assert move == deciding_col, (
            f"{player.name} player didn't make directly winning move ({deciding_col + 1}), made move {move + 1}, \n {one_to_win}"
        )
        move = player.make_move(one_to_lose)
        assert move == deciding_col, (
            f"{player.name} player didn't block directly losing move move ({deciding_col + 1}), made move {move + 1}, \n {one_to_lose}"
        )

    # Row (3 from corners)
    for corner in ["left", "right"]:
        one_to_win, one_to_lose = np.zeros((WIDTH, HEIGHT)), np.zeros((WIDTH, HEIGHT))
        winner_mask = ((col < (GAME_N - 1)) if corner == "left" else (col > (WIDTH - GAME_N))) & (
            row == HEIGHT - 1
        )

        one_to_win[winner_mask] = player.player_id
        one_to_lose[winner_mask] = flip_player_turn[player.player_id]
        one_to_win, one_to_lose = Board(one_to_win), Board(one_to_lose)

        move = player.make_move(one_to_win)
        deciding_move = GAME_N - 1 if corner == "left" else WIDTH - GAME_N
        assert move == deciding_move, (
            f"{player.name} player didn't make directly winning move ({deciding_move + 1}), made move {move + 1}, \n {one_to_win}"
        )
        move = player.make_move(one_to_lose)
        assert move == deciding_move, (
            f"{player.name} player didn't block directly losing move move ({deciding_move + 1}), made move {move + 1}, \n {one_to_lose}"
        )

    print(f"Player {player.name} passed sanity checks.")


minimax = MinMaxPlayer(
    1,
    GAME_N,
    4,
    SimpleHeuristic(GAME_N),
)
abprune = AlphaBetaPlayer(
    1,
    GAME_N,
    2,
    SimpleHeuristic(GAME_N),
)
montecarlo = MCController(
    1, GAME_N, SimpleHeuristic(GAME_N), partial(upper_conf_bound, exploration_c=1), time_s=1
)

sanity_check_player(minimax)
sanity_check_player(abprune)
sanity_check_player(montecarlo)
