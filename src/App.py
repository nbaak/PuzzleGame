from Game import Game
import colors
import pygame
import sys

WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400
BLOCKSIZE = 200


def draw_grid(screen, blocksize=20, game:Game=None):
    if game:
        font = pygame.font.SysFont('Arial', blocksize)
        for y in range(len(game.field)):
            for x in range(len(game.field[y])):
                rect = pygame.Rect(x * blocksize, y * blocksize, blocksize, blocksize)
                pos_value = game.get_at((x, y))
                if pos_value >= 0:
                    pygame.draw.rect(screen, colors.WHITE, rect, 0)  # fill

                else:
                    pygame.draw.rect(screen, colors.GRAY, rect, 0)  # fill

                pygame.draw.rect(screen, colors.BLACK, rect, 1)  # Border

                if pos_value >= 0:
                    screen.blit(font.render(str(pos_value), True, colors.BLACK), (x * blocksize, y * blocksize))

    else:
        exit()


def draw_queue(screen, blocksize=20, start_at_height=0, game:Game=None):
    if game:
        queue = game.get_queue()
        font = pygame.font.SysFont('Arial', blocksize)
        y = start_at_height
        for index, element in enumerate(queue):
            x = index * blocksize
            rect = pygame.Rect(x, y, blocksize, blocksize)
            if index == 0:
                pygame.draw.rect(screen, colors.WHITE, rect, 0)  # fill
            else:
                pygame.draw.rect(screen, colors.GRAY, rect, 0)  # fill
            pygame.draw.rect(screen, colors.BLACK, rect, 1)  # Border
            screen.blit(font.render(str(element), True, colors.BLACK), (x, y))


def set_value(pos:tuple, game:Game):
    total_value = 0
    gameover = False
    
    if game:
        value = game.queue[0]
        placed = game.place_at(value, pos)
        
        
        if placed == value:
            pts, gameover = game.check_rules(pos, value)
            total_value += pts
            game.take_next_queue_element()
            
            while pts > 0:
                pts, gameover = game.check_rules(pos, value)
                total_value += pts

    return total_value, gameover


def main(width=4, height=3):
    # TODO: level Loop
    game = Game(width, height, 0)
    pygame.init()
    pygame.display.set_caption('Block Riddle')
    dims = game.dims()
    window_width = max([dims[0] * BLOCKSIZE, (BLOCKSIZE//2) * len(game.get_queue())])
    window_height = dims[1] * BLOCKSIZE + int(.9 * BLOCKSIZE)
    
    screen = pygame.display.set_mode((window_width, window_height))
    clock = pygame.time.Clock()
    screen.fill(colors.WHITE)

    game.show()
    pos = None
    points = 0
    gameover = False

    while True:
        draw_grid(screen, blocksize=BLOCKSIZE, game=game)
        draw_queue(screen, blocksize=BLOCKSIZE // 2, start_at_height=window_height - BLOCKSIZE // 2, game=game)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                x, y = pos
                x, y = x // BLOCKSIZE, y // BLOCKSIZE
                pos = (x, y)

        if pos:
            pts, gameover = set_value(pos, game)
            points += pts
            pygame.display.set_caption(f'Block Riddle {points}')
            pos = None

        
        if gameover:
            game.reset()
            print("game over")
            gameover = False

        pygame.display.update()

if __name__ == "__main__":
    main(2, 2)
