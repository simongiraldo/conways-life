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

class Pause(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./sprites/pause.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = X_COORD_PAUSE
        self.rect.y = Y_COORD_PAUSE

class Restart(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./sprites/restart.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = X_COORD_RESTART
        self.rect.y = Y_COORD_RESTART

class Music(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./sprites/music.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = X_COORD_MUSIC
        self.rect.y = Y_COORD_MUSIC

class Click_banner(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./sprites/click_start.png").convert_alpha()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = X_COORD_CLICK_BANNER
        self.rect.y = Y_COORD_CLICK_BANNER
        self.speed_alpha = 2

    def set_alpha(self, alpha):
        self.image.set_alpha(alpha)

class Void_screen(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./sprites/initial_animation.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.speed_alpha = 2

    def set_alpha(self, alpha):
        self.image.set_alpha(alpha)

class Play_button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./sprites/play_button.png").convert_alpha()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50


class Game(object):
    def __init__(self):
        self.menu = True
        self.playing = True 
        self.squares = []
        self.areas = {}
        self.initial_animation = True
        self.initial_animation_screen = Void_screen()
        self.game_paused = False
        self.menu_background = pygame.image.load("./utils/img/menu.png").convert()
        self.menu_click_banner = Click_banner()
        self.menu_screen = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        self.paused_screen = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        self.pause_button = Pause()
        self.restart_button = Restart()
        self.music_button = Music()
        self.pause_sprites = pygame.sprite.Group()
        self.play_button = Play_button()
        self.grid_sprites = pygame.sprite.Group()

        self.pause_sprites.add(self.pause_button, self.restart_button, self.music_button)
        self.grid_sprites.add(self.play_button)

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

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu:
                    self.menu = False

                if not self.game_paused:
                    if self.play_button.rect.collidepoint(event.pos):
                        self.play_button.remove(self.grid_sprites)
                        print("Killed")
                    else:
                        square_coords = self.get_square_coord(event.pos)
                        self.areas[square_coords].update()

                elif self.game_paused:
                    if self.pause_button.rect.collidepoint(event.pos):
                        self.game_paused = False
                    elif self.restart_button.rect.collidepoint(event.pos):
                        self.__init__()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.menu:
                self.game_paused = not self.game_paused
                print("Space pressed")

    
    def run_logic(self):
        if self.initial_animation:
            last_alpha = self.initial_animation_screen.image.get_alpha()
            if last_alpha == 0:
                self.initial_animation = False
            else:
                new_alpha = last_alpha - self.initial_animation_screen.speed_alpha
                self.initial_animation_screen.set_alpha(new_alpha)

        if self.menu:
            last_alpha = self.menu_click_banner.image.get_alpha()
            new_alpha = last_alpha - self.menu_click_banner.speed_alpha
            if new_alpha <= 0 or new_alpha > 255:
                self.menu_click_banner.speed_alpha *= -1

            self.menu_click_banner.set_alpha(new_alpha)

        if self.game_paused:
            return

    def display_frame(self, screen):
        screen.fill(BACKGROUND_COLOR)

        if self.menu:
            self.menu_screen.blit(self.menu_background, FIRST_COORDS)
            self.menu_screen.blit(self.menu_click_banner.image, self.menu_click_banner.rect)

            if self.initial_animation:
                self.menu_screen.blit(self.initial_animation_screen.image, self.initial_animation_screen.rect)

            screen.blit(self.menu_screen, FIRST_COORDS)
            display.flip()
            return
        
        for square in self.squares:
            pygame.draw.rect(screen, WHITE_SMOKE, square.shape, width=square.width)
        self.grid_sprites.draw(screen)

        if self.game_paused:
            self.paused_screen.fill(WHITE_BLURRED)
            screen.blit(self.paused_screen, FIRST_COORDS)
            self.pause_sprites.draw(screen)

        display.flip()

    def get_square_coord(self, coords):
        x_mouse = coords[0]
        y_mouse = coords[1]

        x_coord = 0
        y_coord = 0

        if x_mouse <= SQUARE_WIDTH and y_mouse <= SQUARE_HEIGHT:
            return FIRST_COORDS
        
        if x_mouse % SQUARE_WIDTH == 0:
            x_coord = ((x_mouse // SQUARE_WIDTH) - 1) * SQUARE_WIDTH
        else:
            x_coord = (x_mouse // SQUARE_WIDTH) * SQUARE_WIDTH

        if y_mouse % SQUARE_HEIGHT == 0:
            y_coord = ((y_mouse // SQUARE_HEIGHT) - 1) * SQUARE_HEIGHT
        else:
            y_coord = (y_mouse // SQUARE_HEIGHT) * SQUARE_HEIGHT

        return (x_coord, y_coord)

def run():
    pygame.init()
    display.init()

    screen = display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Conway's life game")

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


# Añadir menu de inicio, tal vez con un enlance a una pagina que explique de que trata el juego
# Hacer que al click en restart, hacer una transicion lenta
# 
# (El sonido puede ser una feature para despues)
# 