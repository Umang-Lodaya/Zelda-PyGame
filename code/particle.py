import pygame
from support import importFolder
from random import choice

class AnimationPlayer:
    def __init__(self):
        self.frames = {
            'flame': importFolder("../graphics/particles/flame/frames"),
            'aura': importFolder("../graphics/particles/aura"),
            'heal': importFolder("../graphics/particles/heal/frames"),

            'claw': importFolder("../graphics/particles/claw"),
            'slash': importFolder("../graphics/particles/slash"),
            'sparkle': importFolder("../graphics/particles/sparkle"),
            'leaf_attack': importFolder("../graphics/particles/leaf_attack"),
            'thunder': importFolder("../graphics/particles/thunder"),

            'squid': importFolder("../graphics/particles/smoke_orange"),
            'raccoon': importFolder("../graphics/particles/raccoon"),
            'spirit': importFolder("../graphics/particles/nova"),
            'bamboo': importFolder("../graphics/particles/bamboo"),

            'leaf': (
                importFolder("../graphics/particles/leaf1"),
                importFolder("../graphics/particles/leaf2"),
                importFolder("../graphics/particles/leaf3"),
                importFolder("../graphics/particles/leaf4"),
                importFolder("../graphics/particles/leaf5"),
                importFolder("../graphics/particles/leaf6"),
                self.reflect_images(importFolder("../graphics/particles/leaf1")),
                self.reflect_images(importFolder("../graphics/particles/leaf2")),
                self.reflect_images(importFolder("../graphics/particles/leaf3")),
                self.reflect_images(importFolder("../graphics/particles/leaf4")),
                self.reflect_images(importFolder("../graphics/particles/leaf5")),
                self.reflect_images(importFolder("../graphics/particles/leaf6")),
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