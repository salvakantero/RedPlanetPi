
# ==============================================================================
# Red Planet Pi v1.0
# salvaKantero 2022/23
# ==============================================================================

import pygame # pygame library functions
import sys # exit()
import random

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


#===============================================================================
# Map functions
#===============================================================================

# makes a screen transition between the old map and the new one.
def map_transition():
    # surfaces to save the old and the new map together
    map_trans_horiz = pygame.Surface(
        (constants.MAP_UNSCALED_SIZE[0]*2, constants.MAP_UNSCALED_SIZE[1]))
    map_trans_vert = pygame.Surface(
        (constants.MAP_UNSCALED_SIZE[0], constants.MAP_UNSCALED_SIZE[1]*2))

    if map.scroll == enums.UP:
        # joins the two maps on a single surface
        map_trans_vert.blit(map_surf_bk, (0,0))
        map_trans_vert.blit(map_surf_bk_prev, (0, constants.MAP_UNSCALED_SIZE[1]))
        # scrolls the two maps across the screen
        for y in range(-constants.MAP_UNSCALED_SIZE[1], 0, 4):
            map_surf.blit(map_trans_vert, (0, y))
            update_screen()
    elif map.scroll == enums.DOWN:
        # joins the two maps on a single surface
        map_trans_vert.blit(map_surf_bk_prev, (0,0))
        map_trans_vert.blit(map_surf_bk, (0, constants.MAP_UNSCALED_SIZE[1]))
        # scrolls the two maps across the screen
        for y in range(0, -constants.MAP_UNSCALED_SIZE[1], -4):
            map_surf.blit(map_trans_vert, (0, y))
            update_screen()
    elif map.scroll == enums.LEFT:
        # joins the two maps on a single surface
        map_trans_horiz.blit(map_surf_bk, (0,0))
        map_trans_horiz.blit(map_surf_bk_prev, (constants.MAP_UNSCALED_SIZE[0], 0))
        # scrolls the two maps across the screen
        for x in range(-constants.MAP_UNSCALED_SIZE[0], 0, 6):
            map_surf.blit(map_trans_horiz, (x, 0))
            update_screen()
    else: # right
        # joins the two maps on a single surface
        map_trans_horiz.blit(map_surf_bk_prev, (0,0))
        map_trans_horiz.blit(map_surf_bk, (constants.MAP_UNSCALED_SIZE[0], 0))
        # scrolls the two maps across the screen
        for x in range(0, -constants.MAP_UNSCALED_SIZE[0], -6):
            map_surf.blit(map_trans_horiz, (x, 0))
            update_screen()

# does everything necessary to change the map
def change_map():
    # sets the new map as the current one
    map.last = map.number
    # load the new map
    map.load()
    # preserves the previous 
    if config.map_transition:
        map_surf_bk_prev.blit(map_surf_bk, (0,0))
    # save the new empty background
    map_surf_bk.blit(map_surf, (0,0))
    # performs the screen transition
    if config.map_transition:
        map_transition()  
    # refresh the scoreboard area
    scoreboard.reset()
    scoreboard.map_info(map.number, map.game_percent)
    scoreboard.invalidate()      
    # reset the sprite groups  
    all_sprites_group.empty()
    enemies_group.empty()
    platform_group.empty()
    dust_group.empty()
    # add the player  
    all_sprites_group.add(player)
    # add enemies (and mobile platforms) to the map 
    # reading from 'ENEMIES_DATA' list (enems.h)
    # a maximum of three enemies per map
    for i in range(3):
        enemy_data = constants.ENEMIES_DATA[map.number*3 + i]
        if enemy_data[6] != enums.NONE:
            enemy = Enemy(enemy_data, player)
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
    # shakes the surface of the map if it has been requested
    offset = [0,0]
    if map.shake_timer > 0:
        offset[0] = random.randint(-map.shake[0], map.shake[0])
        offset[1] = random.randint(-map.shake[1], map.shake[1])
        map.shake_timer -= 1
    # scale x 3 the scoreboard
    screen.blit(pygame.transform.scale(
        sboard_surf, constants.SBOARD_SCALED_SIZE), 
        (constants.H_MARGIN, constants.V_MARGIN))
    # scale x 3 the map
    screen.blit(pygame.transform.scale(
        map_surf, constants.MAP_SCALED_SIZE), (constants.H_MARGIN + offset[0], 
        constants.SBOARD_SCALED_SIZE[1] + constants.V_MARGIN + offset[1]))
    support.make_scanlines(screen, scanlines_surf, config)
    pygame.display.update() # refreshes the screen
    clock.tick(60) # 60 FPS

# displays a message to confirm exit
def confirm_exit():
    support.message_box(
        'Leave the current game?', 'PRESS Y TO EXIT OR N TO CONTINUE',
        map_surf, font_BL, font_FL, font_BS, font_FS)
    screen.blit(pygame.transform.scale(sboard_surf, constants.SBOARD_SCALED_SIZE), 
        (constants.H_MARGIN, constants.V_MARGIN))        
    screen.blit(pygame.transform.scale(map_surf, constants.MAP_SCALED_SIZE), 
        (constants.H_MARGIN, constants.SBOARD_SCALED_SIZE[1] + constants.V_MARGIN))
    support.make_scanlines(screen, scanlines_surf, config)
    pygame.display.update()
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_y:                    
                    return True
                elif event.key == pygame.K_n:  
                    return False

# displays a game over message and waits
def game_over():  
    support.message_box('G a m e  O v e r', 'PRESS Y TO TRY AGAIN OR N TO EXIT!',
        map_surf, font_BL, font_FL, font_BS, font_FS)
    screen.blit(pygame.transform.scale(sboard_surf, constants.SBOARD_SCALED_SIZE), 
        (constants.H_MARGIN, constants.V_MARGIN))        
    screen.blit(pygame.transform.scale(map_surf, constants.MAP_SCALED_SIZE), 
        (constants.H_MARGIN, constants.SBOARD_SCALED_SIZE[1] + constants.V_MARGIN))
    support.make_scanlines(screen, scanlines_surf, config)
    pygame.display.update()
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_y:                    
                    return True
                elif event.key == pygame.K_n:  
                    pygame.quit()

# Main menu
def main_menu():
    map_surf.fill(constants.PALETTE['BLACK'])
    sboard_surf.fill(constants.PALETTE['BLACK'])
    support.message_box('Red Planet Pi', 'WIP. Press a key to continue',
        map_surf, font_BL, font_FL, font_BS, font_FS)
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

# collision between the player and an enemy or moving platform
def collision_check():
    # mobile platform
    if platform_group.sprite != None \
    and pygame.sprite.spritecollide(player, platform_group, False, 
    pygame.sprite.collide_rect_ratio(1.15)):
        platform = platform_group.sprite
        # the player is above the platform?
        if player.rect.bottom - 2 < platform.rect.top:                 
            player.rect.bottom = platform.rect.top
            player.direction.y = 0                    
            player.on_ground = True                                        
            # horizontal platform
            if platform.my == 0:
                # if the movement keys are not pressed
                # takes the movement of the platform
                key_state = pygame.key.get_pressed()
                if not key_state[config.left_key] \
                and not key_state[config.right_key]:
                    player.rect.x += platform.mx
    # martians
    if not player.invincible and pygame.sprite.spritecollide(player, 
    enemies_group, False, pygame.sprite.collide_rect_ratio(0.60)):
        player.loses_life()
        scoreboard.invalidate() # redraws the scoreboard

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
map_surf = pygame.Surface(constants.MAP_UNSCALED_SIZE)
# area covered by the scoreboard
sboard_surf = pygame.Surface(constants.SBOARD_UNSCALED_SIZE)
# surface to save the generated map without sprites
map_surf_bk = pygame.Surface(constants.MAP_UNSCALED_SIZE)
# surface to save the previous map (transition effect between screens)
if config.map_transition:
    map_surf_bk_prev = pygame.Surface(constants.MAP_UNSCALED_SIZE)
# surface for HQ scanlines
scanlines_surf = pygame.Surface(constants.WIN_SIZE)
scanlines_surf.set_alpha(40)

# fonts
font_FS = Font('images/fonts/small_font.png', constants.PALETTE['GREEN'], True)
font_BS = Font('images/fonts/small_font.png', constants.PALETTE['DARK_GREEN'], False)
font_FL = Font('images/fonts/large_font.png', constants.PALETTE['WHITE'], True)
font_BL = Font('images/fonts/large_font.png', constants.PALETTE['DARK_GRAY'], False)
aux_font_L = Font('images/fonts/large_font.png', constants.PALETTE['YELLOW'], False)

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

# create the Scoreboard object
scoreboard = Scoreboard(sboard_surf, font_FL, font_BL, font_FS, font_BS)
# create the Map object
map = Map(map_surf)

game_status = enums.OVER
music_status = enums.UNMUTED

# clock to control the FPS
clock = pygame.time.Clock()

#===============================================================================
# Main loop
#===============================================================================

while True:    
    if game_status == enums.OVER: # game not running
        main_menu()
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
        map.number = 0
        map.last = -1
        map.scroll = enums.RIGHT
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
                    if map.number < 44:
                        map.number += 1
                if event.key == pygame.K_LEFT:
                    if map.number > 0:
                        map.number -= 1
                # ==========================

        # change map if neccessary
        if map.number != map.last:
            change_map()

        if game_status == enums.RUNNING:
            # update sprites
            all_sprites_group.update()
            # collision between the player and an enemy or moving platform
            collision_check()
            # game over?
            if player.lives == 0 and game_over():
                game_status = enums.OVER

            # draws the map free of sprites to clean it up
            map_surf.blit(map_surf_bk, (0,0))
            # and change the frame of the animated tiles
            map_surf_bk = map.animate_tiles(map_surf_bk)
            # print sprites
            all_sprites_group.draw(map_surf)
            # updates the scoreboard, only if needed
            scoreboard.update(player)
            # check map change using player's coordinates
            # if the player leaves, the map number changes
            map.check_change(player)
            
        elif game_status == enums.PAUSED:            
            support.message_box('P a u s e', 'THE MASSACRE CAN WAIT',
            map_surf, font_BL, font_FL, font_BS, font_FS)

    # TEST /////////////////////////////////////////////////////////////////////
    # FPS counter using the clock   
    #aux_font_L.render(str(int(clock.get_fps())).rjust(3, '0') + 
    #    ' FPS', sboard_surf, (124, 22))
    # draw collision rects
    #pygame.draw.rect(map_display, globalvars.PALETTE['YELLOW'], player.rect, 1)
    #if platform_group.sprite != None:
    #    pygame.draw.rect(map_display, globalvars.PALETTE['GREEN'], 
    #       platform_group.sprite.rect, 1)
    # any other data
    #aux_font_L.render(str(player.direction.y), sboard_surf, (124, 22))
    #print(player.state)
    # //////////////////////////////////////////////////////////////////////////
    
    update_screen()
