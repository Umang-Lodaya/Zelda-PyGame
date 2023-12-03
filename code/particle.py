import pygame
from support import importFolder
from random import choice

class AnimationPlayer:
    def __init__(self):
        self.frames = {
            'flame': importFolder(r"graphics\particles\flame\frames"),
            'aura': importFolder(r"graphics\particles\aura"),
            'heal': importFolder(r"graphics\particles\heal\frames"),

            'claw': importFolder(r"graphics\particles\claw"),
            'slash': importFolder(r"graphics\particles\slash"),
            'sparkle': importFolder(r"graphics\particles\sparkle"),
            'leaf_attack': importFolder(r"graphics\particles\leaf_attack"),
            'thunder': importFolder(r"graphics\particles\thunder"),

            'squid': importFolder(r"graphics\particles\smoke_orange"),
            'raccoon': importFolder(r"graphics\particles\raccoon"),
            'spirit': importFolder(r"graphics\particles\nova"),
            'bamboo': importFolder(r"graphics\particles\bamboo"),

            'leaf': (
                importFolder(r"graphics\particles\leaf1"),
                importFolder(r"graphics\particles\leaf2"),
                importFolder(r"graphics\particles\leaf3"),
                importFolder(r"graphics\particles\leaf4"),
                importFolder(r"graphics\particles\leaf5"),
                importFolder(r"graphics\particles\leaf6"),
                self.reflect_images(importFolder(r"graphics\particles\leaf1")),
                self.reflect_images(importFolder(r"graphics\particles\leaf2")),
                self.reflect_images(importFolder(r"graphics\particles\leaf3")),
                self.reflect_images(importFolder(r"graphics\particles\leaf4")),
                self.reflect_images(importFolder(r"graphics\particles\leaf5")),
                self.reflect_images(importFolder(r"graphics\particles\leaf6")),
                )
        }
    
    def createGrassParticles(self, pos, groups):
        frames = choice(self.frames['leaf'])
        Particle(pos, frames, groups)
    
    def createParticles(self, type, pos, groups):
        frame = self.frames[type]
        Particle(pos, frame, groups)

    def reflect_images(self, frames):
        newFrames = []
        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            newFrames.append(flipped_frame)
        return newFrames

class Particle(pygame.sprite.Sprite):
    def __init__(self, position, animation_frames, groups):
        super().__init__(groups)
        self.FRAME_INDEX = 0
        self.sprite_type = 'magic'
        self.ANIMATION_SPEED = 0.15

        self.frames = animation_frames
        self.image = self.frames[self.FRAME_INDEX]
        self.rect = self.image.get_rect(center = position)

    def animate(self):
        self.FRAME_INDEX += self.ANIMATION_SPEED
        if self.FRAME_INDEX >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.FRAME_INDEX)]
    
    def update(self):
        self.animate()