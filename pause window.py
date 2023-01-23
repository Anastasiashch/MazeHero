import pygame
import buttonx

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 672, 608
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("menu")

pause = False
menu = "main"

bg_image = pygame.image.load('images/bg_img.png')
font = pygame.font.SysFont('fonts/palatinolinotype_roman.ttf', 50)
font2 = pygame.font.SysFont('times new roman', 28)
FONT_COL = (255, 255, 255)

resume_img = pygame.image.load("images/1x/resume.png").convert_alpha()
options_img = pygame.image.load("images/1x/rules.png").convert_alpha()
quit_img = pygame.image.load("images/1x/exit.png").convert_alpha()
resume2_img = pygame.image.load('images/1x/resume.png').convert_alpha()


resume_btn = buttonx.Buttonx(240, 130, resume_img, 1)
rules_btn = buttonx.Buttonx(240, 260, options_img, 1)
quit_btn = buttonx.Buttonx(240, 385, quit_img, 1)
resume2_btn = buttonx.Buttonx(390, 500, resume2_img, 1)

def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

#game loop
running = True
while running:
  screen.blit(bg_image, (0, 0))
  if pause:
    if menu == "main":
      if resume_btn.draw(screen):
        pause = False
      if rules_btn.draw(screen):
        menu = "rules"

      if quit_btn.draw(screen):
        running = False
    if menu == "rules":
      count = 40
      text1 = 'Правила игры в MazeHero'
      draw_text(text1, pygame.font.SysFont('times new roman bold', 40), (0, 0, 0), 160, 10)
      intro_text = [
                    'Данная игра состоит из разных уровней, и они все',
                    'различаются', ' ',
                    '1. Для начала вам нужно начать игру, нажав на', 'кнопку НАЧАТЬ.', ' ',
                    '2. Суть игры состроить в том, чтобы вы смогли выйти', 'из лабиринта, при этом не умерев.',
                    '(Если проиграли, можно начать заново)', ' ',
                    '3. В каждом уровне у вас будут разные сложности:',
                    'за вами будут гнаться, будут препятствия', 'и еще много интересного',
                    'Поэтому скорее жми на кнопку НАЗАД,', 'чтобы приступить к игре )))']
      for i in range(0, len(intro_text)):

        draw_text(intro_text[i], font2, (0, 0, 0), 10, count)
        count += 30

      if resume2_btn.draw(screen):
        menu = "main"
  else:
    draw_text("Press SPACE", font, FONT_COL, 160, 250)

  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        pause = True
    if event.type == pygame.QUIT:
      running = False

  pygame.display.update()

pygame.quit()

