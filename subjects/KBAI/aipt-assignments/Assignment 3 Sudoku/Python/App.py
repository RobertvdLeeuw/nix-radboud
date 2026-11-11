import os

from Game import Game
from Sudoku import Sudoku

sudoku_folder = os.path.join(os.path.dirname(__file__), "Sudokus")


class App:
    @staticmethod
    def solve_sudoku(sudoku_file):
        game = Game(Sudoku(sudoku_file))
        game.show_sudoku()
        if game.solve() and game.valid_solution():
            print("Solved!")
        else:
            print("Could not solve this sudoku :(")

    @staticmethod
    def start():
        while True:
            type_input = input("[C]omplete or [i]ncomplete sudoku's: ")

            if type_input.lower().startswith("c"):
                sudoku_subfolder = "complete"
            elif type_input.lower().startswith("i"):
                sudoku_subfolder = "."
            else:
                print("Invalid selection, excepted [c]omplete or [i]ncomplete")
                continue

            type_input = input("[V]alid or [i]nvalid sudoku's: ")

            if type_input.lower().startswith("v"):
                sudoku_subfolder += "/."
            elif type_input.lower().startswith("i"):
                sudoku_subfolder += "/wrong"
            else:
                print("Invalid selection, excepted [v]alid or [i]nvalid")
                continue

            n_sudokus = 5 if sudoku_subfolder == "./." else 3
            file_num = input(f"Enter Sudoku file (1-{n_sudokus}): ")
            print("\n")

            file = None
            for filename in os.listdir(os.path.join(sudoku_folder, sudoku_subfolder)):
                if file_num in filename:
                    file = filename
            if file is not None:
                App.solve_sudoku(os.path.join(sudoku_folder, sudoku_subfolder, file))
            else:
                print("Invalid choice")

            continue_input = input("Continue? (yes/no): ")
            if not continue_input.lower().startswith("y"):
                break


if __name__ == "__main__":
    App.start()
