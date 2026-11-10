from copy import deepcopy
from functools import partial
from itertools import combinations

from Field import Field
from Sudoku import Sudoku

n_evals = 0


class EvalLimit(Exception):
    pass


def eval_count(func):
    def inner(*args):
        global n_evals

        n_evals += 1

        if n_evals >= 250_000:
            raise EvalLimit

        return func(*args)

    return inner


def get_eval_count() -> int:
    global n_evals
    return n_evals


# Usage: CONDITIONS[condition](b)(a). Set up this way for easy use with filter().
CONDITIONS = {"eq": lambda b: lambda a: a == b.value, "neq": lambda b: lambda a: a != b.value}


# Quick function to transpose 2D nested lists
def transpose(data: list[list]) -> list[list]:
    return list(zip(*data))


def construct_arcs(s: Sudoku) -> dict:
    """
    Generates arcs for a sukoku board.
    Returns as a dict with only keys for a quick ordered set.
    Each entry is a tuple: (field, condition, field | int).
    """

    arcs = {(a, "neq", b): None for row in s.board for a in row for b in a.get_neighbours()}

    arcs |= {
        # Already given (no need to mirror)
        (field, "eq", field.value): None
        for row in s.board
        for field in row
        if field.value != 0
    }

    # Quality check to catch faulty arcs quickly
    for a, cond, b in arcs:
        assert isinstance(a, Field), (
            f"Misformed arc: a is of type {type(a)}, a={a}, domain={getattr(a, 'domain', None)}"
        )

        assert cond in CONDITIONS, f"Misformed arc: invalid condition '{cond}'"

        assert isinstance(b, Field) or isinstance(b, int), (
            f"Misformed arc: b is of type {type(b)}, b={b}, domain={getattr(b, 'domain', None)}"
        )

    return arcs


def degree(field: Field) -> int:
    # Negative , so fields with more open n eig hbou rs get a lower score
    return -sum(1 for x in field.get_neighbours() if not x.is_finalized())


def pick_arc(agenda: dict, **heuristics) -> tuple:
    """
    Returns the next arc according to heuristics. Removes arc from the agenda.
    Without heuristics an arbitrary arc is taken
    """

    if all(not enabled for enabled in heuristics.values()):
        arc = next(iter(agenda))
        del agenda[arc]

        return arc

    def score_arc(arc: tuple, **heuristics) -> list:
        """
        Scores an arc based on the active heuristics. Lower scores means higher priority/ picked earlier.
        """
        a, _, b = arc
        score = []

        # Finalized score heuristic, 0 if b is finalized, 1 otherwise
        if heuristics.get("finalized", False):
            b_parsed = Field(b) if isinstance(b, int) else b
            score.append(not b_parsed.is_finalized())

        # Minimum remaining values heuristic, number of values left in domain
        if heuristics.get("mrv", False):
            score.append(len(a.domain))

        # Degree, number of open fields a is connected to
        if heuristics.get("degree", False):
            score.append(degree(a))

        return score

    arc = min(agenda, key=lambda arc: score_arc(arc, **heuristics))
    del agenda[arc]

    return arc


def pick_field(board: list[list[Field]], **heuristics) -> tuple[Field, int, int]:
    candidates = [
        (board[r][c], r, c) for r in range(9) for c in range(9) if not board[r][c].is_finalized()
    ]

    if heuristics.get("mrv", False):
        smallest_domain_size = min(len(f.domain) for f, _, _ in candidates)
        candidates = [c for c in candidates if len(c[0].domain) == smallest_domain_size]

    # Degree, number of open fields a is connected to
    if heuristics.get("degree", False):
        smallest_degree = min(degree(f) for f, _, _ in candidates)
        candidates = [c for c in candidates if degree(c[0]) == smallest_degree]

    return candidates[0]


def score_value(value: int, field: Field, **heuristics) -> list:
    score = []

    # Least Constraining Value: Number of unassigned peers that currently have `value` in their domain
    if heuristics.get("lcv", False):
        score.append(
            sum(1 for n in field.get_neighbours() if not n.is_finalized() and value in n.domain)
        )

    return score


def ac3_constrain(sudoku, **heuristics) -> bool:
    """
    Implementation of the AC-3 algorithm
    @return: true if the constraints can be satisfied, false otherwise
    """

    arcs = construct_arcs(sudoku)
    agenda = dict(arcs)

    while agenda:
        print(f"Iterations: {n_evals:,}", end="\r")
        a, cond, b = pick_arc(agenda, **heuristics)

        # Dummy fields around ints so we only need 1 processing func
        b_parsed = Field(b) if isinstance(b, int) else b

        # Condition, (effectively) curried on B and wrapped with eval incrementer
        arc_condition = eval_count(CONDITIONS[cond](b_parsed))

        a_conditioned = set(filter(arc_condition, a.domain))

        # No valid values for a (empty domain ergo no solution)
        if not a_conditioned:
            return False

        if diff := set(a.domain) - a_conditioned:
            for val in diff:
                a.remove_from_domain(val)

            agenda |= {(left, cond, right): None for (left, cond, right) in arcs if right is a}

    # Able to satisfy all constraints.
    return True


def backtrack(sudoku, **heuristics) -> Sudoku | None:
    """
    Returns a valid final solution if it exists within the outcome space. Returns None otherwise.
    """

    if sudoku.filled():
        # Already completely filled in
        return sudoku

    field, row_idx, col_idx = pick_field(sudoku.board, **heuristics)

    for value in sorted(field.domain, key=partial(score_value, field=field, **heuristics)):
        attempt = deepcopy(sudoku)

        # We have to edit exact same instance instead of replacing,
        # since arcs refer to this fields object id/specific instance.
        attempt_field = attempt.board[row_idx][col_idx]

        attempt_field.value = value
        attempt_field.domain = [value]

        if not ac3_constrain(attempt, **heuristics):
            continue

        # If assigning this value to this field leads to a valid solution:
        #   Fill try filling next field, eventually return final solution if reached
        if result := backtrack(attempt, **heuristics):
            return result

    # No values in domain were valid, ergo invalid solution
    return None


class Game:
    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku

        # Set neighbours
        for row in sudoku.board:
            for field in row:
                field.neighbours.extend(row)

        for col in transpose(sudoku.board):
            for field in col:
                field.neighbours.extend(col)

        for row_group in (sudoku.board[0:3], sudoku.board[3:6], sudoku.board[6:9]):
            for region in (
                transpose(row_group)[0:3],
                transpose(row_group)[3:6],
                transpose(row_group)[6:9],
            ):
                flattened = [field for col in region for field in col]
                for field in flattened:
                    field.neighbours.extend(flattened)

        # Deduplicate neighbors
        for row in sudoku.board:
            for field in row:
                field.neighbours = list(set(field.neighbours) - {field})

    def show_sudoku(self):
        print(self.sudoku)

    def solve(self, **heuristics) -> bool:
        global n_evals

        n_evals = 0

        if self.sudoku.filled():
            print("Passed an already completed sudoku, skipping AC-3")
            return self.valid_solution()

        if not ac3_constrain(self.sudoku, **heuristics):
            print(
                f"AC-3 couldn't find consistent solution, no solutions possible ({n_evals:,} evaluations)"
            )
            return False

        if self.sudoku.filled():
            print(f"AC-3 led to final solution, no space search needed ({n_evals:,} evaluations)")
            return True

        print(self.sudoku)

        print(f"Starting space search")
        solution = backtrack(self.sudoku, **heuristics)

        if not solution:
            print(f"Space search couldn't find solution ({n_evals:,} evaluations)")
            return False

        print(f"Space search led to solution ({n_evals:,} evaluations)")
        self.sudoku = solution

        return True

    def valid_solution(self) -> bool:
        """
        Checks the validity of a sudoku solution
        @return: true if the sudoku solution is correct
        """

        print(self.sudoku)

        if not self.sudoku.filled():
            return False

        # Same val twice in row?
        for row in self.sudoku.board:
            for a, b in combinations(range(9), 2):
                if row[a].value == row[b].value:
                    return False

        # Same val twice in col?
        for col in transpose(self.sudoku.board):
            for a, b in combinations(range(9), 2):
                if col[a].value == col[b].value:
                    return False

        # Same val twice in 3x3?
        for region_row in range(0, 9, 3):
            for region_col in range(0, 9, 3):
                vals = [
                    self.sudoku.board[r][c].value
                    for r in range(region_row, region_row + 3)
                    for c in range(region_col, region_col + 3)
                ]

                if len(set(vals)) != 9:
                    return False

        return True
