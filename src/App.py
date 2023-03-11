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
                    pygame.draw.rect(screen, colors.BLACK, rect, 0)  # fill

                pygame.draw.rect(screen, colors.GRAY, rect, 1)  # Border
                
                if pos_value >= 0:
                    screen.blit(font.render(str(pos_value), True, colors.BLACK), (x*blocksize, y*blocksize))
                
    else:
        exit()


def draw_queue(screen, blocksize=20, game:Game=None):
    if game:
        ...

def set_value(value:int, pos:tuple, game:Game):
    total_value = 0
    if value and tuple:
        game.place_at(value, pos)
        # game.show()
        pts = game.check_rules(pos, value)
        # print(f'you earned {pts} points')
        total_value += pts
        while pts > 0:
            pts = game.check_rules(pos, value)
            total_value += pts
            
    return total_value


def main(width=4, height=3):
    game = Game(width, height, 1)
    pygame.init()
    pygame.display.set_caption('Block Riddle')
    dims = game.dims()
    screen = pygame.display.set_mode((dims[0] * BLOCKSIZE, dims[1] * BLOCKSIZE + BLOCKSIZE))
    clock = pygame.time.Clock()
    screen.fill(colors.WHITE)

    game.show()
    pos = None
    points = 0

    while True:
        draw_grid(screen, blocksize=BLOCKSIZE, game=game)
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
            points += set_value(1, pos, game)
            pygame.display.set_caption(f'Block Riddle {points}')
            pos = None
            
            
        pygame.display.update()


if __name__ == "__main__":
    main(4, 3)
