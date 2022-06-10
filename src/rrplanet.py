
# ==============================================================================
# Raspi-Red Planet v1.0
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

p = os.path.dirname(__file__) + "/" # exec path (+ "/" when using VS Code)
jp = os.path.join # forms the folder/file path

win_size = 800, 600 # main window size
map_scaled_size = 720, 480 # map size (scaled x3)
map_unscaled_size = 240, 160 # map size (unscaled)
sboard_scaled_size = 720, 102 # scoreboard size (scaled x3)
sboard_unscaled_size = 240, 34 # scoreboard size (unscaled)
map_number = 0 # current map number
last_map = -1 # last map loaded
game_percent = 0 # % of gameplay completed

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
# Generic functions
#===============================================================================

# get a value from a dictionary
def FindData(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return dic
    return -1



# returns a part of the surface
def Clip(surf,x,y,x_size,y_size):
    handle_surf = surf.copy()
    handle_surf.set_clip(pygame.Rect(x,y,x_size,y_size))
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()



# change one colour for another
def SwapColor(img,old_c,new_c):
    #global e_colorkey
    img.set_colorkey(old_c)
    surf = img.copy()
    surf.fill(new_c)
    surf.blit(img,(0,0))
    return surf



#===============================================================================
# Map functions
#===============================================================================

# loads a map and draws it on screen
def LoadMap(map_number):
    global map_data
    map_data = ProcessMap(jp(p, "maps/map" + str(map_number) + ".json"))
    DrawMap() # draws the tile map on the screen
    DrawMapName() # draws the name of the map at the top



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
    with open(jp(p,"maps/" + tileset)) as json_data:
        t = json.load(json_data)
    # removes the path to each image from the tile file
    data["tiles"] = t["tiles"]
    for tile in range(0, len(data["tiles"])):
        path = data["tiles"][tile]["image"]
        data["tiles"][tile]["image"] = os.path.basename(path)
        data["tiles"][tile]["id"] = data["tiles"][tile]["id"] + 1
    return data



# draws the tile map on the screen
def DrawMap():
    # scroll through the map data
    for y in range(0, map_data["height"]):
        for x in range(0, map_data["width"]):
            # gets the tile number from the list
            t = FindData(map_data["tiles"], "id", map_data["data"][y][x])
            # draws the selected tile
            tile = pygame.image.load(jp(p, "images/" + t["image"])).convert()
            tileRect = tile.get_rect()
            tileRect.topleft = (x * t["imagewidth"], y * t["imageheight"])   
            map_display.blit(tile, tileRect)



# draws the name of the map at the top
def DrawMapName():
    name_x = 0
    name_y = sboard_display.get_height()-14
    progress_x = sboard_unscaled_size[0] - 20
    progress_y = name_y

    sboard_display.fill((0,0,0)) # delete previous text

    bg_font_L.render(map_names[map_number], sboard_display, (name_x+2, name_y+1)) # shadow
    fg_font_L.render(map_names[map_number], sboard_display, (name_x, name_y))
    bg_font_S.render(str(map_number+1) + '/30', sboard_display, (progress_x+1, progress_y+1))
    fg_font_S.render(str(map_number+1) + '/30', sboard_display, (progress_x, progress_y))
    bg_font_S.render(str(game_percent) + ';', sboard_display, (progress_x+1, progress_y+8))
    fg_font_S.render(str(game_percent) + ';', sboard_display, (progress_x, progress_y+7))

#===============================================================================
# Font functions
#===============================================================================

# loads the letters of the font image
def load_font_img(path, font_color, is_transparent):
    fg_color = (255, 0, 0) # original red
    bg_color = (0, 0, 0) # black
    font_img = pygame.image.load(jp(p,path)).convert() # load font image
    font_img = SwapColor(font_img, fg_color, font_color) # apply the requested font colour
    last_x = 0
    letters = []
    letter_spacing = []
    for x in range(font_img.get_width()): # for the entire width of the image
        if font_img.get_at((x, 0))[0] == 127: # gray separator
            # saves in the array the portion of the image with the letter we are interested in.
            letters.append(Clip(font_img, last_x, 0, x - last_x, font_img.get_height()))
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

    # returns the width in pixels of the text
    def width(self, text):
        text_width = 0
        for char in text:
            if char == ' ':
                text_width += self.space_width + self.base_spacing
            else:
                text_width += self.letter_spacing[self.font_order.index(char)] + self.base_spacing
        return text_width

    # draw the text
    def render(self, text, surf, loc, line_width=0):
        x_offset = 0
        y_offset = 0
        if line_width != 0:
            spaces = []
            x = 0
            # ?
            for i, char in enumerate(text):
                if char == ' ':
                    spaces.append((x, i))
                    x += self.space_width + self.base_spacing
                else:
                    x += self.letter_spacing[self.font_order.index(char)] + self.base_spacing
            line_offset = 0
            # ?
            for i, space in enumerate(spaces):
                if (space[0] - line_offset) > line_width:
                    line_offset += spaces[i - 1][0] - line_offset
                    if i != 0:
                        text = text[:spaces[i - 1][1]] + '\n' + text[spaces[i - 1][1] + 1:]
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
# Auxiliar functions
#===============================================================================

# scanlines
def ApplyFilter():
    j = 0
    while j < win_size[1] - 18:
        j+=3
        pygame.draw.line(screen, (15, 15, 15), (40, j), (760, j))



#===============================================================================
# Main
#===============================================================================

# Initialisation
pygame.init()
pygame.mixer.init()

# generates a main window with title, icon, and 32-bit colour.
screen = pygame.display.set_mode(win_size, 0, 32)
pygame.display.set_caption(".:: Raspi-Red Planet ::.")
icon = pygame.image.load(jp(p, "images/icon.png")).convert_alpha()
pygame.display.set_icon(icon)

# area covered by the map
map_display = pygame.Surface(map_unscaled_size)
# area covered by the scoreboard
sboard_display = pygame.Surface(sboard_unscaled_size)

# fonts
fg_font_S = Font('images/small_font.png', (0, 255, 0), True) # green
bg_font_S = Font('images/small_font.png', (0, 80, 0), False) # dark green
fg_font_L = Font('images/large_font.png', (255, 255, 255), True) # white
bg_font_L = Font('images/large_font.png', (80, 80, 80), False) # dark gray

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

    # test 1
    #outlined_text(bg_font, main_font, 'Level - ' + str(map_number), sb_display, (0, 0))

    # scale x 3 the map and transfer to screen
    screen.blit(pygame.transform.scale(map_display, map_scaled_size), 
    ((screen.get_width() - map_scaled_size[0]) // 2, # horizontally centred
    screen.get_height() - map_scaled_size[1] - 14)) # room for the scoreboard
    # scale x 3 the scoreboard and transfer to screen
    screen.blit(pygame.transform.scale(sboard_display, sboard_scaled_size), 
    ((screen.get_width() - sboard_scaled_size[0]) // 2, 0)) # horizontally centred

    ApplyFilter() # scanlines

    pygame.display.update() # refreshes the screen
    clock.tick(60) # 60 FPS
