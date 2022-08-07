
# ==============================================================================
# Raspi-Red Planet v1.0
# salvaKantero 2022
# ==============================================================================

import pygame # pygame library functions
import sys # exit()

from pygame.locals import * # allows constants without typing "pygame."
from pygame.constants import (QUIT, KEYDOWN, K_ESCAPE, K_LEFT, K_RIGHT) 

from globalvars import *
from maps import load_map # map functions
from texts import Font # text and fonts functions
from enemies import Enemy # enemy sprites and mobile platform
from support import apply_scanlines # crt screen filter


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

# area covered by the scoreboard
sboard_display = pygame.Surface(sboard_unscaled_size)

# surface for HQ scanlines
screen_sl = pygame.Surface(win_size)
screen_sl.set_alpha(35)

# sprites
enemy_sprite1 = Enemy(SprType.infected, Mov.lin_x, Dir.left, (8,7), (2,7))
enemy_sprite2 = Enemy(SprType.avirus, Mov.lin_xy, Dir.left, (1,1), (14,3))
enemy_group = pygame.sprite.Group(enemy_sprite1, enemy_sprite2)

# fonts
fg_font_S = Font('images/fonts/small_font.png', pal["GREEN"], True)
bg_font_S = Font('images/fonts/small_font.png', pal["DARK_GREEN"], False)
fg_font_L = Font('images/fonts/large_font.png', pal["WHITE"], True)
bg_font_L = Font('images/fonts/large_font.png', pal["DARK_GRAY"], False)

# scoreboard icons
lives_icon = pygame.image.load(jp(dp, "images/assets/lives.png")).convert()
oxigen_icon = pygame.image.load(jp(dp, "images/tiles/T53.png")).convert()
ammo_icon = pygame.image.load(jp(dp, "images/tiles/T52.png")).convert()
keys_icon = pygame.image.load(jp(dp, "images/tiles/T51.png")).convert()
explosives_icon = pygame.image.load(jp(dp, "images/tiles/T50.png")).convert()

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

    # update enemies
    enemy_group.update()
    enemy_group.draw(map_display)

    # scale x 3 the map
    screen.blit(pygame.transform.scale(map_display, map_scaled_size), (40, 112))
    # scale x 3 the scoreboard
    screen.blit(pygame.transform.scale(sboard_display, sboard_scaled_size), (40, 0))

    # scanlines
    if cfg_scanlines_type == 2: # HQ
        apply_scanlines(screen_sl, win_size[1]-9, 40, 759, 220)
        screen.blit(screen_sl, (0, 0))
    elif cfg_scanlines_type == 1: # fast
        apply_scanlines(screen, win_size[1]-9, 40, 759, 15)

    pygame.display.update() # refreshes the screen
    clock.tick(60) # 60 FPS
