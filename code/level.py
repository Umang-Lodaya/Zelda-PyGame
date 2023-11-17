import pygame

from settings import *
from support import *

from tile import Tile
from player import Player
from random import choice
from weapon import Weapon
from ui import UI

from debug import debug


class Level:
    def __init__(self):
        self.DISPLAY_SURFACE = pygame.display.get_surface()
        self.VISIBLE_SPRITES = YSortCameraGroup()
        self.OBSTACLE_SPRITES = pygame.sprite.Group()

        self.currentAttack = None
        self.createMap()

        # UI
        self.ui = UI()

    def createMap(self):
        layouts = {
            "boundary": importCSV(r"map\map_FloorBlocks.csv"),
            "grass": importCSV(r"map\map_Grass.csv"),
            "object": importCSV(r"map\map_LargeObjects.csv")
            }
        
        graphics = {
            'grass': importFolder(r"graphics\grass"),
            'objects': importFolder(r"graphics\objects")
        }
        
        for style, layout in layouts.items():
            for i, row in enumerate(layout):
                for j, col in enumerate(row):
                    if col != "-1":
                        x, y = j * TILE_SIZE, i * TILE_SIZE # POSITION ON SCREEN
                        if style == "boundary":
                            Tile((x, y), [self.OBSTACLE_SPRITES], "invisible")
                        if style == "grass":
                            random_grass = choice(graphics["grass"])
                            Tile((x, y), [self.VISIBLE_SPRITES, self.OBSTACLE_SPRITES], 'grass', random_grass)
                        if style == "object":
                            surf = graphics["objects"][int(col)]
                            Tile((x, y), [self.VISIBLE_SPRITES, self.OBSTACLE_SPRITES], 'object', surf)


        self.PLAYER = Player(
            (1950, 1280), [self.VISIBLE_SPRITES], self.OBSTACLE_SPRITES, self.createAttack, self.destroyAttack
        )

    def createAttack(self):
        self.currentAttack = Weapon(self.PLAYER, [self.VISIBLE_SPRITES])
    
    def destroyAttack(self):
        if self.currentAttack:
            self.currentAttack.kill()
        self.currentAttack = None

    def run(self):
        self.VISIBLE_SPRITES.customDraw(self.PLAYER)
        self.VISIBLE_SPRITES.update()
        self.ui.display(self.PLAYER)
        # debug(self.PLAYER.STATUS)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.DISPLAY_SURFACE = pygame.display.get_surface()
        self.halfWidth, self.halfHeight = (
            self.DISPLAY_SURFACE.get_size()[0] // 2,
            self.DISPLAY_SURFACE.get_size()[1] // 2,
        )

        self.OFFSET = pygame.math.Vector2()

        # FLOOR
        self.FLOOR_SURFACE = pygame.image.load(r"graphics\tilemap\ground.png").convert()
        self.FLOOR_RECT = self.FLOOR_SURFACE.get_rect(topleft=(0, 0))

    def customDraw(self, player):
        # ADJUSTING PLAYER AT THE CENTER OF FRAME
        # TOP_LEFT - CURRENT_POS => OFFSET FROM TOP_LEFT
        self.OFFSET.x = player.rect.centerx - self.halfWidth
        self.OFFSET.y = player.rect.centery - self.halfHeight

        OFFSET_POS = self.FLOOR_RECT.topleft - self.OFFSET
        self.DISPLAY_SURFACE.blit(self.FLOOR_SURFACE, OFFSET_POS)

        for sprite in sorted(self.sprites(), key=lambda x: x.rect.centery):
            # THEN, ADD HALF-FRAME TO CENTER THE POS
            OFFSET_POS = sprite.rect.topleft - self.OFFSET
            self.DISPLAY_SURFACE.blit(sprite.image, OFFSET_POS)