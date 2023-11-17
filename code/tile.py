import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(
        self,
        position,
        groups,
        sprite_type,
        surface=pygame.Surface((TILE_SIZE, TILE_SIZE)),
    ):
        super().__init__(groups)
        self.image = surface
        if sprite_type == "object":
            self.rect = self.image.get_rect(
                topleft=(position[0], position[1] - TILE_SIZE)
            )
        else:
            self.rect = self.image.get_rect(topleft=position)
        
        self.hitbox = self.rect.inflate(0, 12)