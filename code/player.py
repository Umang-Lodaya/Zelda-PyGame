import pygame
from settings import *
from os import walk
from support import importFolder
from entity import Entity

class Player(Entity):
    def __init__(self, position, groups, obstacleGroups, createAttack, destoryAttack, createMagic):
        super().__init__(groups)
        self.image = pygame.image.load("../graphics/test/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET['player'])
        self.obstaclesGroups = obstacleGroups
        self.createAttack = createAttack
        self.destroyAttack = destoryAttack

        self.createMagic = createMagic
        self.importPlayerAssets()
        
        # MOVEMENTS
        self.STATUS = 'down'
        
        # WEAPONS
        self.ATTACKING = False
        self.ATTACK_COOLDOWN = 400
        self.ATTACK_TIME = None
        self.WEAPON_INDEX = 0
        self.WEAPON = list(WEAPONS_DATA.keys())[self.WEAPON_INDEX]
        self.CAN_SWITCH_WEAPON = True
        self.SWITCH_COOLDOWN = 400
        self.WEAPON_SWITCH_TIME = None

        # MAGIC
        self.MAGIC_INDEX = 0
        self.MAGIC = list(MAGIC_DATA.keys())[self.MAGIC_INDEX]
        self.CAN_SWITCH_MAGIC = True
        self.MAGIC_COOLDOWN = 400
        self.MAGIC_SWITCH_TIME = None


        # STATS
        self.EXP = 100
        self.STATS = INITIAL_STATS
        self.MAX_STATS = MAX_STATS
        self.UPGRADE_COST = UPGRADE_COST
        self.HEALTH = self.STATS['health']
        self.ENERGY = self.STATS['energy']
        self.SPEED = self.STATS['speed']

        self.VULNARABLE = True
        self.HIT_TIME = None
        self.INVULNARABILITY_DURATION = 500

        self.WEAPON_ATTACK_SOUND = pygame.mixer.Sound("../audio/sword.wav")
        self.WEAPON_ATTACK_SOUND.set_volume(0.4)
    
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

        if not self.VULNARABLE:
            self.image.set_alpha(self.waveValue())
        else:
            self.image.set_alpha(255)

    def importPlayerAssets(self):
        CHARACTER_PATH = "../graphics/player"
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
            if KEYS[pygame.K_UP] or KEYS[pygame.K_w]:
                self.directions.y = -1
                self.STATUS = 'up'
            elif KEYS[pygame.K_DOWN] or KEYS[pygame.K_s]:
                self.directions.y = 1
                self.STATUS = 'down'
            else:
                self.directions.y = 0

            if KEYS[pygame.K_LEFT] or KEYS[pygame.K_a]:
                self.directions.x = -1
                self.STATUS = 'left'
            elif KEYS[pygame.K_RIGHT] or KEYS[pygame.K_d]:
                self.STATUS = 'right'
                self.directions.x = 1
            else:
                self.directions.x = 0
            
            # ATTACK INPUT
            if KEYS[pygame.K_SPACE]:
                self.ATTACK_TIME = pygame.time.get_ticks()
                self.ATTACKING = True
                self.createAttack()
                self.WEAPON_ATTACK_SOUND.play()
            
            if KEYS[pygame.K_e] and self.CAN_SWITCH_WEAPON:
                self.CAN_SWITCH_WEAPON = False
                self.WEAPON_SWITCH_TIME = pygame.time.get_ticks()
                self.WEAPON_INDEX += 1
                self.WEAPON_INDEX %= len(WEAPONS_DATA)
                self.WEAPON = list(WEAPONS_DATA.keys())[self.WEAPON_INDEX]
            
            # MAGIC INPUT
            if KEYS[pygame.K_LSHIFT]:
                self.ATTACK_TIME = pygame.time.get_ticks()
                self.ATTACKING = True
                style = self.MAGIC
                strength = MAGIC_DATA[self.MAGIC]['strength'] + self.STATS["magic"]
                cost = MAGIC_DATA[self.MAGIC]['cost']
                self.createMagic(style, strength, cost)
            
            if KEYS[pygame.K_q] and self.CAN_SWITCH_MAGIC:
                self.CAN_SWITCH_MAGIC = False
                self.MAGIC_SWITCH_TIME = pygame.time.get_ticks()
                self.MAGIC_INDEX += 1
                self.MAGIC_INDEX %= len(MAGIC_DATA)
                self.MAGIC = list(MAGIC_DATA.keys())[self.MAGIC_INDEX]

    def cooldowns(self):
        CURRENT_TIME = pygame.time.get_ticks()
        if self.ATTACKING and (self.ATTACK_COOLDOWN + WEAPONS_DATA[self.WEAPON]["cooldown"]) <= (CURRENT_TIME - self.ATTACK_TIME):
            self.ATTACKING = False
            self.destroyAttack()
        
        if not self.CAN_SWITCH_WEAPON and self.SWITCH_COOLDOWN <= (CURRENT_TIME - self.WEAPON_SWITCH_TIME):
            self.CAN_SWITCH_WEAPON = True
        
        if not self.CAN_SWITCH_MAGIC and self.SWITCH_COOLDOWN <= (CURRENT_TIME - self.MAGIC_SWITCH_TIME):
            self.CAN_SWITCH_MAGIC = True
        
        if not self.VULNARABLE and self.INVULNARABILITY_DURATION <= (CURRENT_TIME - self.HIT_TIME):
            self.VULNARABLE = True

    def getWeaponDamage(self):
        base = self.STATS["attack"]
        weapon = WEAPONS_DATA[self.WEAPON]["damage"]
        return base + weapon

    def getMagicDamage(self):
        base = self.STATS["magic"]
        magic = MAGIC_DATA[self.MAGIC]["strength"]
        return base + magic

    def getValueByIndex(self, index):
        return list(self.STATS.values())[index]

    def getCostByIndex(self, index):
        return list(self.UPGRADE_COST.values())[index]
    
    def energyRecovery(self):
        self.ENERGY += 0.01 * self.STATS['magic']
        self.ENERGY = min(self.ENERGY, self.STATS['energy'])

    def update(self):
        self.input()
        self.cooldowns()
        self.getStatus()
        self.animate()
        self.move(self.STATS['speed'])
        self.energyRecovery()
