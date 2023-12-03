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
        MAIN_SOUND = pygame.mixer.Sound(r"audio\main.ogg")
        MAIN_SOUND.set_volume(0.5)
        MAIN_SOUND.play(loops = -1)

    def run(self):
        while True:
            self.SCREEN.fill(WATER_COLOR)
            self.LEVEL.run()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("QUITED!")
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.LEVEL.toggleMenu()

            pygame.display.update()
            self.CLOCK.tick(FPS)


if __name__ == "__main__":
    print("LOADING GAME ...")
    game = Game()
    print("GAME LOADED!")
    game.run()
