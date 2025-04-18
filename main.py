from gui import draw_board, draw_game_over_popup, draw_button, draw_ai_suggestion, draw_scores
from game_logic import create_board, moveUp, moveDown, moveLeft, moveRight, is_game_over
from ai import mcts_best_move
import time
import numpy as np


def get_best_move(board):
    move = mcts_best_move(board)
    # print(f"AI suggests: {move}")
    return move


def apply_move(board, move: str, score):
    if move == "up":
        return moveUp(board, score)
    elif move == "down":
        return moveDown(board, score)
    elif move == "left":
        return moveLeft(board, score)
    elif move == "right":
        return moveRight(board, score)
    return board

def printMetrics(trial_number, start_time, end_time, move_count, score, board):
    win = (np.max(board) > 2048)
    if win:
        outcome = "Win"
    else:
        outcome = "Loss"
    
    time_elapsed = end_time - start_time
    print(f'\nTrial Number: {trial_number}')
    print(f'Time Elapsed: {time_elapsed}')
    print(f'Move Count: {move_count}')
    print(f'Final Score: {score}')
    print(f'Outcome: {outcome}\n')
    print('<><><><><><><><><><><><><><><><><>')

def main():
    import pygame
    import json
    
    # MAKE SURE TO MAKE THIS FALSE FOR MANUAL DEMO
    automated = True

    SCREEN_SIZE = 400
    SUGGEST_BUTTON = pygame.Rect(40, 420, 140, 40)
    AUTO_BUTTON = pygame.Rect(220, 420, 140, 40)
    # === PyGame Initialization ===
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE + 100))
    pygame.display.set_caption("2048")
    clock = pygame.time.Clock()
    gameFont = pygame.font.SysFont("comicsans", 40)
    font = pygame.font.SysFont("comicsans", 16)

    # === Game Initialization ===
    board = create_board()
    game_over = False
    if automated:
        ai_autoplay = True
    else:
        ai_autoplay = False
    suggested_move = None
    suggest_display_timer = 0
    current_score = [0]
    
    move_count = 0
    trial_number = 0
    start_time = time.time()

    with open('scores.json', 'r') as file:
        data = json.load(file)
        high_score = data["High_Score"]

    running = True
    while running:
        screen.fill((250, 248, 239))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # MANUAL CONTROLS
            elif event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_r:
                    board = create_board()
                    game_over = False
                    ai_autoplay = False
                    suggested_move = None
                    current_score[0] = 0

                elif not game_over:
                    move = None
                    if event.key == pygame.K_LEFT:
                        move = "left"
                    elif event.key == pygame.K_RIGHT:
                        move = "right"
                    elif event.key == pygame.K_UP:
                        move = "up"
                    elif event.key == pygame.K_DOWN:
                        move = "down"

                    if move:
                        board = apply_move(board, move, current_score)
                        suggested_move = None
                        if current_score[0] >= high_score:
                            high_score = current_score[0]
                        if is_game_over(board):
                            with open('scores.json', 'w') as file:
                                data["High_Score"] = high_score
                                json.dump(data, file, indent=4)
                            game_over = True

            # MOUSE EVENT
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if SUGGEST_BUTTON.collidepoint(event.pos) and not game_over:
                    suggested_move = get_best_move(board)
                    suggest_display_timer = pygame.time.get_ticks()
                elif AUTO_BUTTON.collidepoint(event.pos) and not game_over:
                    ai_autoplay = not ai_autoplay
                    suggested_move = None

        # === AI Autoplay ===
        if ai_autoplay and not game_over:
            move = get_best_move(board)
            board = apply_move(board, move, current_score)
            move_count += 1
            suggested_move = None
            pygame.time.delay(100)

            if current_score[0] >= high_score:
                high_score = current_score[0]

            if is_game_over(board):
                with open('scores.json', 'w') as file:
                    data["High_Score"] = high_score
                    json.dump(data, file, indent=4)
                game_over = True

        # === Draw Everything ===
        draw_board(screen, board, gameFont)
        pygame.draw.line(screen, (180, 180, 180),
                         (0, SCREEN_SIZE), (SCREEN_SIZE, SCREEN_SIZE), 2)
        draw_scores(screen, font, current_score, high_score)
        draw_button(screen, "Suggest Move", SUGGEST_BUTTON, font)
        draw_button(screen, "AI Autoplay", AUTO_BUTTON,
                    font, active=ai_autoplay)

        if suggested_move:
            now = pygame.time.get_ticks()
            if now - suggest_display_timer < 3000:
                draw_ai_suggestion(screen, font, suggested_move)
            else:
                suggested_move = None

        if game_over:
            draw_game_over_popup(screen, font)
            
            end_time = time.time()
            printMetrics(trial_number, start_time, end_time, move_count, current_score[0], board)
            trial_number += 1
            if automated:
                board = create_board()
                game_over = False
                ai_autoplay = True
                suggested_move = None
                current_score[0] = 0
                move_count = 0
                start_time = time.time()

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


# === Entry Point (Safe for Multiprocessing) ===
if __name__ == '__main__':
    main()
