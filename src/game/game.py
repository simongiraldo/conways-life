import pygame
from ..sprites.square import Square
from ..sprites.pause import Pause
from ..sprites.restart import Restart
from ..sprites.music import Music
from ..sprites.click_banner import ClickBanner
from ..sprites.void_screen import VoidScreen
from ..sprites.play import Play
from ..sprites.pause import Pause
from ..utils.constants import *
from ..utils.colors import *


class Game(object):
    def __init__(self):
        self.playing = True
        self.fps = FPS
        self._menu = True
        self._initial_animation = True
        self._game_paused = True
        self._executing = False
        self._alive_squares = []
        self._squares = []
        self._areas = {}
        self._initial_animation_screen = VoidScreen()
        self._menu_background = pygame.image.load("./assets/static/menu.png").convert()
        self._menu_click_banner = ClickBanner()
        self._menu_screen = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        self._options_menu_rect = pygame.Rect(0, GRID_HEIGHT, SCREEN_WIDTH, OPTIONS_MENU_HEIGHT)
        self._play_button = Play()
        self._pause_button = Pause()
        self._restart_button = Restart()
        self._music_button = Music()
        self._options_menu_sprites = pygame.sprite.Group()

        self._options_menu_sprites.add(self._play_button, self._restart_button, self._music_button)
        self.set_initial_squares()

    def set_initial_squares(self):
        x_coord = 0
        y_coord = 0
        while True:
            if x_coord > SCREEN_WIDTH:
                x_coord = 0
                y_coord += SQUARE_HEIGHT
            if y_coord >= GRID_HEIGHT:
                break

            square = Square(x_coord, y_coord)
            self._squares.append(square)

            area = (x_coord, y_coord)
            self._areas[area] = square

            x_coord += SQUARE_WIDTH

    def proccess_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self._menu:
                    self._menu = False
                    self.fps = GRID_FPS
                    continue

                if self._options_menu_rect.collidepoint(event.pos):
                    if self._pause_button.rect.collidepoint(event.pos):
                        self.change_play_pause_button()
                    elif self._restart_button.rect.collidepoint(event.pos):
                        self.__init__()
                else:
                    self.paint_square_clicked(event.pos)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self._menu:
                self.change_play_pause_button()

    def paint_square_clicked(self, coords):
        square_coords = self.get_square_coords_by_click(coords)
        square = self._areas[square_coords]
        square.update()
        if square.is_alive():
            self._alive_squares.append(square)
            self.set_alive_to_neighbors(square)

        elif square.is_dead():
            self._alive_squares.remove(square)
            self.set_dead_to_neighbors(square)

    def set_alive_to_neighbors(self, square):
        for i in range(NEIGHBORS_QUANTITY):
            coords = square.neighbors_areas[i]
            if self._areas.get(coords, NOT_FOUND) == NOT_FOUND:
                continue
            self._areas[coords].increment_alive_neighbors()

    def set_dead_to_neighbors(self, square):
        for i in range(NEIGHBORS_QUANTITY):
            coords = square.neighbors_areas[i]
            if self._areas.get(coords, NOT_FOUND) == NOT_FOUND:
                continue
            self._areas[coords].decrement_alive_neighbors()

    def change_play_pause_button(self):
        if self._options_menu_sprites.has(self._play_button):
            self._play_button.remove(self._options_menu_sprites)
            self._options_menu_sprites.add(self._pause_button)
            self._executing = True
            self._game_paused = False
        else:
            self._pause_button.remove(self._options_menu_sprites)
            self._options_menu_sprites.add(self._play_button)
            self._executing = False
            self._game_paused = True

    def run_logic(self):
        if self._initial_animation:
            self.run_initial_animation()

        if self._menu:
            self.run_click_banner_animation()

        if self._game_paused:
            return

        if self._executing:
            self.next_generation()

    def run_initial_animation(self):
        last_alpha = self._initial_animation_screen.image.get_alpha()
        if last_alpha == 0:
            self._initial_animation = False
        else:
            new_alpha = last_alpha - self._initial_animation_screen.get_speed_alpha()
            self._initial_animation_screen.image.set_alpha(new_alpha)

    def run_click_banner_animation(self):
        last_alpha = self._menu_click_banner.image.get_alpha()
        new_alpha = last_alpha - self._menu_click_banner.get_speed_alpha()
        if new_alpha <= 0 or new_alpha > 255:
            self._menu_click_banner.change_speed_alpha_sign()

        self._menu_click_banner.image.set_alpha(new_alpha)

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

    def display_frames(self, screen):
        screen.fill(BACKGROUND_COLOR)

        if self._menu:
            self._menu_screen.blit(self._menu_background, FIRST_COORDS)
            self._menu_screen.blit(self._menu_click_banner.image, self._menu_click_banner.rect)

            if self._initial_animation:
                self._menu_screen.blit(self._initial_animation_screen.image, 
                                       self._initial_animation_screen.rect)

            screen.blit(self._menu_screen, FIRST_COORDS)
            pygame.display.flip()
            return
        
        for square in self._squares:
            pygame.draw.rect(screen, WHITE_SMOKE, square.shape, width=square.get_width())

        self._options_menu_sprites.draw(screen)
        pygame.draw.rect(screen, WHITE_BLURRED, self._options_menu_rect, width=0)

        self._options_menu_sprites.draw(screen)

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
