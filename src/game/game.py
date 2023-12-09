import pygame
from ..sprites.square import Square
from ..sprites.pause import Pause
from ..sprites.restart import Restart
from ..sprites.music import Music
from ..sprites.click_banner import Click_banner
from ..sprites.void_screen import Void_screen
from ..sprites.play_button import Play_button
from ..utils.constants import *
from ..utils.colors import *


class Game(object):
    def __init__(self):
        self.playing = True
        self.fps = FPS
        self._menu = True
        self._initial_animation = True
        self._game_paused = False
        self._executing = False
        self._alive_squares = []
        self._squares = []
        self._areas = {}
        self._initial_animation_screen = Void_screen()
        self._menu_background = pygame.image.load("./assets/static/menu.png").convert()
        self._menu_click_banner = Click_banner()
        self._menu_screen = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        self._paused_screen = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        self._pause_button = Pause()
        self._restart_button = Restart()
        self._music_button = Music()
        self._pause_sprites = pygame.sprite.Group()
        self._play_button = Play_button()
        self._grid_sprites = pygame.sprite.Group()

        self._pause_sprites.add(self._pause_button, self._restart_button, self._music_button)
        self._grid_sprites.add(self._play_button)

        x_coord = 0
        y_coord = 0
        while True:
            square = Square(x_coord, y_coord)
            self._squares.append(square)

            area = (x_coord, y_coord)
            self._areas[area] = square

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
                if self._menu:
                    self._menu = False
                    self.fps = GRID_FPS
                    continue

                if not self._game_paused and not self._executing:
                    if self._play_button.rect.collidepoint(event.pos):
                        self._play_button.remove(self._grid_sprites)
                        self._executing = True
                    else:
                        square_coords = self.get_square_coords_by_click(event.pos)
                        square = self._areas[square_coords] 
                        square.update()
                        if square.get_width() == 0:
                            self._alive_squares.append(square)
                            for i in range(NEIGHBORS_QUANTITY):
                                coords = square.neighbors_areas[i]
                                if self._areas.get(coords, NOT_FOUND) == NOT_FOUND:
                                    continue

                                self._areas[coords].increment_alive_neighbors()
                        elif square.get_width() == 1:
                            self._alive_squares.remove(square)
                            for i in range(NEIGHBORS_QUANTITY):
                                coords = square.neighbors_areas[i]
                                if self._areas.get(coords, NOT_FOUND) == NOT_FOUND:
                                    continue

                                self._areas[coords].decrement_alive_neighbors()

                elif self._game_paused:
                    if self._pause_button.rect.collidepoint(event.pos):
                        self._game_paused = False
                    elif self._restart_button.rect.collidepoint(event.pos):
                        self.__init__()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self._menu:
                self._game_paused = not self._game_paused

    
    def run_logic(self):
        if self._initial_animation:
            last_alpha = self._initial_animation_screen.image.get_alpha()
            if last_alpha == 0:
                self._initial_animation = False
            else:
                new_alpha = last_alpha - self._initial_animation_screen.get_speed_alpha()
                self._initial_animation_screen.image.set_alpha(new_alpha)

        if self._menu:
            last_alpha = self._menu_click_banner.image.get_alpha()
            new_alpha = last_alpha - self._menu_click_banner.get_speed_alpha()
            if new_alpha <= 0 or new_alpha > 255:
                self._menu_click_banner.change_speed_alpha_sign()

            self._menu_click_banner.image.set_alpha(new_alpha)

        if self._game_paused:
            return
        
        if self._executing:
            self.next_generation()
    
    def next_generation(self):
        squares_to_die = []
        squares_to_live = []
        for square in self._squares:
            neighbors = square.get_alive_neighbors()

            if square.is_alive() and neighbors > 3:
                # dies cause overpopulaton
                squares_to_die.append(square)

            if square.is_alive() and (neighbors == 2 or neighbors == 3):
                # Stays alive cause stabiliy
                continue

            if square.is_alive() and neighbors < 2:
                # dies cause underpopulation
                squares_to_die.append(square)

            if square.is_dead() and neighbors == 3:
                # Lives cause perfect company
                squares_to_live.append(square)
        
        self.kill_squares(squares_to_die)
        self.born_squares(squares_to_live)


    def kill_squares(self, squares_to_die):
        for square in squares_to_die:
            square.die()
            for i in range(NEIGHBORS_QUANTITY):
                coords = square.neighbors_areas[i]
                if self._areas.get(coords, NOT_FOUND) == NOT_FOUND:
                    continue

                self._areas[coords].decrement_alive_neighbors()

    def born_squares(self, squares_to_live):
        for square in squares_to_live:
            square.born()
            for i in range(NEIGHBORS_QUANTITY):
                coords = square.neighbors_areas[i]
                if self._areas.get(coords, NOT_FOUND) == NOT_FOUND:
                    continue

                self._areas[coords].increment_alive_neighbors()



    def display_frame(self, screen):
        screen.fill(BACKGROUND_COLOR)

        if self._menu:
            self._menu_screen.blit(self._menu_background, FIRST_COORDS)
            self._menu_screen.blit(self._menu_click_banner.image, self._menu_click_banner.rect)

            if self._initial_animation:
                self._menu_screen.blit(self._initial_animation_screen.image, self._initial_animation_screen.rect)

            screen.blit(self._menu_screen, FIRST_COORDS)
            pygame.display.flip()
            return
        
        for square in self._squares:
            pygame.draw.rect(screen, WHITE_SMOKE, square.shape, width=square.get_width())
        self._grid_sprites.draw(screen)

        if self._game_paused:
            self._paused_screen.fill(SQUARE_BORDER_COLOR)
            screen.blit(self._paused_screen, FIRST_COORDS)
            self._pause_sprites.draw(screen)

        pygame.display.flip()

    def get_square_coords_by_click(self, coords):
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
