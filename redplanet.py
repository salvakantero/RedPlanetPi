
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

# pygame library functions
import pygame
from pygame.locals import *
from pygame.constants import *

# own code
import constants, enums

# own classes
from config import Configuration
from game import Game
from map import Map
from scoreboard import Scoreboard
from font import Font
from player import Player
from checkpoint import Checkpoint


#===============================================================================
# Initialisation and creation of the main objects
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
# creates a checkpoint object to load/record game
checkpoint = Checkpoint()
# game object, container for common variables and functions
game = Game(clock, config, checkpoint)
# create the Scoreboard object
scoreboard = Scoreboard(game)
# creates the Map object
map = Map(game)
# creates the player
player = Player(game, map, scoreboard)

# small, opaque font for debug and test
test_font = Font('images/fonts/small_font.png', constants.PALETTE['YELLOW'], False) 

# shows an intro
game.show_intro()

#===============================================================================
# Main loop
#===============================================================================

while True:    
    if game.status == enums.OVER: # game not running
        # creates and displays the initial menu
        game.show_menu()         
        # new unordered playlist with the 12 available music tracks
        pygame.mixer.music.stop()
        game.jukebox.shuffle()
        # reset variables
        map.last = -1
        game.status = enums.RUNNING
        game.floating_text.y = 0
        map.scroll = enums.RIGHT
        if game.new:
            player.reset()
            for hotspot in constants.HOTSPOT_DATA: hotspot[3] = True # all visible hotspots
            for gate in constants.GATE_DATA.values(): gate[2] = True # all visible doors                        
            map.number = 0                        
            scoreboard.game_percent = 0
        else: # load the last checkpoint
            checkpoint.load()
            d = checkpoint.data
            map.number = d['map_number']
            scoreboard.game_percent = d['game_percent']
            player.lives = d['player_lives']
            player.ammo = d['player_ammo']
            player.keys = d['player_keys']
            player.TNT = d['player_TNT']
            player.oxygen = d['player_oxygen']
            player.stacked_TNT = d['player_stacked_TNT']
            player.facing_right = d['player_facing_right']
            player.rect = d['player_rect']
            player.score = d['player_score']
    else: # game running
        # event management
        for event in pygame.event.get():
            # exit when click on the X in the window
            if event.type == pygame.QUIT:
                game.exit()
            if event.type == pygame.KEYDOWN:
                # exit by pressing ESC key
                if event.key == pygame.K_ESCAPE:
                    game.pause_music()
                    if game.confirm_exit():
                        game.status = enums.OVER # go to the main menu
                    else: game.restore_music()                            
                # mute music
                if event.key == config.mute_key :
                    # ====================================================================
                    # save game
                    checkpoint.data = {
                        'map_number' : map.number,
                        'game_percent' : scoreboard.game_percent,
                        'player_lives' : player.lives,
                        'player_ammo' : player.ammo,
                        'player_keys' : player.keys,
                        'player_TNT' : player.TNT,
                        'player_oxygen' : player.oxygen,
                        'player_stacked_TNT' : player.stacked_TNT,
                        'player_facing_right' : player.facing_right,
                        'player_rect' : player.rect,
                        'player_score' : player.score
                    }
                    checkpoint.save()
                    # ====================================================================

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

        # change the map if necessary
        if map.number != map.last:
            map.change(player, scoreboard)

        # update sprites (player, enemies, hotspots, explosions, etc...)
        game.all_sprites_group.update()

        # collision between all entities that may collide
        game.check_collisions(player, scoreboard, map.number, map.tilemap_rect_list)

        # game over?
        if player.lives == 0 or player.oxygen < 0:                
            game.over()
            game.status = enums.OVER
            continue
        
        # change the frame of the animated tiles
        map.animate_tiles()

        # draws the map free of sprites to clean it up
        game.srf_map.blit(game.srf_map_bk, (0,0))
        # draws the sprites in their new positions
        game.all_sprites_group.draw(game.srf_map)

        # updates the floating text, only if needed (y>0)
        game.floating_text.update()

        # updates the scoreboard, only if needed (needs_updating = True)
        scoreboard.update(player)

        # next track in the playlist if the music has been stopped
        if game.music_status == enums.UNMUTED:
            game.jukebox.update()
            
        # check map change using player's coordinates
        # if the player leaves, the map number changes
        map.check_change(player)
            
        # TEST ZONE
        test_font.render(str(int(clock.get_fps())), game.srf_map, (233, 154))

    game.update_screen()
