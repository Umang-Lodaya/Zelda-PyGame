import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, obstacleGroups):
        super().__init__(groups)
        self.image = pygame.image.load(r"graphics\test\player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = position)

        self.directions = pygame.math.Vector2()
        self.speed = 5
        self.obstaclesGroups = obstacleGroups

    def input(self):
        KEYS = pygame.key.get_pressed()
        if KEYS[pygame.K_UP]:
            self.directions.y = -1
        elif KEYS[pygame.K_DOWN]:
            self.directions.y = 1
        else:
            self.directions.y = 0
        
        if KEYS[pygame.K_LEFT]:
            self.directions.x = -1
        elif KEYS[pygame.K_RIGHT]:
            self.directions.x = 1
        else:
            self.directions.x = 0
    
    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstaclesGroups:
                if sprite.rect.colliderect(self.rect):
                    if self.directions.x > 0: # RIGHT
                        self.rect.right = sprite.rect.left
                    elif self.directions.x < 0: # LEFT
                        self.rect.left = sprite.rect.right
        else:
            for sprite in self.obstaclesGroups:
                if sprite.rect.colliderect(self.rect):
                    if self.directions.y > 0: # DOWN
                        self.rect.bottom = sprite.rect.top
                    elif self.directions.y < 0: # UP
                        self.rect.top = sprite.rect.bottom

    
    def move(self, speed):
        # TO MANAGE SPEED WHEN MOVING
        if self.directions.magnitude() != 0:
            self.directions = self.directions.normalize()
        
        self.rect.x += self.directions.x * speed
        self.collision('horizontal')
        self.rect.y += self.directions.y * speed
        self.collision('vertical')

    def update(self):
        self.input()
        self.move(self.speed)