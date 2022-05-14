
# ==============================================================================
# Raspberry-Red Planet v1.0
# salvaKantero 2022
# ==============================================================================

import pygame # pygame library functions
#import sys 
import os # file operations
import json # json file management
#from pygame.locals import *
from pygame.constants import (QUIT, K_UP, K_DOWN, K_LEFT, K_RIGHT) 



#===============================================================================
# Global vars
#===============================================================================

# executable path (+ "/" when using VS Code)
BASEPATH = os.path.dirname(__file__) + "/"
d = os.path.join # forms the folder/file path

mapNumber = 0 # current map number




#===============================================================================
# Map functions
#===============================================================================

def loadMap(mapNumber): # loads the map into memory
    global mapData
    mapData = processMap(d(BASEPATH, "map/map" + str(mapNumber) + ".json"))
    drawMap()



def findData(lst, key, value): # get a value from a dictionary
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return dic
    return -1



# dump tiled map into 'mapdata'.
def processMap(mapFile):
    with open(mapFile) as json_data:
        dataReaded = json.load(json_data)

    data = {"width": dataReaded["width"], "height": dataReaded["height"]}
    rawData = dataReaded["layers"][0]["data"]
    data["data"] = []

    for x in range(0, data["height"]):
        st = x * data["width"]
        data["data"].append(rawData[st: st + data["width"]])

    tileset = dataReaded["tilesets"][0]["source"].replace(".tsx",".json")

    with open(d(BASEPATH,"map/" + tileset)) as json_data:
        t = json.load(json_data)

    data["tiles"] = t["tiles"]
    for tile in range(0, len(data["tiles"])):
        path = data["tiles"][tile]["image"]
        data["tiles"][tile]["image"] = os.path.basename(path)
        data["tiles"][tile]["id"] = data["tiles"][tile]["id"] + 1

    return data



def drawMap():
    # recorre el mapa
    for y in range(0, mapData["height"]):
        for x in range(0, mapData["width"]):
            # obtiene el elemento de la lista
            t = findData(mapData["tiles"], "id", mapData["data"][y][x])
            # pinta el tile del mapa correspondiente teniendo en cuenta la altura del bloque
            tile = pygame.image.load(d(BASEPATH, "gfx/tiles/" + t["image"]))
            tileRect = tile.get_rect()
            tileRect.topleft = (x*16, y*16)   
            screen.blit(tile, tileRect)



#===============================================================================
# Initialisation
#===============================================================================

pygame.init()
# generates a 640x480 window with title and 32-bit colour.
screen = pygame.display.set_mode((640, 480), 0, 32)
pygame.display.set_caption(".:: Raspberry-Red Planet ::.")
# clock to control the FPS
clock = pygame.time.Clock()

loadMap(mapNumber)


#===============================================================================
# Main loop
#===============================================================================

while True:
    # event management
    for event in pygame.event.get():
        if event.type == QUIT: # click on the X in the window
            exit()

    pygame.display.update() # refreshes the screen
    clock.tick(60) # 60 FPS
