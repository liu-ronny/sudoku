from models.sudoku import load_puzzles
from random import randint
from typing import List, Dict

puzzles = load_puzzles()


def rand_puzzle(difficulty: str) -> Dict[str, List[List[int]]]:
    """Returns a random puzzle with the specified difficulty.

    :param difficulty: one of 'easy', 'medium', or 'hard'
    :return: a 2d list
    """
    options = puzzles[difficulty]
    rand_i = randint(0, len(options) - 1)
    return {'puzzle': options[rand_i]}
