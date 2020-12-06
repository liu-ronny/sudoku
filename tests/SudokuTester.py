from unittest import TestCase, main
from models.constants import *
from models.sudoku import Sudoku, is_valid_puzzle, is_valid_solution, load_puzzles


class PuzzleValidatorTester(TestCase):
    def test_empty_board(self):
        self.assertTrue(is_valid_puzzle(EMPTY_BOARD))

    def test_valid_partial_board(self):
        e = EMPTY
        board = [
            [5, 3, 4, 6, e, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, e, 8, 3, 4, 2, e, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, e, 7, 9, 1],
            [7, 1, e, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, e, 9, 6, 3, 5],
            [e, 4, 5, 2, 8, 6, 1, 7, e]
        ]
        self.assertTrue(is_valid_puzzle(board))

    def test_valid_rows(self):
        e = EMPTY
        board = [
            [5, 3, 4, 6, e, 8, 9, 1, 2],
            [e, e, e, e, e, e, e, e, e],
            [e, e, e, e, e, e, e, e, e],
            [e, e, e, e, e, e, e, e, e],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [e, e, e, e, e, e, e, e, e],
            [e, e, e, e, e, e, e, e, e],
            [e, e, e, e, e, e, e, e, e],
            [e, e, e, e, e, e, e, e, e]
        ]
        self.assertTrue(is_valid_puzzle(board))

    def test_valid_cols(self):
        e = EMPTY
        board = [
            [5, 3, 4, 6, e, 8, 9, 1, 2],
            [1, e, e, e, e, e, e, e, e],
            [6, e, e, e, e, e, e, e, e],
            [4, e, e, e, e, e, e, e, e],
            [e, 2, 3, 4, 5, 6, 7, 8, 9],
            [8, e, e, e, e, e, e, e, e],
            [9, e, e, e, e, e, e, e, e],
            [3, e, e, e, e, e, e, e, e],
            [2, e, e, e, e, e, e, e, e]
        ]
        self.assertTrue(is_valid_puzzle(board))

    def test_valid_squares(self):
        e = EMPTY
        board = [
            [1, 2, 3, e, e, e, e, e, e],
            [4, 5, 6, e, e, e, e, e, e],
            [7, 8, 9, e, e, e, e, e, e],
            [e, e, e, 1, 2, 3, e, e, e],
            [e, e, e, 4, 5, 6, e, e, e],
            [e, e, e, 7, 8, 9, e, e, e],
            [e, e, e, e, e, e, 1, 2, 3],
            [e, e, e, e, e, e, 4, 5, 6],
            [e, e, e, e, e, e, 7, 8, 9]
        ]
        self.assertTrue(is_valid_puzzle(board))

    def test_invalid_partial_board(self):
        e = EMPTY
        board = [
            [5, 3, 4, 6, e, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, e, 8, 3, 4, 2, e, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, e, 7, 9, 1],
            [7, 1, e, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, e, 9, 6, 2, 5],    # duplicate 2 on this row
            [e, 4, 5, 2, 8, 6, 1, 7, e]
        ]
        self.assertFalse(is_valid_puzzle(board))

    def test_invalid_row(self):
        e = EMPTY
        board = [
            [e, 3, 4, 6, e, 8, 9, 1, 2],
            [6, 7, e, e, e, 5, 5, 4, 8],    # duplicate 5 on this row
            [1, e, 8, 3, 4, 2, e, 6, 7],
            [e, 5, 9, e, 6, 1, 4, 2, 3],
            [4, e, 6, 8, 5, e, e, 9, 1],
            [7, 1, e, e, 2, 4, e, 5, 6],
            [9, e, 1, e, 3, 7, e, 8, 4],
            [2, 8, 7, 4, e, 9, e, 3, 5],
            [e, 4, e, e, 8, 6, e, 7, e]
        ]
        self.assertFalse(is_valid_puzzle(board))

    def test_invalid_col(self):
        e = EMPTY

        # duplicate 2 on column 1
        board = [
            [e, 3, 4, 6, e, 8, 9, 1, 2],
            [6, 7, e, e, e, 5, 3, 4, 8],
            [1, e, 8, 3, 4, 2, e, 6, 7],
            [e, 5, 9, e, 6, 1, 4, 2, 3],
            [2, e, 6, 8, 5, e, e, 9, 1],
            [7, 1, e, e, 2, 4, e, 5, 6],
            [9, e, 1, e, 3, 7, e, 8, 4],
            [2, 8, 7, 4, e, 9, e, 3, 5],
            [e, 4, e, e, 8, 6, e, 7, e]
        ]
        self.assertFalse(is_valid_puzzle(board))

    def test_invalid_square(self):
        e = EMPTY

        # duplicate 1 on square 1
        board = [
            [e, 3, 4, 6, e, 8, 9, 1, 2],
            [6, 1, e, e, e, 5, 3, 4, 8],
            [1, e, 8, 3, 4, 2, e, 6, 7],
            [e, 5, 9, e, 6, 1, 4, 2, 3],
            [2, e, 6, 8, 5, e, e, 9, 1],
            [7, e, e, e, 2, 4, e, 5, 6],
            [9, e, 1, e, 3, 7, e, 8, 4],
            [2, 8, 7, 4, e, 9, e, 3, 5],
            [e, 4, e, e, 8, 6, e, 7, e]
        ]
        self.assertFalse(is_valid_puzzle(board))

    def test_valid_full_board(self):
        board = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]
        self.assertTrue(is_valid_puzzle(board))


class SolutionValidatorTester(TestCase):
    def test_valid_solution(self):
        e = EMPTY
        puzzle = [
            [5, 3, e, e, 7, e, 9, 1, 2],
            [6, e, 2, 1, 9, 5, e, 4, 8],
            [e, 9, e, e, e, 2, 5, e, 7],
            [8, 5, e, 7, 6, 1, 4, 2, 3],
            [e, 2, 6, 8, e, 3, e, e, 1],
            [7, e, 3, e, 2, 4, 8, 5, 6],
            [e, e, e, 5, e, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, e, e, e, e],
            [3, e, 5, e, 8, e, e, e, e]
        ]
        solution = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]
        self.assertTrue(is_valid_solution(puzzle, solution))

    def test_incomplete_solution(self):
        e = EMPTY
        puzzle = [
            [5, 3, e, e, 7, e, 9, 1, 2],
            [6, e, 2, 1, 9, 5, e, 4, 8],
            [e, 9, e, e, e, 2, 5, e, 7],
            [8, 5, e, 7, 6, 1, 4, 2, 3],
            [e, 2, 6, 8, e, 3, e, e, 1],
            [7, e, 3, e, 2, 4, 8, 5, 6],
            [e, e, e, 5, e, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, e, e, e, e],
            [3, e, 5, e, 8, e, e, e, e]
        ]
        solution = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, e, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, e]
        ]
        self.assertFalse(is_valid_solution(puzzle, solution))
        
    def test_complete_but_altered_solution(self):
        e = EMPTY
        puzzle = [
            [5, 3, e, e, 7, e, 9, 1, 2],
            [6, e, 2, 1, 9, 5, e, 4, 8],
            [e, 9, e, e, e, 2, 5, e, 7],
            [8, 5, e, 7, 6, 1, 4, 2, 3],
            [e, 2, 6, 8, e, 3, e, e, 1],
            [7, e, 3, e, 2, 4, 8, 5, 6],
            [e, e, e, 5, e, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, e, e, e, e],
            [3, e, 5, e, 8, e, e, e, e]
        ]
        solution = [
            [3, 5, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 3, 5, 4, 8],
            [1, 9, 8, 5, 4, 2, 3, 6, 7],
            [8, 3, 9, 7, 6, 1, 4, 2, 5],
            [4, 2, 6, 8, 3, 5, 7, 9, 1],
            [7, 1, 5, 9, 2, 4, 8, 3, 6],
            [9, 6, 1, 3, 5, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 5, 3],
            [5, 4, 3, 2, 8, 6, 1, 7, 9]
        ]
        self.assertTrue(is_valid_puzzle(solution))
        self.assertFalse(is_valid_solution(puzzle, solution))

    def test_invalid_solution(self):
        e = EMPTY
        puzzle = [
            [5, 3, e, e, 7, e, 9, 1, 2],
            [6, e, 2, 1, 9, 5, e, 4, 8],
            [e, 9, e, e, e, 2, 5, e, 7],
            [8, 5, e, 7, 6, 1, 4, 2, 3],
            [e, 2, 6, 8, e, 3, e, e, 1],
            [7, e, 3, e, 2, 4, 8, 5, 6],
            [e, e, e, 5, e, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, e, e, e, e],
            [3, e, 5, e, 8, e, e, e, e]
        ]
        solution = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 7, 1, 7, 9]     # duplicate 7 in this row
        ]
        self.assertFalse(is_valid_solution(puzzle, solution))


class SolverTester(TestCase):
    def test_solver(self):
        e = EMPTY
        puzzle = [
            [5, 3, e, e, 7, e, 9, 1, 2],
            [6, e, 2, 1, 9, 5, e, 4, 8],
            [e, 9, e, e, e, 2, 5, e, 7],
            [8, 5, e, 7, 6, 1, 4, 2, 3],
            [e, 2, 6, 8, e, 3, e, e, 1],
            [7, e, 3, e, 2, 4, 8, 5, 6],
            [e, e, e, 5, e, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, e, e, e, e],
            [3, e, 5, e, 8, e, e, e, e]
        ]
        sudoku = Sudoku(puzzle)
        sudoku.solve()
        solution = sudoku.get_board()
        self.assertTrue(is_valid_solution(puzzle, solution))

    def test_solver_with_generated_puzzles(self):
        puzzles = load_puzzles()

        for puzzle_list in puzzles.values():
            for puzzle in puzzle_list[:3]:
                sudoku = Sudoku(puzzle)
                sudoku.solve()
                solution = sudoku.get_board()
                self.assertTrue(is_valid_solution(puzzle, solution))


if __name__ == "__main__":
    main()
