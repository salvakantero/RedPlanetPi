
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
from floatingtext import FloatingText
from marqueetext import MarqueeText
from jukebox import Jukebox


#===============================================================================
# Map functions
#===============================================================================

# makes a screen transition between the old map and the new one.
def map_transition():
    # surfaces to save the old and the new map together
    map_trans_horiz = pygame.Surface((constants.MAP_UNSCALED_SIZE[0]*2, constants.MAP_UNSCALED_SIZE[1]))
    map_trans_vert = pygame.Surface((constants.MAP_UNSCALED_SIZE[0], constants.MAP_UNSCALED_SIZE[1]*2))

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
    # add the TNT pile if necessary to the background
    if map.number == 44 and player.stacked_TNT:
        map.add_TNT_pile()
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


#===============================================================================
# Main functions
#===============================================================================

# dumps and scales surfaces to the screen
def update_screen():
    if game_status == enums.OVER:
        # scale x 3 the menu
        screen.blit(pygame.transform.scale(menu_surf, constants.MENU_SCALED_SIZE), 
        (constants.H_MARGIN, constants.V_MARGIN))
    else:
        # shakes the surface of the map if it has been requested
        offset = [0,0]
        if map.shake_timer > 0:
            if map.shake_timer == 1: # last frame shaken   
                # it's necessary to clean the edges of the map after shaking it         
                pygame.draw.rect(screen, constants.PALETTE['BLACK'], (20, 120 , 20 , 500))
                pygame.draw.rect(screen, constants.PALETTE['BLACK'], (760, 120 , 20 , 500))
                pygame.draw.rect(screen, constants.PALETTE['BLACK'], (40, 610 , 720 , 20))
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
    aux_surf = pygame.Surface(constants.MAP_UNSCALED_SIZE)    
    aux_surf.blit(map_surf, (0,0))
    # draws the light message on the dark background
    support.message_box(msg1, msg2, aux_surf, font_dict)
    # return the copy with the message on the map surface and redraw it.
    map_surf.blit(aux_surf, (0,0))
    map_surf.set_alpha(None)
    update_screen()
    sfx_message.play()

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
    pygame.mixer.stop()
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
                if event.key == pygame.K_ESCAPE or event.key == config.pause_key:
                    return

def fades_surface(target_surf, aux_surf, opacity, delay):
    aux_surf.set_alpha(0) # totally transparent    
    for z in range(opacity):
        aux_surf.set_alpha(z) # opacity is being applied
        target_surf.blit(aux_surf, (0,0)) # the two surfaces come together to be drawn
        update_screen() # draw target_surf
        pygame.time.wait(delay) # speed of transition

# introductory scene
def intro_scene():
    logo_image = pygame.image.load('images/assets/logo.png').convert() # PlayOnRetro  
    intro1_image = pygame.image.load('images/assets/intro1.png').convert() # background
    intro2_image = pygame.image.load('images/assets/intro2.png').convert_alpha() # title
    intro3_image = pygame.image.load('images/assets/intro3.png').convert_alpha() # pi
    sfx_intro1 = pygame.mixer.Sound('sounds/fx/sfx_intro1.wav') # flash effect
    sfx_intro2 = pygame.mixer.Sound('sounds/fx/sfx_intro2.wav') # text sliding
    sfx_intro3 = pygame.mixer.Sound('sounds/fx/sfx_intro3.wav') # PlayOnRetro
    sfx_intro3.set_volume(.4)
    # auxiliary surface for fading and flashing visual effects
    aux_surf = pygame.Surface(constants.MENU_UNSCALED_SIZE, pygame.SRCALPHA)
    # PlayOnRetro logo
    # fade in
    menu_surf.fill(constants.PALETTE["BLACK"]) # black background
    aux_surf.blit(logo_image, (0, 0))
    fades_surface(menu_surf, aux_surf, 45, 12)
    if support.main_key_pressed(): return # allows skipping the intro
    sfx_intro3.play()
    pygame.time.wait(1500)
    if support.main_key_pressed(): return
    # fade out
    aux_surf.fill(constants.PALETTE["BLACK"]) # black background
    fades_surface(menu_surf, aux_surf, 45, 12)
    if support.main_key_pressed(): return # allows skipping the intro 
    pygame.time.wait(1500)
    if support.main_key_pressed(): return
    # RedPlanetPi
    sfx_intro1.play()
    menu_surf.fill(constants.PALETTE["WHITE"]) # white background
    aux_surf.blit(intro1_image, (0, 0))
    fades_surface(menu_surf, aux_surf, 50, 8)
    pygame.time.wait(200)
    if support.main_key_pressed(): return # allows skipping the intro
    # slide the title "RED PLANET" from the right to its final position
    sfx_intro2.play()
    for x in range(-170, 0, 10):
        menu_surf.blit(intro1_image, (0, 0))
        menu_surf.blit(intro2_image, (x, 0))
        update_screen()
    # slides the PI from the bottom to its final position
    sfx_intro2.play()
    for y in range(140, -5, -10):
        menu_surf.blit(intro1_image, (0, 0))
        menu_surf.blit(intro2_image, (0, 0))
        menu_surf.blit(intro3_image, (198, y))
        update_screen()
    if support.main_key_pressed(): return # allows skipping the intro
    # pause for recreation. Ooohhh how wonderful!
    pygame.time.wait(500)

# main menu
def main_menu():
    # page 1: menu options
    page1_surf = pygame.Surface(constants.MENU_UNSCALED_SIZE)
    page1_surf.set_colorkey(constants.PALETTE['BLACK']) # transparent background
    # page 2: enemy/hotspot information
    page2_surf = pygame.Surface(constants.MENU_UNSCALED_SIZE)
    page2_surf.set_colorkey(constants.PALETTE['BLACK'])
    # page 3: control information
    page3_surf = pygame.Surface(constants.MENU_UNSCALED_SIZE)
    page3_surf.set_colorkey(constants.PALETTE['BLACK'])
    # page 4: high scores
    page4_surf = pygame.Surface(constants.MENU_UNSCALED_SIZE)
    page4_surf.set_colorkey(constants.PALETTE['BLACK'])
    
    # menu fonts
    fnt_LF = Font('images/fonts/large_font.png', constants.PALETTE['WHITE'], True)
    fnt_LB = Font('images/fonts/large_font.png', constants.PALETTE['DARK_GRAY'], True)
    fnt_LF2 = Font('images/fonts/large_font.png', constants.PALETTE['GREEN'], True)
    fnt_LB2 = Font('images/fonts/large_font.png', constants.PALETTE['DARK_GREEN'], True)
    fnt_SF = Font('images/fonts/small_font.png', constants.PALETTE['WHITE'], True)
    fnt_SB = Font('images/fonts/small_font.png', constants.PALETTE['DARK_GRAY'], True)
    fnt_SF2 = Font('images/fonts/small_font.png', constants.PALETTE['CYAN'], True)
    fnt_SB2 = Font('images/fonts/small_font.png', constants.PALETTE['DARK_BLUE'], True)
    # buttons
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
    # enemies
    infected_image = pygame.image.load('images/sprites/infected0.png').convert()
    avirus_image = pygame.image.load('images/sprites/avirus0.png').convert()
    pelusoid_image = pygame.image.load('images/sprites/pelusoid0.png').convert()
    fanty_image = pygame.image.load('images/sprites/fanty0.png').convert()
    # controls
    classic = pygame.image.load('images/assets/classic.png').convert_alpha()
    gamer = pygame.image.load('images/assets/gamer.png').convert_alpha()
    retro = pygame.image.load('images/assets/retro.png').convert_alpha()
    common = pygame.image.load('images/assets/common.png').convert_alpha()
    # sounds
    sfx_switchoff = pygame.mixer.Sound('sounds/fx/sfx_switchoff.wav')
    sfx_menu_click = pygame.mixer.Sound('sounds/fx/sfx_menu_click.wav')

    # page 1 (menu options) ----------------------------------------------------
    x = 83
    y = 67
    support.shaded_text(fnt_LB, fnt_LF, 'Start New Game', page1_surf, x, y, 1)
    support.shaded_text(fnt_LB, fnt_LF, 'Load Checkpoint', page1_surf, x, y+25, 1)
    support.shaded_text(fnt_LB, fnt_LF, 'Options', page1_surf, x, y+50, 1)
    support.shaded_text(fnt_LB, fnt_LF, 'Exit', page1_surf, x, y+75, 1)
    # menu buttons
    x = 50
    y = 60
    page1_surf.blit(button_images[enums.START][0], (x, y))
    page1_surf.blit(button_images[enums.LOAD][0], (x, y+25))
    page1_surf.blit(button_images[enums.OPTIONS][0], (x, y+50))
    page1_surf.blit(button_images[enums.EXIT][0], (x, y+75))
    
    # page 2 (enemies/hotspot info) --------------------------------------------
    x = 20
    y = 60
    support.shaded_text(fnt_LB2, fnt_LF2, 'The Baddies       The Hotspots', page2_surf, x, y, 1)
    x = 40
    y = 90
    support.shaded_text(fnt_SB, fnt_SF, 'Infected (+25)', page2_surf, x, y, 1)
    support.shaded_text(fnt_SB, fnt_SF, 'Arachnovirus (+50)', page2_surf, x, y+20, 1)
    support.shaded_text(fnt_SB, fnt_SF, 'Pelusoid (+75)', page2_surf, x, y+40, 1)   
    support.shaded_text(fnt_SB, fnt_SF, 'Pelusoid Fanty (+100)', page2_surf, x, y+60, 1)
    x = 163
    support.shaded_text(fnt_SB, fnt_SF, 'Explosives', page2_surf, x, y, 1)
    support.shaded_text(fnt_SB, fnt_SF, 'Ammunition', page2_surf, x, y+20, 1)
    support.shaded_text(fnt_SB, fnt_SF, 'Key Card', page2_surf, x, y+40, 1) 
    support.shaded_text(fnt_SB, fnt_SF, 'Oxygen bottle', page2_surf, x, y+60, 1)
    # images of enemies
    x = 17
    y = 84
    page2_surf.blit(infected_image, (x, y))
    page2_surf.blit(avirus_image, (x, y+20))
    page2_surf.blit(pelusoid_image, (x, y+40))
    page2_surf.blit(fanty_image, (x, y+60))
    # images of the hotspots
    x = 139
    page2_surf.blit(hotspot_images[enums.TNT], (x, y))
    page2_surf.blit(hotspot_images[enums.AMMO], (x, y+20))
    page2_surf.blit(hotspot_images[enums.KEY], (x, y+40))
    page2_surf.blit(hotspot_images[enums.OXYGEN], (x, y+60))

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
        menu_surf, Font('images/fonts/small_font.png', constants.PALETTE['YELLOW'], True),
        menu_surf.get_height() - 16, .7, constants.HELP, 1700)
    # credits       
    marquee_credits = MarqueeText(
        menu_surf, Font('images/fonts/small_font.png', constants.PALETTE['ORANGE'], True),
        menu_surf.get_height() - 8, .5, constants.CREDITS, 2900)
        
    sfx_switchoff.play()    
    pygame.mixer.music.load('sounds/music/mus_menu.ogg')
    pygame.mixer.music.play()
    
    menu_page = 0 # page displayed (1 to 4)
    page_timer = 0 # number of loops the page remains on screen
    x = constants.MENU_UNSCALED_SIZE[0] # for sideways scrolling of pages

    pygame.event.clear(pygame.KEYDOWN)
    while True: 
        page_timer += 1        
        menu_surf.blit(menu_image, (0,0)) # blue background image
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
        if menu_page == 1: menu_surf.blit(page1_surf, (x, 0))
        # draws enemy and hotspot information        
        elif menu_page == 2: menu_surf.blit(page2_surf, (x, 0))
        # draws enemy and hotspot information
        elif menu_page == 3: menu_surf.blit(page3_surf, (x, 0))
        # draw the score table
        elif menu_page == 4: menu_surf.blit(page4_surf, (x, 0))              
        else: menu_page = 1
        
        # mouse management
        pos = pygame.mouse.get_pos()
        on_button = 0
        if menu_page == 1 and x == 0: # main menu active?
            if pos[0] > 190 and pos[0] < 260: # cursor over one of the buttons
                if pos[1] > 200 and pos[1] < 280: # START
                    menu_surf.blit(button_images[enums.START][1], (50, 60))
                    on_button = 1
                elif pos[1] > 280 and pos[1] < 350: # LOAD
                    menu_surf.blit(button_images[enums.LOAD][1], (50, 85))
                    on_button = 2
                elif pos[1] > 350 and pos[1] < 430: # OPTIONS
                    menu_surf.blit(button_images[enums.OPTIONS][1], (50, 110))
                    on_button = 3
                elif pos[1] > 430 and pos[1] < 510: # EXIT
                    menu_surf.blit(button_images[enums.EXIT][1], (50, 135))
                    on_button = 4
                # click with the left button?
                if pygame.mouse.get_pressed() == (1,0,0):
                    sfx_menu_click.play()
                    if on_button == 1: # START
                        menu_surf.blit(button_images[enums.START][2], (50, 60))
                        update_screen()
                        pygame.time.wait(320)
                        return
                    elif on_button == 4: # EXIT
                        menu_surf.blit(button_images[enums.EXIT][2], (50, 135))
                        update_screen()
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

        update_screen()

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
                map.shake = [10, 6]
                map.shake_timer = 14
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
            map.shake = [4, 4]
            map.shake_timer = 4
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
                map.shake = [4, 0]
                map.shake_timer = 4
                # bounces the player
                if player.facing_right: player.rect.x -= 5
                else: player.rect.x += 5

# stops the music when the game is paused and a message is displayed.
def pause_music():
    if music_status == enums.UNMUTED:
        pygame.mixer.music.pause()

# restores music if it returns from a message
def restore_music():
    if music_status == enums.UNMUTED:
        pygame.mixer.music.unpause()

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

# generates a main window (or full screen) with title, icon, and 32-bit colour.
flags = 0
if config.full_screen: flags = pygame.FULLSCREEN
screen = pygame.display.set_mode(constants.WIN_SIZE, flags, 32)
pygame.display.set_caption('.:: Red Planet Pi ::.')
icon = pygame.image.load('images/assets/intro3.png').convert_alpha()
pygame.display.set_icon(icon)  

# area covered by the menu
menu_surf = pygame.Surface(constants.MENU_UNSCALED_SIZE)
# surface for HQ scanlines
scanlines_surf = pygame.Surface(constants.WIN_SIZE)
scanlines_surf.set_alpha(40)
# clock to control the FPS
clock = pygame.time.Clock()
game_status = enums.OVER
# shows an intro (resources are being loaded)
intro_scene()

# area covered by the map
map_surf = pygame.Surface(constants.MAP_UNSCALED_SIZE)
# area covered by the scoreboard
sboard_surf = pygame.Surface(constants.SBOARD_UNSCALED_SIZE)
# surface to save the generated map without sprites
map_surf_bk = pygame.Surface(constants.MAP_UNSCALED_SIZE)
# surface to save the previous map (transition effect between screens)
if config.map_transition:
    map_surf_bk_prev = pygame.Surface(constants.MAP_UNSCALED_SIZE)

# fonts
font_dict = {
    enums.SM_GREEN_FG: Font('images/fonts/small_font.png', constants.PALETTE['GREEN'], True),
    enums.SM_GREEN_BG: Font('images/fonts/small_font.png', constants.PALETTE['DARK_GREEN'], False),
    enums.LG_WHITE_FG: Font('images/fonts/large_font.png', constants.PALETTE['WHITE'], True),
    enums.LG_WHITE_BG: Font('images/fonts/large_font.png', constants.PALETTE['DARK_GRAY'], False),
    enums.SM_TEST: Font('images/fonts/small_font.png', constants.PALETTE['GREEN'], False)
}

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
menu_image = pygame.image.load('images/assets/menu_back.png').convert()

# fx sounds
sfx_open_door = pygame.mixer.Sound('sounds/fx/sfx_open_door.wav')
sfx_locked_door = pygame.mixer.Sound('sounds/fx/sfx_locked_door.wav')
sfx_game_over = pygame.mixer.Sound('sounds/fx/sfx_game_over.wav')
sfx_message = pygame.mixer.Sound('sounds/fx/sfx_message.wav')
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

# floating texts
floating_text = FloatingText(map_surf)

# create the Scoreboard object
scoreboard = Scoreboard(sboard_surf, hotspot_images, font_dict)

# create the Map object
map = Map(map_surf, map_surf_bk)

 # creates a playlist with the 12 available tracks
jukebox = Jukebox('sounds/music/', 'mus_ingame_', 12, constants.MUSIC_LOOP_LIST)
music_status = enums.UNMUTED


#===============================================================================
# Main loop
#===============================================================================

while True:    
    if game_status == enums.OVER: # game not running
        pygame.mouse.set_visible(True)
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
        player = Player(dust_animation, all_sprites_group, dust_group, bullet_group, map, scoreboard, config)
        # new unordered playlist with the 12 available music tracks
        pygame.mixer.music.stop()
        jukebox.shuffle()
        # reset variables
        for hotspot in constants.HOTSPOT_DATA: hotspot[3] = True # visible hotspots
        for gate in constants.GATE_DATA.values(): gate[2] = True # visible doors
        game_status = enums.RUNNING
        map.number = 0
        map.last = -1
        map.scroll = enums.RIGHT
        scoreboard.game_percent = 0
        floating_text.y = 0
    else: # game running
        pygame.mouse.set_visible(False)
        # event management
        for event in pygame.event.get():
            # exit when click on the X in the window
            if event.type == pygame.QUIT:
                support.exit()
            if event.type == pygame.KEYDOWN:
                # exit by pressing ESC key
                if event.key == pygame.K_ESCAPE:
                    pause_music()
                    if confirm_exit():
                        game_status = enums.OVER # go to the main menu
                    else: restore_music()
                # pause main loop
                if event.key == config.pause_key:
                    pause_music()
                    pause_game()
                    restore_music()                                
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
            
            # change the frame of the animated tiles
            map.animate_tiles()

            # draws the map free of sprites to clean it up
            map_surf.blit(map_surf_bk, (0,0))
            all_sprites_group.draw(map_surf)

            # draws the floating texts, only if needed
            floating_text.update()

            # updates the scoreboard, only if needed
            scoreboard.update(player)

            # check map change using player's coordinates
            # if the player leaves, the map number changes
            map.check_change(player)

            # next track in the playlist if the music has been stopped
            if music_status == enums.UNMUTED:
                jukebox.update()

            # display FPS (using the clock)
            if config.show_fps:
                font_dict[enums.SM_TEST].render(str(int(clock.get_fps())), map_surf, (233, 154))
            
    update_screen()
