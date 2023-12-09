from pygame import Rect
from ..utils.constants import *


class Square():
    def __init__(self, x, y):
        self.shape = Rect(
            x,
            y,
            SQUARE_WIDTH,
            SQUARE_HEIGHT
        )
        self.neighbors_areas = [
            (x-30, y-30),
            (x, y-30),
            (x+30, y-30), 
            (x-30, y),
            (x+30, y),
            (x-30, y+30),
            (x, y+30),
            (x+30, y+30)
        ]
        self._width = 1
        self._alive_neighbors = 0

    def update(self):
        if self._width == 1:
            self.born()
        else:
            self.die()

    def get_width(self):
        return self._width
    
    def born(self):
        self._width = 0

    def die(self):
        self._width = 1

    def is_alive(self):
        return self._width == 0
    
    def is_dead(self):
        return self._width == 1
    
    def get_alive_neighbors(self):
        return self._alive_neighbors

    def increment_alive_neighbors(self):
        self._alive_neighbors += 1

    def decrement_alive_neighbors(self):
        self._alive_neighbors -= 1