import pygame, sys
from settings import *
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Zelda")
        self.SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.CLOCK = pygame.time.Clock()

        self.LEVEL = Level()
    
    def run(self):
        while True:
            self.SCREEN.fill('black')
            self.LEVEL.run()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()
            self.CLOCK.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()