
# ==============================================================================
# Red Planet Pi v1.0
# salvaKantero 2022/23
# ==============================================================================

import pygame # pygame library functions
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
from hotspot import Hotspot
from gate import Gate
from scoreboard import Scoreboard
from config import Configuration
from explosion import Explosion


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
    scoreboard.map_info(map.number)
    scoreboard.invalidate()      
    # reset the sprite groups  
    all_sprites_group.empty()
    enemies_group.empty()
    hotspot_group.empty()
    gate_group.empty()
    platform_group.empty()
    dust_group.empty()
    blast_group.empty()
    # add the player  
    all_sprites_group.add(player)
    # add the hotspot (if available)
    hotspot = hotspot_data[map.number]
    if hotspot[3] == True: # visible/available?           
        hotspot_sprite = Hotspot(hotspot, hotspot_images[hotspot[0]])
        all_sprites_group.add(hotspot_sprite) # to update/draw it
        hotspot_group.add(hotspot_sprite) # to check for collisions
    # add the gate (if there is one visible on the map)
    gate = gate_data.get(map.number)
    if gate != None and gate[2] == True: # visible/available?
        gate_sprite = Gate(gate, gate_image)
        all_sprites_group.add(gate_sprite) # to update/draw it
        gate_group.add(gate_sprite) # to check for collisions
    # add enemies (and mobile platforms) to the map 
    # reading from 'ENEMIES_DATA' list (enems.h)
    # a maximum of three enemies per map
    for i in range(3):
        enemy_data = constants.ENEMIES_DATA[map.number*3 + i]
        if enemy_data[6] != enums.NONE:
            enemy = Enemy(enemy_data, player)
            all_sprites_group.add(enemy) # to update/draw it
            # enemy sprite? add to the enemy group (to check for collisions)
            if enemy_data[6] != enums.PLATFORM_SPR:
                enemies_group.add(enemy) # to check for collisions
            else: # platform sprite? add to the platform group
                platform_group.add(enemy) # to check for collisions


#===============================================================================
# Main functions
#===============================================================================

# it's necessary to clean the edges of the map after shaking it
def clean_edges():
    pygame.draw.rect(screen, constants.PALETTE['BLACK'], 
        (20, 120 , 20 , 500))
    pygame.draw.rect(screen, constants.PALETTE['BLACK'], 
        (760, 120 , 20 , 500))
    pygame.draw.rect(screen, constants.PALETTE['BLACK'],
        (40, 610 , 720 , 20))

# dumps and scales surfaces to the screen
def update_screen():
    # shakes the surface of the map if it has been requested
    offset = [0,0]
    if map.shake_timer > 0:
        if map.shake_timer == 1: # last frame shaken            
            clean_edges()
        else:
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

# displays a message, darkening the screen
def show_message(msg1, msg2):
    # obscures the surface of the map
    map_surf.set_alpha(120)
    update_screen()
    # saves a copy of the darkened screen
    dim_surf = pygame.Surface(constants.MAP_UNSCALED_SIZE)    
    dim_surf.blit(map_surf, (0,0))
    # draws the light message on the dark background
    support.message_box(msg1, msg2, dim_surf, font_BL, font_FL, font_BS, font_FS)
    # return the copy with the message on the map surface and redraw it.
    map_surf.blit(dim_surf, (0,0))
    map_surf.set_alpha(None)
    update_screen()

# displays a message to confirm exit
def confirm_exit():
    show_message('Leave the current game?', 'ESC TO EXIT. ANY OTHER KEY TO CONTINUE')
    pygame.event.clear(pygame.KEYDOWN)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                support.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:                    
                    return True 
                return False

# displays a 'game over' message and waits
def game_over():  
    show_message('G a m e  O v e r', 'PRESS ANY KEY')
    sfx_game_over.play()
    pygame.event.clear(pygame.KEYDOWN)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                support.exit()
            if event.type == pygame.KEYDOWN:                  
                return

# displays a 'pause' message and waits
def pause_game():
    show_message('P a u s e', 'THE MASSACRE CAN WAIT!')
    pygame.event.clear(pygame.KEYDOWN)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                support.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or \
                event.key == config.pause_key:
                    return

# main menu
def main_menu():
    map_surf.fill(constants.PALETTE['BLACK'])
    sboard_surf.fill(constants.PALETTE['BLACK'])
    show_message('-Red Planet Pi-', 'WIP. PRESS ANY KEY TO CONTINUE')
    pygame.event.clear(pygame.KEYDOWN)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                support.exit()
            if event.type == pygame.KEYDOWN:
                # exit by pressing ESC key
                if event.key == pygame.K_ESCAPE:
                    support.exit()
                return

# collisions (mobile platforms, enemies, bullets, hotspots, gates)
def collision_check():
    # player and mobile platform -----------------------------------------------
    if platform_group.sprite != None \
    and pygame.sprite.spritecollide(player, platform_group, False, 
    pygame.sprite.collide_rect_ratio(1.15)):
        platform = platform_group.sprite
        # the player is above the platform?
        if player.rect.bottom - 2 < platform.rect.top:                 
            player.rect.bottom = platform.rect.top
            player.direction.y = 0                    
            player.on_ground = True                                        
            # horizontal platform?
            if platform.my == 0:
                # if the movement keys are not pressed
                # takes the movement of the platform
                key_state = pygame.key.get_pressed()
                if not key_state[config.left_key] \
                and not key_state[config.right_key]:
                    player.rect.x += platform.mx
    
    # player and martians ------------------------------------------------------
    if not player.invincible and pygame.sprite.spritecollide(player, 
    enemies_group, False, pygame.sprite.collide_rect_ratio(0.60)):
        player.loses_life()        
        scoreboard.invalidate() # redraws the scoreboard
    
    # bullets and martians -----------------------------------------------------
    if not bullet_group.sprite == None:
        for enemy in enemies_group:
            if enemy.rect.colliderect(bullet_group.sprite):
                # shake the map
                map.shake = [10, 6]
                map.shake_timer = 14
                # creates an explosion
                if enemy.type == enums.INFECTED:
                    blast = Explosion([enemy.rect.centerx, enemy.rect.centery-4], 
                        blast_animation[1])
                    sfx_exp_infected.play()
                else: # flying enemies
                    blast = Explosion(enemy.rect.center, blast_animation[0])
                    # explosion sounds according to enemy type
                    if enemy.type == enums.AVIRUS: sfx_exp_avirus.play()
                    elif enemy.type == enums.PELUSOID: sfx_exp_pelusoid.play()
                    else: sfx_exp_fanty.play()
                blast_group.add(blast)
                all_sprites_group.add(blast)
                # removes objects
                enemy.kill()
                bullet_group.sprite.kill()
                break
    
    # player and hotspot -------------------------------------------------------
    if not hotspot_group.sprite == None:
        if player.rect.colliderect(hotspot_group.sprite):
            hotspot = hotspot_group.sprite
            # shake the map (just a little)
            map.shake = [4, 4]
            map.shake_timer = 4
            # creates a magic halo
            blast = Explosion(hotspot.rect.center, blast_animation[2])
            blast_group.add(blast)
            all_sprites_group.add(blast)
            # manages the object according to the type
            if hotspot.type == enums.TNT: 
                player.TNT += 1
                scoreboard.game_percent += 3
            elif hotspot.type == enums.KEY: 
                player.keys += 1
                scoreboard.game_percent += 2
            elif hotspot.type == enums.AMMO: 
                if player.ammo + constants.AMMO_ROUND < constants.MAX_AMMO: 
                    player.ammo += constants.AMMO_ROUND
                else: player.ammo = constants.MAX_AMMO
            elif hotspot.type == enums.OXYGEN: 
                player.oxygen = constants.MAX_OXYGEN
            scoreboard.invalidate()
            # removes objects
            hotspot_group.sprite.kill()
            hotspot_data[map.number][3] = False # not visible

    # player and gate ----------------------------------------------------------
    if gate_group.sprite != None:
        if player.rect.colliderect(gate_group.sprite):
            if player.keys > 0:
                player.keys -= 1
                sfx_door_open.play()
                # creates a magic halo
                blast = Explosion(gate_group.sprite.rect.center, blast_animation[2])
                blast_group.add(blast)
                all_sprites_group.add(blast)
                # deletes the door
                gate_group.sprite.kill()
                gate_data[map.number][2] = False # not visible
                # increases the percentage of game play
                scoreboard.game_percent += 3
                scoreboard.invalidate()
            else: 
                # shake the map (just a little in X)
                map.shake = [4, 0]
                map.shake_timer = 4
                # bounces the player
                if player.facing_right: player.rect.x -= 5
                else: player.rect.x += 5


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

# The following image lists are created here, not in their corresponding classes, 
# as hundreds of DUST and EXPLOSION objects can be generated per game.
hotspot_images = {
    enums.TNT: pygame.image.load('images/sprites/hotspot0.png').convert_alpha(),
    enums.KEY: pygame.image.load('images/sprites/hotspot1.png').convert_alpha(),
    enums.AMMO: pygame.image.load('images/sprites/hotspot2.png').convert_alpha(),
    enums.OXYGEN: pygame.image.load('images/sprites/hotspot3.png').convert_alpha()
}

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

blast_animation = {
    0: [ # explosion 1: on the air
        pygame.image.load('images/sprites/blast0.png').convert_alpha(),
        pygame.image.load('images/sprites/blast1.png').convert_alpha(),
        pygame.image.load('images/sprites/blast2.png').convert_alpha(),
        pygame.image.load('images/sprites/blast3.png').convert_alpha(),
        pygame.image.load('images/sprites/blast4.png').convert_alpha(),
        pygame.image.load('images/sprites/blast5.png').convert_alpha(),                                 
        pygame.image.load('images/sprites/blast6.png').convert_alpha()],
    1: [ # explosion 2: on the ground
        pygame.image.load('images/sprites/blast7.png').convert_alpha(),
        pygame.image.load('images/sprites/blast8.png').convert_alpha(),
        pygame.image.load('images/sprites/blast9.png').convert_alpha(),
        pygame.image.load('images/sprites/blast10.png').convert_alpha(),
        pygame.image.load('images/sprites/blast4.png').convert_alpha(),
        pygame.image.load('images/sprites/blast5.png').convert_alpha(),                                 
        pygame.image.load('images/sprites/blast6.png').convert_alpha()],
    2: [ # explosion 3: magic halo for hotspots
        pygame.image.load('images/sprites/blast11.png').convert_alpha(),
        pygame.image.load('images/sprites/blast12.png').convert_alpha(),
        pygame.image.load('images/sprites/blast13.png').convert_alpha(),
        pygame.image.load('images/sprites/blast14.png').convert_alpha(),
        pygame.image.load('images/sprites/blast15.png').convert_alpha(),
        pygame.image.load('images/sprites/blast16.png').convert_alpha()],                                 
}

gate_image = pygame.image.load('images/tiles/T60.png').convert()

# fx sounds
sfx_door_open = pygame.mixer.Sound('sounds/fx/sfx_door_open.wav')
sfx_exp_avirus = pygame.mixer.Sound('sounds/fx/sfx_exp_avirus.wav')
sfx_exp_fanty = pygame.mixer.Sound('sounds/fx/sfx_exp_fanty.wav')
sfx_exp_infected = pygame.mixer.Sound('sounds/fx/sfx_exp_infected.wav')
sfx_exp_pelusoid = pygame.mixer.Sound('sounds/fx/sfx_exp_pelusoid.wav')
sfx_game_over = pygame.mixer.Sound('sounds/fx/sfx_game_over.wav')

# create the Scoreboard object
scoreboard = Scoreboard(sboard_surf, hotspot_images, 
    font_FL, font_BL, font_FS, font_BS)

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
        hotspot_group = pygame.sprite.GroupSingle()
        gate_group = pygame.sprite.GroupSingle()
        platform_group = pygame.sprite.GroupSingle()
        dust_group = pygame.sprite.GroupSingle()
        bullet_group = pygame.sprite.GroupSingle()
        blast_group = pygame.sprite.GroupSingle()
        # create the player
        player = Player(dust_animation, all_sprites_group, dust_group, 
            bullet_group, map, scoreboard, config)
        # ingame music
        pygame.mixer.music.load('sounds/ingame.ogg')
        #pygame.mixer.music.play(-1)
        # reset variables
        hotspot_data = constants.INIT_HOTSPOT_DATA.copy()
        gate_data = constants.INIT_GATE_DATA.copy()
        game_status = enums.RUNNING
        map.number = 0
        map.last = -1
        map.scroll = enums.RIGHT
        scoreboard.game_percent = 0
    else: # game running or paused
        # event management
        for event in pygame.event.get():
            # exit when click on the X in the window
            if event.type == pygame.QUIT: 
                support.exit()
            if event.type == pygame.KEYDOWN:
                # exit by pressing ESC key
                if event.key == pygame.K_ESCAPE:
                    if confirm_exit():
                        game_status = enums.OVER # go to the main menu

                # pause main loop
                if event.key == config.pause_key:
                    # mute the music if necessary
                    if music_status == enums.UNMUTED:
                        pygame.mixer.music.fadeout(1200)
                    pause_game()
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
            if player.lives == 0 or player.oxygen < 0:
                game_status = enums.OVER
                game_over()
                continue
            # draws the map free of sprites to clean it up
            map_surf.blit(map_surf_bk, (0,0))
            # change the frame of the animated tiles
            map.animate_tiles(map_surf_bk)
            # print sprites
            all_sprites_group.draw(map_surf)
            # updates the scoreboard, only if needed
            scoreboard.update(player)
            # check map change using player's coordinates
            # if the player leaves, the map number changes
            map.check_change(player)
            
    # TEST /////////////////////////////////////////////////////////////////////
    # FPS counter using the clock   
    #aux_font_L.render(str(int(clock.get_fps())).rjust(3, '0') + ' FPS', sboard_surf, (124, 22))
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
