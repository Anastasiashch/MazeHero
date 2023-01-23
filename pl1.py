import pygame
import os
import math
import random
from os import listdir
from os.path import isfile
import sys
from pygame.sprite import spritecollide

# 


# bbg = 'data/bg/skyDay01.png'
BG_FON = 'data/bg/purple.png'
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 672, 608
FPS = 40
STEP = 10
P_COLOR = (255, 0, 0)
GRAVITY = 1
DELAY = 5
level = 'level1'



pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE))
pygame.display.set_caption('platformer')



tile_width = tile_height = 32


def get_the_block(size, path):
    img = pygame.image.load(path).convert_alpha()
    block = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, size, size)
    block.blit(img, (0, 0), rect)
    return block


def get_background(filename):
    image = pygame.image.load(filename)
    x, x, width, height = image.get_rect()
    tiles = []

    for i in range(21):
        for j in range(19):
            pos = (i * width, j * height)
            tiles.append(pos)
    return tiles, image

def flip_img(sprites):
    changed_sprites = []
    for x in sprites:
        changed_sprites.append(pygame.transform.flip(x, True, False))
    return changed_sprites

def load_sheets(directory, w, h, direction=False):
    path = f'data/characters/{directory}'
    imgs = []
    for x in listdir(path):
        if isfile(f'{path}/{x}'):
            imgs.append(x)
    all_sprites = {}

    for img in imgs:
        sprite_sheet = pygame.image.load(f'{path}/{img}').convert_alpha()
        # конвeртирует поверхности в тот же пиксель-формат, которые используется для screen

        sprites = []
        for i in range(sprite_sheet.get_width() // w):
            surface = pygame.Surface((w, h), pygame.SRCALPHA, 32)

            # The pixel format can be controlled by passing the bit depth or an existing Surface.
            # The flags argument is a bitmask of additional features for the surface.
            # You can pass any combination of these flags:

            # HWSURFACE    (obsolete in pygame 2) creates the image in video memory
            # SRCALPHA     the pixel format will include a per-pixel alpha
            # (документация пайгейм)

            ani_rect = pygame.Rect(i * w, 0, w, h)
            surface.blit(sprite_sheet, (0, 0), ani_rect)
            # создаём поверхность для анимации
            sprites.append(surface)

        # directions:
        if direction:
            all_sprites[img.replace(".png", '') + "_r"] = sprites
            all_sprites[img.replace(".png", '') + "_l"] = flip_img(sprites)
        else:
            all_sprites[img.replace(".png", '')] = sprites

    return all_sprites


SPRITES = load_sheets('main', 32, 32, True)

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, w, h):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.x_pos = 0
        self.y_pos = 0
        self.direction = 'r'
        self.spr_pic = 0
        self.falling = 0  # время падения
        self.count = 0 # анимация
        self.jumping = 0

    def jump(self):
        self.y_pos = -GRAVITY * 5
        self.count = 0
        self.jumping += 1
        if self.jumping == 1:
            self.falling = 0
            # убираем гравитацию для первого прыжка


    def move(self, x1, y1):
        self.rect.x += x1
        self.rect.y += y1

    def move_left(self, pos):
        self.x_pos = -pos
        if self.direction != 'l':
            self.direction = 'l'
            self.spr_pic = 0
            self.count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy


    def move_right(self, pos):
        self.x_pos = pos
        if self.direction != 'r':
            self.direction = 'r'
            self.spr_pic = 0
            self.count = 0

    def update_sprite(self):
        sprite_type = 'stand'
        if self.y_pos != 0:
            if self.jumping == 1:
                sprite_type = 'jump'
            elif self.falling == 2:
                sprite_type = 'jump_jump'
        elif self.y_pos > GRAVITY * 3: #чтобы не заедало при падении на землю
            sprite_type = 'fall'
        elif self.x_pos != 0:
            sprite_type = 'walk'

        sprite_type_name = f'{sprite_type}_{self.direction}'
        sprites = SPRITES[sprite_type_name]
        sprite_n = (self.count // DELAY) % len(sprites)
        # каждые 5 кадров (DELAY) будет показан новый спрайт в любой из анимаций
        # делим на длину чтобы работало для каждого набора спрайтов
        self.sprite = sprites[sprite_n]
        self.count += 1
        self.update_displaying()

    def update_displaying(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y)) # постоянно регулируем прямоугольник
        # (его ширину и высоту) в котором наш спрайт, при этом используя те же х и у позиции, что и ранее для rect
        # topleft для определения заданного начального положения координат верхнего левого угла
        self.mask = pygame.mask.from_surface(self.sprite)
        # для проверки столкновения попиксельно (а не прямоугольник нашего спрайта)

    def land_on_the_block(self):
        self.falling = 0
        self.y_pos = 0
        self.jumping = 0

    def hit_the_block(self):
        self.count = 0
        self.y_pos = - self.y_pos
        #меняем направление нашей velocity(x_pos), для того чтобы при ударе верхней части персонажа
        # о блок, он начинал движение вниз

    #зацикливание
    def cycle(self, FPS):
        self.y_pos += min(1, (self.falling / FPS) * GRAVITY)
        # чтобы сделать ускорение при падении, увеличиваем y_pos.
        # для этого нужно знать как долго мы падаем. для того чтобы задать это время в секундах, мы делим falling
        # на fps (при этом каждый цикл (выполнение cycle) fallng увеличивается) и умножаем на коэффицент гравитации,
        # для того чтобы установить вы сколько раз будт изменяться y_pos
        # (self.falling / FPS) вначале будет очень маленьким дробным десятичным числом.
        # тут будет удобнее взять минимум из 1 и этим значением, чтобы каждый кадр мы спускались
        # хотя бы на один пискель вниз и нам бы не приходилось ждать целую секунду до начала гравиации
        self.move(self.x_pos, self.y_pos)

        self.falling += 1
        self.update_sprite()

    #отображение на экране
    def render(self, scr):
        scr.blit(self.sprite, (self.rect.x, self.rect.y))


def draw(screen, background, bg_image, player, objects):
    for tile in background:
        screen.blit(bg_image, tile)

    for x in objects:
        x.render(screen)

    player.render(screen)
    pygame.display.update()

def check_collision(player, objects, y):
    collides = []
    for x in objects:
        if pygame.sprite.collide_mask(player, x):
            if y > 0:
                player.rect.bottom = x.rect.top
                player.land_on_the_block()
                # нижняя часть прямоугольника игрока равна верхней части объекта, с которым происходит коллайд
            elif y < 0:
                player.rect.top = x.rect.bottom
                player.hit_the_block()
        collides.append(x)
    return collides

#проверям сможем ли совершить коллайд с обектом
def collide(player, obj, x):
    player.move(x, 0)
    player.update()
    coll_obj = None
    for i in obj:
        if pygame.sprite.collide_mask(player, i):
            coll_obj = i
            break
    player.move(-x, 0)
    player.update()
    return coll_obj

def check_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_pos = 0
    left_collision = collide(player, objects, STEP * 2)
    right_collision = collide(player, objects, -STEP * 2)

    if keys[pygame.K_RIGHT] and not left_collision:
        player.move_right(STEP)
    if keys[pygame.K_LEFT] and not right_collision:
        player.move_left(STEP)

    check_collision(player, objects, player.y_pos) #y_pos = сколько мы уже прошли




# потом удалить этот класс и заменить на несколько в каждом добавляя информацию
class Map(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)
        self.img = pygame.Surface((w, h), pygame.SRCALPHA)
        self.w = w
        self.h = h
        self.name = name

    def render(self, screen):
        screen.blit(self.img, (self.rect.x, self.rect.y))

class Blocks(Map):
    def __init__(self, x, y, size, n):
        super().__init__(x, y, size, size)
        if n == 'stone':
            stone = get_the_block(size, 'data/platforms/stoneWall.png')
            self.img.blit(stone, (0, 0))
        if n == 'grass':
            grass = get_the_block(size, 'data/platforms/grassMid.png')
            self.img.blit(grass, (0, 0))
        if n == 'flag':
            flag = get_the_block(size, 'data/platforms/flag.png')
            self.img.blit(flag, (0, 0))
        self.mask = pygame.mask.from_surface(self.img)


def show_message(screen, message):
    font = pygame.font.Font(None, 50)
    text = font.render(message, 2, (50, 70, 0))
    text_x = WINDOW_WIDTH // 2 - text.get_width() // 2
    text_y = WINDOW_HEIGHT // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, (200, 150, 50), (text_x - 10, text_y - 10,
                                              text_w + 20, text_h + 20))
    screen.blit(text, (text_x, text_y))


def platformer(screen):
    clock = pygame.time.Clock()
    background, bg_image = get_background(BG_FON)


    player = Player(32, 500, 32, 32)
    screen_rect = screen.get_rect()

    # down_platform = [Blocks(i * b_size, WINDOW_HEIGHT - b_size, b_size) for i in range(-WINDOW_WIDTH // b_size,
    #                                                                           (WINDOW_WIDTH * 2) // b_size)] 576

    platforms = [Blocks(12 * 32, 15 * 32, 32, 'grass'), Blocks(13 * 32, 15 * 32, 32, 'grass'),
                 Blocks(14 * 32, 15 * 32, 32, 'grass'), Blocks(18 * 32, 13 * 32, 32, 'grass'),
                 Blocks(19 * 32, 13 * 32, 32, 'grass'), Blocks(17 * 32, 13 * 32, 32, 'grass'),
                 Blocks(14 * 32, 11 * 32, 32, 'grass'), Blocks(11 * 32, 11 * 32, 32, 'grass'),
                 Blocks(10 * 32, 11 * 32, 32, 'grass'), Blocks(7 * 32, 9 * 32, 32, 'grass'),
                 Blocks(6 * 32, 9 * 32, 32, 'grass'),
                 Blocks(13 * 32, 7 * 32, 32, 'grass'), Blocks(14 * 32, 7 * 32, 32, 'grass'),
                 Blocks(8 * 32, 5 * 32, 32, 'grass'), Blocks(5 * 32, 9 * 32, 32, 'grass'),
                 Blocks(4 * 32, 9 * 32, 32, 'grass'), Blocks(3 * 32, 9 * 32, 32, 'grass'),
                 Blocks(16 * 32, 3 * 32, 32, 'grass'), Blocks(15 * 32, 3 * 32, 32, 'grass'),
                 Blocks(20 * 32, 2 * 32, 32, 'grass'), Blocks(19 * 32, 2 * 32, 32, 'grass'),
                 Blocks(0 * 32, 9 * 32, 32, 'grass'), Blocks(1 * 32, 9 * 32, 32, 'grass'),
                 Blocks(2 * 32, 9 * 32, 32, 'grass'), Blocks(20 * 32, 1 * 32, 32, 'flag')]



    for i in range(0, 22):
        block = Blocks(i * 32, 544, 32, 'grass')
        platforms.append(block)

    for i in range(0, 22):
        block = Blocks(i * 32, 576, 32, 'stone')
        platforms.append(block)

    for i in range(0,20):
        block = Blocks(-32, i * 32, 32, 'stone')
        platforms.append(block)

    for i in range(0, 22):
        block = Blocks(i * 32, -32, 32, 'stone')
        platforms.append(block)

    for i in range(0, 20):
        block = Blocks(672, i * 32, 32, 'stone')
        platforms.append(block)



    # block = [Blocks(0, WINDOW_HEIGHT - b_size, b_size)]

    win = False
    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jumping < 2 and win == False:
                    player.jump()

            if 592 <= player.rect.x <= 630 and player.rect.y == 32 and win == False:
                win = True
                show_message(screen, 'You won')
                level = 'level2'


        if win == True:
            pygame.display.flip()
        else:
            player.cycle(FPS)
            check_move(player, platforms)
            draw(screen, background, bg_image, player, platforms)

    pygame.quit()

if __name__ == '__main__':
    main(screen)


def main(level): #note i added the level parameter that you have to pass in
    if level == "level1":
        platformer(screen)
    else:
        p = Platformer('Adventure Time!', 'map2.tmx', 600, 600, 30)
    p.main_loop()
