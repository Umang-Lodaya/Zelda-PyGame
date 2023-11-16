from settings import *
from tile import Tile
from player import Player
from debug import debug

import pygame

class Level:
    def __init__(self):
        self.DISPLAY_SURFACE = pygame.display.get_surface()
        self.VISIBLE_SPRITES = YSortCameraGroup()
        self.OBSTACLE_SPRITES = pygame.sprite.Group()
        self.createMap()
    
    def createMap(self):
        for i, row in enumerate(WORLD_MAP):
            for j, col in enumerate(row):
                x, y = j * TILE_SIZE, i * TILE_SIZE
                if col == 'x':
                    Tile((x, y), [self.VISIBLE_SPRITES, self.OBSTACLE_SPRITES])
                if col == 'p':
                    self.PLAYER = Player((x, y), [self.VISIBLE_SPRITES], self.OBSTACLE_SPRITES)

    def run(self):
        self.VISIBLE_SPRITES.customDraw(self.PLAYER)
        self.VISIBLE_SPRITES.update()
        # debug(self.PLAYER.directions)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.DISPLAY_SURFACE = pygame.display.get_surface()
        self.halfWidth, self.halfHeight = self.DISPLAY_SURFACE.get_size()[0] // 2, self.DISPLAY_SURFACE.get_size()[1] // 2
        self.OFFSET = pygame.math.Vector2()
    
    def customDraw(self, player):
        for sprite in sorted(self.sprites(), key = lambda x: x.rect.centery):
            # ADJUSTING PLAYER AT THE CENTER OF FRAME
            # TOP_LEFT - CURRENT_POS => OFFSET FROM TOP_LEFT
            # THEN, ADD HALF-FRAME TO CENTER THE POS

            self.OFFSET.x = player.rect.centerx - self.halfWidth
            self.OFFSET.y = player.rect.centery - self.halfHeight

            OFFSET_POS = sprite.rect.topleft - self.OFFSET

            self.DISPLAY_SURFACE.blit(sprite.image, OFFSET_POS)