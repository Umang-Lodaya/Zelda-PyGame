import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        direction = player.STATUS.split("_")[0]

        # GRAPHIC
        path = f"graphics/weapons/{player.WEAPON}/{direction}.png"
        self.image = pygame.image.load(path).convert_alpha()

        # PLACEMENT
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = (player.rect.midright) + pygame.math.Vector2(0, 16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = (player.rect.midleft) + pygame.math.Vector2(0, 16))
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom = (player.rect.midtop) + pygame.math.Vector2(-10, 0))
        else:
            self.rect = self.image.get_rect(midtop = (player.rect.midbottom) + pygame.math.Vector2(-10, 0))
