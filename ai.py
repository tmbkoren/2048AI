import copy
import random
import time
from concurrent.futures import ProcessPoolExecutor

BOARD_SIZE = 4
SIMULATIONS_PER_MOVE = 30


def move_left(board):
    new_board = copy.deepcopy(board)
    moved = False
    score_gained = 0

    for i in range(BOARD_SIZE):
        merged = [False] * BOARD_SIZE
        for j in range(1, BOARD_SIZE):
            if new_board[i][j] == 0:
                continue
            k = j
            while k > 0:
                if new_board[i][k - 1] == 0:
                    new_board[i][k - 1] = new_board[i][k]
                    new_board[i][k] = 0
                    k -= 1
                    moved = True
                elif new_board[i][k - 1] == new_board[i][k] and not merged[k - 1]:
                    new_board[i][k - 1] *= 2
                    new_board[i][k] = 0
                    merged[k - 1] = True
                    score_gained += new_board[i][k - 1]
                    moved = True
                    break
                else:
                    break

    return new_board, moved, score_gained


def move_right(board):
    reversed_board = [row[::-1] for row in board]
    moved_board, moved, score = move_left(reversed_board)
    return [row[::-1] for row in moved_board], moved, score


def transpose(board):
    return [list(row) for row in zip(*board)]


def move_up(board):
    transposed = transpose(board)
    moved_board, moved, score = move_left(transposed)
    return transpose(moved_board), moved, score


def move_down(board):
    transposed = transpose(board)
    moved_board, moved, score = move_right(transposed)
    return transpose(moved_board), moved, score


def add_random_tile(board):
    empty = [(i, j) for i in range(BOARD_SIZE)
             for j in range(BOARD_SIZE) if board[i][j] == 0]
    if not empty:
        return
    i, j = random.choice(empty)
    board[i][j] = 4 if random.random() < 0.1 else 2


def is_game_over(board):
    for move_func in [move_up, move_down, move_left, move_right]:
        _, moved, _ = move_func(board)
        if moved:
            return False
    return True


def random_playout(board):
    b = copy.deepcopy(board)
    score = 0
    while not is_game_over(b):
        moves = []
        for name, func in [('up', move_up), ('down', move_down), ('left', move_left), ('right', move_right)]:
            new_b, moved, _ = func(b)
            if moved:
                moves.append((new_b, name))
        if not moves:
            break
        b, _ = random.choice(moves)
        add_random_tile(b)
        score += sum(sum(row) for row in b)
    return score


def simulate_move(args):
    board, move_name, num_simulations = args
    move_funcs = {
        'up': move_up,
        'down': move_down,
        'left': move_left,
        'right': move_right
    }

    func = move_funcs[move_name]
    scores = []

    for _ in range(num_simulations):
        b = copy.deepcopy(board)
        b, moved, _ = func(b)
        if not moved:
            continue
        add_random_tile(b)
        score = random_playout(b)
        scores.append(score)

    return move_name, scores


def mcts_best_move(board):
    move_names = ['up', 'down', 'left', 'right']

    with ProcessPoolExecutor() as executor:
        args = [(board, move, SIMULATIONS_PER_MOVE) for move in move_names]
        futures = executor.map(simulate_move, args)

    results = {}
    for move_name, scores in futures:
        if scores:
            avg = sum(scores) / len(scores)
            results[move_name] = avg

    best_move = max(results, key=results.get, default='up')
    return best_move


# Example usage
if __name__ == '__main__':
    board = [
        [0, 2, 0, 2],
        [4, 0, 4, 0],
        [2, 2, 2, 2],
        [0, 0, 0, 0]
    ]

    move = mcts_best_move(board)
    print("Best move:", move)
