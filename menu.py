import pygame
import sys
from button import Button
import pytmx

pygame.init()

screen = pygame.display.set_mode((672, 608))
pygame.display.set_caption("Menu")
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 672, 608
FPS = 15
MAPS_DIR = 'maps'
TILE_SIZE = 32
ENEMY_EVENT_TYPE = 30
back_photo = pygame.image.load("assets/Back.png")
clock = pygame.time.Clock()

def Fon_size(size):
    return pygame.font.Font("assets/font.ttf", size)


def Button_play():
    while True:

        class Labyrint_1:
            def __init__(self, filename, go_tiles, win_tiles):
                self.map = pytmx.load_pygame(f'{MAPS_DIR}/{filename}')
                self.height = self.map.height
                self.width = self.map.width
                self.tile_size = self.map.tilewidth
                self.free_tiles = go_tiles
                self.finish_tile = win_tiles

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
                self.image = pygame.image.load(f'images/{pic}')

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
                self.image = pygame.image.load(f'images/{pic}')

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
                if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    next_x += 1
                if pygame.key.get_pressed()[pygame.K_UP]:
                    next_y -= 1
                if pygame.key.get_pressed()[pygame.K_DOWN]:
                    next_y += 1
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
            text = font.render(message, True, (27, 9, 71))
            text_x = WINDOW_WIDTH // 2 - text.get_width() // 2
            text_y = WINDOW_HEIGHT // 2 - text.get_height() // 2
            text_w = text.get_width()
            text_h = text.get_height()
            pygame.draw.rect(screen, (209, 199, 233), (text_x - 10, text_y - 10,
                                                       text_w + 20, text_h + 20))
            screen.blit(text, (text_x, text_y))

        def main():
            pygame.init()
            screen = pygame.display.set_mode(WINDOW_SIZE)

            labyrinth = Labyrint_1('1.tmx', [306, 114], 114)
            hero = Hero('princieska.png', (3, 10))
            enemy = Enemy('pirat.png', (14, 5))
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
                    show_message(screen, 'Ты выиграл)')
                if game.check_lose():
                    game_over = True
                    show_message(screen, 'Ты проиграл(')
                    exit_b = Button(image=pygame.image.load("assets/exit.png"), pos=(340, 500),
                                    words=" ", fon=Fon_size(50), color1="White", color2="White")
                pygame.display.flip()
                clock.tick(FPS)
            pygame.quit()

        if __name__ == '__main__':
            main()


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


def Button_option():
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
                    menu()

        pygame.display.update()

def menu():
    while True:
        screen.blit(back_photo, (0, 0))

        menu_pos = pygame.mouse.get_pos()

        menu_text = Fon_size(50).render("MazeHero", True, "#9400d3")
        menu_rec = menu_text.get_rect(center=(350, 100))

        play_b = Button(image=pygame.image.load("assets/play.png"), pos=(340, 250),
                        words=" ", fon=Fon_size(50), color1="White", color2="White")
        op_b = Button(image=pygame.image.load("assets/options.png"), pos=(340, 380),
                      words=" ", fon=Fon_size(50), color1="White", color2="White")
        exit_b = Button(image=pygame.image.load("assets/exit.png"), pos=(340, 500),
                        words=" ", fon=Fon_size(50), color1="White", color2="White")

        screen.blit(menu_text, menu_rec)

        for button in [play_b, op_b, exit_b]:
            button.changeColor(menu_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_b.checkForInput(menu_pos):
                    Button_play()
                if op_b.checkForInput(menu_pos):
                    Button_option()
                if exit_b.checkForInput(menu_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


menu()