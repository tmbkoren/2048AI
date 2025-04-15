import pygame
from game_logic import create_board, moveUp, moveDown, moveLeft, moveRight
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
                    board = moveUp(board)
                elif event.key == pygame.K_DOWN:
                    board = moveDown(board)
                elif event.key == pygame.K_LEFT:
                    board = moveLeft(board)
                elif event.key == pygame.K_RIGHT:
                    board = moveRight(board)

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
