import pygame
from src.game.game import Game
from src.utils.constants import SCREEN_SIZE

def run():
    pygame.init()
    pygame.display.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Conway's life game")

    icon = pygame.image.load("./assets/static/icon.png").convert()
    pygame.display.set_icon(icon)

    pygame.mixer.music.load("./assets/music/interestellar.mp3", "mp3")
    pygame.mixer.music.play(loops=-1)

    clock = pygame.time.Clock()

    game = Game()

    while game.playing:
        game.proccess_events()

        game.run_logic()

        game.display_frames(screen)

        clock.tick(game.fps)

    pygame.mixer.music.unload()
    pygame.quit()


if __name__ == "__main__":
    run()
