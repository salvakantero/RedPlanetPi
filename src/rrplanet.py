
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

# ruta del ejecutable (+ "/" en VS Code)
BASEPATH = os.path.dirname(__file__) + "/"
mapNumber = 0 # current map number



#===============================================================================
# Map functions
#===============================================================================

def loadMap(mapNumber): # loads the map into memory
    mapData = processMap(os.path.join(BASEPATH, "map/map" + str(mapNumber) + ".json"))



# dump tiled map into 'mapdata'.
def processMap(mapFile):
    with open(mapFile) as json_data:
        dataReaded = json.load(json_data)

    data = {"width": dataReaded["width"], "height": dataReaded["height"]}
    rawData = dataReaded["layers"][0]["data"]
    data["data"] = []

    for x in range(0, data["width"]):
        st = x * data["width"]
        data["data"].append(rawData[st: st + data["height"]])

    tileset = dataReaded["tilesets"][0]["source"].replace(".tsx",".json")

    with open(os.path.join(BASEPATH,"map/" + tileset)) as json_data:
        t = json.load(json_data)

    data["tiles"] = t["tiles"]
    for tile in range(0, len(data["tiles"])):
        path = data["tiles"][tile]["image"]
        data["tiles"][tile]["image"] = os.path.basename(path)
        data["tiles"][tile]["id"] = data["tiles"][tile]["id"] + 1

    return data



def drawMap():
    # recorre el mapa
    for x in range(0, 15):
        for y in range(0, 10):
            # obtiene el elemento de la lista
            t = findData(mapData["tiles"], "id", mapData["data"][y][x])
            # pinta el tile del mapa correspondiente teniendo en cuenta la altura del bloque
            tile = pygame.image.load(os.path.join(BASEPATH, "tiles/" + t["image"]))
            tileRect = tile.get_rect()
            tileRect.topleft = (isoX, isoY - (t["imageheight"]-80))    
            surface.blit(tile, tileRect)

            # si en la coordenada actual está el jugador, lo pinta (por encima del mapa (-32))
            if x == p1["mapX"] and y == p1["mapY"]:
                p1["isoX"] = (x*32)-(y*32) + OFFSETX
                p1["isoY"] = (y*16)+(x*16) + OFFSETY - 32
                imgP1Rect.topleft = (p1["isoX"], p1["isoY"])
                surface.blit(imgP1, imgP1Rect)







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
