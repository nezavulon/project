import sys
import pygame
import pygame.font
from win32api import GetSystemMetrics
from pygame.locals import *
from pygame import *

# Объявляем переменные

fert = open('files/res.txt', mode='r')
data_txt = fert.read().split(' ')
level = 1
lev = 1
wins = int(data_txt[1])
dies = int(data_txt[0])
screen_width = GetSystemMetrics(0)
screen_height = GetSystemMetrics(1)
PLATFORM_WIDTH = 30
PLATFORM_HEIGHT = 30
PLATFORM_COLOR = "#6A5ACD"
back_color = "#003153"
plrMOVE_SPEED = 10
plrWIDTH = 22
plrHEIGHT = 32
JUMP = 10
GRAVITY = 0.40
plrCOLOR = "#18A7B5"
plrANIMATION_RIGHT = [
    'files/r1.png',
    'files/r2.png',
    'files/r3.png',
    'files/r4.png',
    'files/r5.png',
    'files/r6.png',
    'files/r7.png',
    'files/r8.png'
]
plrRIGHT = 0
plrANIMATION_LEFT = [
    'files/l1.png',
    'files/l2.png',
    'files/l3.png',
    'files/l4.png',
    'files/l5.png',
    'files/l6.png',
    'files/l7.png',
    'files/l8.png'
]
plrLEFT = 0
LEFTorRIGHT = 1


# Это класс платформ
class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = image.load("files/platform.png")
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("files/dieBlock.png")


class BlockFinish(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("files/finishBlock.png")


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.startX = x
        self.startY = y
        self.yvel = 0
        self.onGround = False
        self.image = Surface((plrWIDTH, plrHEIGHT))
        self.image.fill(Color(plrCOLOR))
        self.rect = Rect(x, y, plrWIDTH, plrHEIGHT)

    def die(self):
        global dies
        dies += 1
        defeat_screen()

    def win(self):
        global wins
        wins += 1
        victoty_screen()

    def update(self, left, right, up, platforms):
        global plrLEFT, plrRIGHT, LEFTorRIGHT
        if left:
            self.xvel = plrMOVE_SPEED * -1
            pygame.time.Clock().tick(60)
            self.image = image.load(plrANIMATION_LEFT[plrLEFT])
            self.image = image.load(plrANIMATION_LEFT[plrLEFT])
            self.image = image.load(plrANIMATION_LEFT[plrLEFT])
            plrLEFT += 1
            LEFTorRIGHT = 0
            if plrLEFT > 7:
                plrLEFT = 0

        if right:
            self.xvel = plrMOVE_SPEED
            pygame.time.Clock().tick(60)
            self.image = image.load(plrANIMATION_RIGHT[plrRIGHT])
            self.image = image.load(plrANIMATION_RIGHT[plrRIGHT])
            self.image = image.load(plrANIMATION_RIGHT[plrRIGHT])
            plrRIGHT += 1
            LEFTorRIGHT = 1
            if plrRIGHT > 7:
                plrRIGHT = 0

        if not (left or right):
            self.xvel = 0
            if LEFTorRIGHT == 1:
                pygame.time.Clock().tick(60)
                self.image = image.load("files/r0.png")
            elif LEFTorRIGHT == 0:
                pygame.time.Clock().tick(60)
                self.image = image.load("files/l0.png")

        if up:
            if self.onGround:
                self.yvel = JUMP * -1

        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        global won
        for p in platforms:
            if sprite.collide_rect(self, p):
                if isinstance(p, BlockDie):
                    won = 0
                    self.die()
                if isinstance(p, BlockFinish):
                    won = 1
                    self.win()

                if xvel > 0:
                    self.rect.right = p.rect.left

                if xvel < 0:
                    self.rect.left = p.rect.right

                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0

                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + screen_width / 2, -t + screen_height / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-screen_width), l)   # Не движемся дальше правой границы
    t = max(-(camera.height-screen_height), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


# авто-разрешение пока что бесполезно т. к. мне лень сейчас делать полный экран
# оказалось оно работает
def get_resolution():
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h
    return screen_width, screen_height


def main_menu():
    global wins
    global dies
    pygame.init()
    screen = pygame.display.set_mode(get_resolution())
    pygame.display.set_caption("Alpha_0.1")
    screen.fill(Color(back_color))

    def draw_text(text, color, x, y):
        font = pygame.font.SysFont('Calibri', 36)
        label = font.render(text, True, color)
        screen.blit(label, (x, y))


    while True:
        screen.fill((30, 30, 30))
        but_width = screen_width / 2 - 50
        but_h = screen_height / 2 - 50
        draw_text("ESCAPER 2D", (255, 255, 255), screen_width / 2 - 90, screen_height / 2 - 250)
        draw_text("Level 1", (255, 255, 255), but_width, screen_height / 2 - 200)
        draw_text("Level 2", (255, 255, 255), but_width, screen_height / 2 - 150)
        draw_text("Exit", (255, 255, 255), but_width, screen_height / 2 - 100)
        draw_text("Total wins and dies: " + str(wins) + ' ' + str(dies), (255, 255, 255), but_width - 50, but_h)
        draw_text("Reference", (255, 255, 255), but_width, screen_height / 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                f = open("files/res.txt", mode="w")
                dies_and_wins = str(dies) + ' ' + str(wins)
                f.write(dies_and_wins)
                f.close()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if but_width <= x <= but_width + 200 and screen_height / 2 - 200 <= y <= screen_height / 2 - 160:
                    level_1()
                elif but_width <= x <= but_width + 200 and screen_height / 2 - 150 <= y <= screen_height / 2 - 110:
                    level_2()
                elif but_width <= x <= but_width + 200 and screen_height / 2 <= y <= screen_height / 2 + 40:
                    spravka()
                elif but_width <= x <= but_width + 200 and screen_height / 2 - 100 <= y <= screen_height / 2 - 60:
                    f = open("files/res.txt", mode="w")
                    dies_and_wins = str(dies) + ' ' + str(wins)
                    f.write(dies_and_wins)
                    f.close()
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()


def spravka():
    global wins
    global dies
    pygame.init()
    screen = pygame.display.set_mode(get_resolution())
    pygame.display.set_caption("Alpha_0.1")
    screen.fill(Color(back_color))

    def draw_text(text, color, x, y):
        font = pygame.font.SysFont('Calibri', 36)
        label = font.render(text, True, color)
        screen.blit(label, (x, y))

    def draw_name(text, color, x, y):
        font = pygame.font.SysFont('serif', 50)
        label = font.render(text, True, color)
        screen.blit(label, (x, y))

    while True:
        screen.fill((30, 30, 30))
        but_width = screen_width / 2 - 50
        but_h = screen_height / 2 - 50
        draw_name("Авторы:", (255, 255, 255), screen_width / 2 - 150, screen_height / 2 - 250)
        draw_text("Эдльдар Маршанкулов", (255, 255, 255), but_width, screen_height / 2 - 150)
        draw_text("Никита Попов", (255, 255, 255), but_width, screen_height / 2 - 100)
        draw_text("Main menu", (255, 255, 255), but_width, screen_height / 2 - 50)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                f = open("files/res.txt", mode="w")
                dies_and_wins = str(dies) + ' ' + str(wins)
                f.write(dies_and_wins)
                f.close()
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if but_width <= x <= but_width + 200 and screen_height / 2 - 50 <= y <= screen_height / 2 - 10:
                    main_menu()

        pygame.display.flip()


def defeat_screen():
    global wins
    global dies
    pygame.init()
    screen = pygame.display.set_mode(get_resolution())
    pygame.display.set_caption("Alpha_0.1")
    screen.fill(Color(back_color))

    def draw_text(text, color, x, y):
        font = pygame.font.SysFont('Calibri', 36)
        label = font.render(text, True, color)
        screen.blit(label, (x, y))

    def draw_name(text, color, x, y):
        font = pygame.font.SysFont('serif', 50)
        label = font.render(text, True, color)
        screen.blit(label, (x, y))

    while True:
        screen.fill((30, 30, 30))
        but_width = screen_width / 2 - 50
        but_h = screen_height / 2 - 50
        draw_name("GAME OVER", (255, 255, 255), screen_width / 2 - 150, screen_height / 2 - 250)
        draw_text("Restart", (255, 255, 255), but_width, screen_height / 2 - 150)
        draw_text("Main menu", (255, 255, 255), but_width, screen_height / 2 - 100)
        draw_text("Total wins and dies: " + str(wins) + ' ' + str(dies), (255, 255, 255), but_width - 50, but_h)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                f = open("files/res.txt", mode="w")
                dies_and_wins = str(dies) + ' ' + str(wins)
                f.write(dies_and_wins)
                f.close()
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if but_width <= x <= but_width + 200 and screen_height / 2 - 150 <= y <= screen_height / 2 - 110:
                    restart()
                elif but_width <= x <= but_width + 200 and screen_height / 2 - 100 <= y <= screen_height / 2 - 60:
                    main_menu()

        pygame.display.flip()


def victoty_screen():
    global wins
    global dies
    pygame.init()
    screen = pygame.display.set_mode(get_resolution())
    pygame.display.set_caption("Alpha_0.1")
    screen.fill(Color(back_color))

    def draw_text(text, color, x, y):
        font = pygame.font.SysFont('Calibri', 36)
        label = font.render(text, True, color)
        screen.blit(label, (x, y))

    def draw_name(text, color, x, y):
        font = pygame.font.SysFont('serif', 50)
        label = font.render(text, True, color)
        screen.blit(label, (x, y))

    while True:
        screen.fill((30, 30, 30))
        but_width = screen_width / 2 - 50
        but_h = screen_height / 2 - 50
        draw_name("YOU WIN!", (255, 255, 255), screen_width / 2 - 150, screen_height / 2 - 250)
        draw_text("Restart", (255, 255, 255), but_width, screen_height / 2 - 150)
        draw_text("Main menu", (255, 255, 255), but_width, screen_height / 2 - 100)
        draw_text("Total wins and dies: " + str(wins) + ' ' + str(dies), (255, 255, 255), but_width - 50, but_h)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                f = open("files/res.txt", mode="w")
                dies_and_wins = str(dies) + ' ' + str(wins)
                f.write(dies_and_wins)
                f.close()
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if but_width <= x <= but_width + 200 and screen_height / 2 - 150 <= y <= screen_height / 2 - 110:
                    restart()
                elif but_width <= x <= but_width + 200 and screen_height / 2 - 100 <= y <= screen_height / 2 - 60:
                    main_menu()

        pygame.display.flip()


def restart():
    global lev
    if lev == 1:
        level_1()
    elif lev == 2:
        level_2()


def level_1():
    global level
    global lev
    lev = 1
    level = [
        "----------------------------------------------------------------------------------------------------------",
        "-                                                                                                        -",
        "-                                                                                                        -",
        "-                                                                                                       &-",
        "-                                 ----***----     -     -                              -------------------",
        "-                                                          -                                             -",
        "-                       *-----                             -                  -----                      -",
        "-                                                          -                                             -",
        "-                                                          --------------                                -",
        "-                       -----                    *         -                 -----                       -",
        "-                                                *         -                                             -",
        "-                               ------------------         -                         ------------------  -",
        "-                                         -                -                                             -",
        "-                                         -                -                                             -",
        "-                     --------            -  ------*-*-*-*--               --------                      -",
        "-                                         -       *        -                                             -",
        "-                                         -         *      -                                             -",
        "-           --                            -           *    -                                             -",
        "-                                         -             *  ---------------                               -",
        "-                                         -               *-                                             -",
        "-                  ----***----            -                -                      --                     -",
        "-                                         -                -                                             -",
        "-                                         -                                                              -",
        "-                                         -                            --                                -",
        "-                         ------------------               -                   ------------------        -",
        "-                         -                                -                                             -",
        "-         ------**        -                                ---------                                     -",
        "-                         -                                                                              -",
        "-                         -                                                    -      -                  -",
        "-                         -                                                                              -",
        "-                       ---                       ******                                                 -",
        "-                       -                                                                    -           -",
        "-                       -                                                                                -",
        "-                       -                                                                                -",
        "----------------------------------------------------------------------------------------------------------"]
    main()


def level_2():
    global level
    global lev
    lev = 2
    level = [
        "----------------------------------------------------------------------------------------------------------",
        "-                                                                                                        -",
        "-                                                                                                        -",
        "-                                                                                                       &-",
        "-  -------------------------------------------------------------------------------------------------------",
        "-  *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *     -",
        "-                                                                                                        -",
        "-    *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   -",
        "-------------------------------------------------------------------------------------------------------  -",
        "-        ***     ***     ***     ***     ***     ***     ***     ***     ***     ***     ***     ***     -",
        "-                                                                                                        -",
        "-   ***      ***     ***     ***     ***     ***     ***     ***     ***     ***     ***     ***     **  -",
        "-  -------------------------------------------------------------------------------------------------------",
        "-      **    **    **    **    **    **    **    **    **    **    **    **    **    **    **    **      -",
        "-                                                                                                        -",
        "-   **    **    **    **    **    **    **    **    **    **    **    **    **    **    **    **    **   -",
        "-------------------------------------------------------------------------------------------------------  -",
        "-                                                                                                        -",
        "-                                                                                                        -",
        "-   ***     ***     ***     ***     ***     ***     ***     ***     ***     ***     ***     ***     ***  -",
        "-  -------------------------------------------------------------------------------------------------------",
        "-                                                                                                        -",
        "-                                                                                                        -",
        "-      **     **     **     **     **     **     **     **     **     **     **     **     **     **     -",
        "------------------------------------------------------------------------------------------------------   -",
        "-                                                                                                        -",
        "-                                                                                                        -",
        "-        ***            ***              ***                 ***               ***             ***       -",
        "----------------------------------------------------------------------------------------------------------"]
    main()


#
def main():
    global wins
    global dies
    pygame.init()
    screen = pygame.display.set_mode(get_resolution())
    pygame.display.set_caption("Alpha_0.1")
    screen.fill(Color(back_color))
    background_image = pygame.image.load('files/background.png')
    bg = pygame.Surface((get_resolution()))
    bg.blit(background_image, (0, 0))
    if lev == 1:
        hero = Player(55, 1000)
    elif lev == 2:
        hero = Player(55, 800)
    left = right = False
    up = False
    entities = pygame.sprite.Group()
    platforms = []
    entities.add(hero)
    x = y = 0
    for row in level:
        for col in row:
            if col == "-":
                plat = Platform(x, y)
                entities.add(plat)
                platforms.append(plat)
            if col == "*":
                bd = BlockDie(x, y)
                entities.add(bd)
                platforms.append(bd)
            if col == "&":
                fin = BlockFinish(x, y)
                entities.add(fin)
                platforms.append(fin)

            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == QUIT:
                f = open("files/res.txt", mode="w")
                dies_and_wins = str(dies) + ' ' + str(wins)
                f.write(dies_and_wins)
                f.close()
                running = False
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                running = False
                main_menu()
            if e.type == KEYDOWN and e.key == K_a:
                left = True
            if e.type == KEYUP and e.key == K_a:
                left = False
            if e.type == KEYDOWN and e.key == K_d:
                right = True
            if e.type == KEYUP and e.key == K_d:
                right = False
            if e.type == KEYDOWN and e.key == K_w:
                up = True
            if e.type == KEYUP and e.key == K_w:
                up = False
            if e.type == KEYDOWN and e.key == K_SPACE:
                up = True
            if e.type == KEYUP and e.key == K_SPACE:
                up = False
        hero.update(left, right, up, platforms)
        camera.update(hero)  # центризируем камеру относительно персонажа
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        pygame.display.update()
        pygame.time.Clock().tick(120)
        screen.blit(bg, (1, 1))


if __name__ == "__main__":
    pygame.init()
    main_menu()