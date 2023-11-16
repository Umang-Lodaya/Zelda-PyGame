from settings import *
from tile import Tile
from player import Player

import pygame

class Level:
    def __init__(self):
        self.DISPLAY_SURFACE = pygame.display.get_surface()
        self.VISIBLE_SPRITES = pygame.sprite.Group()
        self.OBSTACLE_SPRITES = pygame.sprite.Group()
        self.createMap()
    
    def createMap(self):
        for i, row in enumerate(WORLD_MAP):
            for j, col in enumerate(row):
                x, y = j * TILE_SIZE, i * TILE_SIZE
                if col == 'x':
                    Tile((x, y), [self.VISIBLE_SPRITES, self.OBSTACLE_SPRITES])
                if col == 'p':
                    Player((x, y), [self.VISIBLE_SPRITES])

    def run(self):
        self.VISIBLE_SPRITES.draw(self.DISPLAY_SURFACE)

