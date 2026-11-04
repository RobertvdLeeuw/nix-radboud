from copy import deepcopy
from itertools import combinations

from Field import Field
from Sudoku import Sudoku

CONDITIONS = {"eq": lambda b: lambda a: a == b.value, "neq": lambda b: lambda a: a != b.value}


def transpose(data: list[list]) -> list[list]:
    return list(zip(*data))


def construct_arcs(s: Sudoku) -> set[tuple]:
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

    for a, cond, b in arcs:
        assert isinstance(a, Field), (
            f"Misformed arc: a is of type {type(a)}, a={a}, domain={getattr(a, 'domain', None)}"
        )

        assert cond in CONDITIONS, f"Misformed arc: invalid condition '{cond}'"

        assert isinstance(b, Field) or isinstance(b, int), (
            f"Misformed arc: b is of type {type(b)}, b={b}, domain={getattr(b, 'domain', None)}"
        )

    return arcs


import random


def pick_field(board: list[list[Field]]) -> tuple[Field, int, int]:
    for r, row in enumerate(board):
        for c, field in enumerate(row):
            if field.value == 0:
                return field, r, c

    # return random.choice(filtered)


def pick_value(field: Field) -> int:
    return 1


def ac3_constrain(sudoku, print_reason=False) -> bool:
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

        a_conditioned = list(filter(CONDITIONS[cond](b_parsed), a.domain))

        # No valid values for a (empty domain ergo no solution)
        if not a_conditioned:
            if print_reason:
                print(f"Empty domain, {repr(a)} -({cond} {b})-> {a_conditioned}")
            return False

        if diff := [val for val in a.domain if val not in a_conditioned]:
            for val in diff:
                a.remove_from_domain(val)

            agenda |= {(left, cond, right) for (left, cond, right) in arcs if a is right}

    if print_reason:
        print("Arc consistent")

    return True


def backtrack(sudoku, print_reason=False) -> Sudoku | None:
    """
    Returns a valid final solution if it exists within the outcome space. Returns None otherwise.
    """

    sudoku = deepcopy(sudoku)

    if sudoku.filled():
        # Already completely filled in
        return sudoku

    field, row_idx, col_idx = pick_field(sudoku.board)

    for value in sorted(field.domain, key=pick_value, reverse=False):
        attempt = deepcopy(sudoku)

        attempt_field = attempt.board[row_idx][col_idx]

        attempt_field.value = value
        attempt_field.domain = [value]

        if not ac3_constrain(attempt):
            continue

        # If assigning this value to this field leads to a valid solution, break and return
        if result := backtrack(attempt):
            return result

    # No values in domain were valid, ergo invalid solution
    return None


class Game:
    def __init__(self, sudoku):
        self.sudoku = sudoku

        # Set neighbours
        for row_group in (sudoku.board[0:3], sudoku.board[3:6], sudoku.board[6:9]):
            for group in (
                transpose(row_group)[0:3],
                transpose(row_group)[3:6],
                transpose(row_group)[6:9],
            ):
                flattened = [field for col in group for field in col]
                for i in range(9):
                    flattened[i].set_neighbours(flattened[:i] + flattened[i + 1 :])

    def show_sudoku(self):
        print(self.sudoku)

    def solve(self) -> bool:
        if not ac3_constrain(self.sudoku, print_reason=True):
            print("AC-3 couldn't find consistent solution, no solutions possible")
            return False

        if self.sudoku.filled():
            print("AC-3 led to final solution, no space search needed")
            return True

        print(self.sudoku)

        print("Starting space search")
        solution = backtrack(self.sudoku, print_reason=True)

        if not solution:
            print("Space search couldn't find solution")
            return False

        print("Space search led to solution")
        self.sudoku = solution
        return True

    def valid_solution(self, print_reason=False) -> bool:
        """
        Checks the validity of a sudoku solution
        @return: true if the sudoku solution is correct
        """

        if print_reason:
            print(self.sudoku)

        if not self.sudoku.filled(print_reason):
            return False

        for row_idx, row in enumerate(self.sudoku.board):
            for a, b in combinations(range(len(row)), 2):
                if row[a].value != row[b].value:
                    continue

                if print_reason:
                    print(f"Row {row_idx + 1}: fields {a} and {b} share value {row[a].value}")

                return False

        for col_idx, col in enumerate(transpose(self.sudoku.board)):
            for a, b in combinations(range(len(col)), 2):
                if col[a].value != col[b].value:
                    continue

                if print_reason:
                    print(f"Col {col_idx + 1}: fields {a} and {b} share value {col[a].value}")

                return False

        for row_idx, row in enumerate(self.sudoku.board):
            for col_idx, a in enumerate(row):
                for b in a.get_neighbours():
                    if a.value != b.value:
                        continue

                    if print_reason:
                        print(
                            f"Value at ({row_idx + 1}, {col_idx + 1}) shares value {a.value} with other cell in 3x3 region"
                        )

                    return False

        return True
