
# ==============================================================================
# Red Planet Pi v1.0
# salvaKantero 2022/23
# ==============================================================================

import pygame # pygame library functions
import sys # exit()

# allows constants without typing "pygame."
from pygame.locals import *
from pygame.constants import *

# own code
import globalvars, enums
import config # configuration file
import tiled # maps and tiles
from font import Font # font class
from player import Player # player class
from enemy import Enemy # enemy class

# local vars
map_number = 0 # current map
map_scroll = 0 # scroll direction for map_transition()
last_map = -1 # last map loaded
game_percent = 0 # % of gameplay completed



#===============================================================================
# Main functions
#===============================================================================

# draws scanlines
def scanlines(surface, height, from_x, to_x, rgb):
    j = globalvars.V_MARGIN
    while j < height:
        j+=3
        pygame.draw.line(surface, (rgb, rgb, rgb), (from_x, j), (to_x, j))

# applies scanlines according to the configuration
def make_scanlines():
    if config.scanlines_type == 2: # HQ
        scanlines(screen_sl, globalvars.WIN_SIZE[1]-30, globalvars.H_MARGIN, 
            globalvars.WIN_SIZE[0]-globalvars.H_MARGIN-1, 200)
        screen.blit(screen_sl, (0, 0))
    elif config.scanlines_type == 1: # fast
        scanlines(screen, globalvars.WIN_SIZE[1]-30, globalvars.H_MARGIN, 
            globalvars.WIN_SIZE[0]-globalvars.H_MARGIN-1, 15)

# draws the name of the map and other data at the top
def draw_map_info():
    x = 0
    y = 22
    progress_x = globalvars.SBOARD_UNSCALED_SIZE[0] - 55
    
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
    bg_font_L.render(globalvars.MAP_NAMES[map_number], sboard_display, (x+2, y+2)) # shadow
    fg_font_L.render(globalvars.MAP_NAMES[map_number], sboard_display, (x, y))
    # map number
    bg_font_S.render(text_1, sboard_display, (progress_x+1, y+1)) # shadow
    fg_font_S.render(text_1, sboard_display, (progress_x, y))
    # game percentage
    bg_font_S.render(text_2, sboard_display, (progress_x+1, y+bg_font_S.line_height+1)) # shadow
    fg_font_S.render(text_2, sboard_display, (progress_x, y+fg_font_S.line_height))

# resets the scoreboard data to zero
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
    bg_font_L.render('+15', sboard_display, (220, 6))
    fg_font_L.render('+15', sboard_display, (218, 4))

# update the scoreboard data
def update_scoreboard():
    pygame.draw.rect(sboard_display, globalvars.PALETTE['BLACK'], ((18,4),(13,12)))
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
    globalvars.refresh_scoreboard = False

#dumps and scales surfaces to the screen
def update_screen():
    # scale x 3 the scoreboard
    screen.blit(pygame.transform.scale(sboard_display, globalvars.SBOARD_SCALED_SIZE), 
        (globalvars.H_MARGIN, globalvars.V_MARGIN))
    # scale x 3 the map
    screen.blit(pygame.transform.scale(map_display, globalvars.MAP_SCALED_SIZE), 
        (globalvars.H_MARGIN, globalvars.SBOARD_SCALED_SIZE[1] + globalvars.V_MARGIN))
    make_scanlines()
    pygame.display.update() # refreshes the screen
    clock.tick(60) # 60 FPS

# draws a centred message box erasing the background
def message_box(message1, message2):
    # calculates the dimensions of the box
    height = 36
    message1_len = len(message1) * 7 # approximate length of text 1 in pixels
    message2_len = len(message2) * 4 # approximate length of text 2 in pixels
    # width = length of the longest text + margin
    if message1_len > message2_len:
        width = message1_len + globalvars.V_MARGIN
    else:
        width = message2_len + globalvars.V_MARGIN
    # calculates the position of the box
    x = (globalvars.MAP_UNSCALED_SIZE[0]//2) - (width//2)
    y = (globalvars.MAP_UNSCALED_SIZE[1]//2) - (height//2)
    pygame.draw.rect(map_display, globalvars.PALETTE['BLACK'],(x, y, width, height))
    # draws the text centred inside the box (Y positions are fixed)
    text_x = (x + (width//2)) - (message1_len//2)
    text_y = y + 5
    bg_font_L.render(message1, map_display, (text_x, text_y))
    fg_font_L.render(message1, map_display, (text_x - 2, text_y - 2))
    text_x = (x + (width//2)) - (message2_len//2)
    text_y = y + 24
    bg_font_S.render(message2, map_display, (text_x, text_y))
    fg_font_S.render(message2, map_display, (text_x - 1, text_y - 1))

# displays a message to confirm exit
def confirm_exit():
    message_box('Leave the current game?', 'PRESS Y TO EXIT OR N TO CONTINUE')
    screen.blit(pygame.transform.scale(sboard_display, globalvars.SBOARD_SCALED_SIZE), 
        (globalvars.H_MARGIN, globalvars.V_MARGIN))        
    screen.blit(pygame.transform.scale(map_display, globalvars.MAP_SCALED_SIZE), 
        (globalvars.H_MARGIN, globalvars.SBOARD_SCALED_SIZE[1] + globalvars.V_MARGIN))
    make_scanlines()
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
            # exit by pressing ESC key
                if event.key == pygame.K_y:                    
                    return True
                elif event.key == pygame.K_n:  
                    return False

# Main menu
def main_menu():
    map_display.fill(globalvars.PALETTE['BLACK'])
    sboard_display.fill(globalvars.PALETTE['BLACK'])
    message_box('Red Planet Pi', 'WIP. Press a key to continue')
    update_screen()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
            # exit by pressing ESC key
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# checks if the map needs to be changed (depending on the player's XY position)
def check_map_change(player):
    global map_number, map_scroll
    # player disappears on the left
    # appearing from the right on the new map
    if player.rect.x < -16:
        map_number -= 1
        map_scroll = enums.LEFT
        player.rect.right = globalvars.MAP_UNSCALED_SIZE[0]
    # player disappears on the right
    # appearing from the left on the new map
    elif player.rect.x > globalvars.MAP_UNSCALED_SIZE[0]:
        map_number += 1
        map_scroll = enums.RIGHT
        player.rect.left = 0
    # player disappears over the top
    # appearing at the bottom of the new map
    elif player.rect.y < (-16):
        map_number -= 5
        map_scroll = enums.UP
        player.rect.bottom = globalvars.MAP_UNSCALED_SIZE[1]
    # player disappears from underneath
    #appearing at the top of the new map
    elif player.rect.y > globalvars.MAP_UNSCALED_SIZE[1]:
        map_number += 5
        map_scroll = enums.DOWN
        player.rect.top = 0

# makes a screen transition between the old map and the new one.
def map_transition():
    # surfaces to save the old and the new map together
    map_trans_horiz = pygame.Surface(
        (globalvars.MAP_UNSCALED_SIZE[0]*2, globalvars.MAP_UNSCALED_SIZE[1]))
    map_trans_vert = pygame.Surface(
        (globalvars.MAP_UNSCALED_SIZE[0], globalvars.MAP_UNSCALED_SIZE[1]*2))

    if map_scroll == enums.UP:
        # joins the two maps on a single surface
        map_trans_vert.blit(map_display_backup, (0,0))
        map_trans_vert.blit(map_display_backup_old, (0, globalvars.MAP_UNSCALED_SIZE[1]))
        # scrolls the two maps across the screen
        for y in range(-globalvars.MAP_UNSCALED_SIZE[1], 0, 4):
            map_display.blit(map_trans_vert, (0, y))
            update_screen()
    elif map_scroll == enums.DOWN:
        # joins the two maps on a single surface
        map_trans_vert.blit(map_display_backup_old, (0,0))
        map_trans_vert.blit(map_display_backup, (0, globalvars.MAP_UNSCALED_SIZE[1]))
        # scrolls the two maps across the screen
        for y in range(0, -globalvars.MAP_UNSCALED_SIZE[1], -4):
            map_display.blit(map_trans_vert, (0, y))
            update_screen()
    elif map_scroll == enums.LEFT:
        # joins the two maps on a single surface
        map_trans_horiz.blit(map_display_backup, (0,0))
        map_trans_horiz.blit(map_display_backup_old, (globalvars.MAP_UNSCALED_SIZE[0], 0))
        # scrolls the two maps across the screen
        for x in range(-globalvars.MAP_UNSCALED_SIZE[0], 0, 6):
            map_display.blit(map_trans_horiz, (x, 0))
            update_screen()
    else: # right
        # joins the two maps on a single surface
        map_trans_horiz.blit(map_display_backup_old, (0,0))
        map_trans_horiz.blit(map_display_backup, (globalvars.MAP_UNSCALED_SIZE[0], 0))
        # scrolls the two maps across the screen
        for x in range(0, -globalvars.MAP_UNSCALED_SIZE[0], -6):
            map_display.blit(map_trans_horiz, (x, 0))
            update_screen()

# does everything necessary to change the map
def change_map():
    global last_map, map_number
    # sets the new map as the current one
    last_map = map_number
    # load the new map
    tiled.load_map(map_number, map_display)
    # preserves the previous 
    if config.map_transition:
        map_display_backup_old.blit(map_display_backup, (0,0))
    # save the new empty background
    map_display_backup.blit(map_display, (0,0))
    # refresh the scoreboard area
    draw_map_info()
    init_scoreboard()
    update_scoreboard()
    # performs the screen transition
    if config.map_transition:
        map_transition()        
    # reset the groups  
    all_sprites_group.empty()
    enemies_group.empty()
    globalvars.dust_in_progress = False
    # add the player  
    all_sprites_group.add(player)
    # add enemies to the map reading from 'ENEMIES_DATA' list (enems.h)
    # (a maximum of three enemies per map)
    for i in range(3):
        enemy_data = globalvars.ENEMIES_DATA[map_number*3 + i]
        if enemy_data[6] != 0: # no enemy
            enemy = Enemy(enemy_data)
            all_sprites_group.add(enemy)
            enemies_group.add(enemy)



#===============================================================================
# Main
#===============================================================================

# initialisation
pygame.init()
pygame.mixer.init()

# reads the configuration file to apply the personal settings
config.read()

# generates a main window (or full screen) 
# with title, icon, and 32-bit colour.
flags = 0
if config.full_screen:
    flags = pygame.FULLSCREEN
screen = pygame.display.set_mode(globalvars.WIN_SIZE, flags, 32)
pygame.display.set_caption('.:: Red Planet Pi ::.')
icon = pygame.image.load('images/assets/icon.png').convert_alpha()
pygame.display.set_icon(icon)  

# area covered by the map
map_display = pygame.Surface(globalvars.MAP_UNSCALED_SIZE)
# area covered by the scoreboard
sboard_display = pygame.Surface(globalvars.SBOARD_UNSCALED_SIZE)
# surface to save the generated map without sprites
map_display_backup = pygame.Surface(globalvars.MAP_UNSCALED_SIZE)
# surface to save the previous map (transition effect between screens)
if config.map_transition:
    map_display_backup_old = pygame.Surface(globalvars.MAP_UNSCALED_SIZE)
# surface for HQ scanlines
if config.scanlines_type == 2:
    screen_sl = pygame.Surface(globalvars.WIN_SIZE)
    screen_sl.set_alpha(40)

# fonts
fg_font_S = Font('images/fonts/small_font.png', globalvars.PALETTE['GREEN'], True)
bg_font_S = Font('images/fonts/small_font.png', globalvars.PALETTE['DARK_GREEN'], False)
fg_font_L = Font('images/fonts/large_font.png', globalvars.PALETTE['WHITE'], True)
bg_font_L = Font('images/fonts/large_font.png', globalvars.PALETTE['DARK_GRAY'], False)
aux_font_L = Font('images/fonts/large_font.png', globalvars.PALETTE['YELLOW'], False)

# scoreboard icons
lives_icon = pygame.image.load('images/assets/lives.png').convert()
oxigen_icon = pygame.image.load('images/tiles/T53.png').convert()
ammo_icon = pygame.image.load('images/tiles/T52.png').convert()
keys_icon = pygame.image.load('images/tiles/T51.png').convert()
explosives_icon = pygame.image.load('images/tiles/T50.png').convert()

# sequences of animations for the player depending on its status
player_animation = {
    enums.IDLE: [
        pygame.image.load('images/sprites/player0.png').convert_alpha(),
        pygame.image.load('images/sprites/player1.png').convert_alpha()],
    enums.WALKING: [
        pygame.image.load('images/sprites/player2.png').convert_alpha(),
        pygame.image.load('images/sprites/player0.png').convert_alpha(),
        pygame.image.load('images/sprites/player3.png').convert_alpha(),
        pygame.image.load('images/sprites/player0.png').convert_alpha()],
    enums.JUMPING: [
        pygame.image.load('images/sprites/player4.png').convert_alpha()],
    enums.FALLING: [
        pygame.image.load('images/sprites/player5.png').convert_alpha()]}

# dust images
dust_animation = {
    enums.JUMPING: [
        pygame.image.load('images/sprites/dust0.png').convert_alpha(),
        pygame.image.load('images/sprites/dust1.png').convert_alpha(),
        pygame.image.load('images/sprites/dust2.png').convert_alpha(),
        pygame.image.load('images/sprites/dust3.png').convert_alpha(),                                
        pygame.image.load('images/sprites/dust4.png').convert_alpha()],
    enums.FALLING: [
        pygame.image.load('images/sprites/dust5.png').convert_alpha(),
        pygame.image.load('images/sprites/dust6.png').convert_alpha(),
        pygame.image.load('images/sprites/dust7.png').convert_alpha(),
        pygame.image.load('images/sprites/dust8.png').convert_alpha()],
}

# clock to control the FPS
clock = pygame.time.Clock()

game_status = enums.OVER
music_status = enums.UNMUTED



#===============================================================================
# Main loop
#===============================================================================

while True:    
    if game_status == enums.OVER: # game not running
        #main_menu()
        # sprite control groups
        all_sprites_group = pygame.sprite.Group()     
        enemies_group = pygame.sprite.Group()
        # create the player
        player = Player(player_animation, dust_animation, all_sprites_group)
        # ingame music
        pygame.mixer.music.load('sounds/ingame.ogg')
        #pygame.mixer.music.play(-1)
        # reset variables
        game_status = enums.RUNNING
        map_number = 0
        last_map = -1
        map_scroll = enums.RIGHT
    else: # game running or paused
        # event management
        for event in pygame.event.get():
            # exit when click on the X in the window
            if event.type == pygame.QUIT: 
                exit()
            if event.type == pygame.KEYDOWN:
                # exit by pressing ESC key
                if event.key == pygame.K_ESCAPE:
                    if confirm_exit():
                        game_status = enums.OVER # go to the main menu
                # pause main loop
                if event.key == config.pause_key:
                    if game_status == enums.RUNNING:
                        game_status = enums.PAUSED
                        # mute the music if necessary
                        if music_status == enums.UNMUTED:
                            pygame.mixer.music.fadeout(1200)
                    else:
                        game_status = enums.RUNNING
                        # restore music if necessary
                        if music_status == enums.UNMUTED:
                            pygame.mixer.music.play()
                # mute music
                if event.key == config.mute_key :
                    if music_status == enums.MUTED:
                        music_status = enums.UNMUTED
                        pygame.mixer.music.play()
                    else:
                        music_status = enums.MUTED
                        pygame.mixer.music.fadeout(1200)

                # temp code ================
                if event.key == pygame.K_RIGHT:
                    if map_number < 44:
                        map_number += 1
                if event.key == pygame.K_LEFT:
                    if map_number > 0:
                        map_number -= 1
                # ==========================

        # change map if neccessary
        if map_number != last_map:
            change_map()

        if game_status == enums.RUNNING:
            # update sprites
            all_sprites_group.update()

            # collision between the player and the martians?
            if pygame.sprite.spritecollide(player, enemies_group, False):
                player.lives -= 1 # one life less

            if player.lives == 0:
                # print game over message
                game_status = enums.OVER
            else:
                # immune for 5 seconds
                pass

            # draws the map free of sprites to clean it up
            map_display.blit(map_display_backup, (0,0))
            # and change the frame of the animated tiles
            map_display_backup = tiled.animate_tiles(map_display_backup)
            # print sprites
            all_sprites_group.draw(map_display)
            # updates the scoreboard, only if necessary
            if globalvars.refresh_scoreboard:
                update_scoreboard()
            # check map change using player's coordinates
            # if the player leaves, the map number changes
            check_map_change(player)
            
        elif game_status == enums.PAUSED:            
            message_box('P a u s e', 'THE MASSACRE CAN WAIT')

    # FPS counter using the clock   
    aux_font_L.render(str(int(clock.get_fps())).rjust(3, '0') + 
        ' FPS', sboard_display, (124, 22))

    update_screen()
