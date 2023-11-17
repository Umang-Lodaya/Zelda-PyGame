import pygame
from settings import *
from os import walk
from support import importFolder

class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, obstacleGroups, createAttack, destoryAttack):
        super().__init__(groups)
        self.image = pygame.image.load(r"graphics\test\player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, -26)
        self.obstaclesGroups = obstacleGroups
        self.createAttack = createAttack
        self.destroyAttack = destoryAttack

        self.importPlayerAssets()
        self.STATUS = 'down'

        self.speed = 5
        self.FRAME_INDEX = 0
        self.ANIMATION_SPEED = 0.15

        self.directions = pygame.math.Vector2()
        self.ATTACKING = False
        self.ATTACK_COOLDOWN = 400
        self.ATTACK_TIME = None

        self.WEAPON_INDEX = 0
        self.WEAPON = list(WEAPONS_DATA.keys())[self.WEAPON_INDEX]
        self.CAN_SWITCH_WEAPON = True
        self.SWITCH_COOLDOWN = 400
        self.WEAPON_SWITCH_TIME = None

    
    def getStatus(self):
        # IDLE
        if self.directions.x == 0 and self.directions.y == 0:
            if 'idle' not in self.STATUS and 'attack' not in self.STATUS:
                self.STATUS = self.STATUS + '_idle'
        
        # ATTACK
        if self.ATTACKING:
            self.directions.x = 0
            self.directions.y = 0
            if 'attack' not in self.STATUS:
                if 'idle' in self.STATUS:
                    self.STATUS = self.STATUS.replace('_idle', '')
                self.STATUS =  self.STATUS + '_attack'
        else:
            if 'attack' in self.STATUS:
                self.STATUS = self.STATUS.replace('_attack', '')
    
    def animate(self):
        animation = self.ANIMATIONS[self.STATUS]
        self.FRAME_INDEX += self.ANIMATION_SPEED 
        self.FRAME_INDEX %= len(animation)

        self.image = animation[int(self.FRAME_INDEX)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def importPlayerAssets(self):
        CHARACTER_PATH = r"graphics\player"
        self.ANIMATIONS = {
            'down':[], 'down_attack': [], 'down_idle': [],
            'left':[], 'left_attack': [], 'left_idle': [],
            'right':[], 'right_attack': [], 'right_idle': [],
            'up':[], 'up_attack': [], 'up_idle': [],
        }
        
        for animation in self.ANIMATIONS:
            path = CHARACTER_PATH + '/' + animation
            self.ANIMATIONS[animation] = importFolder(path)

    def input(self):
        if not self.ATTACKING:
            KEYS = pygame.key.get_pressed()

            # MOVEMENT INPUT
            if KEYS[pygame.K_UP]:
                self.directions.y = -1
                self.STATUS = 'up'
            elif KEYS[pygame.K_DOWN]:
                self.directions.y = 1
                self.STATUS = 'down'
            else:
                self.directions.y = 0

            if KEYS[pygame.K_LEFT]:
                self.directions.x = -1
                self.STATUS = 'left'
            elif KEYS[pygame.K_RIGHT]:
                self.STATUS = 'right'
                self.directions.x = 1
            else:
                self.directions.x = 0
            
            # ATTACK INPUT
            if KEYS[pygame.K_SPACE]:
                self.ATTACK_TIME = pygame.time.get_ticks()
                self.ATTACKING = True
                self.createAttack()
            
            # MAGIC INPUT
            if KEYS[pygame.K_LCTRL]:
                self.ATTACK_TIME = pygame.time.get_ticks()
                self.ATTACKING = True
                print("MAGIC")
            
            if KEYS[pygame.K_q] and self.CAN_SWITCH_WEAPON:
                self.CAN_SWITCH_WEAPON = False
                self.WEAPON_SWITCH_TIME = pygame.time.get_ticks()
                self.WEAPON_INDEX += 1
                self.WEAPON_INDEX %= len(WEAPONS_DATA)
                self.WEAPON = list(WEAPONS_DATA.keys())[self.WEAPON_INDEX]


    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstaclesGroups:
                # IF COLLIDED
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.directions.x > 0:  # RIGHT
                        self.hitbox.right = sprite.hitbox.left
                    elif self.directions.x < 0:  # LEFT
                        self.hitbox.left = sprite.hitbox.right
        else:
            for sprite in self.obstaclesGroups:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.directions.y > 0:  # DOWN
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.directions.y < 0:  # UP
                        self.hitbox.top = sprite.hitbox.bottom

    def move(self, speed):
        # TO MANAGE SPEED WHEN MOVING
        if self.directions.magnitude() != 0:
            self.directions = self.directions.normalize()

        self.hitbox.x += self.directions.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.directions.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def cooldowns(self):
        CURRENT_TIME = pygame.time.get_ticks()
        if self.ATTACKING and self.ATTACK_COOLDOWN <= (CURRENT_TIME - self.ATTACK_TIME):
            self.ATTACKING = False
            self.destroyAttack()
        
        if not self.CAN_SWITCH_WEAPON and self.SWITCH_COOLDOWN <= (CURRENT_TIME - self.WEAPON_SWITCH_TIME):
            self.CAN_SWITCH_WEAPON = True

    def update(self):
        self.input()
        self.cooldowns()
        self.getStatus()
        self.animate()
        self.move(self.speed)
