
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
from bullet import Bullet


class Menu():
    def __init__(self, game):
        self.game = game        
        self.srf_menu = game.srf_menu    
        self.selected_option = 0
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
        # menu fonts
        self.fnt_LF = Font('images/fonts/large_font.png', constants.PALETTE['WHITE'], True)
        self.fnt_LB = Font('images/fonts/large_font.png', constants.PALETTE['DARK_GRAY'], True)
        self.fnt_LF2 = Font('images/fonts/large_font.png', constants.PALETTE['SAND'], True)
        self.fnt_LB2 = Font('images/fonts/large_font.png', constants.PALETTE['BROWN'], True)
        self.fnt_SF = Font('images/fonts/small_font.png', constants.PALETTE['WHITE'], True)
        self.fnt_SB = Font('images/fonts/small_font.png', constants.PALETTE['DARK_GRAY'], True)
        self.fnt_SF2 = Font('images/fonts/small_font.png', constants.PALETTE['GREEN'], True)
        self.fnt_SB2 = Font('images/fonts/small_font.png', constants.PALETTE['DARK_GREEN'], True)
        # player
        self.cursor = pygame.image.load('images/sprites/player0.png').convert_alpha()
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
        self.sfx_shot = pygame.mixer.Sound('sounds/fx/sfx_shot.wav')
        # generate menu pages
        self.page_1()
        self.page_2()
        self.page_3()
        self.page_4()
        
    # draws a text with its shadow
    def shaded_text(self, font_BG, font_FG, text, surface, x, y, offset):           
        font_BG.render(text, surface, (x, y))  # shadow
        font_FG.render(text, surface, (x-offset, y-offset))

    def page_1(self): # menu options
        # menu options      
        x = 83
        y = 67
        self.shaded_text(self.fnt_LB, self.fnt_LF, 'Start New Game', self.srf_page1, x, y, 1)
        self.shaded_text(self.fnt_LB, self.fnt_LF, 'Load Checkpoint', self.srf_page1, x, y+25, 1)
        self.shaded_text(self.fnt_LB, self.fnt_LF, 'Options', self.srf_page1, x, y+50, 1)
        self.shaded_text(self.fnt_LB, self.fnt_LF, 'Exit', self.srf_page1, x, y+75, 1)
        self.shaded_text(self.fnt_SB2, self.fnt_SF2, 'Use arrow keys and ENTER to select', self.srf_page1, x-25, y+100, 1)

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
        self.shaded_text(self.fnt_LB2, self.fnt_LF2, 'The Baddies       The Hotspots', self.srf_page2, x, y, 1)
        x = 40
        y = 95
        self.shaded_text(self.fnt_SB, self.fnt_SF, 'Infected (+25)', self.srf_page2, x, y, 1)
        self.shaded_text(self.fnt_SB, self.fnt_SF, 'Arachnovirus (+50)', self.srf_page2, x, y+20, 1)
        self.shaded_text(self.fnt_SB, self.fnt_SF, 'Pelusoid (+75)', self.srf_page2, x, y+40, 1)   
        self.shaded_text(self.fnt_SB, self.fnt_SF, 'Pelusoid Fanty (+100)', self.srf_page2, x, y+60, 1)
        x = 163
        self.shaded_text(self.fnt_SB, self.fnt_SF, 'Explosives', self.srf_page2, x, y, 1)
        self.shaded_text(self.fnt_SB, self.fnt_SF, 'Ammunition', self.srf_page2, x, y+20, 1)
        self.shaded_text(self.fnt_SB, self.fnt_SF, 'Key Card', self.srf_page2, x, y+40, 1) 
        self.shaded_text(self.fnt_SB, self.fnt_SF, 'Oxygen bottle', self.srf_page2, x, y+60, 1)
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
        self.shaded_text(self.fnt_LB2, self.fnt_LF2, 'Controls', self.srf_page3, x, y, 1)
        x = 35
        y = 82
        self.srf_page3.blit(self.img_classic, (x, y)) # image of the classic layout
        self.shaded_text(self.fnt_SB, self.fnt_SF, 'Classic', self.srf_page3, x+10, y+38, 1)
        x = 100
        self.srf_page3.blit(self.img_gamer, (x, y)) # image of the gamer layout
        self.shaded_text(self.fnt_SB, self.fnt_SF, 'Gamer', self.srf_page3, x+12, y+38, 1)
        x = 165
        self.srf_page3.blit(self.img_retro, (x, y)) # image of the retro layout
        self.shaded_text(self.fnt_SB, self.fnt_SF, 'Retro', self.srf_page3, x+18, y+38, 1) 
        x = 110
        y = 140
        self.srf_page3.blit(self.img_common, (x, y)) # image of the common keys
        self.shaded_text(self.fnt_SB, self.fnt_SF, 'Common keys', self.srf_page3, x-52, y+15, 1)

    def page_4(self): # high scores
        x = 90
        y = 60
        self.shaded_text(self.fnt_LB2, self.fnt_LF2, 'High Scores', self.srf_page4, x, y, 1)
        x = 50
        y = 90
        # names
        self.shaded_text(self.fnt_SB, self.fnt_SF, 'Lukas', self.srf_page4, x, y, 1)
        self.shaded_text(self.fnt_SB2, self.fnt_SF2, 'Dany', self.srf_page4, x, y+10, 1)
        self.shaded_text(self.fnt_SB, self.fnt_SF, 'Marina', self.srf_page4, x, y+20, 1)   
        self.shaded_text(self.fnt_SB2, self.fnt_SF2, 'Alvaro', self.srf_page4, x, y+30, 1)
        self.shaded_text(self.fnt_SB, self.fnt_SF, 'Julita', self.srf_page4, x, y+40, 1)
        self.shaded_text(self.fnt_SB2, self.fnt_SF2, 'Luna_314', self.srf_page4, x, y+50, 1)
        self.shaded_text(self.fnt_SB, self.fnt_SF, 'Irenita', self.srf_page4, x, y+60, 1)
        self.shaded_text(self.fnt_SB2, self.fnt_SF2, 'salvaKantero', self.srf_page4, x, y+70, 1)
        # dates and scores
        x = 110
        self.shaded_text(self.fnt_SB, self.fnt_SF, '14/02/2023' + '    00195325', self.srf_page4, x, y, 1)
        self.shaded_text(self.fnt_SB2, self.fnt_SF2, '14/02/2023' + '    00195290', self.srf_page4, x, y+10, 1)
        self.shaded_text(self.fnt_SB, self.fnt_SF, '11/02/2023' + '    00152645', self.srf_page4, x, y+20, 1)   
        self.shaded_text(self.fnt_SB2, self.fnt_SF2, '28/01/2023' + '    00147755', self.srf_page4, x, y+30, 1)
        self.shaded_text(self.fnt_SB, self.fnt_SF, '30/12/2022' + '    00097430', self.srf_page4, x, y+40, 1)
        self.shaded_text(self.fnt_SB2, self.fnt_SF2, '21/01/2023' + '    00042940', self.srf_page4, x, y+50, 1)
        self.shaded_text(self.fnt_SB, self.fnt_SF, '01/02/2023' + '    00008255', self.srf_page4, x, y+60, 1)
        self.shaded_text(self.fnt_SB2, self.fnt_SF2, '30/12/2022' + '    00001985', self.srf_page4, x, y+70, 1)

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
        pygame.mixer.music.load('sounds/music/mus_menu.ogg')
        pygame.mixer.music.play()
    
        menu_page = 0 # page displayed (1 to 4)
        page_timer = 0 # number of loops the page remains on screen
        x = constants.MENU_UNSCALED_SIZE[0] # for sideways scrolling of pages
        
        pygame.event.clear(pygame.KEYDOWN)
        while True:
            page_timer += 1        
            self.srf_menu.blit(self.img_menu, (0,0)) # background image
            # marquee
            marquee_help.update()
            marquee_credits.update()  

            # transition of menu pages
            if page_timer >= 500: # time exceeded?
                menu_page += 1 # change the page
                page_timer = 0 # and reset the timer
                x = constants.MENU_UNSCALED_SIZE[0] # again in the right margin
            elif page_timer >= 450: # time almost exceeded?
                x -= 8 # scrolls the page to the left        
            elif x > 0: # as long as the page does not reach the left margin
                x -= 8 # scrolls the page to the left  

            # draws the main menu
            if menu_page == 1: self.srf_menu.blit(self.srf_page1, (x, 0))
            # draws enemy and hotspot information        
            elif menu_page == 2: self.srf_menu.blit(self.srf_page2, (x, 0))
            # draws enemy and hotspot information
            elif menu_page == 3: self.srf_menu.blit(self.srf_page3, (x, 0))
            # draw the score table
            elif menu_page == 4: self.srf_menu.blit(self.srf_page4, (x, 0))              
            else: menu_page = 1

            # keyboard management
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.exit()
                if event.type == pygame.KEYDOWN:             
                    if event.key == pygame.K_ESCAPE: # exit by pressing ESC key
                        self.game.exit()
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        bullet = Bullet(pygame.Rect(58, 63 + (25 * self.selected_option), 16, 16 ), 0, self.img_bullet)
                        self.game.all_sprites_group.add(bullet)
                        self.sfx_shot.play()
                        for z in range(50):
                            self.game.all_sprites_group.update()
                            self.game.update_screen()

                        if self.selected_option == 0:
                            return
                        elif self.selected_option == 3:
                            self.game.exit()
                    elif menu_page == 1:
                        page_timer = 0   
                        if event.key == pygame.K_DOWN and self.selected_option < 3:
                            self.selected_option += 1
                        elif event.key == pygame.K_UP and self.selected_option > 0:
                            self.selected_option -= 1
                    # pressing any key returns to the main menu
                    else:
                        menu_page = 1
                        page_timer = 0    
            
            if menu_page == 1 and x == 0:
                self.srf_menu.blit(self.cursor, (58, 63 + (25 * self.selected_option)))

            self.game.update_screen()
