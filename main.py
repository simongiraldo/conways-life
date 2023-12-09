import pygame
from src.game.game import Game
from src.utils.constants import SCREEN_SIZE, FPS


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

        game.display_frame(screen)

        clock.tick(game.fps)
        
    pygame.quit()


if __name__ == "__main__":
    run()


# TODO:
# Actalizar el readme con link a paginas con info sobre el juego y poner la info en general del proyeco
# Crear subfunciones para hacer el codigo mas legible y menos spaguetthi
# Separar cada clase en archivos diferentes?
# Hacer que al darle pause, poder parar la ejecucion y ver bien el patron, sin tener que mostar el menu de pause (Tal vez mover los botones en una parte de abajo del grid)
# Hacer una opcion de grid dinamico, mientras se ejecuten las generaciones, puedo vivir o matar cuadros. Harian parte de la generacion despues de 2 segundos de haber hecho click 
# Hacer que el tablero sea infinito, al pasar por el lado derecho, que vuelva por l izquierdo
# 
# (El sonido puede ser una feature para despues)
# 