from Game import Game
from draw import draw_grid, draw_queue, draw_status
import colors
import pygame
import sys
import os
import uuid

WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400
BLOCKSIZE = 200
FONTSIZE_STATUS = 40


def set_value(pos:tuple, game:Game):
    total_value = 0
    gameover = False

    if game:
        value = game.queue[0]
        placed = game.place_at(value, pos, do_step=True)

        if placed == value:
            pts, gameover = game.check_rules(pos, value)
            total_value += pts

            while pts > 0:
                pts, gameover = game.check_rules(pos, value)
                total_value += pts

    return total_value, gameover


def main(width=4, height=3, level=0):
    # TODO: level Loop
    game = Game(width, height, level)
    pygame.init()
    pygame.display.set_caption('Block Riddle')
    dims = game.dims()
    window_width = max([dims[0] * BLOCKSIZE, (BLOCKSIZE // 2) * len(game.get_queue())])
    window_height = dims[1] * BLOCKSIZE + int(.9 * BLOCKSIZE)

    screen = pygame.display.set_mode((window_width, window_height))
    # clock = pygame.time.Clock()
    screen.fill(colors.WHITE)

    game.show()
    pos = None
    gameover = False

    while True:
        draw_grid(screen, blocksize=BLOCKSIZE, game=game)
        draw_queue(screen, blocksize=BLOCKSIZE // 2, start_at_height=window_height - BLOCKSIZE // 2, game=game)
        draw_status(screen, fontsize=FONTSIZE_STATUS, start_at_height=window_height - int(BLOCKSIZE * .9), width=window_width, game=game)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                x, y = pos
                x, y = x // BLOCKSIZE, y // BLOCKSIZE
                pos = (x, y)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    if not os.path.exists('./screenshots'):
                        os.makedirs('./screenshots', exist_ok=True)

                    filename = str(uuid.uuid4())
                    pygame.image.save(screen, f'./screenshots/{filename}.jpg')

                if event.key == pygame.K_r:
                    print('forced reset')
                    game.reset()
                    
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        if pos:
            # _, gameover = set_value(pos, game)
            _, _, gameover = game.play(pos)
            pygame.display.set_caption(f'Block Riddle {game.points}')
            pos = None

        if gameover:
            game.reset()
            print("game over")
            print(len(game.replay_field))
            gameover = False

        pygame.display.update()


if __name__ == "__main__":
    main(5, 5, 0)
