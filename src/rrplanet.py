
# ==============================================================================
# Raspi-Red Planet v1.0
# salvaKantero 2022
# ==============================================================================

import pygame # pygame library functions
import os # file operations
import sys # exit()

from pygame.locals import * # allows constants without typing "pygame."
from pygame.constants import (QUIT, KEYDOWN, K_ESCAPE, K_LEFT, K_RIGHT) 

from maps import load_map # map functions
from texts import Font # text and fonts functions



#===============================================================================
# Global vars
#===============================================================================

win_size = 800, 600 # main window size
map_scaled_size = 720, 480 # map size (scaled x3)
map_unscaled_size = 240, 160 # map size (unscaled)
sboard_scaled_size = 720, 102 # scoreboard size (scaled x3)
sboard_unscaled_size = 240, 34 # scoreboard size (unscaled)
map_number = 0 # current map number
last_map = -1 # last map loaded
game_percent = 0 # % of gameplay completed

# colour palette (Pico8)
BLACK = (0, 0, 0)
DARK_BLUE = (35, 50, 90)
PURPLE = (126, 37, 83)
DARK_GREEN = (0, 135, 81)
BROWN = (171, 82, 54)
DARK_GRAY = (95, 87, 79)
GRAY = (194, 195, 199)
WHITE = (255, 241, 232)
RED = (255, 0, 77)
ORANGE = (255, 163, 0)
YELLOW = (255, 236, 39)
GREEN = (0, 228, 54)
CYAN = (41, 173, 255)
MALVA = (131, 118, 156)
PINK = (255, 119, 168)
SAND = (255, 204, 170)

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
# Scoreboard functions
#===============================================================================

# draws the name of the map and other data at the top
def draw_map_info():
    x = 0
    y = sboard_display.get_height()-bg_font_L.line_height+1
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
    text_2 += str(game_percent) + ';'

    sboard_display.fill((0,0,0)) # delete previous text

    # map name
    bg_font_L.render(map_names[map_number], sboard_display, (x+2, y+2)) # shadow
    fg_font_L.render(map_names[map_number], sboard_display, (x, y+1))
    # map number
    bg_font_S.render(text_1, sboard_display, (progress_x+1, y+1)) # shadow
    fg_font_S.render(text_1, sboard_display, (progress_x, y))
    # game percentage
    bg_font_S.render(text_2, sboard_display, (progress_x+1, y+bg_font_S.line_height+1)) # shadow
    fg_font_S.render(text_2, sboard_display, (progress_x, y+fg_font_S.line_height))



def init_scoreboard():
    pass



def update_scoreboard():
    pass



#===============================================================================
# Auxiliar functions
#===============================================================================

# scanlines
def apply_filter():
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
icon = pygame.image.load(
    os.path.join(os.path.dirname(__file__) + "/", "images/icon.png")).convert_alpha()
pygame.display.set_icon(icon)

# area covered by the map
map_display = pygame.Surface(map_unscaled_size)
# area covered by the scoreboard
sboard_display = pygame.Surface(sboard_unscaled_size)

# fonts
fg_font_S = Font('images/small_font.png', GREEN, True)
bg_font_S = Font('images/small_font.png', DARK_GREEN, False)
fg_font_L = Font('images/large_font.png', WHITE, True)
bg_font_L = Font('images/large_font.png', DARK_GRAY, False)

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
                if map_number < 24:
                    map_number += 1
            if event.key == K_LEFT:
                if map_number > 0:
                    map_number -= 1
            # ==========================

    # change map if neccessary
    if map_number != last_map:
        load_map(map_number, map_display)
        draw_map_info()
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

    apply_filter() # scanlines

    pygame.display.update() # refreshes the screen
    clock.tick(60) # 60 FPS
