
# ==============================================================================
# .::Menu class::.
# Initial menu and additional information displayed on sliding pages
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

import pygame
import constants
import enums

from font import Font
from marqueetext import MarqueeText
from shot import Shot


class Menu():
    def __init__(self, game):
        self.game = game        
        self.srf_menu = game.srf_menu   

        # page 1: menu options
        self.srf_page1 = pygame.Surface(constants.MENU_UNSCALED_SIZE)
        self.srf_page1.set_colorkey(constants.PALETTE['BLACK']) # transparent background
        # page 2: enemy/hotspot information
        self.srf_page2 = pygame.Surface(constants.MENU_UNSCALED_SIZE)
        self.srf_page2.set_colorkey(constants.PALETTE['BLACK'])
        # page 3: control information
        self.srf_page3 = pygame.Surface(constants.MENU_UNSCALED_SIZE)
        self.srf_page3.set_colorkey(constants.PALETTE['BLACK'])
        # page 4: high scores
        self.srf_page4 = pygame.Surface(constants.MENU_UNSCALED_SIZE)
        self.srf_page4.set_colorkey(constants.PALETTE['BLACK'])
        # page 5: options
        self.srf_page5 = pygame.Surface(constants.MENU_UNSCALED_SIZE)
        self.srf_page5.set_colorkey(constants.PALETTE['BLACK'])

        # player (cursor)
        self.img_player = pygame.image.load('images/sprites/player0.png').convert_alpha()
        self.img_bullet = pygame.image.load('images/sprites/bullet.png').convert_alpha()
        # background
        self.img_menu = pygame.image.load('images/assets/menu_back.png').convert()
        # controls
        self.img_classic = pygame.image.load('images/assets/classic.png').convert_alpha()
        self.img_gamer = pygame.image.load('images/assets/gamer.png').convert_alpha()
        self.img_retro = pygame.image.load('images/assets/retro.png').convert_alpha()
        self.img_common = pygame.image.load('images/assets/common.png').convert_alpha()
        # sounds
        self.sfx_switchoff = pygame.mixer.Sound('sounds/fx/sfx_switchoff.wav')
        self.sfx_menu_click = pygame.mixer.Sound('sounds/fx/sfx_menu_click.wav')
        self.sfx_menu_select = pygame.mixer.Sound('sounds/fx/sfx_menu_select.wav')
        # generate menu pages
        self.page_1()
        self.page_2()
        self.page_3()
        self.page_4()
        self.page_5()
        
    # draws a text with its shadow
    def shaded_text(self, font_BG, font_FG, text, surface, x, y, offset):           
        font_BG.render(text, surface, (x, y))  # shadow
        font_FG.render(text, surface, (x-offset, y-offset))

    def page_1(self): # menu options
        # menu options      
        x = 80
        y = 67
        fb = self.game.fonts[enums.L_B_SAND] # brown font for the background
        ff = self.game.fonts[enums.L_F_SAND] # sand font for the foreground
        self.shaded_text(fb, ff, 'Start New Game', self.srf_page1, x, y, 1)
        self.shaded_text(fb, ff, 'Load Checkpoint', self.srf_page1, x, y+20, 1)
        self.shaded_text(fb, ff, 'Options', self.srf_page1, x, y+40, 1)
        self.shaded_text(fb, ff, 'Exit', self.srf_page1, x, y+60, 1)
        self.shaded_text(self.game.fonts[enums.S_B_GREEN], self.game.fonts[enums.S_F_GREEN], 
                         'Use arrow keys and SPACE/ENTER to select', self.srf_page1, x-35, y+90, 1)

    def page_2(self): # enemies/hotspot info
        img_enemies = {
            enums.INFECTED: pygame.image.load('images/sprites/infected0.png').convert(),
            enums.AVIRUS: pygame.image.load('images/sprites/avirus0.png').convert(),
            enums.PELUSOID: pygame.image.load('images/sprites/pelusoid0.png').convert(),
            enums.FANTY: pygame.image.load('images/sprites/fanty0.png').convert()}
        img_hotspot = {
            enums.TNT: pygame.image.load('images/sprites/hotspot0.png').convert(),
            enums.KEY: pygame.image.load('images/sprites/hotspot1.png').convert(),
            enums.AMMO: pygame.image.load('images/sprites/hotspot2.png').convert(),
            enums.OXYGEN: pygame.image.load('images/sprites/hotspot3.png').convert()}
        x = 20
        y = 65
        self.shaded_text(self.game.fonts[enums.L_B_SAND], self.game.fonts[enums.L_F_SAND], 
                         'The Baddies       The Hotspots', self.srf_page2, x, y, 1)
        x = 40
        y = 95
        fb = self.game.fonts[enums.S_B_WHITE] # small gray font for the background
        ff = self.game.fonts[enums.S_F_WHITE] # small white font for the foreground
        self.shaded_text(fb, ff, 'Infected (+25)', self.srf_page2, x, y, 1)
        self.shaded_text(fb, ff, 'Arachnovirus (+50)', self.srf_page2, x, y+20, 1)
        self.shaded_text(fb, ff, 'Pelusoid (+75)', self.srf_page2, x, y+40, 1)   
        self.shaded_text(fb, ff, 'Pelusoid Fanty (+100)', self.srf_page2, x, y+60, 1)
        x = 163
        self.shaded_text(fb, ff, 'Explosives', self.srf_page2, x, y, 1)
        self.shaded_text(fb, ff, 'Ammunition', self.srf_page2, x, y+20, 1)
        self.shaded_text(fb, ff, 'Key Card', self.srf_page2, x, y+40, 1) 
        self.shaded_text(fb, ff, 'Oxygen bottle', self.srf_page2, x, y+60, 1)
        # images of enemies
        x = 17
        y = 89
        self.srf_page2.blit(img_enemies[enums.INFECTED], (x, y))
        self.srf_page2.blit(img_enemies[enums.AVIRUS], (x, y+20))
        self.srf_page2.blit(img_enemies[enums.PELUSOID], (x, y+40))
        self.srf_page2.blit(img_enemies[enums.FANTY], (x, y+60))
        # images of the hotspots
        x = 139
        self.srf_page2.blit(img_hotspot[enums.TNT], (x, y))
        self.srf_page2.blit(img_hotspot[enums.AMMO], (x, y+20))
        self.srf_page2.blit(img_hotspot[enums.KEY], (x, y+40))
        self.srf_page2.blit(img_hotspot[enums.OXYGEN], (x, y+60))

    def page_3(self): # control info
        x = 95
        y = 57
        self.shaded_text(self.game.fonts[enums.L_B_SAND], self.game.fonts[enums.L_F_SAND], 
                         'Controls', self.srf_page3, x, y, 1)
        x = 35
        y = 82
        fb = self.game.fonts[enums.S_B_WHITE] # small gray font for the background
        ff = self.game.fonts[enums.S_F_WHITE] # small white font for the foreground
        self.srf_page3.blit(self.img_classic, (x, y)) # image of the classic layout
        self.shaded_text(fb, ff, 'Classic', self.srf_page3, x+10, y+38, 1)
        x = 100
        self.srf_page3.blit(self.img_gamer, (x, y)) # image of the gamer layout
        self.shaded_text(fb, ff, 'Gamer', self.srf_page3, x+12, y+38, 1)
        x = 165
        self.srf_page3.blit(self.img_retro, (x, y)) # image of the retro layout
        self.shaded_text(fb, ff, 'Retro', self.srf_page3, x+18, y+38, 1) 
        x = 110
        y = 140
        self.srf_page3.blit(self.img_common, (x, y)) # image of the common keys
        self.shaded_text(fb, ff, 'Common keys', self.srf_page3, x-52, y+15, 1)

    def page_4(self): # high scores
        x = 90
        y = 60
        self.shaded_text(self.game.fonts[enums.L_B_SAND], self.game.fonts[enums.L_F_SAND],
                         'High Scores', self.srf_page4, x, y, 1)
        x = 50
        y = 90
        # names
        fb = self.game.fonts[enums.S_B_WHITE] # small gray font for the background
        ff = self.game.fonts[enums.S_F_WHITE] # small white font for the foreground
        fb2 = self.game.fonts[enums.S_B_GREEN] # small dark green font for the background
        ff2 = self.game.fonts[enums.S_F_GREEN] # small green font for the foreground
        self.shaded_text(fb, ff, 'Lukas', self.srf_page4, x, y, 1)
        self.shaded_text(fb2, ff2, 'Dany', self.srf_page4, x, y+10, 1)
        self.shaded_text(fb, ff, 'Marina', self.srf_page4, x, y+20, 1)   
        self.shaded_text(fb2, ff2, 'Alvaro', self.srf_page4, x, y+30, 1)
        self.shaded_text(fb, ff, 'Julita', self.srf_page4, x, y+40, 1)
        self.shaded_text(fb2, ff2, 'Luna_314', self.srf_page4, x, y+50, 1)
        self.shaded_text(fb, ff, 'Irenita', self.srf_page4, x, y+60, 1)
        self.shaded_text(fb2, ff2, 'salvaKantero', self.srf_page4, x, y+70, 1)
        # dates and scores
        x = 110
        self.shaded_text(fb, ff, '14/02/2023' + '    00195325', self.srf_page4, x, y, 1)
        self.shaded_text(fb2, ff2, '14/02/2023' + '    00195290', self.srf_page4, x, y+10, 1)
        self.shaded_text(fb, ff, '11/02/2023' + '    00152645', self.srf_page4, x, y+20, 1)   
        self.shaded_text(fb2, ff2, '28/01/2023' + '    00147755', self.srf_page4, x, y+30, 1)
        self.shaded_text(fb, ff, '30/12/2022' + '    00097430', self.srf_page4, x, y+40, 1)
        self.shaded_text(fb2, ff2, '21/01/2023' + '    00042940', self.srf_page4, x, y+50, 1)
        self.shaded_text(fb, ff, '01/02/2023' + '    00008255', self.srf_page4, x, y+60, 1)
        self.shaded_text(fb2, ff2, '30/12/2022' + '    00001985', self.srf_page4, x, y+70, 1)

    def page_5(self): # options
        # menu options      
        x = 58
        y = 55
        fb = self.game.fonts[enums.L_B_SAND] # brown font for the background
        ff = self.game.fonts[enums.L_F_SAND] # sand font for the foreground
        fb2 = self.game.fonts[enums.L_B_WHITE] # white font for the background
        ff2 = self.game.fonts[enums.L_F_WHITE] # white font for the foreground
        # full screen
        if self.game.config.full_screen == 0: value = 'OFF'
        else: value = 'ON'
        self.shaded_text(fb, ff, 'Full Screen:', self.srf_page5, x, y, 1)
        self.shaded_text(fb2, ff2, value, self.srf_page5, x+116, y, 1)
        # scanlines filter
        if self.game.config.scanlines_type == 0: value = 'OFF' 
        elif self.game.config.scanlines_type == 1: value = 'FAST'
        else: value = 'HQ'
        self.shaded_text(fb, ff, 'Scanlines:', self.srf_page5, x, y+20, 1)
        self.shaded_text(fb2, ff2, value, self.srf_page5, x+116, y+20, 1)
        # map transition
        if self.game.config.map_transition == 0: value = 'OFF' 
        else: value = 'ON'
        self.shaded_text(fb, ff, 'Map Transition:', self.srf_page5, x, y+40, 1)
        self.shaded_text(fb2, ff2, value, self.srf_page5, x+116, y+40, 1)
        # control keys
        if self.game.config.control == 0: value = 'Classic' 
        elif self.game.config.control == 1: value = 'Gamer'
        elif self.game.config.control == 2: value = 'Retro'
        else: value = 'GamePad'
        self.shaded_text(fb, ff, 'Control Keys:', self.srf_page5, x, y+60, 1)
        self.shaded_text(fb2, ff2, value, self.srf_page5, x+116, y+60, 1)
        # exit
        self.shaded_text(fb, ff, 'Exit Options', self.srf_page5, x, y+80, 1)
        
        self.shaded_text(self.game.fonts[enums.S_B_GREEN], self.game.fonts[enums.S_F_GREEN], 
                         'Use arrow keys and SPACE/ENTER to select', self.srf_page5, x-10, y+110, 1)

    def show(self):
        # help
        marquee_help = MarqueeText(
            self.srf_menu, Font('images/fonts/small_font.png', constants.PALETTE['YELLOW'], True),
            self.srf_menu.get_height() - 16, .7, constants.HELP, 1700)
        # credits       
        marquee_credits = MarqueeText(
            self.srf_menu, Font('images/fonts/small_font.png', constants.PALETTE['ORANGE'], True),
            self.srf_menu.get_height() - 8, .5, constants.CREDITS, 2900)
        
        self.sfx_switchoff.play()    
        #pygame.mixer.music.load('sounds/music/mus_menu.ogg')
        #pygame.mixer.music.play()
    
        selected_option = enums.START # option where the cursor is located
        confirmed_option = False # 'True' when a selected option is confirmed
        menu_page = 1 # page displayed (1 to 4 automatically. 5 = config page)
        page_timer = 0 # number of loops the page remains on screen (up to 500)
        x = constants.MENU_UNSCALED_SIZE[0] # for sideways scrolling of pages

        # main menu loop
        pygame.event.clear(pygame.KEYDOWN)
        while True:
            page_timer += 1

            # draws the background image
            self.srf_menu.blit(self.img_menu, (0,0))

            # draws the texts of the marquee in their new position
            marquee_help.update()
            marquee_credits.update()  

            # transition of menu pages
            if page_timer >= 500: # time exceeded?
                menu_page += 1 # change the page
                if menu_page > 4: menu_page = 1 # reset
                page_timer = 0 # and reset the timer
                x = constants.MENU_UNSCALED_SIZE[0] # again in the right margin
                selected_option = 0
            elif page_timer >= 450: # time almost exceeded?
                x -= 8 # scrolls the page to the left (is disappearing)    
            elif x > 0: # as long as the page does not reach the left margin
                x -= 8 # scrolls the page to the left (is appearing)

            # draws the main menu
            if menu_page == 1: self.srf_menu.blit(self.srf_page1, (x, 0))
            # draws enemy and hotspot information        
            elif menu_page == 2: self.srf_menu.blit(self.srf_page2, (x, 0))
            # draws the information of the control keys
            elif menu_page == 3: self.srf_menu.blit(self.srf_page3, (x, 0))
            # draw the score table
            elif menu_page == 4: self.srf_menu.blit(self.srf_page4, (x, 0))     
            # draw the options page
            else: self.srf_menu.blit(self.srf_page5, (x, 0))         

            # keyboard management
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # X button in the main window
                    self.game.exit()
                if event.type == pygame.KEYDOWN: # a key has been pressed         
                    if event.key == pygame.K_ESCAPE: # exit by pressing ESC key
                        self.game.exit()
                    # the selected option is accepted by pressing ENTER or SPACE
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        # creates a shot
                        if menu_page == 1: 
                            shot_x = 58
                            shot_y = 65+(20*selected_option)
                        elif menu_page == 5:
                            shot_x = 46
                            shot_y = -28+(20*selected_option)
                        shot = Shot(pygame.Rect(shot_x, shot_y, constants.TILE_SIZE, constants.TILE_SIZE), 1, self.img_bullet)
                        self.game.shot_group.add(shot)
                        self.sfx_menu_select.play()
                        confirmed_option = True
                    # Main menu and there is no shot in progress?
                    elif menu_page == 1 and not confirmed_option:
                        page_timer = 0 # reset the timer again
                        # the cursor down has been pressed
                        if event.key == pygame.K_DOWN and selected_option < enums.EXIT:
                            selected_option += 1
                            self.sfx_menu_click.play()
                        # the cursor up has been pressed
                        elif event.key == pygame.K_UP and selected_option > enums.START:
                            selected_option -= 1
                            self.sfx_menu_click.play()
                    # Options menu and there is no shot in progress?
                    elif menu_page == 5 and not confirmed_option:
                        page_timer = 0 # reset the timer again
                        # the cursor down has been pressed
                        if event.key == pygame.K_DOWN and selected_option < enums.EXIT2:
                            selected_option += 1
                            self.sfx_menu_click.play()
                        # the cursor up has been pressed
                        elif event.key == pygame.K_UP and selected_option > enums.FULLSCREEN:
                            selected_option -= 1
                            self.sfx_menu_click.play()
                    # pressing any key returns to the main menu
                    else:
                        menu_page = 1
                        page_timer = 0
            
            # main menu or options active on screen?
            if menu_page == 1 or menu_page == 5 and x == 0:
                # shows the player next to the selected option
                if menu_page == 1:
                    self.srf_menu.blit(self.img_player, (55, 64 + (20*selected_option)))
                else:
                    self.srf_menu.blit(self.img_player, (33, -28 + (20*selected_option)))
                # draw the shot (if it exists)
                self.game.shot_group.update()
                self.game.shot_group.draw(self.srf_menu)
                # an option was confirmed and the shot was completed?
                if confirmed_option and self.game.shot_group.sprite == None:
                    if selected_option == enums.START:
                        return
                    elif selected_option == enums.LOAD:
                        pass
                    elif selected_option == enums.OPTIONS:
                        x = constants.MENU_UNSCALED_SIZE[0]
                        confirmed_option = False
                        selected_option = 4
                        menu_page = 5
                        page_timer = 0
                    elif selected_option == enums.EXIT:
                        self.game.exit()
                    elif selected_option == enums.FULLSCREEN:
                        self.game.config.full_screen += 1
                        if self.game.config.full_screen > 1: # reset
                            self.game.config.full_screen = 0
                    elif selected_option == enums.SCANLINES:
                        self.game.config.scanlines_type += 1
                        if self.game.config.scanlines_type > 2: # reset
                            self.game.config.scanlines_type = 0
                    elif selected_option == enums.MAP_TRANSITION:
                        self.game.config.map_transition += 1
                        if self.game.config.map_transition > 1: # reset
                            self.game.config.map_transition = 0
                    elif selected_option == enums.CONTROL:
                        self.game.config.control += 1
                        if self.game.config.control > 3: # reset
                            self.game.config.control = 0
                    elif selected_option == enums.EXIT2:
                        x = constants.MENU_UNSCALED_SIZE[0]
                        confirmed_option = False
                        selected_option = 0
                        menu_page = 1
                        page_timer = 0

            self.game.update_screen()
