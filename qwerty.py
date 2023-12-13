import random
import pygame
import pygame.font
from pygame.locals import *


# авто-разрешение .
def get_resolution():
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h
    return screen_width, screen_height


# иницализация игры
def initialize_game():
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 24)
    clock = pygame.time.Clock()
    screen_width, screen_height = get_resolution()
    fps_max = 60
    screen = pygame.display.set_mode((screen_width, screen_height),
                                     pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN, 32)
    pygame.display.set_caption("Test")
    return clock, screen, fps_max, font


def display_fps(screen, clock, font):
    fps = clock.get_fps()
    fps_surface = pygame.Surface((50, 50))
    fps_surface.set_alpha(128)
    fps_text = font.render(str(int(fps)), True, (0, 255, 0))
    fps_surface.blit(fps_text, (0, 0))
    fps_surface = fps_surface.convert_alpha()
    screen.blit(fps_surface, (10, 10))


# класс спрайта
def handle_events():
    return all(event.type != QUIT for event in pygame.event.get())


# заполняет экран серым (пока что неактивно)
def draw_screen(screen):
    screen.fill((127, 127, 127))


# должен обновлять картинку но пока что тоже не активно
def update_screen():
    ...


# выводит разрешение и максимальный фпс в консоль
def debug():
    print("resolution auto:", get_resolution())
    print("max FPS:", initialize_game()[2])


# основная функция
def main():
    clock, screen, fps_max, font = initialize_game()
    running = True
    draw_screen(screen)
    debug()
    while running:
        clock.tick(fps_max)
        display_fps(screen, clock, font)
        running = handle_events()
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
