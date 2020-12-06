from flask import Flask, request, render_template
from models.sudoku import Sudoku, is_valid_solution
from app.puzzles import rand_puzzle

app = Flask(__name__)


@app.route('/')
def test():
    return render_template('index.html')


@app.route('/puzzles/random')
def random_puzzle():
    difficulty = request.args.get('difficulty', '').lower()
    difficulties = {'easy', 'medium', 'hard'}

    if not difficulty:
        return 'Difficulty not specified', 400

    if difficulty not in difficulties:
        return "The specified difficulty must be one of 'easy', 'medium', or 'hard'", 400

    return rand_puzzle(difficulty)


@app.route('/puzzles/solution_valid', methods=['POST'])
def solution_valid():
    body = request.get_json()
    puzzle = body.get('puzzle', None)
    solution = body.get('solution', None)

    if not puzzle:
        return 'Puzzle not provided', 400

    if not solution:
        return 'Solution not provided', 400

    try:
        is_valid = is_valid_solution(puzzle, solution)
        return {'result': is_valid}
    except:
        return 'Invalid format', 400


@app.route('/puzzles/solution', methods=['POST'])
def solution():
    body = request.get_json()
    puzzle = body.get('puzzle', None)

    if not puzzle:
        return 'Puzzle not provided', 400

    try:
        sudoku = Sudoku(puzzle)
        sudoku.solve()
        return {'solution': sudoku.get_board()}
    except:
        return 'Invalid format', 400
