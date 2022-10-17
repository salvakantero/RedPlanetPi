
# ==============================================================================
# Red Planet Pi v1.0
# salvaKantero 2022/23
# ==============================================================================

import pygame # pygame library functions
import random # random()
import sys # exit()
import json # load(), config file

# allows constants without typing "pygame."
from pygame.locals import *
from pygame.constants import *

# own code
from globalvars import *
import constants
import enums
import texts
import config



#===============================================================================
# Auxiliar and generic functions
#===============================================================================

# get a value from a dictionary
def find_data(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return dic
    return -1

# calculates the distance between two points
def distance (x1, y1, x2, y2):
    dx = abs(x2-x1)
    dy = abs(y2-y1)
    if dx < dy:
        mn = dx
    else:
        mn = dy
    return(dx + dy - (mn >> 1) - (mn >> 2) + (mn >> 4))

def limit(val, min, max):
    if val < min:
        return min
    elif val > max:
        return max
    return val

# draws scanlines
def scanlines(surface, height, from_x, to_x, rgb):
    j = constants.V_MARGIN
    while j < height:
        j+=3
        pygame.draw.line(surface, (rgb, rgb, rgb), (from_x, j), (to_x, j))

# applies scanlines according to the configuration
def make_scanlines():
    if config.cfg_scanlines_type == 2: # HQ
        scanlines(screen_sl, constants.WIN_SIZE[1]-30, constants.H_MARGIN, 
            constants.WIN_SIZE[0]-constants.H_MARGIN-1, 200)
        screen.blit(screen_sl, (0, 0))
    elif config.cfg_scanlines_type == 1: # fast
        scanlines(screen, constants.WIN_SIZE[1]-30, constants.H_MARGIN, 
            constants.WIN_SIZE[0]-constants.H_MARGIN-1, 15)

# draws a centred message box erasing the background
def message_box(message1, message2):
    # calculates the dimensions of the box
    height = 36
    message1_len = len(message1) * 7 # approximate length of text 1 in pixels
    message2_len = len(message2) * 4 # approximate length of text 2 in pixels
    # width = length of the longest text + margin
    if message1_len > message2_len:
        width = message1_len + constants.V_MARGIN
    else:
        width = message2_len + constants.V_MARGIN
    # calculates the position of the box
    x = (constants.MAP_UNSCALED_SIZE[0]//2) - (width//2)
    y = (constants.MAP_UNSCALED_SIZE[1]//2) - (height//2)
    pygame.draw.rect(map_display, constants.PALETTE['BLACK'],(x, y, width, height))
    # paints the text centred inside the box (Y positions are fixed)
    text_x = (x + (width//2)) - (message1_len//2)
    text_y = y + 5
    bg_font_L.render(message1, map_display, (text_x, text_y))
    fg_font_L.render(message1, map_display, (text_x - 2, text_y - 2))
    text_x = (x + (width//2)) - (message2_len//2)
    text_y = y + 24
    bg_font_S.render(message2, map_display, (text_x, text_y))
    fg_font_S.render(message2, map_display, (text_x - 1, text_y - 1))



#===============================================================================
# Map functions
#===============================================================================

# loads a map and draws it on screen
def load_map(map_number, map_display):
    global map_data
    map_data = process_map(jp(dp, 'maps/map{}.json'.format(map_number)))
    draw_map(map_display) # draws the tile map on the screen

# dump tiled map into 'mapdata'
def process_map(map_file):
    # reads the entire contents of the json
    with open(map_file) as json_data:
        data_readed = json.load(json_data)
    # gets the map dimensions
    data = {'width': data_readed['width'], 'height': data_readed['height']}
    # gets a list of all tiles
    raw_data = data_readed['layers'][0]['data']
    data['data'] = []
    # divides the list into tile lines, according to the map dimensions
    for x in range(0, data['height']):
        st = x * data['width']
        data['data'].append(raw_data[st: st + data['width']])
    # gets the name of the tile file
    tileset = data_readed['tilesets'][0]['source'].replace('.tsx','.json')
    # gets the data from the tile file
    with open(jp(dp,'maps/' + tileset)) as json_data:
        t = json.load(json_data)
    # removes the path to each image from the tile file
    data['tiles'] = t['tiles']
    for tile in range(0, len(data['tiles'])):
        path = data['tiles'][tile]['image']
        data['tiles'][tile]['image'] = os.path.basename(path)
        data['tiles'][tile]['id'] = data['tiles'][tile]['id'] + 1
    return data

# extracts the tile number from the filename
def get_tile_number(tile_name):
    tile_name = tile_name.replace('.png', '')
    tile_name = tile_name.replace('T', '')
    return int(tile_name)

# draws the tile map on the screen
def draw_map(map_display):
    tilemap_rect_list.clear()
    tilemap_behaviour_list.clear()
    anim_tiles_list.clear()
    # scroll through the map data
    for y in range(0, map_data['height']):
        for x in range(0, map_data['width']):
            # gets the tile number from the list
            t = find_data(map_data['tiles'], 'id', map_data['data'][y][x])
            # draws the selected tile
            tile = pygame.image.load(jp(dp, 'images/tiles/' + t['image'])).convert()
            tileRect = tile.get_rect()
            tileRect.topleft = (x * t['imagewidth'], y * t['imageheight'])   
            map_display.blit(tile, tileRect)

            # generates the list of rects and behaviour of the current map
            # from T0.png to T15.png: background tiles (NO_ACTION)
            # from T16.png to T35.png: blocking tiles (OBSTABLE)
            # T40.png: platform tile (PLATFORM)
            # from T50.png to T55.png: object tiles (ITEM)
            # T60.png: door tile (DOOR)
            # from T70.png to T75.png: tiles that kill (KILLER)
            # from T80.png: animated tiles (NO_ACTION)
            tn = get_tile_number(t['image'])            
            behaviour = enums.NO_ACTION
            if tn >= 16 and tn <= 35: behaviour = enums.OBSTACLE
            elif tn == 40: behaviour = enums.PLATFORM
            elif tn >= 50 and tn <= 55: behaviour = enums.ITEM
            elif tn == 60: behaviour = enums.DOOR
            elif tn >= 70 and tn <= 75: behaviour = enums.KILLER
            # is only added to the list if there is an active behaviour
            if behaviour != enums.NO_ACTION:
                tilemap_rect_list.append(tileRect)
                tilemap_behaviour_list.append(behaviour)

            # generates the list of animated tiles of the current map
            # (frame_1, frame_2, x, y, num_frame)
            if t['image'] in constants.ANIM_TILES.keys():                
                anim_tiles_list.append(
                    [tile, pygame.image.load(jp(dp, 'images/tiles/' 
                    + constants.ANIM_TILES[t['image']])).convert(), 
                    tileRect.topleft[0], tileRect.topleft[1], 0])

# select some of the animated tiles on the current map to change the frame
def animate_tiles():
    for anim_tile in anim_tiles_list: # for each animated tile on the map
        if random.randint(0,24) == 0: # 4% chance of changing frame
            tile = anim_tile[0+anim_tile[4]] # select image according to frame number
            tileRect = tile.get_rect()
            tileRect.topleft = (anim_tile[2], anim_tile[3]) # sets the xy position
            map_display_backup.blit(tile, tileRect) # draws on the background image
            # update frame number
            anim_tile[4] += 1
            if anim_tile[4] > 1:
                anim_tile[4] = 0
            
          

#===============================================================================
# Scoreboard functions
#===============================================================================

# draws the name of the map and other data at the top
def draw_map_info():
    x = 0
    y = 22
    progress_x = constants.SBOARD_UNSCALED_SIZE[0] - 55
    
    if map_number < 9:
        text_1 = 'SCREEN.......'
    else:
        text_1 = 'SCREEN.....'
    if game_percent < 10:
        text_2 = 'COMPLETED....'
    else:
        text_2 = 'COMPLETED..'
    
    text_1 += str(map_number+1) + '/45'
    text_2 += str(game_percent) + ';' # %

    sboard_display.fill((0,0,0)) # delete previous text

    # map name
    bg_font_L.render(constants.MAP_NAMES[map_number], sboard_display, (x+2, y+2)) # shadow
    fg_font_L.render(constants.MAP_NAMES[map_number], sboard_display, (x, y))
    # map number
    bg_font_S.render(text_1, sboard_display, (progress_x+1, y+1)) # shadow
    fg_font_S.render(text_1, sboard_display, (progress_x, y))
    # game percentage
    bg_font_S.render(text_2, sboard_display, (progress_x+1, y+bg_font_S.line_height+1)) # shadow
    fg_font_S.render(text_2, sboard_display, (progress_x, y+fg_font_S.line_height))

def init_scoreboard():
    # icons
    sboard_display.blit(lives_icon, (0, 2))
    sboard_display.blit(oxigen_icon, (42, 2))
    sboard_display.blit(ammo_icon, (82, 2))
    sboard_display.blit(keys_icon, (145, 2))
    sboard_display.blit(explosives_icon, (186, 2))
    # fixed texts
    bg_font_L.render('+50', sboard_display, (116, 6))
    fg_font_L.render('+50', sboard_display, (114, 4))
    bg_font_L.render('+15', sboard_display, (220, 6))
    fg_font_L.render('+15', sboard_display, (218, 4))

def update_scoreboard():
    # values
    bg_font_L.render(str(player.lives).rjust(2, '0'), sboard_display, (20, 6))
    fg_font_L.render(str(player.lives).rjust(2, '0'), sboard_display, (18, 4))
    bg_font_L.render(str(player.oxigen).rjust(2, '0'), sboard_display, (62, 6))
    fg_font_L.render(str(player.oxigen).rjust(2, '0'), sboard_display, (60, 4))
    bg_font_L.render(str(player.ammo).rjust(2, '0'), sboard_display, (102, 6))
    fg_font_L.render(str(player.ammo).rjust(2, '0'), sboard_display, (100, 4))
    bg_font_L.render(str(player.keys).rjust(2, '0'), sboard_display, (166, 6))
    fg_font_L.render(str(player.keys).rjust(2, '0'), sboard_display, (164, 4))
    bg_font_L.render(str(player.explosives).rjust(2, '0'), sboard_display, (206, 6))
    fg_font_L.render(str(player.explosives).rjust(2, '0'), sboard_display, (204, 4))



#===============================================================================
# Player class
#===============================================================================

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # properties
        self.lives = 10
        self.oxigen = 99
        self.ammo = 5
        self.keys = 0
        self.explosives = 0
        self.dir = enums.RIGHT
        # images
        num_frames = 3
        self.images = []
        for i in range(num_frames):
            # image for the frame
            self.images.append(pygame.image.load(
                jp(dp, 'images/sprites/player{}.png'.format(i))).convert())
            # mask
            self.images[i].set_colorkey((255, 0, 255))
        self.animation_index = 0
        self.animation_speed = 0.08
        self.image = self.images[self.animation_index]
        # initial position
        self.rect = self.image.get_rect()
        self.rect.x = 32
        self.rect.y = 112

    def update(self):
        # animation
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.images):
            self.animation_index = 0
        self.image = self.images[int(self.animation_index)]
        # movement
        self.mx = 0
        self.my = 0
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_o]:
            self.mx -= 1
            self.dir = enums.LEFT
        if key_state[pygame.K_p]:
            self.mx += 1
            self.dir = enums.RIGHT
        if key_state[pygame.K_q]:
            self.my -= 1
            self.dir = enums.UP
        if key_state[pygame.K_a]:            
            self.my += 1
            self.dir = enums.DOWN
        self.rect.x += self.mx
        self.rect.y += self.my
        # tilemap collisions
        index = self.rect.collidelist(tilemap_rect_list) 
        if index >= 0:
            beh = tilemap_behaviour_list[index]
            if beh == enums.OBSTACLE:
                self.rect.x -= self.mx
                self.rect.y -= self.my



#===============================================================================
# Enemy class
#===============================================================================

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_data): # x1, y1, x2, y2, mx, my, type
        super(Enemy, self).__init__()
        # max/min xy values
        self.x = self.x1 = enemy_data[0]
        self.y = self.y1 = enemy_data[1]
        self.x2 = enemy_data[2]
        self.y2 = enemy_data[3]
        # movement
        self.mx = enemy_data[4] / 2
        self.my = enemy_data[5] / 2
        # enemy type
        self.type = enemy_data[6]
        if self.type == 1:
            enemy_name = 'infected'
        elif self.type == 2:
            enemy_name = 'pelusoid'
        elif self.type == 3:
            enemy_name = 'avirus'
        elif self.type == 4:
            enemy_name = 'platform'
        elif self.type == 6:
            enemy_name = 'fanty'
            self.state = 0 # 0=idle  1=pursuing  2=retreating
            self.sight_distance = 64
            self.acceleration = 16
            self.max_speed = 256
        # images
        num_frames = 2
        self.images = []
        for i in range(num_frames):
            # image for the frame
            self.images.append(pygame.image.load(
                jp(dp, 'images/sprites/' + enemy_name + str(i) + '.png')).convert())
            # mask
            self.images[i].set_colorkey((255, 0, 255))
        self.animation_index = 0
        self.animation_speed = 0.08
        self.image = self.images[self.animation_index]
        self.rect = self.image.get_rect()

    def update(self):
        # animation
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.images):
            self.animation_index = 0
        self.image = self.images[int(self.animation_index)]
        # movement
        if self.type != 6: # no fanty  
            self.x += self.mx
            self.y += self.my
            if self.x == self.x1 or self.x == self.x2:
                self.mx = -self.mx
            if self.y == self.y1 or self.y == self.y2:
                self.my = -self.my
        else: # fanty
            if self.state == 0: # idle
                if distance(0, 0, self.x, self.y) <= self.sight_distance:
                    self.state = 1 # pursuing
            elif self.state == 1: # pursuing
                if distance(0, 0, self.x, self.y) > self.sight_distance:
                    self.state = 2 # retreating
                else:
                    #en_an [gpit].vx = limit(en_an [gpit].vx + addsign (player.x - en_an [gpit].x, FANTY_A),-FANTY_MAX_V, FANTY_MAX_V)
                    #en_an [gpit].vy = limit(en_an [gpit].vy + addsign (player.y - en_an [gpit].y, FANTY_A),-FANTY_MAX_V, FANTY_MAX_V)                        
                    #en_an [gpit].x = limit(en_an [gpit].x + en_an [gpit].vx, 0, 14336)
                    #en_an [gpit].y = limit(en_an [gpit].y + en_an [gpit].vy, 0, 9216) 
                    pass               
            else: # retreating
                #en_an [gpit].x += addsign(malotes [enoffsmasi].x - gpen_cx, 64)
                #en_an [gpit].y += addsign(malotes [enoffsmasi].y - gpen_cy, 64)                
                if distance (0, 0, self.x, self.y) <= self.sight_distance:
                    self.state = 1 # pursuing					
                        				
            #gpen_cx = en_an [gpit].x >> 6;
            #gpen_cy = en_an [gpit].y >> 6;
            if self.state == 2 and self.x == self.x1 and self.y == self.y1:
                self.state = 0 # idle

        self.rect.x = self.x
        self.rect.y = self.y





#===============================================================================
# Main functions
#===============================================================================

def confirm_exit():
    message_box('Leave the current game?', 'PRESS Y TO EXIT OR N TO CONTINUE')
    screen.blit(pygame.transform.scale(sboard_display, constants.SBOARD_SCALED_SIZE), 
        (constants.H_MARGIN, constants.V_MARGIN))        
    screen.blit(pygame.transform.scale(map_display, constants.MAP_SCALED_SIZE), 
        (constants.H_MARGIN, constants.SBOARD_SCALED_SIZE[1] + constants.V_MARGIN))
    make_scanlines()
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

#dumps and scales surfaces to the screen
def refresh_screen():
    # scale x 3 the scoreboard
    screen.blit(pygame.transform.scale(sboard_display, constants.SBOARD_SCALED_SIZE), 
        (constants.H_MARGIN, constants.V_MARGIN))
    # scale x 3 the map
    screen.blit(pygame.transform.scale(map_display, constants.MAP_SCALED_SIZE), 
        (constants.H_MARGIN, constants.SBOARD_SCALED_SIZE[1] + constants.V_MARGIN))
    make_scanlines()
    #pygame.display.update() # refreshes the screen
    clock.tick(60) # 60 FPS
    
# Main menu
def main_menu():
    map_display.fill(constants.PALETTE['BLACK'])
    sboard_display.fill(constants.PALETTE['BLACK'])
    message_box('Red Planet Pi', 'WIP. Press a key to continue')
    refresh_screen()
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

# checks if the map needs to be changed (depending on the player's XY position)
def check_map_change(x, y):
    global map_number
    # player disappears on the left
    # appearing from the right on the new map
    if x < -16:
        map_number -= 1
        player.rect.right = constants.MAP_UNSCALED_SIZE[0]
    # player disappears on the right
    # appearing from the left on the new map
    elif x > constants.MAP_UNSCALED_SIZE[0]:
        map_number += 1
        player.rect.left = 0
    # player disappears over the top
    # appearing at the bottom of the new map
    elif y < (-16):
        map_number -= 5
        player.rect.bottom = constants.MAP_UNSCALED_SIZE[1]
    # player disappears from underneath
    #appearing at the top of the new map
    elif y > constants.MAP_UNSCALED_SIZE[1]:
        map_number += 5
        player.rect.top = 0

# makes a screen transition between the old map and the new one.
def map_transition():
    # surfaces to save the old and the new map together
    map_trans_horiz = pygame.Surface(
        (constants.MAP_UNSCALED_SIZE[0]*2, constants.MAP_UNSCALED_SIZE[1]))
    map_trans_vert = pygame.Surface(
        (constants.MAP_UNSCALED_SIZE[0], constants.MAP_UNSCALED_SIZE[1]*2))

    if player.dir == enums.UP:
        # joins the two maps on a single surface
        map_trans_vert.blit(map_display_backup, (0,0))
        map_trans_vert.blit(map_display_backup_old, (0, constants.MAP_UNSCALED_SIZE[1]))
        # scrolls the two maps across the screen
        for y in range(-constants.MAP_UNSCALED_SIZE[1], 0, 4):
            map_display.blit(map_trans_vert, (0, y))
            refresh_screen()
    elif player.dir == enums.DOWN:
        # joins the two maps on a single surface
        map_trans_vert.blit(map_display_backup_old, (0,0))
        map_trans_vert.blit(map_display_backup, (0, constants.MAP_UNSCALED_SIZE[1]))
        # scrolls the two maps across the screen
        for y in range(0, -constants.MAP_UNSCALED_SIZE[1], -4):
            map_display.blit(map_trans_vert, (0, y))
            refresh_screen()
    elif player.dir == enums.LEFT:
        # joins the two maps on a single surface
        map_trans_horiz.blit(map_display_backup, (0,0))
        map_trans_horiz.blit(map_display_backup_old, (constants.MAP_UNSCALED_SIZE[0], 0))
        # scrolls the two maps across the screen
        for x in range(-constants.MAP_UNSCALED_SIZE[0], 0, 6):
            map_display.blit(map_trans_horiz, (x, 0))
            refresh_screen()
    elif player.dir == enums.RIGHT:
        # joins the two maps on a single surface
        map_trans_horiz.blit(map_display_backup_old, (0,0))
        map_trans_horiz.blit(map_display_backup, (constants.MAP_UNSCALED_SIZE[0], 0))
        # scrolls the two maps across the screen
        for x in range(0, -constants.MAP_UNSCALED_SIZE[0], -6):
            map_display.blit(map_trans_horiz, (x, 0))
            refresh_screen()



#===============================================================================
# Main
#===============================================================================

# initialisation
pygame.init()
pygame.mixer.init()

# reads the configuration file and applies the personal settings
config.read_config()

# generates a main window (or full screen) 
# with title, icon, and 32-bit colour.
flags = 0
if config.cfg_full_screen:
    flags = pygame.FULLSCREEN
screen = pygame.display.set_mode(constants.WIN_SIZE, flags, 32)
pygame.display.set_caption('.:: Red Planet Pi ::.')
icon = pygame.image.load(jp(dp, 'images/assets/icon.png')).convert_alpha()
pygame.display.set_icon(icon)  

# area covered by the map
map_display = pygame.Surface(constants.MAP_UNSCALED_SIZE)
# surface to save the generated map without sprites
map_display_backup = pygame.Surface(constants.MAP_UNSCALED_SIZE)
# area covered by the scoreboard
sboard_display = pygame.Surface(constants.SBOARD_UNSCALED_SIZE)
# surface to save the previous map (transition effect between screens)
if config.cfg_map_transition:
    map_display_backup_old = pygame.Surface(constants.MAP_UNSCALED_SIZE)
# surface for HQ scanlines
if config.cfg_scanlines_type == 2:
    screen_sl = pygame.Surface(constants.WIN_SIZE)
    screen_sl.set_alpha(40)

# fonts
fg_font_S = texts.Font('images/fonts/small_font.png', constants.PALETTE['GREEN'], True)
bg_font_S = texts.Font('images/fonts/small_font.png', constants.PALETTE['DARK_GREEN'], False)
fg_font_L = texts.Font('images/fonts/large_font.png', constants.PALETTE['WHITE'], True)
bg_font_L = texts.Font('images/fonts/large_font.png', constants.PALETTE['DARK_GRAY'], True)
aux_font_L = texts.Font('images/fonts/large_font.png', constants.PALETTE['YELLOW'], False)

# scoreboard icons
lives_icon = pygame.image.load(jp(dp, 'images/assets/lives.png')).convert()
oxigen_icon = pygame.image.load(jp(dp, 'images/tiles/T53.png')).convert()
ammo_icon = pygame.image.load(jp(dp, 'images/tiles/T52.png')).convert()
keys_icon = pygame.image.load(jp(dp, 'images/tiles/T51.png')).convert()
explosives_icon = pygame.image.load(jp(dp, 'images/tiles/T50.png')).convert()

# clock to control the FPS
clock = pygame.time.Clock()

game_status = enums.OVER
music_status = enums.UNMUTED 

# Main loop
while True:    
    if game_status == enums.OVER: # game not running
        #main_menu()
        # sprite control groups
        all_sprites_group = pygame.sprite.Group()     
        enemies_group = pygame.sprite.Group()
        # create the player
        player = Player()
        # ingame music
        pygame.mixer.music.load(jp(dp, "sounds/ingame.ogg"))
        #pygame.mixer.music.play(-1)
        # reset variables
        game_status = enums.RUNNING
        map_number = 0
        last_map = -1
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
                if event.key == pygame.K_h:
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
                if event.key == pygame.K_m :
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
            load_map(map_number, map_display)
            # preserves the previous 
            if config.cfg_map_transition:
                map_display_backup_old.blit(map_display_backup, (0,0))
            # save the new empty background
            map_display_backup.blit(map_display, (0,0))
            draw_map_info()
            init_scoreboard()
            update_scoreboard()
            last_map = map_number
            # performs the screen transition
            if config.cfg_map_transition:
                map_transition()        
            # reset the groups  
            all_sprites_group.empty()
            enemies_group.empty()
            # add the player  
            all_sprites_group.add(player)
            # add enemies to the map reading from 'ENEMIES_DATA' list (enems.h)
            # (a maximum of three enemies per map)
            for i in range(3):
                enemy_data = constants.ENEMIES_DATA[map_number*3 + i]
                if enemy_data[6] != 0: # no enemy
                    enemy = Enemy(enemy_data)
                    all_sprites_group.add(enemy)
                    enemies_group.add(enemy)

        if game_status == enums.RUNNING:
            # update sprites
            all_sprites_group.update()
            # collisions
            if player.lives == 0:
                # print game over message
                game_status = enums.OVER
            # paint the map free of sprites to clean it up
            map_display.blit(map_display_backup, (0,0))
            # and change the frame of the animated tiles
            animate_tiles()
            # print sprites
            all_sprites_group.draw(map_display)
            # check map change using player's coordinates
            check_map_change(player.rect.x, player.rect.y)
        elif game_status == enums.PAUSED:            
            message_box('P a u s e', 'THE MASSACRE CAN WAIT')

    # FPS counter using the clock   
    aux_font_L.render(str(int(clock.get_fps())).rjust(3, '0') + ' FPS', sboard_display, (124, 22))

    refresh_screen()
