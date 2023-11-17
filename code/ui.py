import pygame
from settings import *

class UI:
    def __init__(self):
        # GENERAL
        self.DISPLAY_SURFACE = pygame.display.get_surface()
        self.FONT = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        x = 10
        # BAR SETUP
        self.HEALTH_BAR_RECT = pygame.Rect(x, x, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.ENERGY_BAR_RECT = pygame.Rect(x, x*2 + BAR_HEIGHT, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        self.WEAPON_GRAPHICS = []
        for _, weapon in WEAPONS_DATA.items():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.WEAPON_GRAPHICS.append(weapon)

    def showBar(self, currentAmount, maxAmount, bgRect, color):
        # DRAW BG
        pygame.draw.rect(self.DISPLAY_SURFACE, UI_BG_COLOR, bgRect)

        # CONVERT AMOUNT -> PIXELS
        ratio = currentAmount / maxAmount
        ratio = 0.8
        currentWidth = bgRect.width * ratio
        currentRect = bgRect.copy()
        currentRect.width = currentWidth

        # DRAW BAR
        pygame.draw.rect(self.DISPLAY_SURFACE, color, currentRect)
        pygame.draw.rect(self.DISPLAY_SURFACE, UI_BORDER_COLOR, bgRect, 3)
    
    def showEXP(self, exp):
        text = self.FONT.render(str(int(exp)), False, TEXT_COLOR)
        padding = 20
        x = self.DISPLAY_SURFACE.get_size()[0] - padding
        y = self.DISPLAY_SURFACE.get_size()[1] - padding
        text_rect = text.get_rect(bottomright = (x, y))
        pygame.draw.rect(self.DISPLAY_SURFACE, UI_BG_COLOR, text_rect.inflate(20, 20))
        pygame.draw.rect(self.DISPLAY_SURFACE, UI_BORDER_COLOR, text_rect, 3)
        self.DISPLAY_SURFACE.blit(text, text_rect)

    def selectionBox(self, left, top, hasSwitched):
        bgRect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.DISPLAY_SURFACE, UI_BG_COLOR, bgRect)
        if hasSwitched:
            pygame.draw.rect(self.DISPLAY_SURFACE, UI_BORDER_COLOR_ACTIVE, bgRect, 3)
        else:
            pygame.draw.rect(self.DISPLAY_SURFACE, UI_BORDER_COLOR, bgRect, 3)

        return bgRect
    
    def weaponOverlay(self, weaponIndex, hasSwitched):
        bgRect = self.selectionBox(10, self.DISPLAY_SURFACE.get_size()[1] - 10 - ITEM_BOX_SIZE, hasSwitched)
        weaponSurf = self.WEAPON_GRAPHICS[weaponIndex]
        weaponRect = weaponSurf.get_rect(center = bgRect.center)
        self.DISPLAY_SURFACE.blit(weaponSurf, weaponRect)


    def display(self, player):
        self.showBar(player.HEALTH, player.STATS['health'], self.HEALTH_BAR_RECT, HEALTH_COLOR)
        self.showBar(player.ENERGY, player.STATS['energy'], self.ENERGY_BAR_RECT, ENERGY_COLOR)
        self.showEXP(player.EXP)
        self.weaponOverlay(player.WEAPON_INDEX, not player.CAN_SWITCH_WEAPON)
        self.selectionBox(10*2 + ITEM_BOX_SIZE, self.DISPLAY_SURFACE.get_size()[1] - 10 - ITEM_BOX_SIZE, player.CAN_SWITCH_WEAPON)