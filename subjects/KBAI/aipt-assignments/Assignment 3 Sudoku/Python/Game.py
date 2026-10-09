from itertools import combinations

from Field import Field

CONDITIONS = {"eq": lambda b: lambda a: a == b.value, "neq": lambda b: lambda a: a != b.value}


def construct_arcs(s: Sudoku) -> set[tuple]:
    arcs = {
        # Rows
        *[(a, "neq", b) for _, row in s.board for a, b in combinations(row, 2)],
        # Cols
        *[(a, "neq", b) for _, col in zip(*s.board) for a, b in combinations(col, 2)],
        # 3x3's
        *[
            (a, "neq", b)
            for _, row_group in (s.board[0:3], s.board[3:6], s.board[6:9])
            for _, group in (row_group[0:3], row_group[3:6], row_group[6:9])
            for a, b in combinations(group, 2)
        ],
    }

    # Mirror versions
    arcs |= {(b, cond, a) for (a, cond, b) in arcs}

    arcs |= {
        # Already given (no need to mirror)
        (field, "eq", field.value)
        for _, row in s.board
        for _, field in row
        if field.value != 0
    }

    return arcs


class Game:
    def __init__(self, sudoku):
        self.sudoku = sudoku

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
        # TODO: implement valid_solution function
        return False
