
import pygame.display
import colors

from PIL import Image
from Game import Game
import os

WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400
BLOCKSIZE = 200
FONTSIZE_STATUS = 40


def draw_grid(screen, blocksize=20, game:Game=None):
    if game:
        font = pygame.font.SysFont('Arial', int(blocksize * .8))
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
        font = pygame.font.SysFont('Arial', int(blocksize * .8))
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


def draw_status(screen, fontsize=20, start_at_height:int=0, width=20, game:Game=None):
    # fontsize = int(fontsize * .8)
    status_text = game.get_status()
    font = pygame.font.SysFont('Arial', fontsize)

    rect = pygame.Rect(0, start_at_height, width, fontsize)
    pygame.draw.rect(screen, colors.WHITE, rect, 0)  # background
    screen.blit(font.render(status_text, True, colors.BLACK), (5, start_at_height))


def store_screenshot(screen, session, filename):
    path = f"./screenshots/{session}/"
    
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    
    image_file = f'{path}/{filename:05}.jpg'
    pygame.image.save(screen, image_file)
    return image_file

def save_images_as_animation(frames, filename="video.gif", duration=10, loop=1):
    animation_images = []
    for frame in frames:
        animation_images.append(frame)
        
    animation_images[0].save(filename, save_all=True, append_images=animation_images[1:], duration=duration, loop=loop)


def safe_replay(game:Game, session):
    r_game = Game(game.width, game.height, game.level)
    step = 1

    pygame.init()
    pygame.display.set_caption('Block Riddle')
    dims = game.dims()
    window_width = max([dims[0] * BLOCKSIZE, (BLOCKSIZE // 2) * len(game.get_queue())])
    window_height = dims[1] * BLOCKSIZE + int(.9 * BLOCKSIZE)

    screen = pygame.display.set_mode((window_width, window_height))
    screen.fill(colors.WHITE)
    
    frames = []

    for field, queue, pts in zip(game.replay_field, game.replay_queue, game.replay_pts):
        r_game.field = field
        r_game.queue = queue
        r_game.points = pts
        r_game.step = step

        draw_grid(screen, blocksize=BLOCKSIZE, game=r_game)
        draw_queue(screen, blocksize=BLOCKSIZE // 2, start_at_height=window_height - BLOCKSIZE // 2, game=r_game)
        draw_status(screen, fontsize=FONTSIZE_STATUS, start_at_height=window_height - int(BLOCKSIZE * .9), width=window_width, game=r_game)
        
        print(field, pts)
        
        im = store_screenshot(screen, session, step)
        frames.append(Image.open(im))
        step += 1
    
    save_images_as_animation(frames, f'./screenshots/{session}/anim.gif')
    pygame.quit()
