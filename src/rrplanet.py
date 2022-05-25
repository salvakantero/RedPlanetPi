
# ==============================================================================
# Raspberry-Red Planet v1.0
# salvaKantero 2022
# ==============================================================================

import pygame # pygame library functions
import os # file operations
import json # json file management
import sys # exit()
from pygame.locals import * # allows constants without typing "pygame."
from pygame.constants import (QUIT, KEYDOWN, K_ESCAPE, K_LEFT, K_RIGHT) 



#===============================================================================
# Global vars
#===============================================================================

bp = os.path.dirname(__file__) + "/" # exec path (+ "/" when using VS Code)
jp = os.path.join # forms the folder/file path

win_size = 800, 600 # main window size
map_scaled_size = 720, 480 # map size (scaled)
map_unscaled_size = 240, 160 # map size (unscaled)

map_number = 0 # required map number
last_map = -1 # last map loaded

# map names
map_names = {
    0  : "!!!!!!!_CONTROL_CENTRE_!!!!!!!",
	1  : "!!!!!!!_SUPPLY_DEPOT_1_!!!!!!!",
	2  : "!!!!_CENTRAL_HALL_LEVEL_0_!!!!",
	3  : "!!!_TOXIC_WASTE_STORAGE_1A_!!!",
    4  : "!!!_TOXIC_WASTE_STORAGE_1B_!!!",
	5  : "!!!_WEST_PASSAGE__LEVEL_-1_!!!",
	6  : "!!_ACCESS_TO_WEST_PASSAGES_!!!",
	7  : "!!!_CENTRAL_HALL__LEVEL_-1_!!!",
	8  : "!!!!!_ACCESS_TO_DUNGEONS_!!!!!",
	9  : "!!!!!!!!!!_DUNGEONS_!!!!!!!!!!",
	10 : "!!!_WEST_PASSAGE__LEVEL_-2_!!!",
	11 : "!!!!!!!_SUPPLY_DEPOT_2_!!!!!!!",
	12 : "!!!_CENTRAL_HALL__LEVEL_-2_!!!",
	13 : "!!_ACCESS_TO_SOUTHEAST_EXIT_!!",
	14 : "!!!!_EXIT_TO_UNDERGROUND_!!!!!",
	15 : "!!!!!!!_PELUSOIDS_LAIR_!!!!!!!",
	16 : "!!!!!_ALVARITOS_GROTTO_2_!!!!!",
	17 : "!!!!!_ALVARITOS_GROTTO_1_!!!!!",
	18 : "!!!_TOXIC_WASTE_STORAGE_2A_!!!",
	19 : "!!!!!_UNDERGROUND_TUNNEL_!!!!!",
	20 : "!!!!!_SIDE_HALL_LEVEL_-4_!!!!!",
	21 : "!!!!!_ARACHNOVIRUS_LAIR_!!!!!!",
	22 : "!!!!_UNSTABLE_CORRIDORS_1_!!!!",
	23 : "!!!!_UNSTABLE_CORRIDORS_2_!!!!",
	24 : "!!!_TOXIC_WASTE_STORAGE_2B_!!!",
	25 : "!!!!!_SIDE_HALL_LEVEL_-5_!!!!!",
	26 : "!!!!!!_ABANDONED_MINE_1_!!!!!!",
	27 : "!!!!!!_ABANDONED_MINE_2_!!!!!!",
	28 : "!!!!!!_ABANDONED_MINE_3_!!!!!!",
	29 : "!!!!_EXPLOSIVES_STOCKPILE_!!!!",
    30 : "!!!_BACK_TO_CONTROL_CENTER_!!!",
}


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
            map_display.blit(tile, tileRect)



#===============================================================================
# Main
#===============================================================================

# Initialisation
pygame.init()
pygame.mixer.init()
# generates a main window with title, icon, and 32-bit colour.
screen = pygame.display.set_mode(win_size, 0, 32)
pygame.display.set_caption(".:: Raspberry-Red Planet ::.")
icon = pygame.image.load(jp(bp, "images/icon.png")).convert_alpha()
pygame.display.set_icon(icon)
# area covered by the map
map_display = pygame.Surface(map_unscaled_size)
# clock to control the FPS
clock = pygame.time.Clock()

# menu music
# pygame.mixer.music.load(jp(bp, "sounds/ingame.ogg"))
# pygame.mixer.music.play()

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

            # ========================== temporal code
            if event.key == K_RIGHT:
                if map_number < 14:
                    map_number += 1
            if event.key == K_LEFT:
                if map_number > 0:
                    map_number -= 1
            # ==========================

    # change map if neccessary
    if map_number != last_map:
        LoadMap(map_number)
        last_map = map_number

    # scale x 3 the map and transfer to screen
    screen.blit(pygame.transform.scale(map_display, map_scaled_size), 
    ((screen.get_width() - map_scaled_size[0]) // 2, # horizontally centred
    screen.get_height() - map_scaled_size[1] - 20)) # room for the scoreboard
    pygame.display.update() # refreshes the screen
    clock.tick(60) # 60 FPS
