import pygame
import sys
from button import Button

pygame.init()

screen = pygame.display.set_mode((672, 608))
pygame.display.set_caption("Menu")

back_photo = pygame.image.load("assets/Back.png")
FPS = 15
clock = pygame.time.Clock()
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 672, 608
MAPS_DIR = 'maps'
TILE_SIZE = 32
ENEMY_EVENT_TYPE = 30


def Fon_size(size):
    return pygame.font.Font("assets/font.ttf", size)


def Button_play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        screen.blit(back_photo, (0, 0))
        PLAY_TEXT = Fon_size(25).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(350, 50))
        screen.blit(PLAY_TEXT, PLAY_RECT)
        PLAY_BACK = Button(image=pygame.image.load("assets/back_button.png"), pos=(200, 100), words=" ",
                           fon=Fon_size(50), color1="black", color2="Purple")
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    menu()
        pygame.display.update()


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