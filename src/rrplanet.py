
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
from generic import apply_scanlines # crt screen filter



#===============================================================================
# Global vars
#===============================================================================

p = os.path.dirname(__file__) + "/" # exec path (+ "/" when using VS Code)
jp = os.path.join # forms the folder/file path

win_size = 800, 600 # main window size
map_scaled_size = 720, 480 # map size (scaled x3)
map_unscaled_size = 240, 160 # map size (unscaled)
sboard_scaled_size = 720, 108 # scoreboard size (scaled x3)
sboard_unscaled_size = 240, 36 # scoreboard size (unscaled)
map_number = 0 # current map number
last_map = -1 # last map loaded
game_percent = 0 # % of gameplay completed
lives = 10 # remaining player lives
oxigen = 99 # remaining player oxigen
ammo = 5 # bullets available in the gun
keys = 0 # unused keys collected
explosives = 0 # explosives collected

# colour palette (Pico8)
pal = {
    "BLACK":(0, 0, 0),
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
    "SAND" : (255, 204, 170) 
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
# Scoreboard functions
#===============================================================================

# draws the name of the map and other data at the top
def draw_map_info():
    x = 0
    y = 21
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
    sboard_display.blit(lives_icon, (0, 1))
    sboard_display.blit(oxigen_icon, (42, 1))
    sboard_display.blit(ammo_icon, (82, 1))
    sboard_display.blit(keys_icon, (145, 1))
    sboard_display.blit(explosives_icon, (186, 1))
    # fixed texts
    bg_font_L.render("+50", sboard_display, (116, 5))
    fg_font_L.render("+50", sboard_display, (114, 3))
    bg_font_L.render("+10", sboard_display, (220, 5))
    fg_font_L.render("+10", sboard_display, (218, 3))


def update_scoreboard():
    # values
    bg_font_L.render(str(lives).rjust(2, '0'), sboard_display, (20, 5))
    fg_font_L.render(str(lives).rjust(2, '0'), sboard_display, (18, 3))
    bg_font_L.render(str(oxigen).rjust(2, '0'), sboard_display, (62, 5))
    fg_font_L.render(str(oxigen).rjust(2, '0'), sboard_display, (60, 3))
    bg_font_L.render(str(ammo).rjust(2, '0'), sboard_display, (102, 5))
    fg_font_L.render(str(ammo).rjust(2, '0'), sboard_display, (100, 3))
    bg_font_L.render(str(keys).rjust(2, '0'), sboard_display, (166, 5))
    fg_font_L.render(str(keys).rjust(2, '0'), sboard_display, (164, 3))
    bg_font_L.render(str(explosives).rjust(2, '0'), sboard_display, (206, 5))
    fg_font_L.render(str(explosives).rjust(2, '0'), sboard_display, (204, 3))



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
    os.path.join(os.path.dirname(__file__) + "/", "images/assets/icon.png")).convert_alpha()
pygame.display.set_icon(icon)

# area covered by the map
map_display = pygame.Surface(map_unscaled_size)

# area covered by the scoreboard
sboard_display = pygame.Surface(sboard_unscaled_size)

# fonts
fg_font_S = Font('images/fonts/small_font.png', pal["GREEN"], True)
bg_font_S = Font('images/fonts/small_font.png', pal["DARK_GREEN"], False)
fg_font_L = Font('images/fonts/large_font.png', pal["WHITE"], True)
bg_font_L = Font('images/fonts/large_font.png', pal["DARK_GRAY"], False)

# scoreboard icons
lives_icon = pygame.image.load(jp(p, "images/assets/lives.png")).convert()
oxigen_icon = pygame.image.load(jp(p, "images/tiles/T53.png")).convert()
ammo_icon = pygame.image.load(jp(p, "images/tiles/T52.png")).convert()
keys_icon = pygame.image.load(jp(p, "images/tiles/T51.png")).convert()
explosives_icon = pygame.image.load(jp(p, "images/tiles/T50.png")).convert()

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
                if map_number < 29:
                    map_number += 1
            if event.key == K_LEFT:
                if map_number > 0:
                    map_number -= 1
            # ==========================

    # change map if neccessary
    if map_number != last_map:
        load_map(map_number, map_display)
        draw_map_info()
        init_scoreboard()
        update_scoreboard()
        last_map = map_number

    # test 1
    #outlined_text(bg_font, main_font, 'Level - ' + str(map_number), sb_display, (0, 0))

    # scale x 3 the map and transfer to screen
    screen.blit(pygame.transform.scale(map_display, map_scaled_size), 
    ((screen.get_width() - map_scaled_size[0]) // 2, # horizontally centred
    screen.get_height() - map_scaled_size[1] - 8)) # room for the scoreboard

    # scale x 3 the scoreboard and transfer to screen
    screen.blit(pygame.transform.scale(sboard_display, sboard_scaled_size), 
    ((screen.get_width() - sboard_scaled_size[0]) // 2, 0)) # horizontally centred

    apply_scanlines(screen, win_size[1]-15) # scanlines

    pygame.display.update() # refreshes the screen
    clock.tick(60) # 60 FPS
