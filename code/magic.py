import pygame
from settings import *
from random import randint

class MagicPlayer:
    def __init__(self, ANIMATION_PLAYER):
        self.ANIMATION_PLAYER = ANIMATION_PLAYER
        self.SOUNDS = {
            'heal': pygame.mixer.Sound(r"audio\heal.wav"),
            'flame': pygame.mixer.Sound(r"audio\fire.wav")
        }

    def heal(self, player, strength, cost, groups):
        if player.ENERGY >= cost:
            player.ENERGY -= cost
            self.SOUNDS['heal'].play()
            player.HEALTH += strength
            player.HEALTH = min(player.HEALTH, player.STATS['health'])
            self.ANIMATION_PLAYER.createParticles('aura', player.rect.center, groups)
            self.ANIMATION_PLAYER.createParticles('heal', player.rect.center, groups)

    def flame(self, player, cost, groups):
        if player.ENERGY >= cost:
            player.ENERGY -= cost
            self.SOUNDS['flame'].play()
            if player.STATUS.split("_")[0] == "right": direction = pygame.math.Vector2(1, 0)
            elif player.STATUS.split("_")[0] == "left": direction = pygame.math.Vector2(-1, 0)
            elif player.STATUS.split("_")[0] == "up": direction = pygame.math.Vector2(0, -1)
            else: direction = pygame.math.Vector2(0, 1)
            
            for i in range(1, 6):
                if direction.x:
                    offset_x = direction.x * i * TILE_SIZE
                    x = player.rect.centerx + direction.x + offset_x + randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                    y = player.rect.centery + randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                    self.ANIMATION_PLAYER.createParticles('flame', (x, y), groups)
                else:
                    offset_y = direction.y * i * TILE_SIZE
                    x = player.rect.centerx + randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                    y = player.rect.centery + direction.y + offset_y + randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                    self.ANIMATION_PLAYER.createParticles('flame', (x, y), groups)