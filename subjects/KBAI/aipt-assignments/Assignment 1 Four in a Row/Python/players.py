from __future__ import annotations

from abc import abstractmethod
from functools import partial, reduce
from typing import TYPE_CHECKING, Callable

import numpy as np

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


def is_our_turn(abs_depth: int, player_id: int) -> bool:
    return (abs_depth - player_id) % 2 == 0


flip_player_turn = {0: 0, 1: 2, 2: 1}


class MinMaxPlayer(PlayerController):
    """Class for the minmax player using the minmax algorithm
    Inherits from Playercontroller
    """

    def __init__(
        self, player_id: int, game_n: int, max_depth: int, heuristic: Heuristic, root_node: Node
    ) -> None:
        """
        Args:
            player_id (int): id of a player, can take values 1 or 2 (0 = empty)
            game_n (int): n in a row required to win
            depth (int): the max search depth
            heuristic (Heuristic): heuristic used by the player
        """
        super().__init__(player_id, game_n, heuristic)
        self.max_depth: int = max_depth
        self.tree: Node = root_node

    def make_move(self, board: Board) -> int:
        """Gets the column for the player to play in

        Args:
            board (Board): the current board

        Returns:
            int: column to play in
        """

        self.tree.expand_tree(self.max_depth, self.player_id)

        best_move = np.argmax(map(self.minimax, tree.children))

        # Moves tree by one, but keeps root ref alive via node.parent for abs_depth
        self.tree = self.tree.children[best_move]

        return best_move

    def minimax(self, node: Node) -> float:
        if node.is_leaf or node.is_terminal(self.heuristic, self.game_n):
            return self.heuristic.evaluate_board(self.player_id, node.board)

        eval_func = max if is_our_turn(node.abs_depth, self.player_id) else min

        best_eval = reduce(
            lambda best, node: eval_func(best, self.minimax(node)),
            node.children,
            -np.inf if is_our_turn(node.abs_depth, self.player_id) else np.inf,
        )

        return best_eval


class AlphaBetaPlayer(PlayerController):
    """Class for the minmax player using the minmax algorithm with alpha-beta pruning
    Inherits from Playercontroller
    """

    def __init__(
        self, player_id: int, game_n: int, max_depth: int, heuristic: Heuristic, root_node: Node
    ) -> None:
        """
        Args:
            player_id (int): id of a player, can take values 1 or 2 (0 = empty)
            game_n (int): n in a row required to win
            depth (int): the max search depth
            heuristic (Heuristic): heuristic used by the player
        """
        super().__init__(player_id, game_n, heuristic)
        self.max_depth: int = max_depth
        self.tree: Node = root_node

    def make_move(self, board: Board) -> int:
        """Gets the column for the player to play in

        Args:
            board (Board): the current board

        Returns:
            int: column to play in
        """
        # TODO: Reuse old tree, node.find_state -> root.find_state
        self.tree.expand_tree(self.max_depth, self.player_id)

        best_move = np.argmax(map(self.minimaxpruning, tree.children))

        # Moves tree by one, but keeps root ref alive via node.parent for abs_depth
        self.tree = self.tree.children[best_move]

        return best_move

    def minimaxpruning(self, node: Node, alpha=-np.inf, beta=np.inf):
        if node.is_leaf or node.is_terminal(self.heuristic, self.game_n):
            return self.heuristic.evaluate_board(self.player_id, board)

        our_turn = is_our_turn(node.abs_depth, self.player_id)
        eval_func = max if our_turn else min

        # Early termination in AB so we can't reduce :(
        best_eval = float("-inf") if our_turn else float("inf")

        # Must be faster to move child gen to in loop so we don't gen all (use early termination), but not gonna do that now.
        # node.expand_tree(1, self.player_id)

        for n in node.children:
            best_eval = eval_func(best_eval, self.minimaxpruning(n.board, alpha, beta))

            if our_turn:
                alpha = max(alpha, best_eval)
            else:
                beta = min(beta, best_eval)

            if beta <= alpha:
                break

        return best_eval


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
        children: dict[int, Node] | None = None,
        parent: Node | None = None,
    ):
        self.board = board
        self.children = children or {}  # col/move as int -> Node
        self.parent = parent

    @property
    def is_leaf(self) -> bool:
        return len(self.children) == 0

    @property
    def is_root(self) -> bool:
        return self.parent is None

    @property
    def root(self) -> Node:
        return self if self.is_root else self.parent.root

    @property
    def n(self) -> int:
        return 1 if self.is_leaf else sum(c.n for c in self)

    @property
    def abs_depth(self) -> int:
        return 0 if self.is_root else self.parent.abs_depth() + 1

    def is_terminal(self, heuristic: Heuristic, game_n: int = 4) -> bool:
        return heuristic.winning(board.get_board_state(), game_n) != 0

    def find_state(self, board: Board) -> Node | None:
        if self.board == board:
            return self

        if self.is_leaf:
            return None

        child_results = [c.find_state(board) for c in self]

        if any(child_results):
            return next(filter(bool, child_results))

    def add_child(self, col: int, player_id: int) -> Node:
        assert col < self.board.width, "Move outside of game"
        assert self.board.is_valid(col), "Invalid move"

        child = Node(self.board.get_new_board(col, player_id), parent=self)
        self.children[col] = child

        return self

    def expand_tree(self, depth: int, player_id: int) -> Node:
        # Fine for 4-in-a-row, not for Chess (explosion)

        if depth == 0:
            return self

        for col in range(self.board.width):
            if node := self.children[col]:
                node.expand_tree(depth - 1, flip_player_turn[player_id])
            else:
                self.add_child(col, player_id).expand_tree(depth - 1, not player_id)

        return self

    def __iter__(self):
        return iter(self.children.values())

    @property
    def is_fully_expanded(self) -> bool:
        return len(self.children) == self.board.width


class MCNode(Node):
    def __init__(self, board: Board, children: dict = None, parent: "Node" | None = None):
        super().__init__(board, children, parent)

        self.visits: int = 0
        self.total_score: float = 0

    def backprop(self, score: float) -> None:
        self.visits += 1
        self.total_score += score

        if self.parent:
            self.parent.backprop(score)

    def add_child(self, col: int, player_id: int) -> Node:
        assert col < self.board.width, "Move outside of game"
        assert self.board.is_valid(col), "Invalid move"

        child = MCNode(self.board.get_new_board(col, player_id), parent=self)
        self.children[col] = child

        return self


def select_random(node: MCNode) -> MCNode:
    return random.choice(list(node.children.values()))


def upper_conf_bound(node: MCNode, exploration_c: float) -> MCNode:
    def UCB(n: MCNode) -> float:
        avg_reward = n.total_score / n.visits
        ucb_term = exploration_c * np.sqrt(np.log(n.parent.visits) / n.visits)

        return avg_reward + ucb_term

    return max(node.children, key=lambda c: UCB(node.children[c]))


class MCController(PlayerController):
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

        self.selection_start = selection_strat
        self.simulation_strat = simulation_strat

    def make_move(self, board: Board) -> int:
        root = MCNode(board)

        def MC_iteration():
            # Select
            node = root

            while not node.is_leaf and node.is_fully_expanded:
                node = selection_strat(node)

            # Expand
            if not node.is_terminal(self.heuristic, self.game_n) and not node.is_fully_expanded:
                node.expand_tree(1, self.player_id)

            # Simulate
            while not node.is_terminal(self.heuristic, self.game_n):
                node.expand_tree(1, self.player_id)
                node = simulation_strat(node)

            # Backprop
            winner = player.heuristic.winning(node.board.get_board_state(), self.game_n)
            score = 1 if winner == self.player_id else 0.5 if winner == -1 else 0

            node.backprop(score)

        if self.time_s:
            start = time.perf_counter()

            while time.perf_counter() - start < self.time_s / 1000:
                MC_iteration()
        elif self.n_iterations:
            for _ in range(self.n_iterations):
                MC_iteration()

        return max(
            root.children, key=lambda c: root.children[c].total_score / root.children[c].visits
        )
