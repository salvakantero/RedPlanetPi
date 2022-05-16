
# ==============================================================================
# Raspberry-Red Planet v1.0
# salvaKantero 2022
# ==============================================================================

import pygame # pygame library functions
import os # file operations
import json # json file management
import sys # exit()
from pygame.locals import * # allows constants without typing "pygame."
from pygame.constants import (QUIT, KEYDOWN, K_ESCAPE) 



#===============================================================================
# Global vars
#===============================================================================

bp = os.path.dirname(__file__) + "/" # exec path (+ "/" when using VS Code)
jp = os.path.join # forms the folder/file path

base_screen_size = 720, 480 # main window size
map_size = 240, 160 # map size (unscaled)

map_number = 0 # required map number
last_map = -1 # last map loaded



#===============================================================================
# Generic functions
#===============================================================================

# get a value from a dictionary
def FindData(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return dic
    return -1



#===============================================================================
# Map functions
#===============================================================================

# loads the map into memory
def LoadMap(map_number):
    global map_data
    map_data = ProcessMap(jp(bp, "maps/map" + str(map_number) + ".json"))
    DrawMap()



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
            display.blit(tile, tileRect)



#===============================================================================
# Main
#===============================================================================

# Initialisation
pygame.init()
# generates a main window with title, icon, and 32-bit colour.
screen = pygame.display.set_mode((800, 600), 0, 32)
pygame.display.set_caption(".:: Raspberry-Red Planet ::.")
icon = pygame.image.load(jp(bp, "images/icon.png")).convert_alpha()
pygame.display.set_icon(icon)
# area covered by the map
display = pygame.Surface(map_size)
# clock to control the FPS
clock = pygame.time.Clock()

# menu music
pygame.mixer.music.load(jp(bp, "sounds/ingame.ogg"))
pygame.mixer.music.play()

# Main loop
while True:
    # event management
    for event in pygame.event.get():
        if event.type == QUIT: # exit when click on the X in the window
            exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: # exit by pressing ESC key
                pygame.quit()
                sys.exit()

    # change map if neccessary
    if (map_number != last_map):
        LoadMap(map_number)
        last_map = map_number

    # scale x 3 the map and transfer to screen
    screen.blit(pygame.transform.scale(display, base_screen_size), 
    ((screen.get_width() - base_screen_size[0]) // 2, # horizontally centred
    screen.get_height() - base_screen_size[1] - 20)) # room for the scoreboard
    pygame.display.update() # refreshes the screen
    clock.tick(60) # 60 FPS
