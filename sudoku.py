"""Sudoku solver."""

import sys
from typing import List
from itertools import product

"""
A default board can be added like this.

BOARD = [
    ["5", "3", ".", ".", "7", ".", ".", ".", "."],
    ["6", ".", ".", "1", "9", "5", ".", ".", "."],
    [".", "9", "8", ".", ".", ".", ".", "6", "."],
    ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
    ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
    ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
    [".", "6", ".", ".", ".", ".", "2", "8", "."],
    [".", ".", ".", "4", "1", "9", ".", ".", "5"],
    [".", ".", ".", ".", "8", ".", ".", "7", "9"],
] """

BOARD = [
    [".", ".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", "9", "8", ".", ".", ".", ".", "7"],
    [".", "8", ".", ".", "6", ".", ".", "5", "."],
    [".", "5", ".", ".", "4", ".", ".", "3", "."],
    [".", ".", "7", "9", ".", ".", ".", ".", "2"],
    [".", ".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", "2", "7", ".", ".", ".", ".", "9"],
    [".", "4", ".", ".", "5", ".", ".", "6", "."],
    ["3", ".", ".", ".", ".", "6", "2", ".", "."],
]


class Solution:
    """Calculate the solution for a sudoku board."""

    SHAPE = 9
    GRID = 3
    EMPTY = "."
    DIGITS = set([str(num) for num in range(1, SHAPE + 1)])

    def solve_sudoku(self, board: List[List[str]]) -> None:
        """Do not return anything, modify board in-place instead."""
        self.search(board)
        self.show(board)

    def show(self, board) -> None:
        """Print out the solved board."""
        top = "┌───┬───┬───┐"
        mid = "├───┼───┼───┤"
        bot = "└───┴───┴───┘"

        grid = [
            [top],
            [self.build_a_row(board[0])],
            [self.build_a_row(board[1])],
            [self.build_a_row(board[2])],
            [mid],
            [self.build_a_row(board[3])],
            [self.build_a_row(board[4])],
            [self.build_a_row(board[5])],
            [mid],
            [self.build_a_row(board[6])],
            [self.build_a_row(board[7])],
            [self.build_a_row(board[8])],
            [bot],
        ]
        for row in grid:
            print(row[0])

    def build_a_row(self, row: str) -> str:
        """Turn a row of numbers into a printable string."""
        row_char = "│"
        new_row = (
            row_char
            + row[0]
            + row[1]
            + row[2]
            + row_char
            + row[3]
            + row[4]
            + row[5]
            + row_char
            + row[6]
            + row[7]
            + row[8]
            + row_char
        )
        return new_row

    def is_valid_state(self, board) -> bool:
        """Check if it is a valid solution."""
        # validate all the rows
        for row in self.get_rows(board):
            if not set(row) == self.DIGITS:
                return False
        # validate columns
        for col in self.get_cols(board):
            if not set(col) == self.DIGITS:
                return False
        # validate sub-boxes
        for grid in self.get_grids(board):
            if not set(grid) == self.DIGITS:
                return False
        return True

    def get_candidates(self, board, row, col):
        """Return list of candidate values."""
        used_digits = set()
        # remove digits used by the same row
        used_digits.update(self.get_kth_row(board, row))
        # remove digits used by the same column
        used_digits.update(self.get_kth_col(board, col))
        # remove digits used by the 3x3 sub-box
        used_digits.update(self.get_grid_at_row_col(board, row, col))
        used_digits -= set([self.EMPTY])
        candidates = self.DIGITS - used_digits
        return candidates

    def search(self, board):
        """Recursive search method for finding solution."""
        if self.is_valid_state(board):
            return True  # found solution

        # find the next empty spot and take a guess
        for row_index, row in enumerate(board):
            for col_index, elm in enumerate(row):
                if elm == self.EMPTY:
                    # find candidates to construct the next state
                    for candidate in self.get_candidates(board, row_index, col_index):
                        board[row_index][col_index] = candidate
                        # recurse on the modified board
                        is_solved = self.search(board)
                        if is_solved:
                            return True
                        else:
                            # undo the wrong guess and start anew
                            board[row_index][col_index] = self.EMPTY
                    # exhausted all candidates
                    # but none solves the problem
                    return False
        # no empty spot
        return True

    # helper functions for retrieving rows, cols, and grids
    @staticmethod
    def get_kth_row(board, k):
        """Pull a particular row."""
        return board[k]

    def get_rows(self, board):
        """Return a board."""
        for i in range(self.SHAPE):
            yield board[i]

    def get_kth_col(self, board, k):
        """Pull out column k."""
        return [board[row][k] for row in range(self.SHAPE)]

    def get_cols(self, board):
        """Swap columns for rows."""
        for col in range(self.SHAPE):
            ret = [board[row][col] for row in range(self.SHAPE)]
            yield ret

    def get_grid_at_row_col(self, board, row, col):
        """Pull out particular row, col."""
        row = row // self.GRID * self.GRID
        col = col // self.GRID * self.GRID
        return [
            board[r][c]
            for r, c in product(
                range(row, row + self.GRID), range(col, col + self.GRID)
            )
        ]

    def get_grids(self, board):
        """Get the grids."""
        for row in range(0, self.SHAPE, self.GRID):
            for col in range(0, self.SHAPE, self.GRID):
                grid = [
                    board[r][c]
                    for r, c in product(
                        range(row, row + self.GRID), range(col, col + self.GRID)
                    )
                ]
                yield grid


def sudoku_load(file: str) -> List[List[str]]:
    """Read in sudoku file and load it into a board."""
    board = []
    with open(file, "r") as in_file:
        for line in in_file:
            if line[0] == "#":
                continue
            else:
                row = list(line.strip())
                board.append(row)

    return board


def main(files: list[str]) -> int:
    """Control reading sudoku files and solving them."""
    count = len(sys.argv)
    if count > 1:
        for i in range(1, count):
            print(f"\nSolving Sudoku file: {sys.argv[i]}")
            board = sudoku_load(sys.argv[i])
            solver = Solution()
            solver.solve_sudoku(board)
    else:
        print("\nSolving Built-in Sudoku board")
        solver = Solution()
        solver.solve_sudoku(BOARD)

    print("\nSudoku Solver Run Complete")
    return 0


if __name__ == "__main__":
    main(sys.argv)
