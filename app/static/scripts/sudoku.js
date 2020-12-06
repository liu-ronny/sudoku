$(document).ready(() => {
    const board = $('#board');
    const cells = $('.cell');
    const spinner = $('#spinner');
    const spinnerMsg = $('#spinner-msg');
    const success = $('#success');
    const failure = $('#failure');
    let difficulty = $('#difficulty');
    let puzzle;
    let solved = false;
    let focusedCell;
    const EMPTY = -1;
    const PLACEHOLDER = '0';
    const ROWS = 9;
    const COLS = 9;
    const N = 3;
    const CELLS = 81;
    const SQUARES = {};

    const calculateSquares = () => {
        for (let i = 0; i < ROWS; i++) {
            SQUARES[i] = [];
        }

        for (let i = 0; i < CELLS; i++) {
            const row = Math.floor(i / ROWS);
            const col = Math.floor(i % COLS);
            const square = Math.floor(row / N) * N + Math.floor(col / N)

            SQUARES[square].push(`#${row}-${col}`);
        }
    }

    const showBoard = () => {
        board.css('visibility', 'visible');
    }

    const hideBoard = () => {
        board.css('visibility', 'hidden');
    }

    const clearBoard = () => {
        cells.text(PLACEHOLDER);
        cells.css('color', 'var(--black)');
        cells.css('background-color', '');
    }

    const showSpinner = (color) => {
        spinner.css('border', `2px solid var(--${color})`);
        spinner.css('color', `var(--${color})`);
        spinner.css('visibility', 'visible');
    }

    const hideSpinner = () => {
        spinner.css('visibility', 'hidden');
    }

    const showSuccess = () => {
        success.css('visibility', 'visible');
    }

    const hideSuccess = () => {
        success.css('visibility', 'hidden');
    }

    const showFailure = () => {
        failure.css('visibility', 'visible');
    }

    const hideFailure = () => {
        failure.css('visibility', 'hidden');
    }

    const resetStatus = () => {
        solved = false;
        hideSuccess();
    }

    const showLoadingStatus = (msg = 'Loading', color = 'pink') => {
        spinnerMsg.text(msg);
        hideBoard();
        showSpinner(color);
        clearBoard();
    }

    const hideLoadingStatus = (timeout = 1000) => {
        resizeCells();
        setTimeout(() => {
            hideSpinner();
            showBoard();
        }, timeout)
    }

    const setBorders = () => {
        const squareRows = ['.r-2', '.r-5', '.r-8'];
        const squareCols = ['.c-2', '.c-5', '.c-8'];

        for (let squareRow of squareRows) {
            $(`${squareRow}`).each((i, ele) => {
                ele.style.setProperty('border-bottom-width', '2px', 'important');
            })
        }

        for (let squareCol of squareCols) {
            $(`${squareCol}`).each((i, ele) => {
                ele.style.setProperty('border-right-width', '2px', 'important');
            })
        }

        for (let row = 0; row < ROWS; row++) {
            $(`#${row}-0`)[0].style.setProperty('border-left-width', '2px', 'important');
        }

        for (let col = 0; col < COLS; col++) {
            $(`#0-${col}`)[0].style.setProperty('border-top-width', '2px', 'important');
        }
    }

    const resizeCells = () => {
        cells.each(function() {
            const cell = $(this);
            const height = cell.height();
            const width = cell.width();

            if (height > width) {
                cell.width(height);
            } else {
                cell.height(width);
            }
        })
    }

    const dynamicallyResizeCells = () => {
        $(window).resize(() => {
            resizeCells();
        });

        resizeCells();
    }

    const dynamicallyUpdateDifficulty = () => {
        $('.difficulty-option').on('click', function() {
            difficulty.text($(this).text())
        });
    }

    const highlightUnits = (cell) => {
        const id = cell.attr('id');
        const [row, col] = id.split('-');
        const square = Math.floor(row / N) * N + Math.floor(col / N)

        cells.css('background-color', '');
        $(`.r-${row}`).css('background-color', 'var(--light-beige)');
        $(`.c-${col}`).css('background-color', 'var(--light-beige)');

        for (let cell of SQUARES[square]) {
            $(`${cell}`).css('background-color', 'var(--light-beige)');
        }

        cell.css('background-color', 'var(--medium-beige)');
    }

    const handleClick = () => {
        $(window).on('click', function(event) {
            if (!event.target.classList.contains('btn')) {
                const ele = event.target;

                if (ele.classList.contains('cell')) {
                    const [row, col] = ele.id.split('-');

                    if (puzzle[row][col] === EMPTY) {
                        focusedCell = $(event.target);
                        highlightUnits(focusedCell);
                        return;
                    }
                }

                cells.css('background-color', '');
            }

            focusedCell = null;
        });
    }

    const handleKeydown = () => {
        $(window).on('keydown', function(event) {
            if (focusedCell) {
                const num = Number(event.key);
                const isDelete = event.key === 'Backspace' || event.key === 'Delete';
                const isValInput = !isNaN(num) && num >= 1 && num <= 9;
                const isNavUp = event.key === 'ArrowUp' || event.key === 'w';
                const isNavDown = event.key === 'ArrowDown' || event.key === 's';
                const isNavLeft = event.key === 'ArrowLeft' || event.key === 'l';
                const isNavRight = event.key === 'ArrowRight' || event.key === 'r';

                let nextCell;

                if (isDelete) {
                    event.preventDefault();
                    focusedCell.text('');
                    focusedCell.css('color', 'var(--black)');
                } else if (isValInput) {
                    event.preventDefault();
                    focusedCell.text(num);
                    focusedCell.css('color', 'var(--green)');
                } else if (isNavUp) {
                    event.preventDefault();
                    nextCell = findNextSolutionCell('up');
                } else if (isNavDown) {
                    event.preventDefault();
                    nextCell = findNextSolutionCell('down');
                } else if (isNavLeft) {
                    event.preventDefault();
                    nextCell = findNextSolutionCell('left');
                } else if (isNavRight) {
                    event.preventDefault();
                    nextCell = findNextSolutionCell('right');
                }

                if (nextCell) {
                    focusedCell = nextCell;
                    highlightUnits(nextCell);
                }
            }
        })
    }

    const handleNewGame = () => {
        $('#new-game-btn').on('click', () => {
            resetStatus();
            getPuzzle(difficulty.text().trim().toLowerCase());
        })
    }

    const handleReset = () => {
        $('#reset-btn').on('click', () => {
            resetStatus();
            showLoadingStatus('Resetting', 'orange');
            loadValues(puzzle);
            hideLoadingStatus(500);
        });
    }

    const handleSolve = () => {
        $('#solve-btn').on('click', () => {
            solvePuzzle();
        });
    }

    const handleCheckSolution = () => {
        $('#check-solution-btn').on('click', () => {
            cells.css('background-color', '');
            const hasEmptyCells = cells.toArray().some((cell) => $(cell).text().trim() === '');

            if (hasEmptyCells) {
//                cells.each(function() {
//                    const cell = $(this);
//
//                    if (cell.text().trim() === '') {
//                        cell.css('background-color', 'var(--light-red)');
//                    }
//                });
//
//                setTimeout(() => cells.css('background-color', ''), 300);
                solved = true;
                showFailure();

                setTimeout(() => {
                    resetStatus();
                    hideFailure();
                }, 650);
            } else {
                checkSolution();
            }
        });
    }

    const loadValues = (board, withColor = false) => {
        for (let row = 0; row < ROWS; row++) {
            for (let col = 0; col < COLS; col++) {
                const val = board[row][col];
                const cell = $(`#${row}-${col}`);

                if (val != EMPTY) {
                    cell.text(board[row][col]);

                    if (puzzle[row][col] === EMPTY && withColor) {
                        cell.css('color', 'var(--green)');
                    }
                } else if (cell.text() === PLACEHOLDER) {
                    cell.text('');
                }
            }
        }
    }

    const findNextSolutionCell = (direction) => {
        let [row, col] = focusedCell.attr('id').split('-').map((pos) => Number(pos));

        if (direction === 'up') {
            row--;

            while (row >= 0) {
                if (puzzle[row][col] === EMPTY) {
                    break;
                }

                row--;
            }
        } else if (direction === 'down') {
            row++;

            while (row < ROWS) {
                if (puzzle[row][col] === EMPTY) {
                    break;
                }

                row++;
            }
        } else if (direction === 'left') {
            col--;

            while (col >= 0) {
                if (puzzle[row][col] === EMPTY) {
                    break;
                }

                col--;
            }
        } else if (direction === 'right') {
            col++;

            while (col < COLS) {
                if (puzzle[row][col] === EMPTY) {
                    break;
                }

                col++;
            }
        }

        if (row < 0 || row >= ROWS || col < 0 || col >= COLS) {
            return null;
        }

        return $(`#${row}-${col}`);
    }

    const getPuzzle = (difficulty) => {
        showLoadingStatus('Loading game', 'pink');

        axios.get(`/puzzles/random?difficulty=${difficulty}`).then((response) => {
            puzzle = response.data.puzzle;
            loadValues(puzzle);
            hideLoadingStatus();
        })
    }

    const solvePuzzle = () => {
        if (solved) {
            return;
        }

        showLoadingStatus('Solving', 'green');

        axios.post(`/puzzles/solution`, { puzzle }).then((response) => {
            solution = response.data.solution;
            loadValues(solution, true);
            hideLoadingStatus();
        })
    }

    const checkSolution = () => {
        if (solved) {
            return;
        }
        
        const solution = [];

        for (let row = 0; row < ROWS; row++) {
            solution.push([]);

            for (let col = 0; col < COLS; col++) {
                const cell = $(`#${row}-${col}`);
                let val = Number(cell.text().trim());

                if (isNaN(val) || val < 1 || val > 9) {
                   val = -1;
                }

                solution[row].push(val);
            }
        }

        axios.post(`/puzzles/solution_valid`, { puzzle, solution }).then((response) => {
            is_valid_solution = response.data.result;

            if (is_valid_solution) {
                solved = true;
                showSuccess();
            } else {
                solved = true;
                showFailure();

                setTimeout(() => {
                    resetStatus();
                    hideFailure();
                }, 650);
            }
        })

    }

    calculateSquares();
    setBorders();
    dynamicallyResizeCells();
    dynamicallyUpdateDifficulty();
    handleClick();
    handleKeydown();
    handleNewGame();
    handleReset();
    handleSolve();
    handleCheckSolution();
    getPuzzle('easy');
});