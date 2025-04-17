# game_logic.py
import random
import copy


BOARD_SIZE = 4


def create_board() -> list[list[int]]:
    '''Create a new game board with two random tiles.'''
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    board = add_random_tile(board)
    board = add_random_tile(board)
    return board


def is_game_over(board: list[list[int]]) -> bool:
    # Check for any empty cells
    for row in board:
        if 0 in row:
            return False  # Still have room to move

    # Check for horizontal merges
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE - 1):
            if board[i][j] == board[i][j + 1]:
                return False  # Adjacent horizontal merge possible

    # Check for vertical merges
    for j in range(BOARD_SIZE):
        for i in range(BOARD_SIZE - 1):
            if board[i][j] == board[i + 1][j]:
                return False  # Adjacent vertical merge possible

    return True  # No moves left


def didAnythingMove(board1: list[list[int]], board2: list[list[int]]) -> bool:
    '''Checks if the board has changed due to a move. Check before spawning new tile.'''
    return not (board1 == board2)    # TRUE if the board has changed, FALSE if nothing moved


def add_random_tile(board: list[list[int]]) -> list[list[int]]:
    '''Add a random tile (2 or 4) to a random empty space on the board.'''
    empty_tiles = [(i, j) for i in range(BOARD_SIZE)
                   for j in range(BOARD_SIZE) if board[i][j] == 0]
    if empty_tiles:
        i, j = random.choice(empty_tiles)
        board[i][j] = 2 if random.random() < 0.9 else 4
    return board


def transpose(board):
    return [list(row) for row in zip(*board)]


def reverse_rows(board):
    return [row[::-1] for row in board]


def moveLeft(board, score) -> list[list[int]]:
    boardStart = copy.deepcopy(board)

    for i in range(len(board)):
        merged = [False] * len(board[i])
        for j in range(1, len(board[i])):
            if board[i][j] != 0:
                k = j
                while k > 0:
                    if board[i][k-1] == 0:
                        board[i][k-1] = board[i][k]
                        board[i][k] = 0
                        k -= 1
                    elif board[i][k-1] == board[i][k] and not merged[k-1]:
                        board[i][k-1] *= 2
                        score[0] += board[i][k-1]
                        board[i][k] = 0
                        merged[k-1] = True
                        break
                    else:
                        break

    if didAnythingMove(boardStart, board):
        board = add_random_tile(board)
    return board


def moveRight(board, score) -> list[list[int]]:
    board = reverse_rows(board)
    board = moveLeft(board, score)
    return reverse_rows(board)


def moveUp(board, score) -> list[list[int]]:
    board = transpose(board)
    board = moveLeft(board, score)
    return transpose(board)


def moveDown(board, score) -> list[list[int]]:
    board = transpose(board)
    board = reverse_rows(board)
    board = moveLeft(board, score)
    board = reverse_rows(board)
    return transpose(board)
