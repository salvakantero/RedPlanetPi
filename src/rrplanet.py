
# ==============================================================================
# Raspi-Red Planet v1.0
# salvaKantero 2022
# ==============================================================================

import pygame # pygame library functions
import random, os, sys, json # python generic functions


from pygame.locals import * # allows constants without typing "pygame."
from pygame.constants import (QUIT, KEYDOWN, K_ESCAPE, K_LEFT, K_RIGHT) 





#===============================================================================
# Global variables
#===============================================================================

dp = os.path.dirname(__file__) + '/' # exec path (+ '/' when using VS Code)
jp = os.path.join # forms the folder/file path

win_size = 800, 600 # main window size
map_scaled_size = 720, 480 # map size (scaled x3)
map_unscaled_size = 240, 160 # map size (unscaled)
sboard_scaled_size = 720, 114 # scoreboard size (scaled x3)
sboard_unscaled_size = 240, 38 # scoreboard size (unscaled)

# map tiles
tile_width = 16
tile_height = 16
anim_tiles = {
    # frame_1   frame_2
    'T4.png' : 'T70.png',   # computer 1
    'T8.png' : 'T71.png',   # computer 2
    'T9.png' : 'T72.png',   # corpse
    'T25.png' : 'T73.png',  # toxic waste
    'T29.png' : 'T74.png'   # lava
}
anim_tiles_list = [] # (frame_1, frame_2, x, y, num_frame)

map_number = 0 # current map number
last_map = -1 # last map loaded

game_percent = 0 # % of gameplay completed
lives = 10 # remaining player lives
oxigen = 99 # remaining player oxigen
ammo = 5 # bullets available in the gun
keys = 0 # unused keys collected
explosives = 0 # explosives collected

# configuration values
cfg_scanlines_type = 2  # 0 = none, 1 = fast, 2 = HQ

# colour palette (Pico8)
palette = {
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
map_names = {
    0  : 'CONTROL CENTRE',
    1  : 'SUPPLY DEPOT 1',
    2  : 'CENTRAL HALL LEVEL 0',
    3  : 'TOXIC WASTE STORAGE 1A',
    4  : 'TOXIC WASTE STORAGE 1B',
    5  : 'WEST PASSAGE LEVEL -1',
    6  : 'ACCESS TO WEST PASSAGES',
    7  : 'CENTRAL HALL LEVEL -1',
    8  : 'ACCESS TO DUNGEONS',
    9  : 'DUNGEONS',
    10 : 'WEST PASSAGE LEVEL -2',
    11 : 'SUPPLY DEPOT 2',
    12 : 'CENTRAL HALL LEVEL -2',
    13 : 'ACCESS TO SOUTHEAST EXIT',
    14 : 'EXIT TO UNDERGROUND',
    15 : 'PELUSOIDS LAIR',
    16 : 'ALVARITOS GROTTO 2',
    17 : 'ALVARITOS GROTTO 1',
    18 : 'TOXIC WASTE STORAGE 2A',
    19 : 'UNDERGROUND TUNNEL',
    20 : 'SIDE HALL LEVEL -4',
    21 : 'ARACHNOVIRUS LAIR',
    22 : 'UNSTABLE CORRIDORS 1',
    23 : 'UNSTABLE CORRIDORS 2',
    24 : 'TOXIC WASTE STORAGE 2B',
    25 : 'SIDE HALL LEVEL -5',
    26 : 'ABANDONED MINE 1',
    27 : 'ABANDONED MINE 2',
    28 : 'ABANDONED MINE 3',
    29 : 'EXPLOSIVES STOCKPILE',
    30 : 'BACK TO CONTROL CENTER',
}





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

# scanlines
def apply_scanlines(surface, height, from_x, to_x, rgb):
    j = 0
    while j < height:
        j+=3
        pygame.draw.line(surface, (rgb, rgb, rgb), (from_x, j), (to_x, j))





#===============================================================================
# Font class and functions
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

# draws text with border
def outlined_text(bg_font, fg_font, t, surf, pos):
    bg_font.render(t, surf, [pos[0] - 1, pos[1]])
    bg_font.render(t, surf, [pos[0] + 1, pos[1]])
    bg_font.render(t, surf, [pos[0], pos[1] - 1])
    bg_font.render(t, surf, [pos[0], pos[1] + 1])
    fg_font.render(t, surf, [pos[0], pos[1]])





#===============================================================================
# Map functions
#===============================================================================

# loads a map and draws it on screen
def load_map(map_number, map_display):
    global map_data
    map_data = process_map(jp(dp, 'maps/map' + str(map_number) + '.json'))
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
            if t['image'] in anim_tiles.keys():                
                anim_tiles_list.append(
                    [tile, pygame.image.load(jp(dp, 'images/tiles/' + anim_tiles[t['image']])).convert(), 
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
    progress_x = sboard_unscaled_size[0] - 55
    
    if map_number < 9:
        text_1 = 'SCREEN.......'
    else:
        text_1 = 'SCREEN.....'
    if game_percent < 10:
        text_2 = 'COMPLETED....'
    else:
        text_2 = 'COMPLETED..'
    
    text_1 += str(map_number+1) + '/30'
    text_2 += str(game_percent) + ';' # %

    sboard_display.fill((0,0,0)) # delete previous text

    # map name
    bg_font_L.render(map_names[map_number], sboard_display, (x+2, y+2)) # shadow
    fg_font_L.render(map_names[map_number], sboard_display, (x, y))
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
    bg_font_L.render(str(lives).rjust(2, '0'), sboard_display, (20, 6))
    fg_font_L.render(str(lives).rjust(2, '0'), sboard_display, (18, 4))
    bg_font_L.render(str(oxigen).rjust(2, '0'), sboard_display, (62, 6))
    fg_font_L.render(str(oxigen).rjust(2, '0'), sboard_display, (60, 4))
    bg_font_L.render(str(ammo).rjust(2, '0'), sboard_display, (102, 6))
    fg_font_L.render(str(ammo).rjust(2, '0'), sboard_display, (100, 4))
    bg_font_L.render(str(keys).rjust(2, '0'), sboard_display, (166, 6))
    fg_font_L.render(str(keys).rjust(2, '0'), sboard_display, (164, 4))
    bg_font_L.render(str(explosives).rjust(2, '0'), sboard_display, (206, 6))
    fg_font_L.render(str(explosives).rjust(2, '0'), sboard_display, (204, 4))





#===============================================================================
# Enemy class and functions
#===============================================================================

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, mx, my, type):
        super(Enemy, self).__init__()
        # max/min xy values
        self.x = self.x1 = x1
        self.y = self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        # movement
        self.mx = mx / 2
        self.my = my / 2
        # enemy type
        self.type = type
        if type == 1:
            enemy_name = 'infected'
        elif type == 2:
            enemy_name = 'pelusoid'
        elif type == 3:
            enemy_name = 'avirus'
        elif type == 4:
            enemy_name = 'platform'
        elif type == 6:
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

        self.rect = pygame.Rect(self.x, self.y, tile_width, tile_height)





#===============================================================================
# Main
#===============================================================================

# Initialisation
pygame.init()
pygame.mixer.init()

# generates a main window with title, icon, and 32-bit colour.
screen = pygame.display.set_mode(win_size, 0, 32)
pygame.display.set_caption('.:: Raspi-Red Planet ::.')
icon = pygame.image.load(jp(dp, 'images/assets/icon.png')).convert_alpha()
pygame.display.set_icon(icon)

# area covered by the map
map_display = pygame.Surface(map_unscaled_size)
# surface to save the generated map without sprites
map_display_backup = pygame.Surface(map_unscaled_size)
# area covered by the scoreboard
sboard_display = pygame.Surface(sboard_unscaled_size)
# surface for HQ scanlines
screen_sl = pygame.Surface(win_size)
screen_sl.set_alpha(40)

# fonts
fg_font_S = Font('images/fonts/small_font.png', palette['GREEN'], True)
bg_font_S = Font('images/fonts/small_font.png', palette['DARK_GREEN'], False)
fg_font_L = Font('images/fonts/large_font.png', palette['WHITE'], True)
bg_font_L = Font('images/fonts/large_font.png', palette['DARK_GRAY'], False)
aux_font_L = Font('images/fonts/large_font.png', palette['YELLOW'], False)

# scoreboard icons
lives_icon = pygame.image.load(jp(dp, 'images/assets/lives.png')).convert()
oxigen_icon = pygame.image.load(jp(dp, 'images/tiles/T53.png')).convert()
ammo_icon = pygame.image.load(jp(dp, 'images/tiles/T52.png')).convert()
keys_icon = pygame.image.load(jp(dp, 'images/tiles/T51.png')).convert()
explosives_icon = pygame.image.load(jp(dp, 'images/tiles/T50.png')).convert()

# enemy sprites control
enemy_group = pygame.sprite.Group()

# clock to control the FPS
clock = pygame.time.Clock()

# ingame music
pygame.mixer.music.load(jp(dp, "sounds/ingame.ogg"))
pygame.mixer.music.play(-1)

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

            # temp code ================
            if event.key == K_RIGHT:
                if map_number < 29:
                    map_number += 1
            if event.key == K_LEFT:
                if map_number > 0:
                    map_number -= 1
            # ==========================

    # change map if neccessary
    if map_number != last_map:
        load_map(map_number, map_display)
        # save the empty background
        map_display_backup.blit(map_display, (0,0))
        draw_map_info()
        init_scoreboard()
        update_scoreboard()
        last_map = map_number

        # load enemies for the map (enems.h)
        enemy_group.empty()
        # CONTROL CENTRE
        if map_number == 0: 
            # parameters:    X1   Y1  X2   Y2  mX mY  Type
            enemy_1 = Enemy(128, 112, 32, 112, -2, 0, 1)
            enemy_2 = Enemy(16, 16, 224, 48, 2, 2, 2)
            enemy_group.add(enemy_1, enemy_2)
        # SUPPLY DEPOT 1
        elif map_number == 1:
            enemy_1 = Enemy(192, 112, 32, 112, -4, 0, 1)
            enemy_2 = Enemy(208, 16, 144, 64, -1, 1, 2)
            enemy_3 = Enemy(80, 64, 80, 16, 0, -2, 3)
            enemy_group.add(enemy_1, enemy_2, enemy_3)   
        # CENTRAL HALL LEVEL 0  
        elif map_number == 2:
            enemy_1 = Enemy(112, 144, 112, 32, 0, -2, 4)
            enemy_2 = Enemy(208, 112, 16, 80, -2, -2, 2)
            enemy_group.add(enemy_1, enemy_2)   
        # TOXIC WASTE STORAGE 1A
        elif map_number == 3:
            enemy_1 = Enemy(160, 48, 32, 48, -4, 0, 1)
            enemy_2 = Enemy(16, 80, 208, 112, 4, 4, 3)
            enemy_group.add(enemy_1, enemy_2)   
        # TOXIC WASTE STORAGE 1B
        elif map_number == 4:
            enemy_1 = Enemy(64, 80, 64, 16, 0, -2, 3)
            enemy_2 = Enemy(144, 16, 144, 128, 0, 2, 3)
            enemy_3 = Enemy(208, 112, 208, 96, 0, -2, 6)
            enemy_group.add(enemy_1, enemy_2, enemy_3) 
        # WEST PASSAGE LEVEL -1
        elif map_number == 5:
            enemy_1 = Enemy(32, 48, 192, 48, 2, 0, 1)
            enemy_2 = Enemy(192, 80, 32, 80, -2, 0, 1)
            enemy_3 = Enemy(144, 128, 160, 128, 2, 0, 6)
            enemy_group.add(enemy_1, enemy_2, enemy_3) 
        # ACCESS TO WEST PASSAGES
        elif map_number == 6:
            enemy_1 = Enemy(96, 48, 48, 16, -2, -2, 3)
            enemy_2 = Enemy(144, 80, 144, 16, 0, -2, 3)
            enemy_3 = Enemy(16, 112, 16, 96, 0, -2, 6)
            enemy_group.add(enemy_1, enemy_2, enemy_3) 
        # CENTRAL HALL LEVEL -1
        elif map_number == 7:
            enemy_1 = Enemy(112, 144, 112, 16, 0, -2, 4)
            enemy_2 = Enemy(208, 96, 16, 96, -2, 0, 3)
            enemy_3 = Enemy(16, 32, 192, 64, 1, 1, 2)
            enemy_group.add(enemy_1, enemy_2, enemy_3) 
        # ACCESS TO DUNGEONS
        elif map_number == 8:
            enemy_1 = Enemy(208, 64, 192, 64, -2, 0, 6)
            enemy_2 = Enemy(64, 64, 64, 32, 0, -1, 3)
            enemy_group.add(enemy_1, enemy_2)  
        # DUNGEONS
        elif map_number == 9:
            enemy_1 = Enemy(144, 128, 144, 16, 0, -4, 3)
            enemy_2 = Enemy(80, 16, 80, 128, 0, 4, 3)
            enemy_3 = Enemy(192, 128, 208, 128, 2, 0, 6)
            enemy_group.add(enemy_1, enemy_2, enemy_3) 
        # WEST PASSAGE LEVEL -2
        elif map_number == 10: 
            enemy_1 = Enemy(128, 128, 144, 128, 2, 0, 6)
            enemy_2 = Enemy(176, 64, 160, 16, -2, -2, 3)
            enemy_3 = Enemy(32, 16, 16, 64, -2, 2, 3)
            enemy_group.add(enemy_1, enemy_2, enemy_3) 
        # SUPPLY DEPOT 2
        elif map_number == 11:
            enemy_1 = Enemy(192, 80, 32, 80, -4, 0, 1)
            enemy_2 = Enemy(32, 48, 192, 48, 4, 0, 1)
            enemy_3 = Enemy(192, 16, 32, 16, -4, 0, 1)
            enemy_group.add(enemy_1, enemy_2, enemy_3) 
        # CENTRAL HALL LEVEL -2
        elif map_number == 12:
            enemy_1 = Enemy(112, 128, 112, 16, 0, -2, 4)
            enemy_2 = Enemy(208, 112, 32, 112, -2, 0, 2)
            enemy_3 = Enemy(16, 48, 208, 48, 2, 0, 2)
            enemy_group.add(enemy_1, enemy_2, enemy_3) 
        # ACCESS TO SOUTHEAST EXIT
        elif map_number == 13:
            enemy_1 = Enemy(128, 112, 144, 112, 2, 0, 6)
            enemy_2 = Enemy(144, 128, 208, 128, 2, 0, 1)
            enemy_3 = Enemy(16, 80, 48, 16, 2, -2, 2)
            enemy_group.add(enemy_1, enemy_2, enemy_3) 
        # EXIT TO UNDERGROUND
        elif map_number == 14:
            enemy_1 = Enemy(112, 128, 112, 16, 0, -4, 3)
            enemy_2 = Enemy(48, 16, 48, 128, 0, 4, 3)
            enemy_3 = Enemy(96, 16, 96, 128, 0, 2, 3)
            enemy_group.add(enemy_1, enemy_2, enemy_3) 
        # PELUSOIDS LAIR
        elif map_number == 15:
            enemy_1 = Enemy(96, 128, 80, 128, -2, 0, 6)
            enemy_2 = Enemy(112, 112, 144, 112, 2, 0, 2)
            enemy_group.add(enemy_1, enemy_2)  
        # ALVARITOS GROTTO 2
        elif map_number == 16:
            enemy_1 = Enemy(192, 64, 32, 32, -2, -2, 2)
            enemy_2 = Enemy(48, 128, 224, 112, 2, -2, 2)
            enemy_3 = Enemy(16, 64, 32, 64, 2, 0, 6)
            enemy_group.add(enemy_1, enemy_2, enemy_3) 
        # ALVARITOS GROTTO 1
        elif map_number == 17:
            enemy_1 = Enemy(160, 128, 160, 16, 0, -4, 3)
            enemy_2 = Enemy(112, 32, 112, 128, 0, 4, 3)
            enemy_3 = Enemy(64, 128, 16, 16, -4, -4, 2)
            enemy_group.add(enemy_1, enemy_2, enemy_3) 
        # TOXIC WASTE STORAGE 2A
        elif map_number == 18:
            enemy_1 = Enemy(192, 96, 32, 96, -4, 0, 1)
            enemy_2 = Enemy(32, 64, 192, 64, 2, 0, 1)
            enemy_3 = Enemy(192, 32, 32, 32, -4, 0, 1)
            enemy_group.add(enemy_1, enemy_2, enemy_3) 
        # UNDERGROUND TUNNEL
        elif map_number == 19:
            enemy_1 = Enemy(64, 16, 64, 128, 0, 4, 3)
            enemy_2 = Enemy(112, 128, 112, 16, 0, -4, 3)
            enemy_3 = Enemy(16, 112, 16, 16, 0, -4, 3)
            enemy_group.add(enemy_1, enemy_2, enemy_3) 
        # SIDE HALL LEVEL -4
        elif map_number == 20:
            enemy_1 = Enemy(112, 144, 112, 32, 0, -2, 4)
            enemy_2 = Enemy(208, 144, 16, 48, -1, -1, 2)
            enemy_3 = Enemy(128, 16, 128, 144, 0, 4, 3)
            enemy_group.add(enemy_1, enemy_2, enemy_3) 
        # ARACHNOVIRUS LAIR
        elif map_number == 21:
            enemy_1 = Enemy(160, 128, 96, 128, -2, 0, 3)
            enemy_2 = Enemy(208, 128, 208, 96, 0, -1, 3)
            enemy_group.add(enemy_1, enemy_2) 
        # UNSTABLE CORRIDORS 1
        elif map_number == 22:
            enemy_1 = Enemy(64, 128, 48, 32, -2, -2, 2)
            enemy_2 = Enemy(208, 128, 208, 32, 0, -4, 3)
            enemy_3 = Enemy(128, 32, 160, 128, 2, 2, 2)
            enemy_group.add(enemy_1, enemy_2, enemy_3) 
        # UNSTABLE CORRIDORS 2
        elif map_number == 23:
            enemy_1 = Enemy(16, 32, 32, 128, 2, 2, 2)
            enemy_2 = Enemy(128, 128, 128, 32, 0, -4, 3)
            enemy_3 = Enemy(160, 32, 160, 128, 0, 4, 3)
            enemy_group.add(enemy_1, enemy_2, enemy_3) 
        # TOXIC WASTE STORAGE 2B
        elif map_number == 24:
            enemy_1 = Enemy(48, 32, 192, 64, 4, 4, 2)
            enemy_2 = Enemy(48, 128, 192, 128, 4, 0, 1)
            enemy_3 = Enemy(192, 96, 64, 96, -2, 0, 1)
            enemy_group.add(enemy_1, enemy_2, enemy_3) 
        # SIDE HALL LEVEL -5
        elif map_number == 25:
            enemy_1 = Enemy(112, 128, 112, 16, 0, -2, 4)
            enemy_2 = Enemy(208, 48, 16, 48, -2, 0, 3)
            enemy_3 = Enemy(16, 112, 208, 112, 4, 0, 3)
            enemy_group.add(enemy_1, enemy_2, enemy_3) 
        # ABANDONED MINE 1
        elif map_number == 26:
            enemy_1 = Enemy(192, 128, 32, 128, -4, 0, 1)
            enemy_2 = Enemy(80, 32, 192, 32, 4, 0, 1)
            enemy_3 = Enemy(16, 32, 32, 32, 2, 0, 6)
            enemy_group.add(enemy_1, enemy_2, enemy_3) 
        # ABANDONED MINE 2
        elif map_number == 27:
            enemy_1 = Enemy(160, 32, 160, 128, 0, 4, 3)
            enemy_2 = Enemy(192, 128, 96, 128, -1, 0, 1)
            enemy_group.add(enemy_1, enemy_2) 
        # ABANDONED MINE 3
        elif map_number == 28:
            enemy_1 = Enemy(112, 128, 128, 128, 2, 0, 6)
            enemy_2 = Enemy(32, 32, 32, 128, 0, 2, 3)
            enemy_3 = Enemy(96, 48, 176, 48, 4, 0, 1)
            enemy_group.add(enemy_1, enemy_2, enemy_3) 
        # EXPLOSIVES STOCKPILE
        elif map_number == 29:
            enemy_1 = Enemy(128, 32, 128, 48, 0, 2, 6)
            enemy_group.add(enemy_1) 

    # paint the map free of sprites to clean it up
    map_display.blit(map_display_backup, (0,0))
    # and change the frame of the animated tiles
    animate_tiles()

    # update enemies
    enemy_group.update()
    enemy_group.draw(map_display)

    # FPS counter using the clock   
    aux_font_L.render(str(int(clock.get_fps())).rjust(3, '0') + ' FPS', sboard_display, (124, 22))

    # scale x 3 the map
    screen.blit(pygame.transform.scale(map_display, map_scaled_size), (40, 112))
    # scale x 3 the scoreboard
    screen.blit(pygame.transform.scale(sboard_display, sboard_scaled_size), (40, 0))

    # scanlines
    if cfg_scanlines_type == 2: # HQ
        apply_scanlines(screen_sl, win_size[1]-9, 40, 759, 200)
        screen.blit(screen_sl, (0, 0))
    elif cfg_scanlines_type == 1: # fast
        apply_scanlines(screen, win_size[1]-9, 40, 759, 15)

    pygame.display.update() # refreshes the screen
    clock.tick(60) # 60 FPS


