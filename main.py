import pygame, sys
import pygame.display as display
from utils.colors import *


def draw_initial_scene(screen):
    screen.fill(WHITE)

    pygame.draw.circle(surface=screen, color=YELLOW, radius=100, center=(0, 0))


def start_game(screen):
    while True:
        quit_game_if_closes_screen()

        draw_initial_scene(screen)

        display.flip()


def quit_game_if_closes_screen():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def run():
    pygame.init()
    display.init()

    screen = display.set_mode(size=(700, 700))
    #screen = display.set_mode(size=(700, 700), flags=pygame.NOFRAME)
    start_game(screen)


if __name__ == "__main__":
    run()
