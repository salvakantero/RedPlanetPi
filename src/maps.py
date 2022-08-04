#===============================================================================
# Map functions
#===============================================================================

import pygame, os, json
from globalvars import jp, dp
from support import find_data


# loads a map and draws it on screen
def load_map(map_number, map_display):
    global map_data
    map_data = process_map(jp(dp, "maps/map" + str(map_number) + ".json"))
    draw_map(map_display) # draws the tile map on the screen


# dump tiled map into 'mapdata'
def process_map(map_file):
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
    with open(jp(dp,"maps/" + tileset)) as json_data:
        t = json.load(json_data)
    # removes the path to each image from the tile file
    data["tiles"] = t["tiles"]
    for tile in range(0, len(data["tiles"])):
        path = data["tiles"][tile]["image"]
        data["tiles"][tile]["image"] = os.path.basename(path)
        data["tiles"][tile]["id"] = data["tiles"][tile]["id"] + 1
    return data


# draws the tile map on the screen
def draw_map(map_display):
    # scroll through the map data
    for y in range(0, map_data["height"]):
        for x in range(0, map_data["width"]):
            # gets the tile number from the list
            t = find_data(map_data["tiles"], "id", map_data["data"][y][x])
            # draws the selected tile
            tile = pygame.image.load(jp(dp, "images/tiles/" + t["image"])).convert()
            tileRect = tile.get_rect()
            tileRect.topleft = (x * t["imagewidth"], y * t["imageheight"])   
            map_display.blit(tile, tileRect)
