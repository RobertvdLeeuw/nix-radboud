from copy import deepcopy
from itertools import combinations

from Field import Field
from Sudoku import Sudoku

n_evals = 0


def eval_count(func):
    def inner(*args):
        global n_evals

        n_evals += 1
        return func(*args)

    return inner


# Usage: CONDITIONS[condition](b)(a). Set up this way for easy use with filter().
CONDITIONS = {"eq": lambda b: lambda a: a == b.value, "neq": lambda b: lambda a: a != b.value}


# Quick function to transpose 2D nested lists
def transpose(data: list[list]) -> list[list]:
    return list(zip(*data))


def construct_arcs(s: Sudoku) -> set[tuple]:
    """
    Generates arcs for a sukoku board. Returns as a set.
    Each entry is a tuple: (field, condition, field | int).
    """

    arcs = {(a, "neq", b) for row in s.board for a, b in combinations(row, 2)}  # Rows
    arcs |= {(a, "neq", b) for col in transpose(s.board) for a, b in combinations(col, 2)}  # Cols

    # Mirror versions
    arcs |= {(b, cond, a) for (a, cond, b) in arcs}

    # 3x3's (No need to mirror since we're looping over every field)
    arcs |= {(a, "neq", b) for row in s.board for a in row for b in a.get_neighbours()}

    arcs |= {
        # Already given (no need to mirror)
        (field, "eq", field.value)
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


def pick_field(board: list[list[Field]]) -> tuple[Field, int, int]:
    for r, row in enumerate(board):
        for c, field in enumerate(row):
            if field.value == 0:
                return field, r, c

    # return random.choice(filtered)


def pick_value(field: Field) -> int:
    return 1


def ac3_constrain(sudoku) -> bool:
    """
    Implementation of the AC-3 algorithm
    @return: true if the constraints can be satisfied, false otherwise
    """

    arcs = construct_arcs(sudoku)
    agenda = set(arcs)

    while agenda:
        a, cond, b = agenda.pop()

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

            agenda |= {(left, cond, right) for (left, cond, right) in arcs if a is right}

    # Able to satisfy all constraints.
    return True


def backtrack(sudoku) -> Sudoku | None:
    """
    Returns a valid final solution if it exists within the outcome space. Returns None otherwise.
    """

    if sudoku.filled():
        # Already completely filled in
        return sudoku

    field, row_idx, col_idx = pick_field(sudoku.board)

    for value in sorted(field.domain, key=pick_value, reverse=False):
        attempt = deepcopy(sudoku)

        # We have to edit exact same instance instead of replacing,
        # since arcs refer to this fields object id/specific instance.
        attempt_field = attempt.board[row_idx][col_idx]

        attempt_field.value = value
        attempt_field.domain = [value]

        if not ac3_constrain(attempt):
            continue

        # If assigning this value to this field leads to a valid solution:
        #   Fill try filling next field, eventually return final solution if reached
        if result := backtrack(attempt):
            return result

    # No values in domain were valid, ergo invalid solution
    return None


class Game:
    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku

        # Set neighbours
        for row_group in (sudoku.board[0:3], sudoku.board[3:6], sudoku.board[6:9]):
            for region in (
                transpose(row_group)[0:3],
                transpose(row_group)[3:6],
                transpose(row_group)[6:9],
            ):
                flattened = [field for col in region for field in col]
                for i in range(9):
                    flattened[i].set_neighbours(flattened[:i] + flattened[i + 1 :])

    def show_sudoku(self):
        print(self.sudoku)

    def solve(self) -> bool:
        global n_evals

        n_evals = 0

        if self.sudoku.filled():
            print("Passed an already completed sudoku, skipping AC-3")
            return self.valid_solution()

        if not ac3_constrain(self.sudoku):
            print(
                f"AC-3 couldn't find consistent solution, no solutions possible ({n_evals:,} evalutations)"
            )
            return False

        if self.sudoku.filled():
            print(f"AC-3 led to final solution, no space search needed ({n_evals:,} evalutations)")
            return True

        print(self.sudoku)

        print(f"Starting space search")
        solution = backtrack(self.sudoku)

        if not solution:
            print(f"Space search couldn't find solution ({n_evals:,} evalutations)")
            return False

        print(f"Space search led to solution ({n_evals:,} evalutations)")
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
        for row in self.sudoku.board[::3]:
            for a in row[::3]:
                for b in a.get_neighbours():
                    if a.value == b.value:
                        return False

        return True
