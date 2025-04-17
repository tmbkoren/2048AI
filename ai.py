import copy
import random
import time

BOARD_SIZE = 4
SIMULATION_TIME = 1.5  # Seconds to run MCTS per decision


def move_left(board):
    new_board = copy.deepcopy(board)
    moved = False
    for i in range(BOARD_SIZE):
        row = [v for v in new_board[i] if v != 0]
        j = 0
        while j < len(row) - 1:
            if row[j] == row[j + 1]:
                row[j] *= 2
                row[j + 1] = 0
                j += 2
                moved = True
            else:
                j += 1
        row = [v for v in row if v != 0]
        row += [0] * (BOARD_SIZE - len(row))
        if new_board[i] != row:
            moved = True
        new_board[i] = row
    return new_board, moved


def move_right(board):
    reversed_board = [row[::-1] for row in board]
    moved_board, moved = move_left(reversed_board)
    return [row[::-1] for row in moved_board], moved


def transpose(board):
    return [list(row) for row in zip(*board)]


def move_up(board):
    transposed = transpose(board)
    moved_board, moved = move_left(transposed)
    return transpose(moved_board), moved


def move_down(board):
    transposed = transpose(board)
    moved_board, moved = move_right(transposed)
    return transpose(moved_board), moved


def add_random_tile(board):
    empty = [(i, j) for i in range(BOARD_SIZE)
             for j in range(BOARD_SIZE) if board[i][j] == 0]
    if not empty:
        return
    i, j = random.choice(empty)
    board[i][j] = 4 if random.random() < 0.1 else 2


def is_game_over(board):
    for move_func in [move_up, move_down, move_left, move_right]:
        _, moved = move_func(board)
        if moved:
            return False
    return True


def random_playout(board):
    b = copy.deepcopy(board)
    score = 0
    while not is_game_over(b):
        moves = []
        for name, func in [('up', move_up), ('down', move_down), ('left', move_left), ('right', move_right)]:
            new_b, moved = func(b)
            if moved:
                moves.append((new_b, name))
        if not moves:
            break
        b, _ = random.choice(moves)
        add_random_tile(b)
        score += sum(sum(row) for row in b)  # Can adjust metric here
    return score


def mcts_best_move(board):
    move_funcs = {
        'up': move_up,
        'down': move_down,
        'left': move_left,
        'right': move_right
    }

    results = {move: [] for move in move_funcs}
    start_time = time.time()

    while time.time() - start_time < SIMULATION_TIME:
        for move_name, func in move_funcs.items():
            board_copy = copy.deepcopy(board)
            new_board, moved = func(board_copy)
            if not moved:
                continue
            add_random_tile(new_board)
            score = random_playout(new_board)
            results[move_name].append(score)

    # Choose move with highest average score
    best_move = None
    best_score = -float('inf')
    for move, scores in results.items():
        if scores:
            avg_score = sum(scores) / len(scores)
            if avg_score > best_score:
                best_score = avg_score
                best_move = move

    return best_move or 'up'  # Fallback if no move possible


# Example usage:
if __name__ == '__main__':
    board = [
        [0, 2, 0, 2],
        [4, 0, 4, 0],
        [2, 2, 2, 2],
        [0, 0, 0, 0]
    ]

    move = mcts_best_move(board)
    print("Best move:", move)
