import sys
import pygame

import time
from random import choice, randint

from settings import *
from support import *

from particle import AnimationPlayer
from upgrade import Upgrade
from magic import MagicPlayer
from tile import Tile
from player import Player
from weapon import Weapon
from ui import UI
from enemy import Enemy
from debug import debug


class Level:
    def __init__(self):
        self.DISPLAY_SURFACE = pygame.display.get_surface()
        self.VISIBLE_SPRITES = YSortCameraGroup()
        self.OBSTACLE_SPRITES = pygame.sprite.Group()
        self.GAME_PAUSED = False
        self.GAMEOVER = False

        self.currentAttack = None
        self.ATTACK_SPRITE = pygame.sprite.Group()
        self.ATTACKABLE_SPRITE = pygame.sprite.Group()

        self.createMap()

        # UI
        self.ui = UI()

        # PARTICLES
        self.ANIMATION_PLAYER = AnimationPlayer()
        self.MAGIC_PLAYER = MagicPlayer(self.ANIMATION_PLAYER)
        self.UPGRADE = Upgrade(self.PLAYER)

    def createMap(self):
        layouts = {
            "boundary": importCSV(r"map\map_FloorBlocks.csv"),
            "grass": importCSV(r"map\map_Grass.csv"),
            "object": importCSV(r"map\map_LargeObjects.csv"),
            "entities": importCSV(r"map\map_Entities.csv")
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
                            Tile((x, y), 
                                    [self.VISIBLE_SPRITES, self.OBSTACLE_SPRITES, self.ATTACKABLE_SPRITE], 
                                    'grass', random_grass)
                        if style == "object":
                            surf = graphics["objects"][int(col)]
                            Tile((x, y), [self.VISIBLE_SPRITES, self.OBSTACLE_SPRITES], 'object', surf)
                        if style == 'entities':
                            if col == "394":
                                self.PLAYER = Player(
                                    (x, y), [self.VISIBLE_SPRITES], 
                                    self.OBSTACLE_SPRITES, self.createAttack, self.destroyAttack, self.createMagic
                                )
                            else:
                                monsters = {"390": "bamboo", "391": "spirit", "392": "raccoon"}
                                name = monsters.get(col, "squid")
                                Enemy(name, (x, y), 
                                        [self.VISIBLE_SPRITES, self.ATTACKABLE_SPRITE], 
                                        self.OBSTACLE_SPRITES, self.damagePlayer, self.createDeathParticles, self.addEXP)

    def createAttack(self):
        self.currentAttack = Weapon(self.PLAYER, [self.VISIBLE_SPRITES, self.ATTACK_SPRITE])
    
    def destroyAttack(self):
        if self.currentAttack:
            self.currentAttack.kill()
        self.currentAttack = None

    def createMagic(self, style, strength, cost):
        if style == 'heal':
            self.MAGIC_PLAYER.heal(self.PLAYER, strength, cost, [self.VISIBLE_SPRITES])
        elif style == 'flame':
            self.MAGIC_PLAYER.flame(self.PLAYER, cost, [self.VISIBLE_SPRITES, self.ATTACK_SPRITE])
    
    def playerAttackLogic(self):
        if self.ATTACK_SPRITE:
            for attack in self.ATTACK_SPRITE:
                collisions = pygame.sprite.spritecollide(attack, self.ATTACKABLE_SPRITE, False)
                if collisions:
                    for target in collisions:
                        if target.sprite_type == 'grass':
                            pos = target.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for leaf in range(randint(3, 6)):
                                self.ANIMATION_PLAYER.createGrassParticles(pos - offset, [self.VISIBLE_SPRITES])
                            target.kill()
                        else:
                            target.getDamage(self.PLAYER, attack.sprite_type)

    def damagePlayer(self, amount, type):
        if self.PLAYER.VULNARABLE:
            self.PLAYER.HEALTH -= amount
            if self.PLAYER.HEALTH <= 0:
                self.GAMEOVER = True
            self.PLAYER.VULNARABLE = False
            self.PLAYER.HIT_TIME = pygame.time.get_ticks()
            self.ANIMATION_PLAYER.createParticles(type, self.PLAYER.rect.center, [self.VISIBLE_SPRITES])
    
    def createDeathParticles(self, pos, type):
        self.ANIMATION_PLAYER.createParticles(type, pos, [self.VISIBLE_SPRITES])
    
    def addEXP(self, amount):
        self.PLAYER.EXP += amount
    
    def run(self):
        if self.GAMEOVER:
            sys.exit()
        
        self.VISIBLE_SPRITES.customDraw(self.PLAYER)
        self.ui.display(self.PLAYER)

        if self.GAME_PAUSED:
            self.UPGRADE.display()
        else:
            self.VISIBLE_SPRITES.update()
            self.VISIBLE_SPRITES.enemyUpdate(self.PLAYER)
            self.playerAttackLogic()
    
    def toggleMenu(self):
        self.GAME_PAUSED = not self.GAME_PAUSED

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
    
    def enemyUpdate(self, player):
        enemySprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemySprites:
            enemy.enemyUpdate(player)