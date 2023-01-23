import pygame
import os
import math
import random
from os import listdir
from os.path import isfile
import sys
import pytmx
from button1 import Button
from buttonx import Buttonx
from pygame.sprite import spritecollide


back_photo = pygame.image.load("assets/Back.png")
clock = pygame.time.Clock()
a = True
b = True


# bbg = 'data/bg/skyDay01.png'
BG_FON = 'data/bg/purple.png'
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 672, 608
FPS = 30
FPS2 = 15
STEP = 10
P_COLOR = (255, 0, 0)
GRAVITY = 1
DELAY = 5
MAPS_DIR = 'maps'
TILE_SIZE = 32
ENEMY_EVENT_TYPE = 30
LEVEL = 'start_menu'
game_over_1 = False
win_lab = False

hero_pics = ['wnv2_rt2.png', 'wnv2_bk2.png', 'wnv2_fr2.png', 'wnv2_lf1.png']
hero_pic_n = 0


def start_menuxx():
    pygame.init()

    screen = pygame.display.set_mode((672, 608))
    pygame.display.set_caption("Menu")
    def Fon_size(size):
        return pygame.font.Font("assets/font.ttf", size)


    def blit_text(surface, text, pos, font, color=pygame.Color(27, 9, 71)):
        words = [word.split(' ') for word in text.splitlines()]
        space = font.size(' ')[0]
        max_width, max_height = surface.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]
                    y += word_height
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]
            y += word_height

    pygame.display.update()
    while True:
        op_pos = pygame.mouse.get_pos()
        screen.blit(back_photo, (0, 0))
        text = "Привила игры в MazeHero \n" \
               "Данная игра состоит из разных уровней, и она все различаются. \n " \
               "1. Для начала вам нужно начать игру нажав на кнопку Начать. \n" \
               "2. Суть игры состроить в том, чтобы вы смогли выйти из лабиринта, при этом не умерев. " \
               "(Если проиграли," \
               " можно начать заново) \n" \
               "3. В каждом уровне у вас будут разные сложности: за вами будут гнаться, будут " \
               "препятствия и еще много интересного. \n" \
               "Поэтому скорее жми на кнопку Назад, чтобы приступить к игре )))"
        font = pygame.font.SysFont('Times New Roman', 30)
        blit_text(screen, text, (20, 20), font)

        op_back_b = Button(image=pygame.image.load("assets/back_button.png"), pos=(500, 500),
                           words=" ", fon=Fon_size(50), color1="Black", color2="Purple")

        op_back_b.changeColor(op_pos)
        op_back_b.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if op_back_b.checkForInput(op_pos):
                    LEVEL = 'level1'
                    platformer(screen)

        pygame.display.update()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

player_image = load_image('wnv2_rt2.png')

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE))
pygame.display.set_caption('platformer')
bg_image = pygame.image.load('images/bg_img.png')


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

def from2to3():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    screen.blit(bg_image, (0, 0))

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    font = pygame.font.SysFont('fonts/palatinolinotype_roman.ttf', 50)
    text1 = 'нажмите пробел, чтобы продолжить'
    draw_text(text1, pygame.font.SysFont('times new roman bold', 40), (255, 255, 255), 110, 300)
    text2 = 'Вы победили!'
    draw_text(text2, pygame.font.SysFont('times new roman bold', 40), (255, 255, 255), 110, 250)
    clock = pygame.time.Clock()
    running = True
    win = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    LEVEL = 'level3'
                    win = True
                    lab2()
        if win == True:
            pygame.display.flip()
            labyrinth1()

        pygame.display.flip()
        clock.tick(FPS2)
    pygame.quit()

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
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jumping < 2 and win == False:
                    player.jump()

            if 592 <= player.rect.x <= 630 and player.rect.y == 32 and win == False:
                win = True
                show_message(screen, 'You won')


        if win == True:
            pygame.display.flip()
            LEVEL = 'level2'
            from1to2()
        else:
            player.cycle(FPS)
            check_move(player, platforms)
            draw(screen, background, bg_image, player, platforms)

class Labyrinth:
    def __init__(self, filename, free_tiles, finish_tile):
        self.map = pytmx.load_pygame(f'{MAPS_DIR}/{filename}')
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        self.free_tiles = free_tiles
        self.finish_tile = finish_tile

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                screen.blit(image, (x * self.tile_size, y * self.tile_size))

    def get_tile_id(self, position):
        return self.map.tiledgidmap[self.map.get_tile_gid(*position, 0)]

    def is_free(self, position):
        return self.get_tile_id(position) in self.free_tiles

    def find_path_step(self, start, target):
        INF = 1000
        x, y = start
        distance = [[INF] * self.width for _ in range(self.height)]
        distance[y][x] = 0
        prev = [[None] * self.width for _ in range(self.height)]
        queue = [(x, y)]
        while queue:
            x, y = queue.pop(0)
            for dx, dy in (1, 0), (0, 1), (-1, 0), (0, -1):
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < self.width and 0 < next_y < self.height and \
                        self.is_free((next_x, next_y)) and distance[next_y][next_x] == INF:
                    distance[next_y][next_x] = distance[y][x] + 1
                    prev[next_y][next_x] = (x, y)
                    queue.append((next_x, next_y))
        x, y = target
        if distance[y][x] == INF or start == target:
            return start
        while prev[y][x] != start:
            x, y = prev[y][x]
        return x, y


class Hero:
    def __init__(self, pic, position):
        self.x, self.y = position
        self.image = pygame.image.load(f'data/{pic}')


    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen):
        delta = (self.image.get_width() - TILE_SIZE) // 2
        screen.blit(self.image, (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))


class Enemy:
    def __init__(self, pic, position):
        self.x, self.y = position
        self.delay = 100
        pygame.time.set_timer(ENEMY_EVENT_TYPE, self.delay)
        self.image = pygame.image.load(f'data/{pic}')

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen):
        delta = (self.image.get_width() - TILE_SIZE) // 2
        screen.blit(self.image, (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))


class Game:
    def __init__(self, labyrinth, hero, enemy):
        self.labyrinth = labyrinth
        self.hero = hero
        self.enemy = enemy

    def render(self, screen):
        self.labyrinth.render(screen)
        self.hero.render(screen)
        self.enemy.render(screen)

    def update_hero(self):
        next_x, next_y = self.hero.get_position()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            next_x -= 1
            hero_pic_n = 0
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            next_x += 1
            hero_pic_n = 3
        if pygame.key.get_pressed()[pygame.K_UP]:
            next_y -= 1
            hero_pic_n = 1
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            next_y += 1
            hero_pic_n = 2
        if self.labyrinth.is_free((next_x, next_y)):
            self.hero.set_position((next_x, next_y))

    def move_enemy(self):
        next_position = self.labyrinth.find_path_step(self.enemy.get_position(),
                                                      self.hero.get_position())
        self.enemy.set_position(next_position)


    def check_win(self):
        return self.labyrinth.get_tile_id(self.hero.get_position()) == self.labyrinth.finish_tile

    def check_lose(self):
        return self.hero.get_position() == self.enemy.get_position()


def show_message(screen, message):
    font = pygame.font.Font(None, 50)
    text = font.render(message, 1, (50, 70, 0))
    text_x = WINDOW_WIDTH // 2 - text.get_width() // 2
    text_y = WINDOW_HEIGHT // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, (200, 150, 50), (text_x - 10, text_y - 10,
                                              text_w + 20, text_h + 20))
    screen.blit(text, (text_x, text_y))

def from1to2():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    screen.blit(bg_image, (0, 0))

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    font = pygame.font.SysFont('fonts/palatinolinotype_roman.ttf', 50)
    text1 = 'нажмите пробел, чтобы продолжить'
    draw_text(text1, pygame.font.SysFont('times new roman bold', 40), (255, 255, 255), 110, 300)
    clock = pygame.time.Clock()
    running = True
    win = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    LEVEL = 'level2'
                    win = True
                    labyrinth1()
        if win == True:
            pygame.display.flip()
            labyrinth1()

        pygame.display.flip()
        clock.tick(FPS2)
    pygame.quit()

def from3to4():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    screen.blit(bg_image, (0, 0))

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    font = pygame.font.SysFont('fonts/palatinolinotype_roman.ttf', 50)
    text1 = 'нажмите пробел, чтобы продолжить'
    draw_text(text1, pygame.font.SysFont('times new roman bold', 40), (255, 255, 255), 110, 300)
    clock = pygame.time.Clock()
    running = True
    win = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    LEVEL = 'level4'
                    win = True
                    lab3()
        if win == True:
            pygame.display.flip()
            lab3()

        pygame.display.flip()
        clock.tick(FPS2)
    pygame.quit()


def lab3():
    pygame.init()
    screen2 = pygame.display.set_mode(WINDOW_SIZE)

    labyrinth = Labyrinth('1.tmx', [306, 114], 114)
    hero = Hero('princieska.png', (3, 10))
    enemy = Enemy('pirat.png', (14, 5))
    game = Game(labyrinth, hero, enemy)

    clock = pygame.time.Clock()
    game_over_3 = False
    running = True
    win_lab3 = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == ENEMY_EVENT_TYPE and not game_over_3:
                game.move_enemy()
        if not game_over_3:
            game.update_hero()

        screen.fill((0, 0, 0))
        game.render(screen)

        if game.check_win():
            game_over_3 = True
            win_lab3 = True
            show_message(screen, 'вы выйграли!')
        if game.check_lose() and win_lab3 == False:
            game_over_3 = True
            show_message(screen, 'вы проиграли!')

        if game_over_3 == True and win_lab3 == False:
            lab3()
        pygame.display.flip()
        clock.tick(FPS2)
    pygame.quit()

def lab2():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)

    labyrinth = Labyrinth('secondLevel.tmx', [849, 850, 725], 725)
    hero = Hero('heror.png', (5, 10))
    enemy = Enemy('enemy.png', (16, 4))
    game = Game(labyrinth, hero, enemy)

    clock = pygame.time.Clock()
    game_over2 = False
    running = True
    win_lab2 = False
    menu_pos = pygame.mouse.get_pos()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == ENEMY_EVENT_TYPE and not game_over2:
                game.move_enemy()
        if not game_over2:
            game.update_hero()


        screen.fill((0, 0, 0))
        game.render(screen)

        if game.check_win():
            game_over2 = True
            win_lab2 = True
            show_message(screen, 'вы выйграли!')
            LEVEL = 'from3to4'

        if game.check_lose() and win_lab2 == False:
            game_over2 = True
            show_message(screen, 'вы проиграли!')

        if game_over2 == True and win_lab2 == False:
            lab2()

        if game_over_1 == True and win_lab == True:
            from3to4()

        pygame.display.flip()
        clock.tick(FPS2)
    pygame.quit()

def labyrinth1():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)

    fon = pygame.transform.scale(load_image('bg_forest_1.jpg'), (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(fon, (0, 0))



    labyrinth = Labyrinth('map1lvl.tmx', [5124, 1253, 3737, 4760, 3735, 624], 5124)
    hero = Hero(hero_pics[hero_pic_n], (0, 14))
    enemy = Enemy('sp.png', (9, 14))
    game = Game(labyrinth, hero, enemy)

    clock = pygame.time.Clock()
    game_over_1 = False
    win_lab = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == ENEMY_EVENT_TYPE and not game_over_1:
                game.move_enemy()
        if not game_over_1:
            game.update_hero()

        screen.fill((0, 0, 0))
        game.render(screen)
        if game.check_win():
            game_over_1 = True
            win_lab = True
            show_message(screen, 'вы выйграли!')
            LEVEL = 'from2to3'
        if game.check_lose() and win_lab == False:
            game_over_1 = True
            show_message(screen, 'вы проиграли!')

        if game_over_1 == True and win_lab == False:
            labyrinth1()

        if game_over_1 == True and win_lab == True:
            pygame.display.flip()
            from2to3()

        pygame.display.flip()
        clock.tick(FPS2)
    pygame.quit()


def main():
    if LEVEL == 'start_menu':
        start_menuxx()
    if LEVEL == 'level1':
        platformer(screen)
    elif LEVEL == '1 to 2':
        from1to2()
    elif LEVEL == 'level2':
        labyrinth1()
    elif LEVEL == 'from2to3':
        from2to3()
    elif LEVEL == 'level3':
        lab2()
    elif LEVEL == 'from3to4':
        from3to4()
    elif LEVEL == 'level4':
        lab3()


if __name__ == '__main__':
    main()

