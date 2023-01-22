import pygame
import pytmx
import os
import sys

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 672, 608
FPS = 15
MAPS_DIR = 'maps'
TILE_SIZE = 32
ENEMY_EVENT_TYPE = 30

hero_pics = ['wnv2_rt2.png', 'wnv2_bk2.png', 'wnv2_fr2.png', 'wnv2_lf1.png']
hero_pic_n = 0

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

player_image = load_image('wnv2_rt2.png')
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


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)

    fon = pygame.transform.scale(load_image('bg_forest_1.jpg'), (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(fon, (0, 0))



    labyrinth = Labyrinth('map1lvl.tmx', [5124, 1253, 3737, 4760, 3735, 624], 5124)
    hero = Hero(hero_pics[hero_pic_n], (0, 14))
    enemy = Enemy('sp.png', (9, 14))
    game = Game(labyrinth, hero, enemy)

    clock = pygame.time.Clock()
    game_over = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == ENEMY_EVENT_TYPE and not game_over:
                game.move_enemy()
        if not game_over:
            game.update_hero()

        screen.fill((0, 0, 0))
        game.render(screen)
        if game.check_win():
            game_over = True
            show_message(screen, 'You won')
        if game.check_lose():
            game_over = True
            show_message(screen, 'You lost')
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()