import random
import pygame
import time
import pygame.font
from pygame.locals import *
from pygame import *

# Объявляем переменные
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 30
PLATFORM_COLOR = "#6A5ACD"
back_color = "#003153"
plrMOVE_SPEED = 10
plrWIDTH = 22
plrHEIGHT = 20
JUMP = 10
GRAVITY = 0.40
plrCOLOR = "#18A7B5"

# Это класс платформ
class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


# Это класс игрока как обьекта где назодяться основные данные и формулы и условия
# В будующем планирую добавить к этому классу большую часть игры
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

    def update(self, left, right, up, platforms):
        if left:
            self.xvel = plrMOVE_SPEED * -1

        if right:
            self.xvel = plrMOVE_SPEED

        if not (left or right):
            self.xvel = 0
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
        for p in platforms:
            if sprite.collide_rect(self, p):

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


# авто-разрешение пока что бесполезно т. к. мне лень сейчас делать полный экран
# оказалось оно работает
def get_resolution():
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h
    return screen_width, screen_height

#
def main():
    pygame.init()
    screen = pygame.display.set_mode(get_resolution())
    pygame.display.set_caption("Alpha_0.1")
    screen.fill(Color(back_color))
    bg = pygame.Surface((get_resolution()))
    bg.fill(Color(back_color))
    hero = Player(55, 55)
    left = right = False
    up = False
    entities = pygame.sprite.Group()
    platforms = []
    entities.add(hero)
    level = [
        "-----------------------------------------------------",
        "-                                                   -",
        "-                                                   -",
        "-                                                   -",
        "-                                 -----------       -",
        "-                                                   -",
        "-                      -------                      -",
        "-                                                   -",
        "-     --------------                                -",
        "-                       -----                       -",
        "-                                                   -",
        "-                               ------------------  -",
        "-                                                   -",
        "-                                                   -",
        "-                     --------                      -",
        "-                                                   -",
        "-                                                   -",
        "-                                                   -",
        "-     ---------------                               -",
        "-                                                   -",
        "-                  -----------                      -",
        "-                                                   -",
        "-                                                   -",
        "-                         --------------            -",
        "-                                                   -",
        "-                                                   -",
        "-      --------                                     -",
        "-                                                   -",
        "-                                                   -",
        "-                                                   -",
        "-----------------------------------------------------"]

    running = True
    while running:
        x = y = 0
        for row in level:
            for col in row:
                if col == "-":
                    plat = Platform(x, y)
                    entities.add(plat)
                    platforms.append(plat)

                x += PLATFORM_WIDTH
            y += PLATFORM_HEIGHT
            x = 0
        for e in pygame.event.get():
            if e.type == QUIT:
                running = False
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYUP and e.key == K_UP:
                up = False
        hero.update(left, right, up, platforms)
        entities.draw(screen)
        pygame.display.update()
        pygame.time.Clock().tick(60)
        screen.blit(bg, (1, 1))


if __name__ == "__main__":
    main()