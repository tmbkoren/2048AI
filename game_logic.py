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

def apply_move(board, direction: int) -> list[list[int]]:
    '''Direction: 0 = UP, 1 = RIGHT, 2 = DOWN, 3 = LEFT'''
    # Implement the logic to move tiles in the specified direction
    board = add_random_tile(board)
    return board

