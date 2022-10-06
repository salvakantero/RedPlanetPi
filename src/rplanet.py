
# ==============================================================================
# Red Planet Pi v1.0
# salvaKantero 2022
# ==============================================================================

import pygame # pygame library functions
import random # random()
import os # path()
import sys # exit()
import json # load()

# allows constants without typing "pygame."
from pygame.locals import *
from pygame.constants import *




#===============================================================================
# Global variables
#===============================================================================

dp = os.path.dirname(__file__) + '/' # exec path (+ '/' when using VS Code)
jp = os.path.join # forms the folder/file path

WIN_SIZE = 800, 640 # main window size
MAP_SCALED_SIZE = 720, 480 # map size (scaled x3)
MAP_UNSCALED_SIZE = 240, 160 # map size (unscaled)
SBOARD_SCALED_SIZE = 720, 114 # scoreboard size (scaled x3)
SBOARD_UNSCALED_SIZE = 240, 38 # scoreboard size (unscaled)
H_MARGIN = 40 # horizontal distance between the edge and the playing area
V_MARGIN = 20 # vertical distance between the edge and the playing area

# animated tiles
anim_tiles_list = [] # (frame_1, frame_2, x, y, num_frame)
ANIM_TILES = {
    # frame_1   frame_2
    'T4.png' : 'T70.png',   # computer 1
    'T8.png' : 'T71.png',   # computer 2
    'T9.png' : 'T72.png',   # corpse
    'T25.png' : 'T73.png',  # toxic waste
    'T29.png' : 'T74.png'   # lava
}

map_number = 0 # current map number
last_map = -1 # last map loaded
game_percent = 0 # % of gameplay completed

# game states
RUNNING, PAUSED, OVER = 0, 1, 2

# music states
UNMUTED, MUTED = 0, 1

# configuration values
cfg_scanlines_type = 2  # 0 = none, 1 = fast, 2 = HQ
cfg_full_screen = 0 # 0 = no, 1 = yes

# colour palette (Pico8)
PALETTE = {
    'BLACK': (0, 0, 0),
    'DARK_BLUE' : (35, 50, 90),
    'PURPLE' : (126, 37, 83),
    'DARK_GREEN' : (0, 135, 81),
    'BROWN' : (171, 82, 54),
    'DARK_GRAY' : (95, 87, 79),
    'GRAY' : (194, 195, 199),
    'WHITE' : (255, 241, 232),
    'RED' : (255, 0, 77),
    'ORANGE' : (255, 163, 0),
    'YELLOW' : (255, 236, 39),
    'GREEN' : (0, 228, 54),
    'CYAN' : (41, 173, 255),
    'MALVA' : (131, 118, 156),
    'PINK' : (255, 119, 168),
    'SAND' : (255, 204, 170),
    'KEY' : (255, 0, 255) # Mask colour
}

# screen names
MAP_NAMES = {
    # level 1
    0  : 'CONTROL CENTRE',
    1  : 'SUPPLY DEPOT 1',
    2  : 'CENTRAL HALL',
    3  : 'TOXIC WASTE STORAGE 1A',
    4  : 'TOXIC WASTE STORAGE 1B',
    5  : 'WEST CORRIDOR',
    6  : 'ACCESS TO WEST CORRIDORS',
    7  : 'CENTRAL HALL',
    8  : 'ACCESS TO DUNGEONS',
    9  : 'DUNGEONS',
    10 : 'WEST CORRIDOR',
    11 : 'SUPPLY DEPOT 2',
    12 : 'CENTRAL HALL',
    13 : 'ACCESS TO SOUTHEAST EXIT',
    14 : 'EXIT TO UNDERGROUND',
    # level 2
    15 : 'WAREHOUSE ACCESS',
    16 : 'CONVECTION CORRIDOR',
    17 : 'SEWER MAINTENANCE',
    18 : 'COLD ZONE ACCESS CORRIDOR',
    19 : 'COLD ZONE ACCESS CORRIDOR',
    20 : 'FROZEN WAREHOUSE 1',
    21 : 'CONVECTION CORRIDOR',
    22 : 'TOXIC SEWERS 1',
    23 : 'ICE CAVE',
    24 : 'ACCESS TO ICE CAVE',
    25 : 'FROZEN WAREHOUSE 2',
    26 : 'CONVECTION CORRIDOR',
    27 : 'TOXIC SEWERS 1',
    28 : 'ACCESS TO THE WARM ZONE',
    29 : 'EXIT TO THE WARM ZONE',
    # level 3
    30 : 'PELUSOIDS LAIR',
    31 : 'ALVARITOS GROTTO 2',
    32 : 'ALVARITOS GROTTO 1',
    33 : 'TOXIC WASTE STORAGE 2A',
    34 : 'UNDERGROUND TUNNEL',
    35 : 'SIDE HALL',
    36 : 'ARACHNOVIRUS LAIR',
    37 : 'UNSTABLE CORRIDORS 1',
    38 : 'UNSTABLE CORRIDORS 2',
    39 : 'TOXIC WASTE STORAGE 2B',
    40 : 'SIDE HALL',
    41 : 'ABANDONED MINE 1',
    42 : 'ABANDONED MINE 2',
    43 : 'ABANDONED MINE 3',
    44 : 'EXPLOSIVES STOCKPILE',
    45 : 'BACK TO CONTROL CENTER',
}

# enemies per map
ENEMIES_DATA = [
    #-----------LEVEL 1-------------
    # CONTROL CENTRE
    [128, 112, 32, 112, -2, 0, 1],
	[16, 16, 224, 48, 2, 2, 2],
	[0, 0, 0, 0, 0, 0, 0],
    # SUPPLY DEPOT 1
	[192, 112, 32, 112, -4, 0, 1],
	[208, 16, 144, 64, -1, 1, 2],
	[80, 64, 80, 16, 0, -2, 3],
    # CENTRAL HALL  
	[112, 144, 112, 32, 0, -2, 4],
	[208, 112, 16, 80, -2, -2, 2],
	[0, 0, 0, 0, 0, 0, 0],
    # TOXIC WASTE STORAGE 1A
	[160, 48, 32, 48, -4, 0, 1],
	[16, 80, 208, 112, 4, 4, 3],
	[0, 0, 0, 0, 0, 0, 0],
    # TOXIC WASTE STORAGE 1B
	[64, 80, 64, 16, 0, -2, 3],
	[144, 16, 144, 128, 0, 2, 3],
	[208, 112, 208, 96, 0, -2, 6],
    # WEST CORRIDOR
	[32, 48, 192, 48, 2, 0, 1],
	[192, 80, 32, 80, -2, 0, 1],
	[144, 128, 160, 128, 2, 0, 6],
    # ACCESS TO THE WEST CORRIDORS
	[96, 48, 48, 16, -2, -2, 3],
	[144, 80, 144, 16, 0, -2, 3],
	[16, 112, 16, 96, 0, -2, 6],
    # CENTRAL HALL
	[112, 144, 112, 16, 0, -2, 4],
	[208, 96, 16, 96, -2, 0, 3],
	[16, 32, 192, 64, 1, 1, 2],
    # ACCESS TO DUNGEONS
	[208, 64, 192, 64, -2, 0, 6],
	[64, 64, 64, 32, 0, -1, 3],
	[0, 0, 0, 0, 0, 0, 0],
    # DUNGEONS
	[144, 128, 144, 16, 0, -4, 3],
	[80, 16, 80, 128, 0, 4, 3],
	[192, 128, 208, 128, 2, 0, 6],
    # WEST CORRIDOR
	[128, 128, 144, 128, 2, 0, 6],
	[176, 64, 160, 16, -2, -2, 3],
	[32, 16, 16, 64, -2, 2, 3],
    # SUPPLY DEPOT 2
	[192, 80, 32, 80, -4, 0, 1],
	[32, 48, 192, 48, 4, 0, 1],
	[192, 16, 32, 16, -4, 0, 1],
    # CENTRAL HALL
	[112, 128, 112, 16, 0, -2, 4],
	[208, 112, 32, 112, -2, 0, 2],
	[16, 48, 208, 48, 2, 0, 2],
    # ACCESS TO SOUTHEAST EXIT
	[128, 112, 144, 112, 2, 0, 6],
	[144, 128, 208, 128, 2, 0, 1],
	[16, 80, 48, 16, 2, -2, 2],
    # EXIT TO UNDERGROUND
	[112, 128, 112, 16, 0, -4, 3],
	[48, 16, 48, 128, 0, 4, 3],
	[96, 16, 96, 128, 0, 2, 3],
    
    #-----------LEVEL 2-------------
    # WAREHOUSE ACCESS
    [32, 96, 32, 112, 0, 1, 6],
	[192, 16, 128, 128, -2, 2, 2],
	[0, 0, 0, 0, 0, 0, 0],
    # CONVECTION CORRIDOR
    [176, 48, 64, 48, -1, 0, 1],
	[48, 128, 32, 16, -2, -2, 3],
	[64, 48, 176, 48, 2, 0, 1],
    # SEWER MAINTENANCE
    [64, 16, 80, 128, 2, 2, 2],
	[96, 32, 160, 32, 2, 0, 1],
	[16, 96, 16, 16, 0, -2, 3],
    # COLD ZONE ACCESS CORRIDOR
    [48, 112, 208, 80, 2, -2, 2],
	[192, 48, 48, 16, -2, -2, 2],
	[16, 80, 16, 16, 0, -1, 3],
    # COLD ZONE ACCESS CORRIDOR
	[32, 48, 192, 48, 2, 0, 1],
	[160, 112, 112, 112, -2, 0, 1],
    [0, 0, 0, 0, 0, 0, 0],
    # FROZEN WAREHOUSE 1
	[112, 48, 32, 48, -2, 0, 1],
	[144, 128, 144, 80, 0, -2, 3],
	[64, 128, 64, 80, 0, -2, 3], 
    # CONVECTION CORRIDOR
	[112, 112, 112, 16, 0, -4, 4],
	[208, 128, 144, 16, -2, -2, 2],
	[80, 16, 32, 128, -2, 2, 2],  
    # TOXIC SEWERS 1
	[48, 112, 48, 16, 0, -2, 4],
	[144, 32, 192, 32, 2, 0, 1],
	[80, 16, 80, 112, 0, 4, 3],
    # ICE CAVE
	[160, 112, 80, 32, -2, -2, 2],
	[160, 32, 80, 112, -2, 2, 2],
	[48, 48, 64, 96, 2, 2, 3],    
    # ACCESS TO ICE CAVE
	[144, 32, 144, 112, 0, 4, 3],
	[80, 96, 80, 48, 0, -2, 3],
	[176, 128, 176, 16, 0, -4, 3],
    # FROZEN WAREHOUSE 2
	[80, 32, 80, 16, 0, -1, 6],
	[96, 128, 96, 96, 0, -2, 3],
	[160, 64, 176, 16, 2, -2, 3],
    # CONVECTION CORRIDOR
	[48, 112, 176, 112, 2, 0, 4],
	[32, 32, 208, 32, 4, 0, 3],
	[192, 64, 48, 64, -4, 0, 3],
    # TOXIC SEWERS 1
	[144, 128, 144, 16, 0, -4, 3],
	[80, 16, 80, 112, 0, 4, 3],
	[96, 32, 128, 32, 1, 0, 1],
    # ACCESS TO THE WARM ZONE
	[160, 80, 208, 16, 2, -2, 2],
	[144, 32, 80, 16, -2, -2, 3],
	[64, 80, 32, 16, -2, -2, 2],
    # EXIT TO THE WARM ZONE
	[112, 16, 160, 128, 4, 4, 2],
	[64, 32, 32, 128, -2, 2, 2],
	[16, 48, 16, 16, 0, -1, 3],

    #-----------LEVEL 3-------------
    # PELUSOIDS LAIR
	[80, 128, 112, 128, 2, 0, 6],
	[112, 112, 144, 112, 2, 0, 2],
	[0, 0, 0, 0, 0, 0, 0],
    # ALVARITOS GROTTO 2
	[192, 64, 32, 32, -2, -2, 2],
	[48, 128, 224, 112, 2, -2, 2],
	[16, 64, 32, 64, 2, 0, 6],
    # ALVARITOS GROTTO 1
	[160, 128, 160, 16, 0, -4, 3],
	[112, 32, 112, 128, 0, 4, 3],
	[64, 128, 16, 16, -4, -4, 2],
    # TOXIC WASTE STORAGE 2A
	[192, 96, 32, 96, -4, 0, 1],
	[32, 64, 192, 64, 2, 0, 1],
	[192, 32, 32, 32, -4, 0, 1],
    # UNDERGROUND TUNNEL
	[64, 16, 64, 128, 0, 4, 3],
	[112, 128, 112, 16, 0, -4, 3],
	[16, 112, 16, 16, 0, -4, 3],
    # SIDE HALL
	[112, 144, 112, 16, 0, -2, 4],
	[208, 144, 16, 48, -1, -1, 3],
	[128, 16, 128, 144, 0, 4, 3],
    # ARACHNOVIRUS LAIR
	[160, 128, 96, 128, -2, 0, 3],
	[208, 128, 208, 96, 0, -1, 3],
	[80, 112, 128, 112, 1, 0, 0],
    # UNSTABLE CORRIDORS 1
	[64, 128, 48, 32, -2, -2, 2],
	[208, 128, 208, 32, 0, -4, 3],
	[128, 32, 160, 128, 2, 2, 2],
    # UNSTABLE CORRIDORS 2
	[16, 32, 32, 128, 2, 2, 2],
	[128, 128, 128, 32, 0, -4, 3],
	[160, 32, 160, 128, 0, 4, 3],
    # TOXIC WASTE STORAGE 2B
	[48, 32, 192, 64, 4, 4, 2],
	[48, 128, 192, 128, 4, 0, 1],
	[192, 96, 64, 96, -2, 0, 1],
    # SIDE HALL
	[112, 128, 112, 16, 0, -2, 4],
	[208, 48, 16, 48, -2, 0, 3],
	[16, 112, 208, 112, 4, 0, 3],
    # ABANDONED MINE 1
	[192, 128, 32, 128, -4, 0, 1],
	[80, 32, 192, 32, 4, 0, 1],
	[16, 32, 32, 32, 2, 0, 6],
    # ABANDONED MINE 2
	[160, 32, 160, 128, 0, 4, 3],
	[192, 128, 96, 128, -1, 0, 1],
	[112, 32, 112, 128, 0, 2, 0],
    # ABANDONED MINE 3
	[112, 128, 128, 128, 2, 0, 6],
	[32, 32, 32, 128, 0, 2, 3],
	[96, 48, 176, 48, 4, 0, 1],
    # EXPLOSIVES STOCKPILE
	[128, 32, 128, 48, 0, 2, 6],
	[0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0]
]





#===============================================================================
# Auxiliar and generic functions
#===============================================================================

# get a value from a dictionary
def find_data(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return dic
    return -1

# returns a part of the surface
def clip(surf,x,y,x_size,y_size):
    handle_surf = surf.copy()
    handle_surf.set_clip(pygame.Rect(x,y,x_size,y_size))
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()

# change one colour for another
def swap_color(img,old_c,new_c):
    img.set_colorkey(old_c)
    surf = img.copy()
    surf.fill(new_c)
    surf.blit(img,(0,0))
    return surf

# calculates the distance between two points
def distance (x1, y1, x2, y2):
    dx = abs(x2-x1)
    dy = abs(y2-y1)
    if dx < dy:
        mn = dx
    else:
        mn = dy
    return(dx + dy - (mn >> 1) - (mn >> 2) + (mn >> 4))

def limit(val, min, max):
    if val < min:
        return min
    elif val > max:
        return max
    return val

# draws scanlines
def scanlines(surface, height, from_x, to_x, rgb):
    j = V_MARGIN
    while j < height:
        j+=3
        pygame.draw.line(surface, (rgb, rgb, rgb), (from_x, j), (to_x, j))

# applies scanlines according to the configuration
def make_scanlines():
    if cfg_scanlines_type == 2: # HQ
        scanlines(screen_sl, WIN_SIZE[1]-30, H_MARGIN, WIN_SIZE[0]-H_MARGIN-1, 200)
        screen.blit(screen_sl, (0, 0))
    elif cfg_scanlines_type == 1: # fast
        scanlines(screen, WIN_SIZE[1]-30, H_MARGIN, WIN_SIZE[0]-H_MARGIN-1, 15)

# draws a centred message box erasing the background
def message_box(message1, message2):
    # calculates the dimensions of the box
    height = 36
    message1_len = len(message1) * 7 # approximate length of text 1 in pixels
    message2_len = len(message2) * 4 # approximate length of text 2 in pixels
    # width = length of the longest text + margin
    if message1_len > message2_len:
        width = message1_len + V_MARGIN
    else:
        width = message2_len + V_MARGIN
    # calculates the position of the box
    x = (MAP_UNSCALED_SIZE[0]//2) - (width//2)
    y = (MAP_UNSCALED_SIZE[1]//2) - (height//2)
    pygame.draw.rect(map_display, PALETTE['BLACK'],(x, y, width, height))
    # paints the text centred inside the box (Y positions are fixed)
    text_x = (x + (width//2)) - (message1_len//2)
    text_y = y + 5
    bg_font_L.render(message1, map_display, (text_x, text_y))
    fg_font_L.render(message1, map_display, (text_x - 2, text_y - 2))
    text_x = (x + (width//2)) - (message2_len//2)
    text_y = y + 24
    bg_font_S.render(message2, map_display, (text_x, text_y))
    fg_font_S.render(message2, map_display, (text_x - 1, text_y - 1))





#===============================================================================
# Font class
#===============================================================================

# generates the letters (and letter spacing) from the font image
def load_font_img(path, font_color, is_transparent):
    fg_color = (255, 0, 0) # original red
    bg_color = (0, 0, 0) # black
    font_img = pygame.image.load(jp(dp,path)).convert() # load font image
    font_img = swap_color(font_img, fg_color, font_color) # apply the requested font colour
    last_x = 0
    letters = []
    letter_spacing = []
    for x in range(font_img.get_width()): # for the entire width of the image
        if font_img.get_at((x, 0))[0] == 127: # gray separator
            # saves in the array the portion of the image with the letter we are interested in.
            letters.append(clip(font_img, last_x, 0, x - last_x, font_img.get_height()))
            # saves the width of the letter
            letter_spacing.append(x - last_x)
            last_x = x + 1
        x += 1
    if is_transparent:
        # erases the background colour of each letter in the array
        for letter in letters:
            letter.set_colorkey(bg_color) 

    return letters, letter_spacing, font_img.get_height()

# creates a new font from an image path and a colour
class Font():
    def __init__(self, path, color, transparent):
        self.letters, self.letter_spacing, self.line_height = load_font_img(path, color, transparent)
        self.font_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
        'N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e',
        'f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w',
        'x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5',
        '6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';']
        self.space_width = self.letter_spacing[0]
        self.base_spacing = 1
        self.line_spacing = 2

    # draw the text
    def render(self, text, surf, loc):
        x_offset = 0
        y_offset = 0
        for char in text:
            if char not in ['\n', ' ']:
                # draw the letter and add the width
                surf.blit(self.letters[self.font_order.index(char)], (loc[0] + x_offset, loc[1] + y_offset))
                x_offset += self.letter_spacing[self.font_order.index(char)] + self.base_spacing
            elif char == ' ':
                x_offset += self.space_width + self.base_spacing
            else: # line feed
                y_offset += self.line_spacing + self.line_height
                x_offset = 0





#===============================================================================
# Map functions
#===============================================================================

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

# draws the tile map on the screen
def draw_map(map_display):
    anim_tiles_list.clear()
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
            # generates the list of animated tiles of the current map
            # (frame_1, frame_2, x, y, num_frame)
            if t['image'] in ANIM_TILES.keys():                
                anim_tiles_list.append(
                    [tile, pygame.image.load(jp(dp, 'images/tiles/' + ANIM_TILES[t['image']])).convert(), 
                    tileRect.topleft[0], tileRect.topleft[1], 0])

# select some of the animated tiles on the current map to change the frame
def animate_tiles():
    for anim_tile in anim_tiles_list: # for each animated tile on the map
        if random.randint(0,24) == 0: # 4% chance of changing frame
            tile = anim_tile[0+anim_tile[4]] # select image according to frame number
            tileRect = tile.get_rect()
            tileRect.topleft = (anim_tile[2], anim_tile[3]) # sets the xy position
            map_display_backup.blit(tile, tileRect) # draws on the background image
            # update frame number
            anim_tile[4] += 1
            if anim_tile[4] > 1:
                anim_tile[4] = 0
            
          



#===============================================================================
# Scoreboard functions
#===============================================================================

# draws the name of the map and other data at the top
def draw_map_info():
    x = 0
    y = 22
    progress_x = SBOARD_UNSCALED_SIZE[0] - 55
    
    if map_number < 9:
        text_1 = 'SCREEN.......'
    else:
        text_1 = 'SCREEN.....'
    if game_percent < 10:
        text_2 = 'COMPLETED....'
    else:
        text_2 = 'COMPLETED..'
    
    text_1 += str(map_number+1) + '/45'
    text_2 += str(game_percent) + ';' # %

    sboard_display.fill((0,0,0)) # delete previous text

    # map name
    bg_font_L.render(MAP_NAMES[map_number], sboard_display, (x+2, y+2)) # shadow
    fg_font_L.render(MAP_NAMES[map_number], sboard_display, (x, y))
    # map number
    bg_font_S.render(text_1, sboard_display, (progress_x+1, y+1)) # shadow
    fg_font_S.render(text_1, sboard_display, (progress_x, y))
    # game percentage
    bg_font_S.render(text_2, sboard_display, (progress_x+1, y+bg_font_S.line_height+1)) # shadow
    fg_font_S.render(text_2, sboard_display, (progress_x, y+fg_font_S.line_height))

def init_scoreboard():
    # icons
    sboard_display.blit(lives_icon, (0, 2))
    sboard_display.blit(oxigen_icon, (42, 2))
    sboard_display.blit(ammo_icon, (82, 2))
    sboard_display.blit(keys_icon, (145, 2))
    sboard_display.blit(explosives_icon, (186, 2))
    # fixed texts
    bg_font_L.render('+50', sboard_display, (116, 6))
    fg_font_L.render('+50', sboard_display, (114, 4))
    bg_font_L.render('+10', sboard_display, (220, 6))
    fg_font_L.render('+10', sboard_display, (218, 4))

def update_scoreboard():
    # values
    bg_font_L.render(str(player.lives).rjust(2, '0'), sboard_display, (20, 6))
    fg_font_L.render(str(player.lives).rjust(2, '0'), sboard_display, (18, 4))
    bg_font_L.render(str(player.oxigen).rjust(2, '0'), sboard_display, (62, 6))
    fg_font_L.render(str(player.oxigen).rjust(2, '0'), sboard_display, (60, 4))
    bg_font_L.render(str(player.ammo).rjust(2, '0'), sboard_display, (102, 6))
    fg_font_L.render(str(player.ammo).rjust(2, '0'), sboard_display, (100, 4))
    bg_font_L.render(str(player.keys).rjust(2, '0'), sboard_display, (166, 6))
    fg_font_L.render(str(player.keys).rjust(2, '0'), sboard_display, (164, 4))
    bg_font_L.render(str(player.explosives).rjust(2, '0'), sboard_display, (206, 6))
    fg_font_L.render(str(player.explosives).rjust(2, '0'), sboard_display, (204, 4))





#===============================================================================
# Player class
#===============================================================================

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # properties
        self.lives = 10
        self.oxigen = 99
        self.ammo = 5
        self.keys = 0
        self.explosives = 0
        # images
        num_frames = 3
        self.images = []
        for i in range(num_frames):
            # image for the frame
            self.images.append(pygame.image.load(
                jp(dp, 'images/sprites/player{}.png'.format(i))).convert())
            # mask
            self.images[i].set_colorkey((255, 0, 255))
        self.animation_index = 0
        self.animation_speed = 0.08
        self.image = self.images[self.animation_index]
        # initial position
        self.rect = self.image.get_rect()
        self.rect.x = 32
        self.rect.y = 112

    def update(self):
        # animation
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.images):
            self.animation_index = 0
        self.image = self.images[int(self.animation_index)]
        # movement
        self.mx = 0
        self.my = 0
        key_state = pygame.key.get_pressed()
        if key_state[K_o]:
            self.mx -= 1
        if key_state[K_p]:
            self.mx += 1
        if key_state[K_q]:
            self.my -= 1
        if key_state[K_a]:
            self.my += 1
        self.rect.x += self.mx
        self.rect.y += self.my





#===============================================================================
# Enemy class
#===============================================================================

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_data): # x1, y1, x2, y2, mx, my, type
        super(Enemy, self).__init__()
        # max/min xy values
        self.x = self.x1 = enemy_data[0]
        self.y = self.y1 = enemy_data[1]
        self.x2 = enemy_data[2]
        self.y2 = enemy_data[3]
        # movement
        self.mx = enemy_data[4] / 2
        self.my = enemy_data[5] / 2
        # enemy type
        self.type = enemy_data[6]
        if self.type == 1:
            enemy_name = 'infected'
        elif self.type == 2:
            enemy_name = 'pelusoid'
        elif self.type == 3:
            enemy_name = 'avirus'
        elif self.type == 4:
            enemy_name = 'platform'
        elif self.type == 6:
            enemy_name = 'fanty'
            self.state = 0 # 0=idle  1=pursuing  2=retreating
            self.sight_distance = 64
            self.acceleration = 16
            self.max_speed = 256
        # images
        num_frames = 2
        self.images = []
        for i in range(num_frames):
            # image for the frame
            self.images.append(pygame.image.load(
                jp(dp, 'images/sprites/' + enemy_name + str(i) + '.png')).convert())
            # mask
            self.images[i].set_colorkey((255, 0, 255))
        self.animation_index = 0
        self.animation_speed = 0.08
        self.image = self.images[self.animation_index]
        self.rect = self.image.get_rect()

    def update(self):
        # animation
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.images):
            self.animation_index = 0
        self.image = self.images[int(self.animation_index)]
        # movement
        if self.type != 6: # no fanty  
            self.x += self.mx
            self.y += self.my
            if self.x == self.x1 or self.x == self.x2:
                self.mx = -self.mx
            if self.y == self.y1 or self.y == self.y2:
                self.my = -self.my
        else: # fanty
            if self.state == 0: # idle
                if distance(0, 0, self.x, self.y) <= self.sight_distance:
                    self.state = 1 # pursuing
            elif self.state == 1: # pursuing
                if distance(0, 0, self.x, self.y) > self.sight_distance:
                    self.state = 2 # retreating
                else:
                    #en_an [gpit].vx = limit(en_an [gpit].vx + addsign (player.x - en_an [gpit].x, FANTY_A),-FANTY_MAX_V, FANTY_MAX_V)
                    #en_an [gpit].vy = limit(en_an [gpit].vy + addsign (player.y - en_an [gpit].y, FANTY_A),-FANTY_MAX_V, FANTY_MAX_V)                        
                    #en_an [gpit].x = limit(en_an [gpit].x + en_an [gpit].vx, 0, 14336)
                    #en_an [gpit].y = limit(en_an [gpit].y + en_an [gpit].vy, 0, 9216) 
                    pass               
            else: # retreating
                #en_an [gpit].x += addsign(malotes [enoffsmasi].x - gpen_cx, 64)
                #en_an [gpit].y += addsign(malotes [enoffsmasi].y - gpen_cy, 64)                
                if distance (0, 0, self.x, self.y) <= self.sight_distance:
                    self.state = 1 # pursuing					
                        				
            #gpen_cx = en_an [gpit].x >> 6;
            #gpen_cy = en_an [gpit].y >> 6;
            if self.state == 2 and self.x == self.x1 and self.y == self.y1:
                self.state = 0 # idle

        self.rect.x = self.x
        self.rect.y = self.y





#===============================================================================
# Main functions
#===============================================================================

def confirm_exit():
    message_box('Leave the current game?', 'PRESS Y / ENTER TO EXIT OR N TO CONTINUE')
    screen.blit(pygame.transform.scale(sboard_display, SBOARD_SCALED_SIZE), (H_MARGIN, V_MARGIN))        
    screen.blit(pygame.transform.scale(map_display, MAP_SCALED_SIZE), (H_MARGIN, SBOARD_SCALED_SIZE[1] + V_MARGIN))
    make_scanlines()
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYUP:
            # exit by pressing ESC key
                if event.key == K_y:                    
                    return True
                elif event.key == K_n:  
                    return False

# Main menu
def main_menu():
    map_display.fill(PALETTE['BLACK'])
    sboard_display.fill(PALETTE['BLACK'])
    message_box('Red Planet Pi', 'WIP. Press a key to continue')
    screen.blit(pygame.transform.scale(sboard_display, SBOARD_SCALED_SIZE), (H_MARGIN, V_MARGIN))     
    screen.blit(pygame.transform.scale(map_display, MAP_SCALED_SIZE), (H_MARGIN, SBOARD_SCALED_SIZE[1] + V_MARGIN))
    make_scanlines()
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYUP:
                waiting = False
            # exit by pressing ESC key
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()





#===============================================================================
# Main loop
#===============================================================================

# Initialisation
pygame.init()
pygame.mixer.init()
# generates a main window (or full screen) 
# with title, icon, and 32-bit colour.
flags = 0
if cfg_full_screen:
    flags = FULLSCREEN
screen = pygame.display.set_mode(WIN_SIZE, flags, 32)
pygame.display.set_caption('.:: Red Planet Pi ::.')
icon = pygame.image.load(jp(dp, 'images/assets/icon.png')).convert_alpha()
pygame.display.set_icon(icon)   
# area covered by the map
map_display = pygame.Surface(MAP_UNSCALED_SIZE)
# surface to save the generated map without sprites
map_display_backup = pygame.Surface(MAP_UNSCALED_SIZE)
# area covered by the scoreboard
sboard_display = pygame.Surface(SBOARD_UNSCALED_SIZE)
# surface for HQ scanlines
screen_sl = pygame.Surface(WIN_SIZE)
screen_sl.set_alpha(40)

# fonts
fg_font_S = Font('images/fonts/small_font.png', PALETTE['GREEN'], True)
bg_font_S = Font('images/fonts/small_font.png', PALETTE['DARK_GREEN'], False)
fg_font_L = Font('images/fonts/large_font.png', PALETTE['WHITE'], True)
bg_font_L = Font('images/fonts/large_font.png', PALETTE['DARK_GRAY'], True)
aux_font_L = Font('images/fonts/large_font.png', PALETTE['YELLOW'], False)

# scoreboard icons
lives_icon = pygame.image.load(jp(dp, 'images/assets/lives.png')).convert()
oxigen_icon = pygame.image.load(jp(dp, 'images/tiles/T53.png')).convert()
ammo_icon = pygame.image.load(jp(dp, 'images/tiles/T52.png')).convert()
keys_icon = pygame.image.load(jp(dp, 'images/tiles/T51.png')).convert()
explosives_icon = pygame.image.load(jp(dp, 'images/tiles/T50.png')).convert()

# clock to control the FPS
clock = pygame.time.Clock()

game_status = OVER
music_status = UNMUTED 

# Main loop
while True:    
    if game_status == OVER: # game not running
        main_menu()
        # sprite control groups
        all_sprites_group = pygame.sprite.Group()     
        enemies_group = pygame.sprite.Group()
        # create the player
        player = Player()
        # ingame music
        pygame.mixer.music.load(jp(dp, "sounds/ingame.ogg"))
        pygame.mixer.music.play(-1)
        # reset variables
        game_status = RUNNING
        last_map = -1
    else: # game running or paused
        # event management
        for event in pygame.event.get():
            # exit when click on the X in the window
            if event.type == QUIT: 
                exit()
            if event.type == KEYDOWN:
                # exit by pressing ESC key
                if event.key == K_ESCAPE:
                    if confirm_exit():
                        game_status = OVER # go to the main menu
                # pause main loop
                if event.key == K_h:
                    if game_status == RUNNING:
                        game_status = PAUSED
                        # mute the music if necessary
                        if music_status == UNMUTED:
                            pygame.mixer.music.fadeout(1200)
                    else:
                        game_status = RUNNING
                        # restore music if necessary
                        if music_status == UNMUTED:
                            pygame.mixer.music.play()
                # mute music
                if event.key == K_m :
                    if music_status == MUTED:
                        music_status = UNMUTED
                        pygame.mixer.music.play()
                    else:
                        music_status = MUTED
                        pygame.mixer.music.fadeout(1200)

                # temp code ================
                if event.key == K_RIGHT:
                    if map_number < 44:
                        map_number += 1
                if event.key == K_LEFT:
                    if map_number > 0:
                        map_number -= 1
                # ==========================

        # change map if neccessary
        if map_number != last_map:
            load_map(map_number, map_display)
            # save the new empty background
            map_display_backup.blit(map_display, (0,0))
            draw_map_info()
            init_scoreboard()
            update_scoreboard()
            last_map = map_number        
            # reset the groups  
            all_sprites_group.empty()
            enemies_group.empty()
            # add the player  
            all_sprites_group.add(player)
            # add enemies to the map reading from 'ENEMIES_DATA' list (enems.h)
            # (a maximum of three enemies per map)
            for i in range(3):
                enemy_data = ENEMIES_DATA[map_number*3 + i]
                if enemy_data[6] != 0: # no enemy
                    enemy = Enemy(enemy_data)
                    all_sprites_group.add(enemy)
                    enemies_group.add(enemy)

        if game_status == RUNNING:
            # update sprites
            all_sprites_group.update()
            # collisions
            if player.lives == 0:
                # print game over message
                game_status = OVER
            # paint the map free of sprites to clean it up
            map_display.blit(map_display_backup, (0,0))
            # and change the frame of the animated tiles
            animate_tiles()
            # print sprites
            all_sprites_group.draw(map_display)
        elif game_status == PAUSED:            
            message_box('P a u s e', 'THE MASSACRE CAN WAIT')

    # FPS counter using the clock   
    # aux_font_L.render(str(int(clock.get_fps())).rjust(3, '0') + ' FPS', sboard_display, (124, 22))

    # scale x 3 the scoreboard
    screen.blit(pygame.transform.scale(sboard_display, SBOARD_SCALED_SIZE), 
        (H_MARGIN, V_MARGIN))
    # scale x 3 the map
    screen.blit(pygame.transform.scale(map_display, MAP_SCALED_SIZE), 
        (H_MARGIN, SBOARD_SCALED_SIZE[1] + V_MARGIN))
    
    make_scanlines()
    pygame.display.update() # refreshes the screen
    clock.tick(60) # 60 FPS