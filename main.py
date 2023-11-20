import pygame
import pygame.display as display
from utils.colors import *
from utils.constants import *

class Square():
    def __init__(self, x, y):
        self.shape = pygame.Rect(
            x,
            y,
            SQUARE_WIDTH,
            SQUARE_HEIGHT
        )
        self.area = (x+30, y+30)
        self.width = 1

    def update(self):
        if self.width == 1:
            self.born()
        else:
            self.die()

    def born(self):
        self.width = 0

    def die(self):
        self.width = 1


class Game(object):
    def __init__(self):
        self.playing = True 
        self.squares = []
        self.areas = {}

        x_coord = 0
        y_coord = 0
        while True:
            square = Square(x_coord, y_coord)
            self.squares.append(square)

            area = (x_coord, y_coord)
            self.areas[area] = square

            x_coord += SQUARE_WIDTH

            if x_coord > SCREEN_WIDTH:
                x_coord = 0
                y_coord += SQUARE_HEIGHT
            if y_coord > SCREEN_HEIGHT:
                break

    def proccess_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x_mouse, y_mouse = event.pos
                mouse_position = (x_mouse, y_mouse)
                for area, square in self.areas.items():
                    if pygame.Rect(area, (SQUARE_WIDTH, SQUARE_HEIGHT)).collidepoint(mouse_position):
                        square.update()
                        break
    
    def run_logic(self):
        pass

    def display_frame(self, screen):
        screen.fill(BACKGROUND_COLOR)

        for square in self.squares:
            pygame.draw.rect(screen, WHITE_SMOKE, square.shape, width=square.width)

        display.flip()


def run():
    pygame.init()
    display.init()

    screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()

    game = Game()

    while game.playing:
        game.proccess_events()

        game.run_logic()

        game.display_frame(screen)

        clock.tick(FPS)
        
    pygame.quit()


if __name__ == "__main__":
    run()
