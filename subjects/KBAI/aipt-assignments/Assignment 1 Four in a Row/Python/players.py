from __future__ import annotations

from abc import abstractmethod
from functools import partial, reduce
from typing import TYPE_CHECKING, Callable, Self

import numpy as np
from sympy.strategies import condition

if TYPE_CHECKING:
    from board import Board
    from heuristics import Heuristic


class PlayerController:
    """Abstract class defining a player"""

    def __init__(self, player_id: int, game_n: int, heuristic: Heuristic) -> None:
        """
        Args:
            player_id (int): id of a player, can take values 1 or 2 (0 = empty)
            game_n (int): n in a row required to win
            heuristic (Heuristic): heuristic used by the player
        """
        self.player_id = player_id
        self.game_n = game_n
        self.heuristic = heuristic

    def get_eval_count(self) -> int:
        """
        Returns:
            int: The amount of times the heuristic was used to evaluate a board state
        """
        return self.heuristic.eval_count

    def __str__(self) -> str:
        """
        Returns:
            str: representation for representing the player on the board
        """
        if self.player_id == 1:
            return "X"
        return "O"

    @abstractmethod
    def make_move(self, board: Board) -> int:
        """Gets the column for the player to play in

        Args:
            board (Board): the current board

        Returns:
            int: column to play in
        """
        pass


def is_our_turn(abs_depth: int) -> bool:
    return abs_depth % 2 == 0


flip_player_turn = {0: 0, 1: 2, 2: 1}


class MinMaxPlayer(PlayerController):
    """Class for the minmax player using the minmax algorithm
    Inherits from Playercontroller
    """

    name = "Minimax"

    def __init__(self, player_id: int, game_n: int, max_depth: int, heuristic: Heuristic) -> None:
        """
        Args:
            player_id (int): id of a player, can take values 1 or 2 (0 = empty)
            game_n (int): n in a row required to win
            depth (int): the max search depth
            heuristic (Heuristic): heuristic used by the player
        """
        super().__init__(player_id, game_n, heuristic)
        self.max_depth: int = max_depth

    def make_move(self, board: Board) -> int:
        """Gets the column for the player to play in

        Args:
            board (Board): the current board

        Returns:
            int: column to play in
        """

        def minimax(node: Node) -> float:
            if node.abs_depth >= self.max_depth or node.is_terminal(self.heuristic, self.game_n):
                return self.heuristic.evaluate_board(self.player_id, node.board)

            node.expand_tree(1)
            eval_func = max if is_our_turn(node.abs_depth) else min

            return reduce(
                lambda best, child: eval_func(best, minimax(child)),
                node.children.values(),
                -np.inf if is_our_turn(node.abs_depth) else np.inf,
            )

        root = Node(board, self)

        assert not root.is_terminal(self.heuristic, self.game_n), (
            "Trying to minimax from terminal node"
        )

        root.expand_tree(1)
        return max(root.children, key=lambda c: minimax(root.children[c]))


class AlphaBetaPlayer(PlayerController):
    """Class for the minmax player using the minmax algorithm with alpha-beta pruning
    Inherits from Playercontroller
    """

    name = "AB Prune"

    def __init__(self, player_id: int, game_n: int, max_depth: int, heuristic: Heuristic) -> None:
        """
        Args:
            player_id (int): id of a player, can take values 1 or 2 (0 = empty)
            game_n (int): n in a row required to win
            depth (int): the max search depth
            heuristic (Heuristic): heuristic used by the player
        """
        super().__init__(player_id, game_n, heuristic)
        self.max_depth: int = max_depth

    def make_move(self, board: Board) -> int:
        """Gets the column for the player to play in

        Args:
            board (Board): the current board

        Returns:
            int: column to play in
        """

        def ab_prune(
            node: Node, alpha: float = -np.inf, beta: float = np.inf, return_move_instead=False
        ) -> float | int:
            if node.abs_depth >= self.max_depth or node.is_terminal(self.heuristic, self.game_n):
                return self.heuristic.evaluate_board(self.player_id, node.board)

            our_turn = is_our_turn(node.abs_depth)

            node.expand_tree(1)
            eval_func = max if our_turn else min

            # Early termination in AB so we can't reduce :(
            best_eval = -np.inf if our_turn else np.inf
            best_move = None

            # Must be faster to move child gen to in loop so we don't gen all (use early termination), but not gonna do that now.
            # node.expand_tree(1, self.player_id)

            for col, child in node.children.items():
                eval = ab_prune(child, alpha, beta)

                old_best = best_eval
                best_eval = eval_func(best_eval, eval)

                if best_eval != old_best:
                    best_move = col

                if our_turn:
                    alpha = max(alpha, best_eval)
                else:
                    beta = min(beta, best_eval)

                if beta <= alpha:
                    break

            return best_move if return_move_instead else best_eval

        root = Node(board, self)
        return ab_prune(root, return_move_instead=True)


class HumanPlayer(PlayerController):
    """Class for the human player
    Inherits from Playercontroller
    """

    def __init__(self, player_id: int, game_n: int, heuristic: Heuristic) -> None:
        """
        Args:
            player_id (int): id of a player, can take values 1 or 2 (0 = empty)
            game_n (int): n in a row required to win
            heuristic (Heuristic): heuristic used by the player
        """
        super().__init__(player_id, game_n, heuristic)

    def make_move(self, board: Board) -> int:
        """Gets the column for the player to play in

        Args:
            board (Board): the current board

        Returns:
            int: column to play in
        """
        print(board)

        if self.heuristic is not None:
            print(f"Heuristic {self.heuristic} calculated the best move is:", end=" ")
            print(self.heuristic.get_best_action(self.player_id, board) + 1, end="\n\n")

        col: int = self.ask_input(board)

        print(f"Selected column: {col}")
        return col - 1

    def ask_input(self, board: Board) -> int:
        """Gets the input from the user

        Args:
            board (Board): the current board

        Returns:
            int: column to play in
        """
        try:
            col: int = int(input(f"Player {self}\nWhich column would you like to play in?\n"))
            assert 0 < col <= board.width
            assert board.is_valid(col - 1)
            return col
        except ValueError:  # If the input can't be converted to an integer
            print("Please enter a number that corresponds to a column.", end="\n\n")
            return self.ask_input(board)
        except AssertionError:  # If the input matches a full or non-existing column
            print(
                "Please enter a valid column.\nThis column is either full or doesn't exist!",
                end="\n\n",
            )
            return self.ask_input(board)


import random
import time
from copy import deepcopy


class Node:
    def __init__(
        self,
        board: Board,
        player_owner: PlayerController,
        children: dict[int, Node] | None = None,
        parent: Self | None = None,
    ):
        self.board = board
        self.children = children or dict()  # col/move as int -> Node
        self.parent = parent
        self.player_owner = player_owner

    @property
    def is_leaf(self) -> bool:
        return len(self.children) == 0

    @property
    def is_root(self) -> bool:
        return self.parent is None

    @property
    def root(self) -> Self:
        return self if self.is_root else self.parent.root

    @property
    def n(self) -> int:
        return 1 if self.is_leaf else sum(c.n for c in self)

    @property
    def abs_depth(self) -> int:
        return 0 if self.is_root else self.parent.abs_depth + 1

    def is_terminal(self, heuristic: Heuristic, game_n: int = 4) -> bool:
        return heuristic.winning(self.board.get_board_state(), game_n) != 0

    def add_child(self, col: int) -> Self:
        assert not self.is_terminal(self.player_owner.heuristic, self.player_owner.game_n), (
            "Trying to create a child for a terminal node"
        )
        assert col < self.board.width, "Move outside of game"
        assert self.board.is_valid(col), "Invalid move"

        player_id = (
            self.player_owner.player_id
            if is_our_turn(self.abs_depth)
            else flip_player_turn[self.player_owner.player_id]
        )

        child = Node(
            self.board.get_new_board(col, player_id),
            self.player_owner,
            parent=self,
        )
        self.children[col] = child

        return child

    def expand_tree(self, depth: int) -> Self:
        # Fine for 4-in-a-row, not for Chess (explosion)

        if depth == 0 or self.is_terminal(self.player_owner.heuristic, self.player_owner.game_n):
            return self

        for col in filter(self.board.is_valid, range(self.board.width)):
            if col not in self.children:
                self.add_child(col).expand_tree(depth - 1)
            else:
                self.children[col].expand_tree(depth - 1)

        return self

    def __iter__(self):
        return iter(self.children.values())

    @property
    def is_fully_expanded(self) -> bool:
        total_valid = filter(self.board.is_valid, range(self.board.width))
        return len(self.children) == len(list(total_valid))


class MCNode(Node):
    def __init__(
        self,
        board: Board,
        player_owner: PlayerController,
        children: dict = None,
        parent: "Node" | None = None,
    ):
        super().__init__(board, player_owner, children, parent)

        self.visits: int = 0
        self.total_score: float = 0

    def backprop(self, score: float) -> None:
        self.visits += 1
        self.total_score += score

        if self.parent:
            self.parent.backprop(score)

    def add_child(self, col: int) -> Self:
        assert col < self.board.width, "Move outside of game"
        assert self.board.is_valid(col), "Invalid move"

        player_id = (
            self.player_owner.player_id
            if is_our_turn(self.abs_depth)
            else flip_player_turn[self.player_owner.player_id]
        )

        child = MCNode(self.board.get_new_board(col, player_id), self.player_owner, parent=self)
        self.children[col] = child

        return child


def select_random(node: MCNode) -> MCNode:
    return random.choice(list(node))


def upper_conf_bound(node: MCNode, exploration_c: float) -> MCNode:
    def UCB(n: MCNode) -> float:
        if n.visits == 0:
            return np.inf

        avg_reward = n.total_score / n.visits
        ucb_term = exploration_c * np.sqrt(np.log(n.parent.visits) / n.visits)

        return avg_reward + ucb_term

    best = max(node.children, key=lambda c: UCB(node.children[c]))
    return node.children[best]


class MCController(PlayerController):
    name = "Monte Carlo"

    def __init__(
        self,
        player_id: int,
        game_n: int,
        heuristic: Heuristic,
        selection_strat: Callable[[MCNode], MCNode],
        simulation_strat: Callable[[MCNode], MCNode] = select_random,
        time_s: float | None = None,
        n_iterations: int | None = None,
    ):

        assert (time_s is not None) ^ (n_iterations is not None), (
            "Must give either a max time or an n iterations (XOR)"
        )

        super().__init__(player_id, game_n, heuristic)

        self.time_s = time_s
        self.n_iterations = n_iterations

        self.selection_strat = selection_strat
        self.simulation_strat = simulation_strat

    def make_move(self, board: Board) -> int:
        def MC_iteration():
            # Select
            node = self.selection_strat(root.expand_tree(1))

            while not node.is_leaf and node.is_fully_expanded:
                node.expand_tree(1)

                node = self.selection_strat(node)

            # Expand
            if not node.is_terminal(self.heuristic, self.game_n):
                node.expand_tree(1)
                node = self.selection_strat(node)

            # Simulate
            playout_node = deepcopy(node)

            while not playout_node.is_terminal(self.heuristic, self.game_n):
                playout_node.expand_tree(1)

                playout_node = self.simulation_strat(playout_node)

            # Backprop
            winner = self.heuristic.winning(playout_node.board.get_board_state(), self.game_n)
            score = 1 if winner == self.player_id else 0.5 if winner == -1 else 0

            node.backprop(score)

        root = MCNode(board, self)
        assert not root.is_terminal(self.heuristic, self.game_n), (
            "Trying to MCTS from terminal node"
        )

        if self.time_s:
            start = time.perf_counter()

            while time.perf_counter() - start < self.time_s:
                MC_iteration()
        elif self.n_iterations:
            for _ in range(self.n_iterations):
                MC_iteration()

        return max(root.children, key=lambda c: root.children[c].visits)
