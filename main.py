import pygame
import json
from game_logic import create_board, moveUp, moveDown, moveLeft, moveRight, is_game_over
from gui import draw_board, draw_game_over_popup, draw_button, draw_ai_suggestion

# === Placeholder AI function ===

def get_best_move(board):
    return "up"  # Replace with real AI logic


# === Setup ===
pygame.init()
SCREEN_SIZE = 400
gameFont = pygame.font.SysFont("comicsans", 40)
font = pygame.font.SysFont("comicsans", 16)
screen = pygame.display.set_mode(
    (SCREEN_SIZE, SCREEN_SIZE + 100))  # Increased height

pygame.display.set_caption("2048")
clock = pygame.time.Clock()

# Button positions
# Updated button positions
SUGGEST_BUTTON = pygame.Rect(40, 420, 140, 40)
AUTO_BUTTON = pygame.Rect(220, 420, 140, 40)



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


def main():
    with open('scores.json', 'r') as file:
        board = create_board()
        game_over = False
        running = True
        ai_autoplay = False
        suggested_move = None
        suggest_display_timer = 0  # Time marker for how long to display suggestion
        data = json.load(file)
        high_score = data["High_Score"]
        current_score = [0]
        while running:
            screen.fill((250, 248, 239))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if game_over and event.key == pygame.K_r:
                        board = create_board()
                        game_over = False
                        ai_autoplay = False
                        suggested_move = None

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
                            if current_score[0] >= high_score :
                                high_score = current_score[0]
                            if is_game_over(board):
                                with open('scores.json', 'w') as file:
                                    data["High_Score"] = high_score
                                    json.dump(data, file, indent = 4)
                                current_score[0] = 0
                                game_over = True

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if SUGGEST_BUTTON.collidepoint(event.pos) and not game_over:
                        suggested_move = get_best_move(board)
                        suggest_display_timer = pygame.time.get_ticks()

                    elif AUTO_BUTTON.collidepoint(event.pos) and not game_over:
                        ai_autoplay = not ai_autoplay
                        suggested_move = None

            # AI autoplay logic
            if ai_autoplay and not game_over:
                move = get_best_move(board)
                board = apply_move(board, move, current_score)
                suggested_move = None
                pygame.time.delay(100)
                if current_score[0] >= high_score :
                    high_score = current_score[0]
                if is_game_over(board):
                    with open('scores.json', 'w') as file:
                        data["High_Score"] = high_score
                        json.dump(data, file, indent = 4)
                    current_score[0] = 0
                    game_over = True

            # Draw the game
            draw_board(screen, board, gameFont)
            pygame.draw.line(screen, (180, 180, 180),
                            (0, SCREEN_SIZE), (SCREEN_SIZE, SCREEN_SIZE), 2)

            draw_button(screen, "Suggest Move", SUGGEST_BUTTON, font)
            draw_button(screen, "AI Autoplay", AUTO_BUTTON,
                        font, active=ai_autoplay)

            # Display AI suggestion if recent
            if suggested_move:
                now = pygame.time.get_ticks()
                if now - suggest_display_timer < 3000:  # Show for 3 seconds
                    draw_ai_suggestion(screen, font, suggested_move)
                else:
                    suggested_move = None

            if game_over:
                draw_game_over_popup(screen, font)


            pygame.display.flip()
            clock.tick(30)

    pygame.quit()


if __name__ == '__main__':
    main()
