
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
import constants, enums
import support # generic functions

# classes
from map import Map
from font import Font
from player import Player
from enemy import Enemy
from scoreboard import Scoreboard
from config import Configuration

# local vars
map_number = 0 # current map
map_scroll = 0 # scroll direction for map_transition()
last_map = -1 # last map loaded
game_percent = 0 # % of gameplay completed


#===============================================================================
# Map functions
#===============================================================================

# checks if the map needs to be changed (depending on the player's XY position)
def check_map_change(player):
    global map_number, map_scroll
    # player disappears on the left
    # appearing from the right on the new map
    if player.rect.x < -(player.rect.width - 1):
        map_number -= 1
        map_scroll = enums.LEFT
        player.rect.right = constants.MAP_UNSCALED_SIZE[0]
    # player disappears on the right
    # appearing from the left on the new map
    elif player.rect.x > constants.MAP_UNSCALED_SIZE[0] - 1:
        map_number += 1
        map_scroll = enums.RIGHT
        player.rect.left = 0
    # player disappears over the top
    # appearing at the bottom of the new map 
    elif player.rect.y < (-16):
        map_number -= 5
        map_scroll = enums.UP
        player.rect.bottom = constants.MAP_UNSCALED_SIZE[1]
        # jumps again on some maps to facilitate the return
        if map_number in (2, 7, 14, 19):
            player.direction.y = constants.JUMP_VALUE
    # player disappears from underneath
    #appearing at the top of the new map
    elif player.rect.y > constants.MAP_UNSCALED_SIZE[1]:
        map_number += 5
        map_scroll = enums.DOWN
        player.rect.top = 0

# makes a screen transition between the old map and the new one.
def map_transition():
    # surfaces to save the old and the new map together
    map_trans_horiz = pygame.Surface(
        (constants.MAP_UNSCALED_SIZE[0]*2, constants.MAP_UNSCALED_SIZE[1]))
    map_trans_vert = pygame.Surface(
        (constants.MAP_UNSCALED_SIZE[0], constants.MAP_UNSCALED_SIZE[1]*2))

    if map_scroll == enums.UP:
        # joins the two maps on a single surface
        map_trans_vert.blit(map_display_backup, (0,0))
        map_trans_vert.blit(map_display_backup_old, (0, constants.MAP_UNSCALED_SIZE[1]))
        # scrolls the two maps across the screen
        for y in range(-constants.MAP_UNSCALED_SIZE[1], 0, 4):
            map_display.blit(map_trans_vert, (0, y))
            update_screen()
    elif map_scroll == enums.DOWN:
        # joins the two maps on a single surface
        map_trans_vert.blit(map_display_backup_old, (0,0))
        map_trans_vert.blit(map_display_backup, (0, constants.MAP_UNSCALED_SIZE[1]))
        # scrolls the two maps across the screen
        for y in range(0, -constants.MAP_UNSCALED_SIZE[1], -4):
            map_display.blit(map_trans_vert, (0, y))
            update_screen()
    elif map_scroll == enums.LEFT:
        # joins the two maps on a single surface
        map_trans_horiz.blit(map_display_backup, (0,0))
        map_trans_horiz.blit(map_display_backup_old, (constants.MAP_UNSCALED_SIZE[0], 0))
        # scrolls the two maps across the screen
        for x in range(-constants.MAP_UNSCALED_SIZE[0], 0, 6):
            map_display.blit(map_trans_horiz, (x, 0))
            update_screen()
    else: # right
        # joins the two maps on a single surface
        map_trans_horiz.blit(map_display_backup_old, (0,0))
        map_trans_horiz.blit(map_display_backup, (constants.MAP_UNSCALED_SIZE[0], 0))
        # scrolls the two maps across the screen
        for x in range(0, -constants.MAP_UNSCALED_SIZE[0], -6):
            map_display.blit(map_trans_horiz, (x, 0))
            update_screen()

# does everything necessary to change the map
def change_map():
    global last_map, map_number
    # sets the new map as the current one
    last_map = map_number
    # load the new map
    #.load_map(map_number, map_display)
    map.load(map_number)
    # preserves the previous 
    if config.map_transition:
        map_display_backup_old.blit(map_display_backup, (0,0))
    # save the new empty background
    map_display_backup.blit(map_display, (0,0))
    # refresh the scoreboard area
    scoreboard.reset()
    scoreboard.map_info(map_number, game_percent)
    scoreboard.invalidate()
    # performs the screen transition
    if config.map_transition:
        map_transition()        
    # reset the sprite groups  
    all_sprites_group.empty()
    enemies_group.empty()
    platform_group.empty()
    dust_group.empty()
    # add the player  
    all_sprites_group.add(player)
    # add enemies (and mobile platforms) to the map reading from 'ENEMIES_DATA' list (enems.h)
    # a maximum of three enemies per map
    for i in range(3):
        enemy_data = constants.ENEMIES_DATA[map_number*3 + i]
        if enemy_data[6] != enums.NONE:
            enemy = Enemy(enemy_data)
            all_sprites_group.add(enemy)
            # enemy sprite? add to the enemy group (to check for collisions)
            if enemy_data[6] != enums.PLATFORM_SPR:
                enemies_group.add(enemy)
            else: # platform sprite? add to the platform group
                platform_group.add(enemy)


#===============================================================================
# Main functions
#===============================================================================

#dumps and scales surfaces to the screen
def update_screen():
    # scale x 3 the scoreboard
    screen.blit(pygame.transform.scale(sboard_display, constants.SBOARD_SCALED_SIZE), 
        (constants.H_MARGIN, constants.V_MARGIN))
    # scale x 3 the map
    screen.blit(pygame.transform.scale(map_display, constants.MAP_SCALED_SIZE), 
        (constants.H_MARGIN, constants.SBOARD_SCALED_SIZE[1] + constants.V_MARGIN))
    support.make_scanlines(screen, screen_sl, config)
    pygame.display.update() # refreshes the screen
    clock.tick(60) # 60 FPS

# displays a message to confirm exit
def confirm_exit():
    support.message_box(
        'Leave the current game?', 'PRESS Y TO EXIT OR N TO CONTINUE',
        map_display, font_BL, font_FL, font_BS, font_FS)
    screen.blit(pygame.transform.scale(sboard_display, constants.SBOARD_SCALED_SIZE), 
        (constants.H_MARGIN, constants.V_MARGIN))        
    screen.blit(pygame.transform.scale(map_display, constants.MAP_SCALED_SIZE), 
        (constants.H_MARGIN, constants.SBOARD_SCALED_SIZE[1] + constants.V_MARGIN))
    support.make_scanlines(screen, screen_sl, config)
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
    map_display.fill(constants.PALETTE['BLACK'])
    sboard_display.fill(constants.PALETTE['BLACK'])
    support.message_box('Red Planet Pi', 'WIP. Press a key to continue',
        map_display, font_BL, font_FL, font_BS, font_FS)
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


#===============================================================================
# Main
#===============================================================================

# initialisation
pygame.init()
pygame.mixer.init()
pygame.mouse.set_visible(False)

# reads the configuration file to apply the personal settings
config = Configuration()
config.read()

# generates a main window (or full screen) 
# with title, icon, and 32-bit colour.
flags = 0
if config.full_screen:
    flags = pygame.FULLSCREEN
screen = pygame.display.set_mode(constants.WIN_SIZE, flags, 32)
pygame.display.set_caption('.:: Red Planet Pi ::.')
icon = pygame.image.load('images/assets/icon.png').convert_alpha()
pygame.display.set_icon(icon)  

# area covered by the map
map_display = pygame.Surface(constants.MAP_UNSCALED_SIZE)
# area covered by the scoreboard
sboard_display = pygame.Surface(constants.SBOARD_UNSCALED_SIZE)
# surface to save the generated map without sprites
map_display_backup = pygame.Surface(constants.MAP_UNSCALED_SIZE)
# surface to save the previous map (transition effect between screens)
if config.map_transition:
    map_display_backup_old = pygame.Surface(constants.MAP_UNSCALED_SIZE)
# surface for HQ scanlines
screen_sl = pygame.Surface(constants.WIN_SIZE)
screen_sl.set_alpha(40)

# fonts
font_FS = Font('images/fonts/small_font.png', constants.PALETTE['GREEN'], True)
font_BS = Font('images/fonts/small_font.png', constants.PALETTE['DARK_GREEN'], False)
font_FL = Font('images/fonts/large_font.png', constants.PALETTE['WHITE'], True)
font_BL = Font('images/fonts/large_font.png', constants.PALETTE['DARK_GRAY'], False)
#aux_font_L = Font('images/fonts/large_font.png', globalvars.PALETTE['YELLOW'], False)

scoreboard = Scoreboard(sboard_display, font_FL, font_BL, font_FS, font_BS)
map = Map(map_display)

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
        platform_group = pygame.sprite.GroupSingle()
        dust_group = pygame.sprite.GroupSingle()
        # create the player
        player = Player(player_animation, dust_animation, 
            all_sprites_group, dust_group, map, scoreboard, config)
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
            if not player.invincible and pygame.sprite.spritecollide(player, 
                enemies_group, False, pygame.sprite.collide_rect_ratio(0.60)):
                player.loses_life()
                scoreboard.invalidate()

            # collision between the player and a mobile platform?
            if pygame.sprite.spritecollide(player, platform_group, False,
                pygame.sprite.collide_rect_ratio(1.15)):
                # the player is above the platform?
                if player.rect.bottom - 2 < platform_group.sprite.rect.top:                 
                    player.rect.bottom = platform_group.sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True

            if player.lives == 0:
                # print game over message
                game_status = enums.OVER

            # draws the map free of sprites to clean it up
            map_display.blit(map_display_backup, (0,0))
            # and change the frame of the animated tiles
            map_display_backup = map.animate_tiles(map_display_backup)

            # print sprites
            all_sprites_group.draw(map_display)

            # updates the scoreboard, only if needed
            scoreboard.update(player)

            # check map change using player's coordinates
            # if the player leaves, the map number changes
            check_map_change(player)
            
        elif game_status == enums.PAUSED:            
            support.message_box('P a u s e', 'THE MASSACRE CAN WAIT',
            map_display, font_BL, font_FL, font_BS, font_FS)

    # TEST /////////////////////////////////////////////////////////////////////
    # FPS counter using the clock   
    #aux_font_L.render(str(int(clock.get_fps())).rjust(3, '0') + 
    #    ' FPS', sboard_display, (124, 22))
    # draw collision rects
    #pygame.draw.rect(map_display, globalvars.PALETTE['YELLOW'], player.rect, 1)
    #if platform_group.sprite != None:
    #    pygame.draw.rect(map_display, globalvars.PALETTE['GREEN'], 
    #       platform_group.sprite.rect, 1)
    #print(player.y_speed)
    # //////////////////////////////////////////////////////////////////////////
    
    update_screen()
