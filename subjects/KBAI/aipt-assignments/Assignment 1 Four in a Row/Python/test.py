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


test_tree()


def sanity_check_player(player: PlayerController):
    # Column
    for filled_row_start in range(WIDTH):
        one_to_win, one_to_lose = np.zeros((WIDTH, HEIGHT)), np.zeros((WIDTH, HEIGHT))

        row, col = np.indices((WIDTH, HEIGHT))
        winner_mask = ((HEIGHT - row) < GAME_N - 1) & (col == filled_row_start)
        one_to_win[winner_mask] = player.player_id
        one_to_lose[winner_mask] = flip_player_turn[player.player_id]
        one_to_win, one_to_lose = Board(one_to_win), Board(one_to_lose)

        move = player.make_move(one_to_win)
        assert move == filled_row_start, (
            f"{player.name} player didn't make directly winning move (column {filled_row_start}), made move {move}, \n {one_to_win.get_board_state()}"
        )
        move = player.make_move(one_to_lose)
        assert move == filled_row_start, (
            f"{player.name} player didn't block directly losing move move (column {filled_row_start}), made move {move}, \n {one_to_lose.get_board_state()}"
        )

    # Row
    for filled_row_start in range(WIDTH - GAME_N):
        one_to_win, one_to_lose = np.zeros((WIDTH, HEIGHT)), np.zeros((WIDTH, HEIGHT))

        row, col = np.indices((width, height))
        winner_mask = ((HEIGHT - row) == 0) & (filled_row_start <= col < filled_row_start + GAME_N)
        one_to_win[winner_mask] = player.player_id
        one_to_lose[winner_mask] = flip_player_turn[player.player_id]
        one_to_win, one_to_lose = Board(one_to_win), Board(one_to_lose)

        move = player.make_move(one_to_win)
        assert move in (filled_row_start + GAME_N, filled_row_start - 1), (
            f"{player.name} player didn't make directly winning move (left of {filled_row_start - 1} or right of {filled_row_start + GAME_N}), made move {move}, \n {one_to_win.get_board_state()}"
        )
        move = player.make_move(one_to_lose)
        assert move == (filled_row_start + GAME_N, filled_row_start - 1), (
            f"{player.name} player didn't block directly losing move move (left of {filled_row_start - 1} or right of {filled_row_start + GAME_N}), made move {move}, \n {one_to_lose.get_board_state()}"
        )

    # Diagonal
    for filled_row_start in range(WIDTH - GAME_N):
        one_to_win, one_to_lose = np.zeros((WIDTH, HEIGHT)), np.zeros((WIDTH, HEIGHT))

        row, col = np.indices((WIDTH, HEIGHT))
        winner_mask = (HEIGHT - row) == (col + filled_row_start) & (
            filled_row_start <= col < filled_row_start + GAME_N
        )
        loser_mask = (HEIGHT - row) < (col + filled_row_start) & (
            filled_row_start <= col < filled_row_start + GAME_N
        )

        one_to_win[winner_mask] = player.player_id
        one_to_win[loser_mask] = flip_player_turn[player.player_id]
        one_to_lose[winner_mask] = flip_player_turn[player.player_id]
        one_to_win[loser_mask] = player.player_id

        one_to_win, one_to_lose = Board(one_to_win), Board(one_to_lose)

        move = player.make_move(one_to_win)
        assert move in (filled_row_start + GAME_N, filled_row_start - 1), (
            f"{player.name} player didn't make directly winning move (diagonal {filled_row_start + GAME_N}), made move {move}, \n {one_to_win.get_board_state()}"
        )
        move = player.make_move(one_to_lose)
        assert move == (filled_row_start + GAME_N, filled_row_start - 1), (
            f"{player.name} player didn't block directly losing move move (diagonal {filled_row_start + GAME_N}), made move {move}, \n {one_to_lose.get_board_state()}"
        )


minimax = MinMaxPlayer(
    1,
    GAME_N,
    4,
    SimpleHeuristic(GAME_N),
)
abprune = AlphaBetaPlayer(
    1,
    GAME_N,
    4,
    SimpleHeuristic(GAME_N),
)
montecarlo = MCController(
    1, GAME_N, SimpleHeuristic(GAME_N), partial(upper_conf_bound, exploration_c=1), time_s=1
)

for player in (minimax, abprune, montecarlo):
    sanity_check_player(player)
