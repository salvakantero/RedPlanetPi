
# ==============================================================================
# Raspi-Red Planet v1.0
# salvaKantero 2022
# ==============================================================================

import pygame # pygame library functions
import os, sys, json # python generic functions

from enum import Enum
from pygame.locals import * # allows constants without typing "pygame."
from pygame.constants import (QUIT, KEYDOWN, K_ESCAPE, K_LEFT, K_RIGHT) 





#===============================================================================
# Global variables
#===============================================================================

dp = os.path.dirname(__file__) + "/" # exec path (+ "/" when using VS Code)
jp = os.path.join # forms the folder/file path

win_size = 800, 600 # main window size
map_scaled_size = 720, 480 # map size (scaled x3)
map_unscaled_size = 240, 160 # map size (unscaled)
sboard_scaled_size = 720, 114 # scoreboard size (scaled x3)
sboard_unscaled_size = 240, 38 # scoreboard size (unscaled)

# tile size in pixels
tile_width = 16
tile_height = 16

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

# types of sprites
class SprType(Enum):
    player = 0
    infected = 1
    pelusoid = 2
    avirus = 3
    platform = 4
    none = 5

# directions
class Dir(Enum):
    up = 0
    down = 1
    left = 2
    right = 3

# movements
class Mov(Enum):
    lin_x = 0 
    lin_y = 1
    lin_xy = 2
    fanty = 3

# speed
class Speed(Enum):
    slow = 0 
    normal = 1
    fast = 2

# colour palette (Pico8)
palette = {
    "BLACK": (0, 0, 0),
    "DARK_BLUE" : (35, 50, 90),
    "PURPLE" : (126, 37, 83),
    "DARK_GREEN" : (0, 135, 81),
    "BROWN" : (171, 82, 54),
    "DARK_GRAY" : (95, 87, 79),
    "GRAY" : (194, 195, 199),
    "WHITE" : (255, 241, 232),
    "RED" : (255, 0, 77),
    "ORANGE" : (255, 163, 0),
    "YELLOW" : (255, 236, 39),
    "GREEN" : (0, 228, 54),
    "CYAN" : (41, 173, 255),
    "MALVA" : (131, 118, 156),
    "PINK" : (255, 119, 168),
    "SAND" : (255, 204, 170),
    "KEY" : (255, 0, 255) # Mask colour
}

# screen names
map_names = {
    0  : "CONTROL CENTRE",
    1  : "SUPPLY DEPOT 1",
    2  : "CENTRAL HALL LEVEL 0",
    3  : "TOXIC WASTE STORAGE 1A",
    4  : "TOXIC WASTE STORAGE 1B",
    5  : "WEST PASSAGE LEVEL -1",
    6  : "ACCESS TO WEST PASSAGES",
    7  : "CENTRAL HALL LEVEL -1",
    8  : "ACCESS TO DUNGEONS",
    9  : "DUNGEONS",
    10 : "WEST PASSAGE LEVEL -2",
    11 : "SUPPLY DEPOT 2",
    12 : "CENTRAL HALL LEVEL -2",
    13 : "ACCESS TO SOUTHEAST EXIT",
    14 : "EXIT TO UNDERGROUND",
    15 : "PELUSOIDS LAIR",
    16 : "ALVARITOS GROTTO 2",
    17 : "ALVARITOS GROTTO 1",
    18 : "TOXIC WASTE STORAGE 2A",
    19 : "UNDERGROUND TUNNEL",
    20 : "SIDE HALL LEVEL -4",
    21 : "ARACHNOVIRUS LAIR",
    22 : "UNSTABLE CORRIDORS 1",
    23 : "UNSTABLE CORRIDORS 2",
    24 : "TOXIC WASTE STORAGE 2B",
    25 : "SIDE HALL LEVEL -5",
    26 : "ABANDONED MINE 1",
    27 : "ABANDONED MINE 2",
    28 : "ABANDONED MINE 3",
    29 : "EXPLOSIVES STOCKPILE",
    30 : "BACK TO CONTROL CENTER",
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
    bg_font_L.render("+50", sboard_display, (116, 6))
    fg_font_L.render("+50", sboard_display, (114, 4))
    bg_font_L.render("+10", sboard_display, (220, 6))
    fg_font_L.render("+10", sboard_display, (218, 4))

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
    def __init__(self, enemy_type, mov, dir, pos, max, min, speed):
        super(Enemy, self).__init__()
        num_frames = 2
        self.images = []
        for i in range(num_frames):
            # image for the frame
            self.images.append(pygame.image.load(
                jp(dp, "images/sprites/" + enemy_type.name + str(i) + ".png")).convert())
            # mask
            self.images[i].set_colorkey((255, 0, 255))

        self.animation_index = 0
        self.animation_speed = 0.08
        self.image = self.images[self.animation_index]
    
        self.mov = mov
        self.dir = dir
        self.speed = speed
        # position
        self.x = pos[0] * tile_width
        self.y = pos[1] * tile_height
        # limits of the movement
        self.max = max * tile_height
        self.min = min * tile_height

    def update(self):
        # animation
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.images):
            self.animation_index = 0
        self.image = self.images[int(self.animation_index)]
        
        # movement
        #=================== linear motion on the X axis =======================
        if self.mov == Mov.lin_x: 
            if self.dir == Dir.right:
                # if it has not exceeded the maximum X, moves the sprite to the right
                if self.x < self.max:
                    self.x += self.speed
                else: # if there is no place change the direction
                    self.dir = Dir.left
            else:
                # if it has not exceeded the minimum X, moves the sprite to the left
                if self.x > self.min:
                    self.x -= self.speed
                else: # if there is no place change the direction
                    self.dir = Dir.right
        
        #=================== linear motion on the Y axis =======================
        elif self.mov == Mov.lin_y: 
            if self.dir == Dir.down:
                # if it has not exceeded the maximum Y, move the sprite down
                if self.y < self.max:
                    self.y += self.speed
                else: # if there is no place change the direction
                    self.dir = Dir.up
            else:
                # if it has not exceeded the minimum Y, move the sprite up
                if self.y > self.min:
                    self.y -= self.speed
                else: # if there is no place change the direction
                    self.dir = Dir.down

        self.rect = pygame.Rect(self.x, self.y, tile_width, tile_height)

def load_enemies():
    # CONTROL CENTRE
    if map_number == 0:
        # parameters: Enemy_Type , Movement , Direction , Position , Max, Min , Speed    
        enemy_1 = Enemy(SprType.infected, Mov.lin_x, Dir.left, (8,7), 8, 2, 1)
        enemy_2 = Enemy(SprType.avirus, Mov.lin_y, Dir.down, (1,1), 5, 1, 1) 
        enemy_group.add(enemy_1, enemy_2)      
    # SUPPLY DEPOT 1        
    elif map_number == 1:
        enemy_1 = Enemy(SprType.pelusoid, Mov.lin_y, Dir.left, (8,7), 8, 2, 1)
        enemy_2 = Enemy(SprType.pelusoid, Mov.lin_x, Dir.down, (1,1), 5, 1, 1) 
        enemy_group.add(enemy_1, enemy_2)     
    # CENTRAL HALL LEVEL 0
    # TOXIC WASTE STORAGE 1A
    # TOXIC WASTE STORAGE 1B
    # WEST PASSAGE LEVEL -1
    # ACCESS TO WEST PASSAGES
    # CENTRAL HALL LEVEL -1
    # ACCESS TO DUNGEONS
    # DUNGEONS
    # WEST PASSAGE LEVEL -2
    # SUPPLY DEPOT 2
    # CENTRAL HALL LEVEL -2
    # ACCESS TO SOUTHEAST EXIT
    # EXIT TO UNDERGROUND
    # PELUSOIDS LAIR
    # ALVARITOS GROTTO 2
    # ALVARITOS GROTTO 1
    # TOXIC WASTE STORAGE 2A
    # UNDERGROUND TUNNEL
    # SIDE HALL LEVEL -4
    # ARACHNOVIRUS LAIR
    # UNSTABLE CORRIDORS 1
    # UNSTABLE CORRIDORS 2
    # TOXIC WASTE STORAGE 2B
    # SIDE HALL LEVEL -5
    # ABANDONED MINE 1
    # ABANDONED MINE 2
    # ABANDONED MINE 3
    # EXPLOSIVES STOCKPILE
    # BACK TO CONTROL CENTER
    





#===============================================================================
# Main
#===============================================================================

# Initialisation
pygame.init()
pygame.mixer.init()

# generates a main window with title, icon, and 32-bit colour.
screen = pygame.display.set_mode(win_size, 0, 32)
pygame.display.set_caption(".:: Raspi-Red Planet ::.")
icon = pygame.image.load(jp(dp, "images/assets/icon.png")).convert_alpha()
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
fg_font_S = Font('images/fonts/small_font.png', palette["GREEN"], True)
bg_font_S = Font('images/fonts/small_font.png', palette["DARK_GREEN"], False)
fg_font_L = Font('images/fonts/large_font.png', palette["WHITE"], True)
bg_font_L = Font('images/fonts/large_font.png', palette["DARK_GRAY"], False)
aux_font_L = Font('images/fonts/large_font.png', palette['YELLOW'], True)

# scoreboard icons
lives_icon = pygame.image.load(jp(dp, "images/assets/lives.png")).convert()
oxigen_icon = pygame.image.load(jp(dp, "images/tiles/T53.png")).convert()
ammo_icon = pygame.image.load(jp(dp, "images/tiles/T52.png")).convert()
keys_icon = pygame.image.load(jp(dp, "images/tiles/T51.png")).convert()
explosives_icon = pygame.image.load(jp(dp, "images/tiles/T50.png")).convert()

# enemy sprites control
enemy_group = pygame.sprite.Group()

# clock to control the FPS
clock = pygame.time.Clock()

# ingame music
#pygame.mixer.music.load(jp(dp, "sounds/ingame.ogg"))
#pygame.mixer.music.play(-1)

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
        map_display_backup.blit(map_display, (0,0))
        draw_map_info()
        init_scoreboard()
        update_scoreboard()
        load_enemies()
        last_map = map_number        

    # paint the map free of sprites to clean it up
    map_display.blit(map_display_backup, (0,0))

    # update enemies
    enemy_group.update()
    enemy_group.draw(map_display)

    # FPS counter using the clock   
    pygame.draw.rect(sboard_display,palette['BLACK'],(124,22,50,12))
    aux_font_L.render(str(int(clock.get_fps())) + " FPS", sboard_display, (124, 22))

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


