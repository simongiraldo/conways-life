import pygame
from src.game.game import Game
from src.utils.constants import SCREEN_SIZE


def run():
    pygame.init()
    pygame.display.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Conway's life game")

    clock = pygame.time.Clock()

    game = Game()

    while game.playing:
        game.proccess_events()

        game.run_logic()

        game.display_frames(screen)

        clock.tick(game.fps)
        
    pygame.quit()


if __name__ == "__main__":
    run()