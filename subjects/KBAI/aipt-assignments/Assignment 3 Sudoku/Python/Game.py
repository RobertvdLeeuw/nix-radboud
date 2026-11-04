from copy import deepcopy
from itertools import combinations

from Field import Field
from Sudoku import Sudoku

CONDITIONS = {"eq": lambda b: lambda a: a == b.value, "neq": lambda b: lambda a: a != b.value}


def transpose(data: list[list]) -> list[list]:
    return list(zip(*data))


def construct_arcs(s: Sudoku) -> set[tuple]:
    arcs = {(a, "neq", b) for row in s.board for a, b in combinations(row, 2)}  # Rows
    arcs |= {(a, "neq", b) for col in zip(*s.board) for a, b in combinations(col, 2)}  # Cols

    arcs |= {(a, "neq", b) for row in s.board for a in row for b in a.get_neighbours()}  # 3x3's

    # Mirror versions
    arcs |= {(b, cond, a) for (a, cond, b) in arcs}

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
        """
        Implementation of the AC-3 algorithm
        @return: true if the constraints can be satisfied, false otherwise
        """
        arcs = construct_arcs(self.sudoku)
        agenda = set(arcs)

        while agenda:
            a, cond, b = agenda.pop()

            # Dummy fields around ints so we only need 1 processing func
            b_parsed = Field(b) if isinstance(b, int) else b

            a_conditioned = list(filter(CONDITIONS[cond](b_parsed), a.domain))

            if diff := [val for val in a.domain if val not in a_conditioned]:
                for val in diff:
                    a.remove_from_domain(val)

                agenda |= {(left, cond, right) for (left, cond, right) in arcs if a == right}

        return True

    def valid_solution(self) -> bool:
        """
        Checks the validity of a sudoku solution
        @return: true if the sudoku solution is correct
        """

        print(self.sudoku)

        for row_idx, row in enumerate(self.sudoku.board):
            for col_idx, field in enumerate(row):
                if field.value == 0:
                    print(f"({row_idx}, {col_idx}) not filled in")
                    return False

        for row_idx, row in enumerate(self.sudoku.board):
            for a, b in combinations(range(len(row)), 2):
                if row[a].value == row[b].value:
                    print(f"Row {row_idx}: fields {a} and {b} share value {row[a].value}")
                    return False

        for col_idx, col in enumerate(transpose(self.sudoku.board)):
            for a, b in combinations(range(len(col)), 2):
                if col[a].value == col[b].value:
                    print(f"Col {col_idx}: fields {a} and {b} share value {col[a].value}")
                    return False

        for row_idx, row in enumerate(self.sudoku.board):
            for col_idx, a in enumerate(row):
                for b in a.get_neighbours():
                    if a.value == b.value:
                        print(
                            f"Value at ({row_idx}, {col_idx}) shares value {a.value} with other cell in 3x3 region"
                        )
                        return False

        return True
