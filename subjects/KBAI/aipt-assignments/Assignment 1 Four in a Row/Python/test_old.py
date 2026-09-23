from typing import List

import numpy as np
from board import Board
from heuristics import Heuristic, SimpleHeuristic
from numba import jit
from players import AlphaBetaPlayer, HumanPlayer, MinMaxPlayer, PlayerController

board = Board(7, 6)

player = 1
for col in [3, 3, 4, 2, 5, 4]:
    board.play(col, player)
    player = 3 - player  # Switch between player 1 and 2

print(board)

# player setup
h1 = SimpleHeuristic(4)
h2 = SimpleHeuristic(4)
minimax_testplayer = MinMaxPlayer(1, 4, 4, h1)
alphabeta_testplayer = AlphaBetaPlayer(1, 4, 4, h2)

# tests weather both players take the same move
print(minimax_testplayer.make_move(board), alphabeta_testplayer.make_move(board))
print(minimax_testplayer.get_eval_count(), alphabeta_testplayer.get_eval_count())

# test for other board state, not immediately winning
player = 1
for col in [3, 3, 1, 2, 3, 4]:
    board.play(col, player)
    player = 3 - player  # Switch between player 1 and 2

print(board)
print(minimax_testplayer.make_move(board), alphabeta_testplayer.make_move(board))
print(minimax_testplayer.get_eval_count(), alphabeta_testplayer.get_eval_count())

# test for weather Player 1 blocks the winning placement for Player 2
board = Board(7, 6)
board.play(0, 2)
board.play(4, 1)
board.play(1, 2)
board.play(6, 1)
board.play(2, 2)
board.play(4, 1)
print(board)
print(minimax_testplayer.make_move(board), alphabeta_testplayer.make_move(board))
print(minimax_testplayer.get_eval_count(), alphabeta_testplayer.get_eval_count())
