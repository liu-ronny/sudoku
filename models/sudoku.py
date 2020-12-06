from copy import deepcopy
from random import shuffle
from typing import List, Optional, Dict
from models.constants import *


class Sudoku:
    def __init__(self, board: Optional[List[List[int]]] = None):
        """Creates a Sudoku game from a 2d list representing the game state.

        :param board: a 2d list of integers representing Sudoku values
        """
        self._board = deepcopy(board) if board else deepcopy(EMPTY_BOARD)

        # keep track of the state of the board's units (rows, columns, and squares)
        self._row_vals = [set() for _ in range(ROWS)]
        self._col_vals = [set() for _ in range(COLS)]
        self._square_vals = [set() for _ in range(SQUARES)]

        # sync the state of the board and the unit structures
        for i in range(CELLS):
            row = get_row(i)
            col = get_col(i)
            self.add_to_board(i, self._board[row][col])

        # store the current state as the last saved state
        self.save()

    def get_board(self) -> List[List[int]]:
        """Returns the board corresponding to the state of the game.

        :return: the board as a 2d list
        """
        return self._board

    def get_candidate_vals(self, i: int) -> List[int]:
        """Returns the possible values for a given cell index in the board's current state. The values are shuffled and
        returned in a random order.

        :param i: a cell index between [0, CELLS - 1]
        :return: a list of possible values for the given cell index
        """
        row = get_row(i)
        col = get_col(i)
        square = get_square(i)

        row_candidates = {n for n in range(1, 10) if n not in self._row_vals[row]}
        col_candidates = {n for n in range(1, 10) if n not in self._col_vals[col]}
        square_candidates = {n for n in range(1, 10) if n not in self._square_vals[square]}

        # the set of valid values is the intersection of valid row, column, and square values
        candidate_vals = list(row_candidates & col_candidates & square_candidates)
        shuffle(candidate_vals)

        return candidate_vals

    def add_to_board(self, i: int, val: int) -> None:
        """Adds a value to the given cell index on the board.

        :param i: a cell index between [0, CELLS - 1]
        :param val: an integer value to add to the board
        :return: None
        """
        row = get_row(i)
        col = get_col(i)
        square = get_square(i)

        self._board[row][col] = val
        self._row_vals[row].add(val)
        self._col_vals[col].add(val)
        self._square_vals[square].add(val)

    def remove_from_board(self, i: int) -> int:
        """Removes the value from the given cell index on the board. If the value at the position is already empty, the
        board's state will remain the same.

        :param i: a cell index between [0, CELLS - 1]
        :return: the removed value
        """
        row = get_row(i)
        col = get_col(i)
        square = get_square(i)

        val = self._board[row][col]
        self._board[row][col] = EMPTY

        # only update the unit structures if there is a value to remove
        if val != EMPTY:
            self._row_vals[row].remove(val)
            self._col_vals[col].remove(val)
            self._square_vals[square].remove(val)

        return val

    def solve(self, i: Optional[int] = 0, skip_index: Optional[int] = None, skip_val: Optional[int] = None) -> bool:
        """Solves the board recursively starting from the given cell index.

        :param i: the cell index to start solving from
        :param skip_index: the cell index where the skip_val should not be used as a possible solution
        :param skip_val: a value to ignore as a possible solution at the given skip_index
        :return: True if the board is solvable from the given cell index, or False otherwise
        """
        # exit once there are no more cells to explore
        if i >= CELLS:
            return True

        row = get_row(i)
        col = get_col(i)
        original_val = self._board[row][col]

        # ignore any values that have already been filled
        if original_val != EMPTY:
            return self.solve(i + 1, skip_index, skip_val)

        candidate_vals = self.get_candidate_vals(i)
        self.remove_from_board(i)

        # try all candidate values for the current cell index, but skip any cell specified by the optional parameters
        for val in candidate_vals:
            if not (i == skip_index and val == skip_val):
                self.add_to_board(i, val)

                if self.solve(i + 1, skip_index, skip_val):
                    return True

                # backtrack if the attempt does not lead to a solution
                self.remove_from_board(i)

        self.add_to_board(i, original_val)
        return False

    def save(self) -> None:
        """Saves the current state of the board.

        :return: None
        """
        self._saved_board = deepcopy(self._board)
        self._saved_row_vals = deepcopy(self._row_vals)
        self._saved_col_vals = deepcopy(self._col_vals)
        self._saved_square_vals = deepcopy(self._square_vals)

    def restore(self) -> None:
        """Restores the last saved state of the board.

        :return: None
        """
        has_saved_state = self._saved_board and self._saved_row_vals and self._saved_col_vals and self._saved_square_vals

        if has_saved_state:
            self._board = deepcopy(self._saved_board)
            self._row_vals = deepcopy(self._saved_row_vals)
            self._col_vals = deepcopy(self._saved_col_vals)
            self._square_vals = deepcopy(self._saved_square_vals)

    @staticmethod
    def generate(remove_count: Optional[int] = EASY_COUNT) -> 'Sudoku':
        """Generates a random Sudoku puzzle.

        :param remove_count: the number of values to removed from the solution
        :return: a Sudoku instance representing the newly created puzzle
        """
        # create an empty game and solve it randomly
        sudoku = Sudoku()
        sudoku.solve()

        remaining_cells = [i for i in range(CELLS)]
        shuffle(remaining_cells)

        # remove up to the specified number of cells at random
        while remaining_cells and remove_count > 0:
            i = remaining_cells.pop()
            val = sudoku.remove_from_board(i)
            sudoku.save()

            # backtrack if removing val leads to multiple solutions
            has_multiple_solutions = sudoku.solve(0, i, val)
            sudoku.restore()

            if has_multiple_solutions:
                sudoku.add_to_board(i, val)
            else:
                remove_count -= 1

        return sudoku

    @classmethod
    def easy(cls) -> 'Sudoku':
        """Generates an "easy" Sudoku puzzle.

        :return: a randomly generated "easy" Sudoku
        """
        return cls.generate(EASY_COUNT)

    @classmethod
    def medium(cls) -> 'Sudoku':
        """Generates a "medium" Sudoku puzzle.

        :return: a randomly generated "medium" Sudoku
        """
        return cls.generate(MEDIUM_COUNT)

    @classmethod
    def hard(cls) -> 'Sudoku':
        """Generates a "hard" Sudoku puzzle.

        :return: a randomly generated "hard" Sudoku
        """
        return cls.generate(HARD_COUNT)


def get_row(i: int) -> int:
    """Returns the row index of a cell index.

    :param i: a cell index between [0, CELLS - 1]
    :return: the row index of the cell
    """
    return i // ROWS


def get_col(i: int) -> int:
    """Returns the column index of a cell index.

    :param i: a cell index between [0, CELLS - 1]
    :return: the column index of the cell
    """
    return i % COLS


def get_square(i: int) -> int:
    """Returns the square index of a cell index.

    :param i: a cell index between [0, CELLS - 1]
    :return: the square index of the cell
    """
    return (get_row(i) // N) * N + get_col(i) // N


def is_valid_solution(puzzle: List[List[int]], solution: List[List[int]]) -> bool:
    """Checks whether a given solution to a Sudoku puzzle is correct.

    :param puzzle: a 2d list of integers representing the puzzle
    :param solution: a 2d list of integers representing the solution
    :return: True if the solution is valid, or False otherwise
    """
    row_vals = [set() for _ in range(ROWS)]
    col_vals = [set() for _ in range(COLS)]
    square_vals = [set() for _ in range(SQUARES)]

    for row in range(ROWS):
        for col in range(COLS):
            square = (row // N) * N + col // N
            problem_val = puzzle[row][col]
            solution_val = solution[row][col]

            # check whether the solution value is a valid digit and whether it differs from the original value
            is_invalid = not (str(solution_val).isdigit() and 1 <= solution_val <= 9)
            is_altered = problem_val != EMPTY and problem_val != solution_val

            if is_invalid or is_altered:
                return False

            # check whether the solution value meets the constraints of a Sudoku solution
            is_duplicate = solution_val in row_vals[row] or solution_val in col_vals[col] or solution_val in square_vals[square]

            if is_duplicate:
                return False

            row_vals[row].add(solution_val)
            col_vals[col].add(solution_val)
            square_vals[square].add(solution_val)

    return True


def is_valid_puzzle(board: List[List[int]]) -> bool:
    """Checks whether a given board represents a valid Sudoku puzzle. This is useful for validating randomly generated
    puzzles.

    :param board: a 2d list of integers representing the board
    :return: True if the board is valid, or False otherwise
    """
    row_vals = [set() for _ in range(ROWS)]
    col_vals = [set() for _ in range(COLS)]
    square_vals = [set() for _ in range(SQUARES)]

    for row in range(ROWS):
        for col in range(COLS):
            val = board[row][col]
            square = (row // N) * N + col // N

            # check that non-empty values meet the constraints of Sudoku
            if val != EMPTY:
                if val in row_vals[row] or val in col_vals[col] or val in square_vals[square]:
                    return False

                row_vals[row].add(val)
                col_vals[col].add(val)
                square_vals[square].add(val)

    return True


def serialize_board(board: List[List[int]]) -> str:
    """Serializes a board into a string of 81 characters.

    :param board: a 2d list of integer values representing a Sudoku board
    :return: a compact representation of the input board
    """
    res = ""

    for row in range(ROWS):
        for col in range(COLS):
            val = board[row][col]

            if val == EMPTY:
                res += "."
            else:
                res += str(val)

    return res


def deserialize_board(board_str: str) -> List[List[int]]:
    """Deserializes a board into a 2d list representation.

    :param board_str: a 81 character representation of a Sudoku board
    :return: a 2d list representation of the input board
    """
    board = deepcopy(EMPTY_BOARD)

    for i, ch in enumerate(board_str):
        row = get_row(i)
        col = get_col(i)

        if ch == ".":
            val = EMPTY
        else:
            val = int(ch)

        board[row][col] = val

    return board


def load_puzzles() -> Dict[str, List[List[List[int]]]]:
    """Reads the Sudoku puzzles stored on disk and returns 2d list representations of them.

    :return: a dictionary of puzzles
    """
    puzzles = {"easy": [], "medium": [], "hard": []}

    for difficulty in puzzles.keys():
        with open(f"./puzzles/{difficulty}.txt") as serialized_puzzles:
            for puzzle in serialized_puzzles:
                board = deserialize_board(puzzle.strip())
                puzzles[difficulty].append(board)

    return puzzles
