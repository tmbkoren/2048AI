# game_logic.py
import random


BOARD_SIZE = 4


def create_board() -> list[list[int]]:
    '''Create a new game board with two random tiles.'''
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    board = add_random_tile(board)
    board = add_random_tile(board)
    return board

def add_random_tile(board: list[list[int]]) -> list[list[int]]:
    '''Add a random tile (2 or 4) to a random empty space on the board.'''
    empty_tiles = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if board[i][j] == 0]
    if empty_tiles:
        i, j = random.choice(empty_tiles)
        board[i][j] = 2 if random.random() < 0.9 else 4
    return board


def moveUp(board) -> list[list[int]]:
    '''Move tiles up'''
    for j in range(BOARD_SIZE):
        for i in range(1, BOARD_SIZE):
            if board[i][j] != 0:
                k = i
                while k > 0 and (board[k-1][j] == 0 or board[k-1][j] == board[k][j]):
                    if board[k-1][j] == board[k][j]:
                        board[k-1][j] *= 2
                        board[k][j] = 0
                    else:
                        board[k-1][j] = board[k][j]
                        board[k][j] = 0
                    k -= 1
    board = add_random_tile(board)
    return board

def moveDown(board) -> list[list[int]]:
    '''Move tiles down'''
    for j in range(BOARD_SIZE):
        for i in range(BOARD_SIZE-2, -1, -1):
            if board[i][j] != 0:
                k = i
                while k < BOARD_SIZE-1 and (board[k+1][j] == 0 or board[k+1][j] == board[k][j]):
                    if board[k+1][j] == board[k][j]:
                        board[k+1][j] *= 2
                        board[k][j] = 0
                    else:
                        board[k+1][j] = board[k][j]
                        board[k][j] = 0
                    k += 1
    board = add_random_tile(board)
    return board

def moveLeft(board) -> list[list[int]]:
    '''Move tiles left'''
    for i in range(BOARD_SIZE):
        for j in range(1, BOARD_SIZE):
            if board[i][j] != 0:
                k = j
                while k > 0 and (board[i][k-1] == 0 or board[i][k-1] == board[i][k]):
                    if board[i][k-1] == board[i][k]:
                        board[i][k-1] *= 2
                        board[i][k] = 0
                    else:
                        board[i][k-1] = board[i][k]
                        board[i][k] = 0
                    k -= 1
    board = add_random_tile(board)
    return board

def moveRight(board) -> list[list[int]]:
    '''Move tiles right'''
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE-2, -1, -1):
            if board[i][j] != 0:
                k = j
                while k < BOARD_SIZE-1 and (board[i][k+1] == 0 or board[i][k+1] == board[i][k]):
                    if board[i][k+1] == board[i][k]:
                        board[i][k+1] *= 2
                        board[i][k] = 0
                    else:
                        board[i][k+1] = board[i][k]
                        board[i][k] = 0
                    k += 1
    board = add_random_tile(board)
    return board