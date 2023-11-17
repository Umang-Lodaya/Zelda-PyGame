import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.FRAME_INDEX = 0
        self.ANIMATION_SPEED = 0.15
        self.directions = pygame.math.Vector2()
    
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