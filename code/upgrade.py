import pygame
from settings import *

class Upgrade:
    def __init__(self, player):
        self.PLAYER = player
        self.DISPLAY_SURFACE = pygame.display.get_surface()
        
        self.FONT = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.ATTRIBUTE_NUMBER = len(self.PLAYER.STATS)
        self.ATTRIBUTE_NAMES = list(self.PLAYER.STATS.keys())
        self.MAX_VALUES = list(self.PLAYER.MAX_STATS.values())

        self.HEIGHT = self.DISPLAY_SURFACE.get_size()[1] * 0.8
        self.WIDTH = self.DISPLAY_SURFACE.get_size()[0] // (self.ATTRIBUTE_NUMBER + 1)
        self.createItems()

        self.SELECTION_INDEX = 0
        self.SELECTION_TIME = None
        self.CAN_MOVE = True
    
    def input(self):
        keys = pygame.key.get_pressed()

        if self.CAN_MOVE:
            if keys[pygame.K_RIGHT] and self.SELECTION_INDEX < self.ATTRIBUTE_NUMBER - 1:
                self.SELECTION_INDEX += 1
                self.CAN_MOVE = False
                self.SELECTION_TIME = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT] and self.SELECTION_INDEX >= 1:
                self.SELECTION_INDEX -= 1
                self.CAN_MOVE = False
                self.SELECTION_TIME = pygame.time.get_ticks()
        
            if keys[pygame.K_SPACE]:
                self.CAN_MOVE = False
                self.SELECTION_TIME = pygame.time.get_ticks()
                self.ITEMS[self.SELECTION_INDEX].trigger(self.PLAYER)
    
    def selectionCooldown(self):
        if not self.CAN_MOVE:
            currentTime = pygame.time.get_ticks()
            if currentTime - self.SELECTION_TIME >= 300:
                self.CAN_MOVE = True

    def createItems(self):
        self.ITEMS = []
        for item, index in enumerate(range(self.ATTRIBUTE_NUMBER)):
            top = self.DISPLAY_SURFACE.get_size()[1] * 0.1
            width = self.DISPLAY_SURFACE.get_size()[0]
            incr = width // self.ATTRIBUTE_NUMBER
            left = item * incr + (incr - self.WIDTH) // 2

            item = Item(left, top, self.WIDTH, self.HEIGHT, index, self.FONT)
            self.ITEMS.append(item)

    def display(self):
        self.input()
        self.selectionCooldown()
        for index, item in enumerate(self.ITEMS):
            name = self.ATTRIBUTE_NAMES[index]
            value = self.PLAYER.getValueByIndex(index)
            maxVal = self.MAX_VALUES[index]
            cost = self.PLAYER.getCostByIndex(index)
            item.display(self.DISPLAY_SURFACE, self.SELECTION_INDEX, name, value, maxVal, cost)


class Item:
    def __init__(self, left, top, width, height, index, font):
        self.rect = pygame.Rect(left, top, width, height)
        self.index = index
        self.font = font
    
    def displayNames(self, surface, name, cost, selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR
        titleSurf = self.font.render(name, False, color)
        titleRect = titleSurf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0, 20))

        costSurf = self.font.render(f"{int(cost)}", False, color)
        costRect = costSurf.get_rect(midbottom = self.rect.midbottom - pygame.math.Vector2(0, 20))
        
        surface.blit(titleSurf, titleRect)
        surface.blit(costSurf, costRect)

    def displayBar(self, surface, value, maxVal, selected):
        top = self.rect.midtop + pygame.math.Vector2(0, 60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0, 60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        fullHeight = bottom[1] - top[1]
        relativeNumber = value / maxVal * fullHeight
        valueRect = pygame.Rect(top[0] - 15, bottom[1] - relativeNumber, 30, 10)

        pygame.draw.line(surface, color, top, bottom, 5)
        pygame.draw.rect(surface, color, valueRect)

    def trigger(self, player):
        upgrade_attribute = list(player.STATS.keys())[self.index]
        if player.EXP >= player.UPGRADE_COST[upgrade_attribute] and player.STATS[upgrade_attribute] < player.MAX_STATS[upgrade_attribute]:
            player.EXP -= player.UPGRADE_COST[upgrade_attribute]
            player.STATS[upgrade_attribute] *= 1.2
            player.UPGRADE_COST[upgrade_attribute] *= 1.4
        
        player.STATS[upgrade_attribute] = min(player.MAX_STATS[upgrade_attribute], player.STATS[upgrade_attribute])


    def display(self, display_surface, selection_num, name, value, maxVal, cost):
        if self.index == selection_num:
            pygame.draw.rect(display_surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
        else:
            pygame.draw.rect(display_surface, UI_BG_COLOR, self.rect)
        pygame.draw.rect(display_surface, UI_BORDER_COLOR, self.rect, 4)
        self.displayNames(display_surface, name, cost, self.index == selection_num)
        self.displayBar(display_surface, value, maxVal, self.index == selection_num)