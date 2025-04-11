import pygame
from game_logic import create_board

# Initialize Pygame
pygame.init()
SCREEN_SIZE = 400
BOARD_SIZE = 4
screen = pygame.display.set_mode((SCREEN_SIZE + 200, SCREEN_SIZE))
pygame.display.set_caption('2048 Game')
clock = pygame.time.Clock()


def draw_board(screen, board, font):
    tile_size = SCREEN_SIZE // BOARD_SIZE
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            value = board[i][j]
            rect = pygame.Rect(j * tile_size, i * tile_size,
                               tile_size, tile_size)
            color = get_tile_color(value)  # Define based on value
            pygame.draw.rect(screen, color, rect)
            if value:
                text_surface = font.render(str(value), True, (119, 110, 101))
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)

def get_tile_color(value):
    if value == 0:
        return (204, 192, 179)  # Empty tile color
    elif value == 2:
        return (238, 228, 218)
    elif value == 4:
        return (237, 224, 200)
    elif value == 8:
        return (242, 177, 121)
    elif value == 16:
        return (245, 149, 99)
    elif value == 32:
        return (246, 124, 95)
    elif value == 64:
        return (246, 94, 59)
    elif value == 128:
        return (237, 207, 114)
    elif value == 256:
        return (237, 204, 97)
    elif value == 512:
        return (237, 200, 80)
    elif value == 1024:
        return (237, 197, 63)
    elif value == 2048:
        return (237, 194, 46)
