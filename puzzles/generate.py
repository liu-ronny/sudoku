from sys import argv
from models.sudoku import Sudoku, serialize_board


def print_error_msg(msg: str) -> None:
    """Prints an error message describing the source of the error.

    :param msg: a string describing the source of the error.
    :return: None
    """
    print(msg)
    print("Usage: generate.py <difficulty: 'easy' | 'medium' | 'hard'> <count>")


def generate_puzzles() -> None:
    """Randomly generates puzzles based on the difficulty given as a command line argument.

    :return: None
    """
    # check whether the number of arguments is valid
    if len(argv) != 3:
        print_error_msg("Invalid number of arguments")
        return

    difficulty = argv[1].lower()

    # validate the given count
    try:
        count = int(argv[2])

        if count < 1:
            print_error_msg("The specified count must be >= 1")
            return
    except ValueError:
        print_error_msg("The specified count must be an integer")
        return

    # select a generator method based on the given difficulty
    if difficulty == "easy":
        generate_puzzle = Sudoku.easy
    elif difficulty == "medium":
        generate_puzzle = Sudoku.medium
    elif difficulty == "hard":
        generate_puzzle = Sudoku.hard
    else:
        print_error_msg("The specified difficulty must be one of 'easy', 'medium', or 'hard'")
        return

    # write the requested number of puzzles into the appropriate text file
    with open(f"{difficulty}.txt", "w") as puzzles:
        for i in range(count):
            puzzle = generate_puzzle()
            puzzles.write(f"{serialize_board(puzzle.get_board())}\n")


if __name__ == "__main__":
    generate_puzzles()
