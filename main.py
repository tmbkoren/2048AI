import pygame
from game_logic import create_board, apply_move
from gui import draw_board


def main():
    board = create_board()
    print(board)
    font = pygame.font.SysFont("comicsans", 40)
    running = True
    ai_control = False  # Toggle this to let your AI take over
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif not ai_control and event.type == pygame.KEYDOWN:
                # Map arrow keys to moves
                if event.key == pygame.K_UP:
                    move = 0
                elif event.key == pygame.K_DOWN:
                    move = 2
                elif event.key == pygame.K_LEFT:
                    move = 3
                elif event.key == pygame.K_RIGHT:
                    move = 1
                else:
                    move = None

                board = apply_move(board, move)


        # Render the board.
        draw_board(pygame.display.get_surface(), board, font)
        pygame.display.update()
        pygame.time.delay(100)
        # if game_over(board):
        #     print("Game Over!")
        #     running = False

    pygame.quit()


if __name__ == '__main__':
    main()
