#  Player image by NotMatter
#  https://notmatter.itch.io/1

import pygame
import pytmx

# from pygame.locals import *
FPS = 15
MAPS_DIR = 'maps'
TILE_SIZE = 32
ENEMY_EVENT_TYPE = 30


pygame.init()

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 672, 608
BG = (50, 50, 50)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('platformer')

player_image = pygame.image.load('images/hero1_04.png')


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False




    screen.fill(BG)
    screen.blit(player_image, (300, 300))
    pygame.display.flip()
pygame.quit()


# labyrinth = Labyrinth('map1.tmx',
    #                       [323, 72, 47, 48, 49, 50, 51, 163, 143, 84, 83, 82, 81, 80, 79, 598, 599, 600, 601,
    #                        602, 630, 631, 632, 633, 634, 44, 76, 302, 387, 29, 257, 225, 226, 227, 228, 259,
    #                        260, 258, 175, 240, 322, 299], 1793)