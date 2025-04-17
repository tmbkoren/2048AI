import pygame

# Constants
SCREEN_SIZE = 400
BOARD_SIZE = 4


def draw_board(screen, board, font):
    tile_size = SCREEN_SIZE // BOARD_SIZE
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            value = board[i][j]
            rect = pygame.Rect(j * tile_size, i * tile_size,
                               tile_size, tile_size)
            color = get_tile_color(value)
            pygame.draw.rect(screen, color, rect)
            if value:
                text_surface = font.render(str(value), True, (119, 110, 101))
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)


def draw_game_over_popup(screen, font):
    overlay = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    game_over_text = font.render("Game Over", True, (255, 255, 255))
    prompt_text = font.render("Press R to Restart", True, (200, 200, 200))

    screen.blit(game_over_text, game_over_text.get_rect(
        center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2 - 30)))
    screen.blit(prompt_text, prompt_text.get_rect(
        center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2 + 20)))


def draw_button(screen, text, rect, font, active=False):
    color = (120, 180, 120) if active else (200, 200, 200)
    pygame.draw.rect(screen, color, rect, border_radius=8)
    label = font.render(text, True, (0, 0, 0))
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)


def draw_ai_suggestion(screen, font, move_name):
    label = font.render(
        f"AI Suggests: {move_name.upper()}", True, (80, 80, 80))
    screen.blit(label, (100, 470))  # move below the buttons

def draw_scores(screen, font, score, high_score):
    score_text = font.render(f"Score: {score[0]}", True, (0, 0, 0))
    high_text = font.render(f"High: {high_score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(high_text, (220, 10))

def get_tile_color(value):
    return {
        0: (204, 192, 179),
        2: (238, 228, 218),
        4: (237, 224, 200),
        8: (242, 177, 121),
        16: (245, 149, 99),
        32: (246, 124, 95),
        64: (246, 94, 59),
        128: (237, 207, 114),
        256: (237, 204, 97),
        512: (237, 200, 80),
        1024: (237, 197, 63),
        2048: (237, 194, 46),
    }.get(value, (60, 58, 50))  # default for higher tiles
