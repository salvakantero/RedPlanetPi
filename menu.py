
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
import support
import constants
import enums
from font import Font

class Menu():
    def __init__(self, screen, game_status, hotspot_images):
        self.screen = screen
        self.game_status = game_status
        self.hotspot_images = hotspot_images
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
        self.fnt_LF2 = Font('images/fonts/large_font.png', constants.PALETTE['GREEN'], True)
        self.fnt_LB2 = Font('images/fonts/large_font.png', constants.PALETTE['DARK_GREEN'], True)
        self.fnt_SF = Font('images/fonts/small_font.png', constants.PALETTE['WHITE'], True)
        self.fnt_SB = Font('images/fonts/small_font.png', constants.PALETTE['DARK_GRAY'], True)
        self.fnt_SF2 = Font('images/fonts/small_font.png', constants.PALETTE['CYAN'], True)
        self.fnt_SB2 = Font('images/fonts/small_font.png', constants.PALETTE['DARK_BLUE'], True)
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
        # generate menu pages
        self.page_1()
        self.page_2()
        self.page_3()
        self.page_4()
        
    def page_1(self): # page 1 (menu options)
        button_images = {
            enums.START: [
                pygame.image.load('images/assets/button1_0.png').convert_alpha(),
                pygame.image.load('images/assets/button1_1.png').convert_alpha(),                              
                pygame.image.load('images/assets/button1_2.png').convert_alpha()],
            enums.LOAD: [
                pygame.image.load('images/assets/button2_0.png').convert_alpha(),
                pygame.image.load('images/assets/button2_1.png').convert_alpha(),
                pygame.image.load('images/assets/button2_2.png').convert_alpha()],
            enums.OPTIONS: [
                pygame.image.load('images/assets/button3_0.png').convert_alpha(),
                pygame.image.load('images/assets/button3_1.png').convert_alpha(),
                pygame.image.load('images/assets/button3_2.png').convert_alpha()],
            enums.EXIT: [
                pygame.image.load('images/assets/button4_0.png').convert_alpha(),
                pygame.image.load('images/assets/button4_1.png').convert_alpha(),
                pygame.image.load('images/assets/button4_2.png').convert_alpha()]}
        # menu options      
        x = 83
        y = 67
        support.shaded_text(self.fnt_LB, self.fnt_LF, 'Start New Game', self.srf_page1, x, y, 1)
        support.shaded_text(self.fnt_LB, self.fnt_LF, 'Load Checkpoint', self.srf_page1, x, y+25, 1)
        support.shaded_text(self.fnt_LB, self.fnt_LF, 'Options', self.srf_page1, x, y+50, 1)
        support.shaded_text(self.fnt_LB, self.fnt_LF, 'Exit', self.srf_page1, x, y+75, 1)
        # menu buttons
        x = 50
        y = 60
        self.srf_page1.blit(button_images[enums.START][0], (x, y))
        self.srf_page1.blit(button_images[enums.LOAD][0], (x, y+25))
        self.srf_page1.blit(button_images[enums.OPTIONS][0], (x, y+50))
        self.srf_page1.blit(button_images[enums.EXIT][0], (x, y+75))
    
    def page_2(self): # page 2 (enemies/hotspot info)
        img_infected = pygame.image.load('images/sprites/infected0.png').convert()
        img_avirus = pygame.image.load('images/sprites/avirus0.png').convert()
        img_pelusoid = pygame.image.load('images/sprites/pelusoid0.png').convert()
        img_fanty = pygame.image.load('images/sprites/fanty0.png').convert()
        x = 20
        y = 60
        support.shaded_text(self.fnt_LB2, self.fnt_LF2, 'The Baddies       The Hotspots', self.page2_surf, x, y, 1)
        x = 40
        y = 90
        support.shaded_text(self.fnt_SB, self.fnt_SF, 'Infected (+25)', self.page2_surf, x, y, 1)
        support.shaded_text(self.fnt_SB, self.fnt_SF, 'Arachnovirus (+50)', self.page2_surf, x, y+20, 1)
        support.shaded_text(self.fnt_SB, self.fnt_SF, 'Pelusoid (+75)', self.page2_surf, x, y+40, 1)   
        support.shaded_text(self.fnt_SB, self.fnt_SF, 'Pelusoid Fanty (+100)', self.page2_surf, x, y+60, 1)
        x = 163
        support.shaded_text(self.fnt_SB, self.fnt_SF, 'Explosives', self.page2_surf, x, y, 1)
        support.shaded_text(self.fnt_SB, self.fnt_SF, 'Ammunition', self.page2_surf, x, y+20, 1)
        support.shaded_text(self.fnt_SB, self.fnt_SF, 'Key Card', self.page2_surf, x, y+40, 1) 
        support.shaded_text(self.fnt_SB, self.fnt_SF, 'Oxygen bottle', self.page2_surf, x, y+60, 1)
        # images of enemies
        x = 17
        y = 84
        self.page2_surf.blit(img_infected, (x, y))
        self.page2_surf.blit(img_avirus, (x, y+20))
        self.page2_surf.blit(img_pelusoid, (x, y+40))
        self.page2_surf.blit(img_fanty, (x, y+60))
        # images of the hotspots
        x = 139
        self.page2_surf.blit(self.hotspot_images[enums.TNT], (x, y))
        self.page2_surf.blit(self.hotspot_images[enums.AMMO], (x, y+20))
        self.page2_surf.blit(self.hotspot_images[enums.KEY], (x, y+40))
        self.page2_surf.blit(self.hotspot_images[enums.OXYGEN], (x, y+60))

    # page 3 (control info) ----------------------------------------------------
    x = 95
    y = 57
    support.shaded_text(fnt_LB2, fnt_LF2, 'Controls', page3_surf, x, y, 1)
    x = 35
    y = 82
    page3_surf.blit(classic, (x, y)) # image of the classic layout
    support.shaded_text(fnt_SB, fnt_SF, 'Classic', page3_surf, x+10, y+38, 1)
    x = 100
    page3_surf.blit(gamer, (x, y)) # image of the gamer layout
    support.shaded_text(fnt_SB, fnt_SF, 'Gamer', page3_surf, x+12, y+38, 1)
    x = 165
    page3_surf.blit(retro, (x, y)) # image of the retro layout
    support.shaded_text(fnt_SB, fnt_SF, 'Retro', page3_surf, x+18, y+38, 1) 
    x = 110
    y = 140
    page3_surf.blit(common, (x, y)) # image of the common keys
    support.shaded_text(fnt_SB, fnt_SF, 'Common keys', page3_surf, x-52, y+15, 1)

    # page 4 (high scores) --------------------------------------------
    x = 90
    y = 60
    support.shaded_text(fnt_LB2, fnt_LF2, 'High Scores', page4_surf, x, y, 1)
    x = 50
    y = 90
    # names
    support.shaded_text(fnt_SB, fnt_SF, 'Lukas', page4_surf, x, y, 1)
    support.shaded_text(fnt_SB2, fnt_SF2, 'Dany', page4_surf, x, y+10, 1)
    support.shaded_text(fnt_SB, fnt_SF, 'Marina', page4_surf, x, y+20, 1)   
    support.shaded_text(fnt_SB2, fnt_SF2, 'Alvaro', page4_surf, x, y+30, 1)
    support.shaded_text(fnt_SB, fnt_SF, 'Julita', page4_surf, x, y+40, 1)
    support.shaded_text(fnt_SB2, fnt_SF2, 'Luna_314', page4_surf, x, y+50, 1)
    support.shaded_text(fnt_SB, fnt_SF, 'Irenita', page4_surf, x, y+60, 1)
    support.shaded_text(fnt_SB2, fnt_SF2, 'salvaKantero', page4_surf, x, y+70, 1)
    # dates and scores
    x = 110
    support.shaded_text(fnt_SB, fnt_SF, '14/02/2023' + '    00195325', page4_surf, x, y, 1)
    support.shaded_text(fnt_SB2, fnt_SF2, '14/02/2023' + '    00195290', page4_surf, x, y+10, 1)
    support.shaded_text(fnt_SB, fnt_SF, '11/02/2023' + '    00152645', page4_surf, x, y+20, 1)   
    support.shaded_text(fnt_SB2, fnt_SF2, '28/01/2023' + '    00147755', page4_surf, x, y+30, 1)
    support.shaded_text(fnt_SB, fnt_SF, '30/12/2022' + '    00097430', page4_surf, x, y+40, 1)
    support.shaded_text(fnt_SB2, fnt_SF2, '21/01/2023' + '    00042940', page4_surf, x, y+50, 1)
    support.shaded_text(fnt_SB, fnt_SF, '01/02/2023' + '    00008255', page4_surf, x, y+60, 1)
    support.shaded_text(fnt_SB2, fnt_SF2, '30/12/2022' + '    00001985', page4_surf, x, y+70, 1)

    # help
    marquee_help = MarqueeText(
        screen.menu_surf, Font('images/fonts/small_font.png', constants.PALETTE['YELLOW'], True),
        screen.menu_surf.get_height() - 16, .7, constants.HELP, 1700)
    # credits       
    marquee_credits = MarqueeText(
        screen.menu_surf, Font('images/fonts/small_font.png', constants.PALETTE['ORANGE'], True),
        screen.menu_surf.get_height() - 8, .5, constants.CREDITS, 2900)
        
    sfx_switchoff.play()    
    pygame.mixer.music.load('sounds/music/mus_menu.ogg')
    pygame.mixer.music.play()
    
    menu_page = 0 # page displayed (1 to 4)
    page_timer = 0 # number of loops the page remains on screen
    x = constants.MENU_UNSCALED_SIZE[0] # for sideways scrolling of pages

    pygame.event.clear(pygame.KEYDOWN)
    while True: 
        page_timer += 1        
        screen.menu_surf.blit(menu_image, (0,0)) # blue background image
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
        if menu_page == 1: screen.menu_surf.blit(page1_surf, (x, 0))
        # draws enemy and hotspot information        
        elif menu_page == 2: screen.menu_surf.blit(page2_surf, (x, 0))
        # draws enemy and hotspot information
        elif menu_page == 3: screen.menu_surf.blit(page3_surf, (x, 0))
        # draw the score table
        elif menu_page == 4: screen.menu_surf.blit(page4_surf, (x, 0))              
        else: menu_page = 1
        
        # mouse management
        pos = pygame.mouse.get_pos()
        on_button = 0
        if menu_page == 1 and x == 0: # main menu active?
            if pos[0] > 190 and pos[0] < 260: # cursor over one of the buttons
                if pos[1] > 200 and pos[1] < 280: # START
                    screen.menu_surf.blit(button_images[enums.START][1], (50, 60))
                    on_button = 1
                elif pos[1] > 280 and pos[1] < 350: # LOAD
                    screen.menu_surf.blit(button_images[enums.LOAD][1], (50, 85))
                    on_button = 2
                elif pos[1] > 350 and pos[1] < 430: # OPTIONS
                    screen.menu_surf.blit(button_images[enums.OPTIONS][1], (50, 110))
                    on_button = 3
                elif pos[1] > 430 and pos[1] < 510: # EXIT
                    screen.menu_surf.blit(button_images[enums.EXIT][1], (50, 135))
                    on_button = 4
                # click with the left button?
                if pygame.mouse.get_pressed() == (1,0,0):
                    sfx_menu_click.play()
                    if on_button == 1: # START
                        screen.menu_surf.blit(button_images[enums.START][2], (50, 60))
                        #update_screen()
                        screen.update(game_status)
                        pygame.time.wait(320)
                        return
                    elif on_button == 4: # EXIT
                        screen.menu_surf.blit(button_images[enums.EXIT][2], (50, 135))
                        #update_screen()
                        screen.update(game_status)
                        pygame.time.wait(320)
                        support.exit()

        # keyboard management
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                support.exit()
            if event.type == pygame.KEYDOWN:                
                if event.key == pygame.K_ESCAPE: # exit by pressing ESC key
                    support.exit()
                # pressing any key returns to the main menu
                elif menu_page != 1:
                    menu_page = 1
                    page_timer = 0    

        #update_screen()
        screen.update(game_status)

