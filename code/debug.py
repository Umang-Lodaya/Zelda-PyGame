import pygame
pygame.init()

FONT = pygame.font.Font(None, 30)

def debug(info, y = 10, x = 10):
    DISPLAY_SURFACE = pygame.display.get_surface()
    debugMSG = FONT.render(str(info), True, 'White')
    debugRECT = debugMSG.get_rect(topleft = (x, y))
    pygame.draw.rect(DISPLAY_SURFACE, 'Black', debugRECT)
    DISPLAY_SURFACE.blit(debugMSG, debugRECT)