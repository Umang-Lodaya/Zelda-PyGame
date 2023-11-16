from csv import reader
from os import walk

import pygame
pygame.init()

def importCSV(path):
    terrain = []
    with open(path) as mapp:
        for row in reader(mapp, delimiter=','):
            terrain.append(list(row))

    return terrain

def importFolder(path):
    surfs = []
    for _, _, files in walk(path):
        for file in files:
            p = path + '/' + file
            surf = pygame.image.load(p).convert_alpha()
            surfs.append(surf)
    
    return surfs