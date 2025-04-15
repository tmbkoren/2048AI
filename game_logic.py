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
    empty_tiles = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if board[i][j] == 0]
    if empty_tiles:
        i, j = random.choice(empty_tiles)
        board[i][j] = 2 if random.random() < 0.9 else 4
    return board


def moveUp(board) -> list[list[int]]:
    boardStart = copy.deepcopy(board)
    for j in range(BOARD_SIZE):
        merged = [False] * BOARD_SIZE
        for i in range(1, BOARD_SIZE):
            if board[i][j] != 0:
                k = i
                while k > 0:
                    if board[k-1][j] == 0:
                        board[k-1][j] = board[k][j]
                        board[k][j] = 0
                        k -= 1
                    elif board[k-1][j] == board[k][j] and not merged[k-1]:
                        board[k-1][j] *= 2
                        board[k][j] = 0
                        merged[k-1] = True
                        break
                    else:
                        break
    if didAnythingMove(boardStart, board):
        board = add_random_tile(board)
    return board


def moveDown(board) -> list[list[int]]:
    boardStart = copy.deepcopy(board)
    for j in range(BOARD_SIZE):
        merged = [False] * BOARD_SIZE
        for i in range(BOARD_SIZE - 2, -1, -1):
            if board[i][j] != 0:
                k = i
                while k < BOARD_SIZE - 1:
                    if board[k+1][j] == 0:
                        board[k+1][j] = board[k][j]
                        board[k][j] = 0
                        k += 1
                    elif board[k+1][j] == board[k][j] and not merged[k+1]:
                        board[k+1][j] *= 2
                        board[k][j] = 0
                        merged[k+1] = True
                        break
                    else:
                        break
    if didAnythingMove(boardStart, board):
        board = add_random_tile(board)
    return board



def moveLeft(board) -> list[list[int]]:
    boardStart = copy.deepcopy(board)
    for i in range(BOARD_SIZE):
        merged = [False] * BOARD_SIZE
        for j in range(1, BOARD_SIZE):
            if board[i][j] != 0:
                k = j
                while k > 0:
                    if board[i][k-1] == 0:
                        board[i][k-1] = board[i][k]
                        board[i][k] = 0
                        k -= 1
                    elif board[i][k-1] == board[i][k] and not merged[k-1]:
                        board[i][k-1] *= 2
                        board[i][k] = 0
                        merged[k-1] = True
                        break
                    else:
                        break
    if didAnythingMove(boardStart, board):
        board = add_random_tile(board)
    return board



def moveRight(board) -> list[list[int]]:
    boardStart = copy.deepcopy(board)
    for i in range(BOARD_SIZE):
        merged = [False] * BOARD_SIZE  # Track merges in this row
        for j in range(BOARD_SIZE - 2, -1, -1):  # Start from second-to-last cell
            if board[i][j] != 0:
                k = j
                while k < BOARD_SIZE - 1:
                    if board[i][k+1] == 0:
                        board[i][k+1] = board[i][k]
                        board[i][k] = 0
                        k += 1
                    elif board[i][k+1] == board[i][k] and not merged[k+1]:
                        board[i][k+1] *= 2
                        board[i][k] = 0
                        # Mark as merged so it doesn't merge again
                        merged[k+1] = True
                        break
                    else:
                        break
    if didAnythingMove(boardStart, board):
        board = add_random_tile(board)
    return board
