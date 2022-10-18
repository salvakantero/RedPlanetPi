#===============================================================================
# Map functions
#===============================================================================

import pygame
import os
import json
import random

import constants, enums, globalvars
from globalvars import jp, dp # to build file paths

# loads a map and draws it on screen
def load_map(map_number, map_display):
    global map_data
    map_data = process_map(jp(dp, 'maps/map{}.json'.format(map_number)))
    draw_map(map_display) # draws the tile map on the screen

# dump tiled map into 'mapdata'
def process_map(map_file):
    # reads the entire contents of the json
    with open(map_file) as json_data:
        data_readed = json.load(json_data)
    # gets the map dimensions
    data = {'width': data_readed['width'], 'height': data_readed['height']}
    # gets a list of all tiles
    raw_data = data_readed['layers'][0]['data']
    data['data'] = []
    # divides the list into tile lines, according to the map dimensions
    for x in range(0, data['height']):
        st = x * data['width']
        data['data'].append(raw_data[st: st + data['width']])
    # gets the name of the tile file
    tileset = data_readed['tilesets'][0]['source'].replace('.tsx','.json')
    # gets the data from the tile file
    with open(jp(dp,'maps/' + tileset)) as json_data:
        t = json.load(json_data)
    # removes the path to each image from the tile file
    data['tiles'] = t['tiles']
    for tile in range(0, len(data['tiles'])):
        path = data['tiles'][tile]['image']
        data['tiles'][tile]['image'] = os.path.basename(path)
        data['tiles'][tile]['id'] = data['tiles'][tile]['id'] + 1
    return data

# extracts the tile number from the filename
def get_tile_number(tile_name):
    tile_name = tile_name.replace('.png', '')
    tile_name = tile_name.replace('T', '')
    return int(tile_name)

# get a value from a dictionary
def find_data(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return dic
    return -1

# draws the tile map on the screen
def draw_map(map_display):
    globalvars.tilemap_rect_list.clear()
    globalvars.tilemap_behaviour_list.clear()
    globalvars.anim_tiles_list.clear()
    # scroll through the map data
    for y in range(0, map_data['height']):
        for x in range(0, map_data['width']):
            # gets the tile number from the list
            t = find_data(map_data['tiles'], 'id', map_data['data'][y][x])
            # draws the selected tile
            tile = pygame.image.load(jp(dp, 'images/tiles/' + t['image'])).convert()
            tileRect = tile.get_rect()
            tileRect.topleft = (x * t['imagewidth'], y * t['imageheight'])   
            map_display.blit(tile, tileRect)

            # generates the list of rects and behaviour of the current map
            # from T0.png to T15.png: background tiles (NO_ACTION)
            # from T16.png to T35.png: blocking tiles (OBSTABLE)
            # T40.png: platform tile (PLATFORM)
            # from T50.png to T55.png: object tiles (ITEM)
            # T60.png: door tile (DOOR)
            # from T70.png to T75.png: tiles that kill (KILLER)
            # from T80.png: animated tiles (NO_ACTION)
            tn = get_tile_number(t['image'])            
            behaviour = enums.NO_ACTION
            if tn >= 16 and tn <= 35: behaviour = enums.OBSTACLE
            elif tn == 40: behaviour = enums.PLATFORM
            elif tn >= 50 and tn <= 55: behaviour = enums.ITEM
            elif tn == 60: behaviour = enums.DOOR
            elif tn >= 70 and tn <= 75: behaviour = enums.KILLER
            # is only added to the list if there is an active behaviour
            if behaviour != enums.NO_ACTION:
                globalvars.tilemap_rect_list.append(tileRect)
                globalvars.tilemap_behaviour_list.append(behaviour)

            # generates the list of animated tiles of the current map
            # (frame_1, frame_2, x, y, num_frame)
            if t['image'] in constants.ANIM_TILES.keys():                
                globalvars.anim_tiles_list.append(
                    [tile, pygame.image.load(jp(dp, 'images/tiles/' 
                    + constants.ANIM_TILES[t['image']])).convert(), 
                    tileRect.topleft[0], tileRect.topleft[1], 0])                 

# select some of the animated tiles on the current map to change the frame
# and apply to the surface
def animate_tiles(surf):
    for anim_tile in globalvars.anim_tiles_list: # for each animated tile on the map
        if random.randint(0,24) == 0: # 4% chance of changing frame
            tile = anim_tile[0+anim_tile[4]] # select image according to frame number
            tileRect = tile.get_rect()
            tileRect.topleft = (anim_tile[2], anim_tile[3]) # sets the xy position
            surf.blit(tile, tileRect) # draws on the background image
            # update frame number
            anim_tile[4] += 1
            if anim_tile[4] > 1:
                anim_tile[4] = 0    
    return surf                   