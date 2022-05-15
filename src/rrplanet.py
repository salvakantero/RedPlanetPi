
# ==============================================================================
# Raspberry-Red Planet v1.0
# salvaKantero 2022
# ==============================================================================

import pygame # pygame library functions
import os # file operations
import json # json file management
from pygame.locals import *
from pygame.constants import (QUIT, K_UP, K_DOWN, K_LEFT, K_RIGHT) 



#===============================================================================
# Global vars
#===============================================================================

bp = os.path.dirname(__file__) + "/" # exec path (+ "/" when using VS Code)
jp = os.path.join # forms the folder/file path

map_number = 0 # current map number



#===============================================================================
# Map functions
#===============================================================================

# loads the map into memory
def LoadMap(map_number):
    global map_data
    map_data = ProcessMap(jp(bp, "maps/map" + str(map_number) + ".json"))
    DrawMap()



# get a value from a dictionary
def FindData(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return dic
    return -1



# dump tiled map into 'mapdata'
def ProcessMap(map_file):
    # reads the entire contents of the json
    with open(map_file) as json_data:
        data_readed = json.load(json_data)
    # gets the map dimensions
    data = {"width": data_readed["width"], "height": data_readed["height"]}
    # gets a list of all tiles
    raw_data = data_readed["layers"][0]["data"]
    data["data"] = []
    # divides the list into tile lines, according to the map dimensions
    for x in range(0, data["height"]):
        st = x * data["width"]
        data["data"].append(raw_data[st: st + data["width"]])
    # gets the name of the tile file
    tileset = data_readed["tilesets"][0]["source"].replace(".tsx",".json")
    # gets the data from the tile file
    with open(jp(bp,"maps/" + tileset)) as json_data:
        t = json.load(json_data)
    # removes the path to each image from the tile file
    data["tiles"] = t["tiles"]
    for tile in range(0, len(data["tiles"])):
        path = data["tiles"][tile]["image"]
        data["tiles"][tile]["image"] = os.path.basename(path)
        data["tiles"][tile]["id"] = data["tiles"][tile]["id"] + 1

    return data



# loads the tile map on screen
def DrawMap():
    # scroll through the map data
    for y in range(0, map_data["height"]):
        for x in range(0, map_data["width"]):
            # gets the tile number from the list
            t = FindData(map_data["tiles"], "id", map_data["data"][y][x])
            # paints the selected tile
            tile = pygame.image.load(jp(bp, "images/" + t["image"])).convert()
            tileRect = tile.get_rect()
            tileRect.topleft = (x * t["imagewidth"], y * t["imageheight"])   
            screen.blit(tile, tileRect)
            #screen.blit(pygame.transform.scale(display, base_screen_size), ((screen.get_width() - base_screen_size[0]) // 2, (screen.get_height() - base_screen_size[1]) // 2))



#===============================================================================
# Initialisation
#===============================================================================

pygame.init()
# generates a 640x480 window with title and 32-bit colour.
screen = pygame.display.set_mode((640, 480), 0, 32)
pygame.display.set_caption(".:: Raspberry-Red Planet ::.")
# clock to control the FPS
clock = pygame.time.Clock()

LoadMap(map_number)


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
