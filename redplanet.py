
# ==============================================================================
# .::Red Planet Pi::. v1.0
# Initialization and main loop
# ==============================================================================
#
#  This file is part of "Red Planet Pi". Copyright (C) 2023 @salvakantero
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ==============================================================================

import pygame # pygame library functions

# allows constants without typing "pygame."
from pygame.locals import *
from pygame.constants import *

# own code
import constants, enums
import support # generic functions

# classes
from config import Configuration
from game import Game
from intro import Intro
from menu import Menu
from map import Map
from scoreboard import Scoreboard
from font import Font
from player import Player
from enemy import Enemy
from hotspot import Hotspot
from gate import Gate
from explosion import Explosion
from floatingtext import FloatingText
from jukebox import Jukebox


#===============================================================================
# Main functions
#===============================================================================

# does everything necessary to change the map
def change_map():
    # sets the new map as the current one
    map.last = map.number
    # load the new map
    map.load()
    # preserves the previous 
    if config.map_transition:
        game.srf_map_bk_prev.blit(game.srf_map_bk, (0,0))
    # save the new empty background
    game.srf_map_bk.blit(game.srf_map, (0,0))
    # add the TNT pile if necessary to the background
    if map.number == 44 and player.stacked_TNT:
        map.add_TNT_pile()
    # performs the screen transition
    if config.map_transition:
        map.transition()
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
    hotspot = constants.HOTSPOT_DATA[map.number]
    if hotspot[3] == True: # visible/available?           
        hotspot_sprite = Hotspot(hotspot, hotspot_images[hotspot[0]])
        all_sprites_group.add(hotspot_sprite) # to update/draw it
        hotspot_group.add(hotspot_sprite) # to check for collisions
    # add the gate (if there is one visible on the map)
    gate = constants.GATE_DATA.get(map.number)
    if gate != None and gate[2] == True: # visible/available?
        gate_sprite = Gate(gate, gate_image)
        all_sprites_group.add(gate_sprite) # to update/draw it
        gate_group.add(gate_sprite) # to check for collisions
    # add enemies (and mobile platforms) to the map reading from 'ENEMIES_DATA' list.
    # a maximum of three enemies per map
    # ENEMIES_DATA = (x1, y1, x2, y2, vx, vy, type)
    for i in range(3):
        enemy_data = constants.ENEMIES_DATA[map.number*3 + i]
        if enemy_data[6] != enums.NONE:
            enemy = Enemy(enemy_data, player.rect)
            all_sprites_group.add(enemy) # to update/draw it
            # enemy sprite? add to the enemy group (to check for collisions)
            if enemy_data[6] != enums.PLATFORM_SPR:
                enemies_group.add(enemy) # to check for collisions
            else: # platform sprite? add to the platform group
                platform_group.add(enemy) # to check for collisions

# collisions (mobile platforms, enemies, bullets, hotspots, gates)
def collision_check():
    # player and mobile platform -----------------------------------------------
    if platform_group.sprite != None \
    and pygame.sprite.spritecollide(player, platform_group, False, pygame.sprite.collide_rect_ratio(1.15)):
        platform = platform_group.sprite
        # the player is above the platform?
        if player.rect.bottom - 2 < platform.rect.top:               
            player.rect.bottom = platform.rect.top
            player.direction.y = 0                    
            player.on_ground = True                                        
            # horizontal platform?
            if platform.vy == 0:
                # if the movement keys are not pressed
                # takes the movement of the platform
                key_state = pygame.key.get_pressed()
                if not key_state[config.left_key] and not key_state[config.right_key]:
                    player.rect.x += platform.vx
    
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
                game.shake = [10, 6]
                game.shake_timer = 14
                # creates an explosion
                if enemy.type == enums.INFECTED:
                    blast = Explosion([enemy.rect.centerx, enemy.rect.centery-4], blast_animation[1])
                    floating_text.text = '+25'
                else: # flying enemies
                    blast = Explosion(enemy.rect.center, blast_animation[0])
                    if enemy.type == enums.AVIRUS: floating_text.text = '+50'
                    elif enemy.type == enums.PELUSOID: floating_text.text = '+75'
                    else: floating_text.text = '+100' # fanty           
                blast_group.add(blast)
                all_sprites_group.add(blast)
                sfx_enemy_down[enemy.type].play()
                # floating text position                                
                floating_text.x = enemy.rect.x
                floating_text.y = enemy.rect.y
                # removes objects
                enemy.kill()
                bullet_group.sprite.kill()
                break

    # bullets and map tiles ----------------------------------------------------
    if not bullet_group.sprite == None:
        bullet_rect = bullet_group.sprite.rect
        for tile in map.tilemap_rect_list:
            if tile.colliderect(bullet_rect):
                bullet_group.sprite.kill()
                
    # player and hotspot -------------------------------------------------------
    if not hotspot_group.sprite == None:
        if player.rect.colliderect(hotspot_group.sprite):
            hotspot = hotspot_group.sprite
            # shake the map (just a little)
            game.shake = [4, 4]
            game.shake_timer = 4
            # creates a magic halo
            blast = Explosion(hotspot.rect.center, blast_animation[2])
            blast_group.add(blast)
            all_sprites_group.add(blast)
            sfx_hotspot[hotspot.type].play()
            # manages the object according to the type
            if hotspot.type == enums.TNT:
                player.TNT += 1
                scoreboard.game_percent += 3
                floating_text.text = str(player.TNT) + '/15' 
            elif hotspot.type == enums.KEY: 
                player.keys += 1
                scoreboard.game_percent += 2
                floating_text.text = '+1' 
            elif hotspot.type == enums.AMMO:
                if player.ammo + constants.AMMO_ROUND < constants.MAX_AMMO: 
                    player.ammo += constants.AMMO_ROUND
                else: player.ammo = constants.MAX_AMMO
                floating_text.text = '+25'
            elif hotspot.type == enums.OXYGEN:
                player.oxygen = constants.MAX_OXYGEN
                floating_text.text = '+99'                                
            scoreboard.invalidate()
            floating_text.x = hotspot.x*constants.TILE_SIZE
            floating_text.y = hotspot.y*constants.TILE_SIZE           
            # removes objects
            hotspot_group.sprite.kill()
            constants.HOTSPOT_DATA[map.number][3] = False # not visible

    # player and gate ----------------------------------------------------------
    if gate_group.sprite != None:
        if player.rect.colliderect(gate_group.sprite):
            if player.keys > 0:
                player.keys -= 1
                sfx_open_door.play()
                # creates a magic halo
                blast = Explosion(gate_group.sprite.rect.center, blast_animation[2])
                blast_group.add(blast)
                all_sprites_group.add(blast)
                # deletes the door
                gate_group.sprite.kill()
                constants.GATE_DATA[map.number][2] = False # not visible
                # increases the percentage of game play
                scoreboard.game_percent += 3
                scoreboard.invalidate()
            else: 
                sfx_locked_door.play()
                # shake the map (just a little in X)
                game.shake = [4, 0]
                game.shake_timer = 4
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

# clock to control the FPS and timers
clock = pygame.time.Clock()

# game object, for common or general tasks
game = Game(clock, config)
 
# The following image lists are created here, not in their corresponding classes, 
# as hundreds of DUST and EXPLOSION objects can be generated per game.
hotspot_images = {
    enums.TNT: pygame.image.load('images/sprites/hotspot0.png').convert_alpha(),
    enums.KEY: pygame.image.load('images/sprites/hotspot1.png').convert_alpha(),
    enums.AMMO: pygame.image.load('images/sprites/hotspot2.png').convert_alpha(),
    enums.OXYGEN: pygame.image.load('images/sprites/hotspot3.png').convert_alpha()
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
sfx_open_door = pygame.mixer.Sound('sounds/fx/sfx_open_door.wav')
sfx_locked_door = pygame.mixer.Sound('sounds/fx/sfx_locked_door.wav')
sfx_enemy_down = {
    enums.INFECTED: pygame.mixer.Sound('sounds/fx/sfx_exp_infected.wav'),
    enums.PELUSOID: pygame.mixer.Sound('sounds/fx/sfx_exp_pelusoid.wav'),
    enums.AVIRUS: pygame.mixer.Sound('sounds/fx/sfx_exp_avirus.wav'),
    enums.FANTY: pygame.mixer.Sound('sounds/fx/sfx_exp_fanty.wav')
}
sfx_hotspot = {
    enums.TNT: pygame.mixer.Sound('sounds/fx/sfx_TNT.wav'),
    enums.KEY: pygame.mixer.Sound('sounds/fx/sfx_key.wav'),
    enums.AMMO: pygame.mixer.Sound('sounds/fx/sfx_ammo.wav'),
    enums.OXYGEN: pygame.mixer.Sound('sounds/fx/sfx_oxygen.wav')
}

# shows an intro
intro = Intro(game)
intro.play()

# create the Floating texts
floating_text = FloatingText(game.srf_map)

# create the Scoreboard object
scoreboard = Scoreboard(game.srf_sboard, game.fonts, hotspot_images)

# create the Map object
map = Map(game)

 # creates a playlist with the 12 available tracks
jukebox = Jukebox('sounds/music/', 'mus_ingame_', 12, constants.MUSIC_LOOP_LIST)

# creates the initial Menu object
menu = Menu(game)

# small, opaque font for the FPS counter
test_font = Font('images/fonts/small_font.png', constants.PALETTE['GREEN'], False) 

#===============================================================================
# Main loop
#===============================================================================

while True:    
    if game.status == enums.OVER: # game not running
        pygame.mouse.set_visible(True)
        menu.show()
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
        player = Player(all_sprites_group, dust_group, bullet_group, map, scoreboard, config)
        # new unordered playlist with the 12 available music tracks
        pygame.mixer.music.stop()
        jukebox.shuffle()
        # reset variables
        for hotspot in constants.HOTSPOT_DATA: hotspot[3] = True # all visible hotspots
        for gate in constants.GATE_DATA.values(): gate[2] = True # all visible doors
        game.status = enums.RUNNING
        map.number = 0
        map.last = -1
        map.scroll = enums.RIGHT
        scoreboard.game_percent = 0
        floating_text.y = 0
        pygame.mouse.set_visible(False)
    else: # game running
        # event management
        for event in pygame.event.get():
            # exit when click on the X in the window
            if event.type == pygame.QUIT:
                support.exit()
            if event.type == pygame.KEYDOWN:
                # exit by pressing ESC key
                if event.key == pygame.K_ESCAPE:
                    game.pause_music()
                    if game.confirm_exit():
                        game.status = enums.OVER # go to the main menu
                    else: game.restore_music()
                # pause main loop
                if event.key == config.pause_key:
                    game.pause_music()
                    game.pause()
                    game.restore_music()                                
                # mute music
                if event.key == config.mute_key :
                    if game.music_status == enums.MUTED:
                        game.music_status = enums.UNMUTED
                        pygame.mixer.music.play()
                    else:
                        game.music_status = enums.MUTED
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

        if game.status == enums.RUNNING: # (not paused)
            # update sprites
            all_sprites_group.update()

            # collision between all entities
            collision_check()

            # game over?
            if player.lives == 0 or player.oxygen < 0:
                game.status = enums.OVER
                game.over()
                continue
            
            # change the frame of the animated tiles
            map.animate_tiles()

            # draws the map free of sprites to clean it up
            game.srf_map.blit(game.srf_map_bk, (0,0))
            all_sprites_group.draw(game.srf_map)

            # draws the floating texts, only if needed
            floating_text.update()

            # updates the scoreboard, only if needed
            scoreboard.update(player)

            # check map change using player's coordinates
            # if the player leaves, the map number changes
            map.check_change(player)

            # next track in the playlist if the music has been stopped
            if game.music_status == enums.UNMUTED:
                jukebox.update()

            # display FPS (using the clock)
            if config.show_fps:
                test_font.render(str(int(clock.get_fps())), game.srf_map, (233, 154))
            
    game.update_screen()
