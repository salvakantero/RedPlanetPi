
#===============================================================================
# Map class
#===============================================================================

import pygame
import json
import os
import random
import constants
import enums

class Map():
    def __init__(self, map_surf):
        self.number = 0 # current map
        self.scroll = 0 # scroll direction for map_transition()
        self.last = -1 # last map loaded
        self.game_percent = 0 # % of gameplay completed
        self.tilemap_rect_list = [] # list of tile rects
        self.tilemap_behaviour_list = [] # list of tile behaviours
        self.anim_tiles_list = [] # (frame_1, frame_2, x, y, num_frame)
        self.hotspots = constants.HOTSPOTS_DATA # objects
        self.map_data = {}
        self.map_surf = map_surf        
        # modifies the XY position of the map on the screen to create 
        # a shaking effect for a given number of frames
        self.shake = [0, 0]
        self.shake_timer = 0

    # loads a map and draws it on screen
    def load(self):
        self.map_data = self.process_map('maps/map{}.json'.format(self.number))
        self.draw_map() # draws the tile map on the screen

    # dump tiled map into 'mapdata'
    def process_map(self, map_file):
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
        with open('maps/' + tileset) as json_data:
            t = json.load(json_data)
        # removes the path to each image from the tile file
        data['tiles'] = t['tiles']
        for tile in range(0, len(data['tiles'])):
            path = data['tiles'][tile]['image']
            data['tiles'][tile]['image'] = os.path.basename(path)
            data['tiles'][tile]['id'] = data['tiles'][tile]['id'] + 1
        return data

    # extracts the tile number from the filename
    def get_tile_number(self, tile_name):
        tile_name = tile_name.replace('.png', '')
        tile_name = tile_name.replace('T', '')
        return int(tile_name)

    # get a value from a dictionary
    def find_data(self, lst, key, value):
        for i, dic in enumerate(lst):
            if dic[key] == value:
                return dic
        return -1

    # draws the tile map on the screen
    def draw_map(self):
        self.tilemap_rect_list.clear()
        self.tilemap_behaviour_list.clear()
        self.anim_tiles_list.clear()
        # scroll through the map data
        for y in range(0, self.map_data['height']):
            for x in range(0, self.map_data['width']):
                # gets the tile number from the list
                t = self.find_data(self.map_data['tiles'], 'id', self.map_data['data'][y][x])
                # draws the selected tile
                tile = pygame.image.load('images/tiles/' + t['image']).convert()
                tileRect = tile.get_rect()
                tileRect.topleft = (x * t['imagewidth'], y * t['imageheight'])   
                self.map_surf.blit(tile, tileRect)

                # generates the list of rects and behaviour of the current map
                # from T16.png to T35.png: blocking tiles (OBSTABLE)
                # T40.png: platform tile (PLATFORM)
                # from T70.png to T75.png: tiles that kill (KILLER)
                tn = self.get_tile_number(t['image'])            
                behaviour = enums.NO_ACTION
                if tn >= 16 and tn <= 35:   behaviour = enums.OBSTACLE
                elif tn == 40:              behaviour = enums.PLATFORM_TILE
                elif tn >= 70 and tn <= 75: behaviour = enums.KILLER
                # is only added to the list if there is an active behaviour
                if behaviour != enums.NO_ACTION:
                    self.tilemap_rect_list.append(tileRect)
                    self.tilemap_behaviour_list.append(behaviour)

                # generates the list of animated tiles of the current map
                # (frame_1, frame_2, x, y, num_frame)
                if t['image'] in constants.ANIM_TILES.keys():                
                    self.anim_tiles_list.append(
                        [tile, pygame.image.load('images/tiles/' 
                        + constants.ANIM_TILES[t['image']]).convert(), 
                        tileRect.topleft[0], tileRect.topleft[1], 0])

    # select some of the animated tiles on the current map to change the frame
    # and apply to the surface. 
    # anim_tiles_list = (frame_1, frame_2, x, y, num_frame)
    def animate_tiles(self, surface):
        for anim_tile in self.anim_tiles_list: # for each animated tile on the map
            if random.randint(0,24) == 0: # 4% chance of changing frame
                tile = anim_tile[0+anim_tile[4]] # select image according to frame number
                tileRect = tile.get_rect()
                tileRect.topleft = (anim_tile[2], anim_tile[3]) # sets the xy position
                surface.blit(tile, tileRect) # draws on the background image
                # update frame number
                anim_tile[4] += 1
                if anim_tile[4] > 1:
                    anim_tile[4] = 0    
        return surface

    # checks if the map needs to be changed (depending on the player's XY position)
    def check_change(self, player):
        # player disappears on the left
        # appearing from the right on the new map
        if player.rect.x < -(player.rect.width - 8):
            self.number -= 1
            self.scroll = enums.LEFT
            player.rect.right = constants.MAP_UNSCALED_SIZE[0]
        # player disappears on the right
        # appearing from the left on the new map
        elif player.rect.x > constants.MAP_UNSCALED_SIZE[0] - 8:
            self.number += 1
            self.scroll = enums.RIGHT
            player.rect.left = 0
        # player disappears over the top
        # appearing at the bottom of the new map 
        # and jumps again to facilitate the return
        elif player.rect.y < (-16):
            self.number -= 5
            self.scroll = enums.UP
            player.rect.bottom = constants.MAP_UNSCALED_SIZE[1]            
            player.direction.y = constants.JUMP_VALUE
        # player disappears from underneath
        #appearing at the top of the new map
        elif player.rect.y > constants.MAP_UNSCALED_SIZE[1]:
            self.number += 5
            self.scroll = enums.DOWN
            player.rect.top = 0

            