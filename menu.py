
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
        # player (cursor)
        self.img_player = pygame.image.load('images/sprites/player0.png').convert_alpha()
        self.img_bullet = pygame.image.load('images/sprites/bullet.png').convert_alpha()
        # background
        self.img_menu = pygame.image.load('images/assets/menu_back.png').convert()
        # controls
        self.img_classic = pygame.image.load('images/assets/classic.png').convert_alpha()
        self.img_gamer = pygame.image.load('images/assets/gamer.png').convert_alpha()
        self.img_retro = pygame.image.load('images/assets/retro.png').convert_alpha()
        self.img_joypad = pygame.image.load('images/assets/joypad.png').convert_alpha()
        self.img_common = pygame.image.load('images/assets/common.png').convert_alpha()
        # sounds
        self.sfx_switchoff = pygame.mixer.Sound('sounds/fx/sfx_switchoff.wav')
        self.sfx_menu_click = pygame.mixer.Sound('sounds/fx/sfx_menu_click.wav')
        self.sfx_menu_select = pygame.mixer.Sound('sounds/fx/sfx_menu_select.wav')

        # page 0: menu options
        # page 1: hotspot information
        # page 2: enemy/gift information
        # page 3: control information
        # page 4: high scores
        # page 5: options
        self.menu_pages = []
        for i in range(0, 6):
            surface = pygame.Surface(constants.MENU_UNSCALED_SIZE)
            surface.set_colorkey(constants.PALETTE['BLACK'])
            self.menu_pages.append(surface)   
        self.page_0()
        self.page_1()
        self.page_2()
        self.page_3()
        self.page_4()
        
    # draws a text with its shadow
    def shaded_text(self, font_BG, font_FG, text, surface, x, y, offset):           
        font_BG.render(text, surface, (x, y))  # shadow
        font_FG.render(text, surface, (x-offset, y-offset))

    def page_0(self): # menu options    
        options = ['Start New Game', 'Continue Game', 'Options', 'Exit']
        x, y = 80, 67
        for i, option in enumerate(options):
            self.shaded_text(self.game.fonts[enums.L_B_SAND], self.game.fonts[enums.L_F_SAND], 
                             option, self.menu_pages[0], x, y + i*20, 1)            
        self.shaded_text(self.game.fonts[enums.S_B_GREEN], self.game.fonts[enums.S_F_GREEN], 
                        'Use arrow keys and SPACE/ENTER to select', self.menu_pages[0], x-35, y+90, 1)

    def page_1(self): # hotspot info
        fb, ff = self.game.fonts[enums.S_B_WHITE], self.game.fonts[enums.S_F_WHITE]
        left_items = [
            ('Explosives', 50, enums.TNT),
            ('Ammunition', 75, enums.AMMO),
            ('Key Card', 125, enums.KEY)]
        right_items = [
            ('Oxygen bottle', 100, enums.OXYGEN),
            ('Closed door', 0, enums.GATE),
            ('Checkpoint', 0, enums.CHECKPOINT)]

        self.shaded_text(self.game.fonts[enums.L_B_SAND], self.game.fonts[enums.L_F_SAND], 
                         'The Hotspots', self.menu_pages[1], 70, 65, 1)
        
        for i, (name, score, img_index) in enumerate(left_items):
            self.menu_pages[1].blit(self.game.hotspot_images[img_index], (42, 89+i*25))
            self.shaded_text(fb, ff, f"{name} (+{score})", self.menu_pages[1], 65, 100+i*25, 1)        
        for i, (name, score, img_index) in enumerate(right_items):
            self.menu_pages[1].blit(self.game.hotspot_images[img_index], (132, 89+i*25))
            self.shaded_text(fb, ff, f"{name} (+{score})", self.menu_pages[1], 155, 100+i*25, 1)

    def page_2(self): # enemies/gifts info
        x, y = 50, 95
        fb, ff = self.game.fonts[enums.S_B_WHITE], self.game.fonts[enums.S_F_WHITE]
        enemies = [
            ('Infected', 25, enums.INFECTED), 
            ('Arachnovirus', 50, enums.AVIRUS), 
            ('Pelusoid', 75, enums.PELUSOID), 
            ('Pelusoid Fanty', 100, enums.FANTY)]
        gifts = [
            ('Burguer', 500, enums.BURGUER), 
            ('Cake', 350, enums.CAKE), 
            ('Donut', 200, enums.DONUT)]

        self.shaded_text(self.game.fonts[enums.L_B_SAND], self.game.fonts[enums.L_F_SAND], 
                    'The Baddies     The Gifts', self.menu_pages[2], 30, 65, 1)
        for i, (name, score, img_index) in enumerate(enemies):
            self.menu_pages[2].blit(self.game.enemy_images[img_index][0], (27, 89+i*20))
            self.shaded_text(fb, ff, f"{name} (+{score})", self.menu_pages[2], x, y+i*20, 1)        
        for i, (name, score, img_index) in enumerate(gifts):
            self.menu_pages[2].blit(self.game.hotspot_images[img_index], (139, 89+i*20))
            self.shaded_text(fb, ff, f"{name} (+{score})", self.menu_pages[2], 162, y+i*20, 1)

    def page_3(self): # control info
        fb, ff = self.game.fonts[enums.S_B_WHITE], self.game.fonts[enums.S_F_WHITE]
        layouts = [
            (self.img_classic, (30, 82), 'Classic', (39, 120)),
            (self.img_gamer, (95, 82), 'Gamer', (104, 120)),
            (self.img_retro, (160, 82), 'Retro', (169, 120)),
            (self.img_joypad, (53, 138), 'Joypad', (23, 153)),
            (self.img_common, (118, 138), 'Common keys', (180, 153))]
        
        self.shaded_text(self.game.fonts[enums.L_B_SAND], self.game.fonts[enums.L_F_SAND], 'Controls', self.menu_pages[3], 90, 57, 1)        
        for i, (image, img_pos, text, text_pos) in enumerate(layouts):
            self.menu_pages[3].blit(image, img_pos)
            self.shaded_text(fb, ff, text, self.menu_pages[3], text_pos[0], text_pos[1], 1)

    def page_4(self): # high scores
        # header
        x, y = 90, 62
        self.shaded_text(self.game.fonts[enums.L_B_SAND], self.game.fonts[enums.L_F_SAND],
                         'High Scores', self.menu_pages[4], x, y, 1)                
        y = 90
        for i in range(8):
            if i % 2 == 0: # index even
                fb = self.game.fonts[enums.S_B_WHITE] # small gray font for the background
                ff = self.game.fonts[enums.S_F_WHITE] # small white font for the foreground
            else: # index odd 
                fb = self.game.fonts[enums.S_B_GREEN] # small dark green font for the background
                ff = self.game.fonts[enums.S_F_GREEN] # small green font for the foreground
            # names
            self.shaded_text(fb, ff, self.game.high_scores[i][0], self.menu_pages[4], 55, y, 1)
            # dates and scores
            self.shaded_text(fb, ff, self.game.high_scores[i][1] + '    ' + 
                str(self.game.high_scores[i][2]).rjust(6, '0'), self.menu_pages[4], 120, y, 1)
            y += 10

    def page_5(self): # options
        # menu options      
        x, y = 60, 55
        fb = self.game.fonts[enums.L_B_SAND] # brown font for the background
        ff = self.game.fonts[enums.L_F_SAND] # sand font for the foreground
        fb2 = self.game.fonts[enums.L_B_WHITE] # white font for the background
        ff2 = self.game.fonts[enums.L_F_WHITE] # white font for the foreground
        # full screen
        if self.game.config.data['full_screen']: value = 'ON'
        else: value = 'OFF'
        self.shaded_text(fb, ff, 'Full Screen:', self.menu_pages[5], x, y, 1)
        self.shaded_text(fb2, ff2, value, self.menu_pages[5], x+115, y, 1)
        # scanlines filter
        if self.game.config.data['scanlines'] == 0: value = 'OFF' 
        elif self.game.config.data['scanlines'] == 1: value = 'FAST'
        else: value = 'HQ'
        self.shaded_text(fb, ff, 'Scanlines:', self.menu_pages[5], x, y+20, 1)
        self.shaded_text(fb2, ff2, value, self.menu_pages[5], x+115, y+20, 1)
        # map transition
        if self.game.config.data['map_transition']: value = 'ON' 
        else: value = 'OFF'
        self.shaded_text(fb, ff, 'Map Transition:', self.menu_pages[5], x, y+40, 1)
        self.shaded_text(fb2, ff2, value, self.menu_pages[5], x+115, y+40, 1)
        # control keys
        if self.game.config.data['control'] == enums.CLASSIC: value = 'CLASSIC' 
        elif self.game.config.data['control'] == enums.GAMER: value = 'GAMER'
        elif self.game.config.data['control'] == enums.RETRO: value = 'RETRO'
        else: value = 'JOYPAD'
        self.shaded_text(fb, ff, 'Control Keys:', self.menu_pages[5], x, y+60, 1)
        self.shaded_text(fb2, ff2, value, self.menu_pages[5], x+115, y+60, 1)
        # exit
        self.shaded_text(fb, ff, 'Exit Options', self.menu_pages[5], x, y+80, 1)
        
        self.shaded_text(self.game.fonts[enums.S_B_GREEN], self.game.fonts[enums.S_F_GREEN], 
                         'Use arrow keys and SPACE/ENTER to select', self.menu_pages[5], x-10, y+110, 1)

    def show(self):
        # help text on the marquee
        marquee_help = MarqueeText(
            self.srf_menu, Font('images/fonts/small_font.png', constants.PALETTE['YELLOW'], True),
            self.srf_menu.get_height() - 16, .7, constants.HELP, 1700)
        # credit text on the marquee      
        marquee_credits = MarqueeText(
            self.srf_menu, Font('images/fonts/small_font.png', constants.PALETTE['ORANGE'], True),
            self.srf_menu.get_height() - 8, .5, constants.CREDITS, 3200)
                
        self.sfx_switchoff.play() # cool sound effect... who turned off the light?
        # main theme song
        #pygame.mixer.music.load('sounds/music/mus_menu.ogg')
        #pygame.mixer.music.play()
    
        # some local variables are initialised
        selected_option = enums.START # option where the cursor is located
        confirmed_option = False # 'True' when a selected option is confirmed
        menu_page = 0 # page displayed (0 to 4 automatically. 5 = config page)
        page_timer = 0 # number of loops the page remains on screen (up to 500)
        x = constants.MENU_UNSCALED_SIZE[0] # for sideways scrolling of pages

        # ============================= main menu loop =========================
        pygame.event.clear(pygame.KEYDOWN)
        while True:
            page_timer += 1

            # draws the background image
            self.srf_menu.blit(self.img_menu, (0,0))

            # draws the texts of the marquee in their new position
            marquee_help.update()
            marquee_credits.update()  

            # ========== transition of menu pages from right to left ===========
            if page_timer >= 500: # time exceeded?
                menu_page += 1 # change the page
                if menu_page > 4: menu_page = 0 # reset
                page_timer = 0 # and reset the timer
                x = constants.MENU_UNSCALED_SIZE[0] # again in the right margin
                selected_option = enums.START
            elif page_timer >= 450: # time almost exceeded?
                x -= 8 # scrolls the page to the left (is disappearing)    
            elif x > 0: # as long as the page does not reach the left margin
                x -= 8 # scrolls the page to the left (is appearing)           
             # draw one of the 6 menu pages
            for i in range(0, 6):
                if menu_page == i:
                    self.srf_menu.blit(self.menu_pages[i], (x, 0))
                    break

            # ====================== keyboard management =======================
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # X button in the main window
                    self.game.exit()
                if event.type == pygame.KEYDOWN and x == 0: # a key has been pressed         
                    # active pages
                    if menu_page == 0 or menu_page == 5:
                        if event.key == pygame.K_ESCAPE: 
                            if menu_page == 0: self.game.exit() # exits the application completely
                            else: # on page 5, return to page 0
                                menu_page = 0
                                selected_option = 0
                                break
                        # the selected option is accepted by pressing ENTER or SPACE
                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            # creates a shot.
                            # the starting position depends on the current page and the selected option
                            if menu_page == 0:
                                shot_x, shot_y = 58, 65+(20*selected_option)
                            elif menu_page == 5:
                                shot_x, shot_y = 38, -28+(20*selected_option)
                            shot = Shot(pygame.Rect(shot_x, shot_y, constants.TILE_SIZE, constants.TILE_SIZE), 1, self.img_bullet, 8)
                            self.game.shot_group.add(shot)
                            self.sfx_menu_select.play()
                            confirmed_option = True

                        # Main menu and there is no shot in progress?
                        elif menu_page == 0 and not confirmed_option:                            
                            # the cursor down has been pressed
                            if event.key == pygame.K_DOWN and selected_option < enums.EXIT:
                                selected_option += 1
                                self.sfx_menu_click.play()
                                page_timer = 0
                            # the cursor up has been pressed
                            elif event.key == pygame.K_UP and selected_option > enums.START:
                                selected_option -= 1
                                self.sfx_menu_click.play()
                                page_timer = 0
                        # Options menu and there is no shot in progress?
                        elif menu_page == 5 and not confirmed_option:
                            # the cursor down has been pressed
                            if event.key == pygame.K_DOWN and selected_option < enums.EXIT_OPTIONS:
                                selected_option += 1
                                self.sfx_menu_click.play()
                                page_timer = 0
                            # the cursor up has been pressed
                            elif event.key == pygame.K_UP and selected_option > enums.FULLSCREEN:
                                selected_option -= 1
                                self.sfx_menu_click.play()
                                page_timer = 0                             
                    # pressing any key on a passive page, returns to the main menu
                    else:
                        menu_page = 0
                        page_timer = 0
            
            # =================== management of active pages ===================
            if (menu_page == 0 or menu_page == 5) and x == 0:
                # shows the player (cursor) next to the selected option
                if menu_page == 0:
                    self.srf_menu.blit(self.img_player, (55, 64 + (20*selected_option)))
                else: # page 5
                    self.srf_menu.blit(self.img_player, (34, -28 + (20*selected_option)))
                
                # draw the shot (if it exists)
                self.game.shot_group.update()
                self.game.shot_group.draw(self.srf_menu)

                # an option was confirmed and the shot was completed?
                if confirmed_option and self.game.shot_group.sprite == None:
                    # main menu page
                    if selected_option == enums.START:
                        self.game.new = True
                        return                        
                    elif selected_option == enums.LOAD:
                        self.game.new = False
                        return
                    elif selected_option == enums.OPTIONS:
                        # reinitialises common variables and loads the page
                        x = constants.MENU_UNSCALED_SIZE[0]
                        selected_option = enums.FULLSCREEN
                        menu_page = 5
                    elif selected_option == enums.EXIT:
                        self.game.exit()

                    # options menu page
                    elif selected_option == enums.FULLSCREEN:  # 0 = no, 1 = yes
                        self.game.config.data['full_screen'] = (self.game.config.data['full_screen'] + 1) % 2
                    elif selected_option == enums.SCANLINES: # 0 = none, 1 = fast, 2 = HQ
                        self.game.config.data['scanlines'] = (self.game.config.data['scanlines'] + 1) % 3
                    elif selected_option == enums.MAP_TRANSITION: # 0 = no, 1 = yes
                        self.game.config.data['map_transition'] = (self.game.config.data['map_transition'] + 1) % 2
                    elif selected_option == enums.CONTROL: # 0 = classic, 1 = gamer, 2 = retro, 3 = joypad
                        self.game.config.data['control'] = (self.game.config.data['control'] + 1) % 4
                        self.game.config.apply_controls() # remap the keyboard
                    elif selected_option == enums.EXIT_OPTIONS:
                        x = constants.MENU_UNSCALED_SIZE[0]
                        menu_page = 0
                        selected_option = enums.START

                    # common values for pages 1 and 6
                    confirmed_option = False
                    page_timer = 0

                    if menu_page == 5:
                        # create joystick/joypad/gamepad object (if it exists)
                        self.game.joystick = self.game.config.prepare_joystick()                        
                        # saves and apply possible changes to the configuration
                        self.game.config.save()  
                        self.game.apply_display_settings()                     
                        # recreate the page with the new data
                        self.menu_pages[5] = pygame.Surface(constants.MENU_UNSCALED_SIZE)
                        self.menu_pages[5].set_colorkey(constants.PALETTE['BLACK'])
                        self.page_5()

            self.game.update_screen()
