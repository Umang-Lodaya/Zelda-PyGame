from entity import Entity
from settings import *
import pygame
from support import *

class Enemy(Entity):
    def __init__(self, monsterName, position, groups, obstaclesGroups, damagePlayer):
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # GRAPHICS
        self.importGraphics(monsterName)
        self.STATUS = 'idle'
        self.image = self.ANIMATIONS[self.STATUS][self.FRAME_INDEX]
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstaclesGroups = obstaclesGroups

        # stats
        self.MONSTER_NAME = monsterName
        MONSTER_INFO = ENEMY_DATA[self.MONSTER_NAME]
        self.HEALTH = MONSTER_INFO['health']
        self.EXP = MONSTER_INFO['exp']
        self.SPEED = MONSTER_INFO['speed']
        self.ATTACK_DAMAGE = MONSTER_INFO['damage']
        self.RESISTANCE = MONSTER_INFO['resistance']
        self.ATTACK_RADIUS = MONSTER_INFO['attack_radius']
        self.NOTICE_RADIUS = MONSTER_INFO['notice_radius']
        self.ATTACK_TYPE = MONSTER_INFO['attack_type']

        # PLAYER INTERACTION
        self.CAN_ATTACK = True
        self.ATTACK_TIME = None
        self.ATTACK_COOLDOWN = 400

        self.VULNARABLE = True
        self.HIT_TIME = None
        self.INVINCIBILITY_DURATION = 300
        self.damagePlayer = damagePlayer
    
    def importGraphics(self, name):
        CHARACTER_PATH = f"graphics\monsters\{name}"
        self.ANIMATIONS = {
            'move':[], 'attack': [], 'idle': []
        }
        
        for animation in self.ANIMATIONS:
            path = CHARACTER_PATH + '/' + animation
            self.ANIMATIONS[animation] = importFolder(path)
    
    def getPlayerInfo(self, player):
        enemyVec = pygame.math.Vector2(self.rect.center)
        playerVec = pygame.math.Vector2(player.rect.center)
        distance = (playerVec - enemyVec).magnitude()
        if distance > 0:
            direction = (playerVec - enemyVec).normalize()
        else:
            direction = pygame.math.Vector2((0, 0))

        return distance, direction
    
    def actions(self, player):
        if self.STATUS == "attack":
            self.damagePlayer(self.ATTACK_DAMAGE, self.ATTACK_TYPE)
            self.ATTACK_TIME = pygame.time.get_ticks()
        elif self.STATUS == "move":
            self.directions = self.getPlayerInfo(player)[1]
        else:
            self.directions = pygame.math.Vector2((0, 0))

    def getStatus(self, player):
        distance = self.getPlayerInfo(player)[0]

        if distance <= self.ATTACK_RADIUS and self.CAN_ATTACK:
            if self.STATUS != "attack":
                self.FRAME_INDEX = 0
            self.STATUS = "attack"
        elif distance <= self.NOTICE_RADIUS:
            self.STATUS = "move"
        else:
            self.STATUS = "idle"

    def animate(self):
        animation = self.ANIMATIONS[self.STATUS]
        self.FRAME_INDEX += self.ANIMATION_SPEED 
        if self.FRAME_INDEX >= len(animation):
            if self.STATUS == "attack":
                self.CAN_ATTACK = False
            self.FRAME_INDEX = 0

        self.image = animation[int(self.FRAME_INDEX)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.VULNARABLE:
            alpha = self.waveValue()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def update(self):
        self.hitReaction()
        self.move(self.SPEED)
        self.animate()
        self.cooldown()
        self.checkDeath()
    
    def cooldown(self):
        CURRENT_TIME = pygame.time.get_ticks()
        if not self.CAN_ATTACK:
            if CURRENT_TIME - self.ATTACK_TIME >= self.ATTACK_COOLDOWN:
                self.CAN_ATTACK = True
        
        if not self.VULNARABLE:
            if CURRENT_TIME - self.HIT_TIME >= self.INVINCIBILITY_DURATION:
                self.VULNARABLE = True


    def getDamage(self, player, attack_type):
        if self.VULNARABLE:
            self.directions = self.getPlayerInfo(player)[1]
            if attack_type == 'weapon':
                self.HEALTH -= player.getWeaponDamage()
            else:
                pass
            self.HIT_TIME = pygame.time.get_ticks()
            self.VULNARABLE = False
    
    def hitReaction(self):
        if not self.VULNARABLE:
            self.directions *= -self.RESISTANCE
    
    def checkDeath(self):
        if self.HEALTH <= 0:
            self.kill()

    def enemyUpdate(self, player):
        self.actions(player)
        self.getStatus(player)