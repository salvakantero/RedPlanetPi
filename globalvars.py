#===============================================================================
# Global variables
#===============================================================================

import pygame

map_number = 0 # current map number
last_map = -1 # last map loaded
game_percent = 0 # % of gameplay completed

tilemap_rect_list = [] # list of tile rects
tilemap_behaviour_list = [] # list of tile behaviours
anim_tiles_list = [] # (frame_1, frame_2, x, y, num_frame)

cfg_full_screen = 0 # 0 = no, 1 = yes
cfg_scanlines_type = 0 # 0 = none, 1 = fast, 2 = HQ   
cfg_map_transition = 0 # 0 = no, 1 = yes

# default keys
left_key = pygame.K_a
right_key = pygame.K_d
jump_key = pygame.K_w
action_key = pygame.K_s
pause_key = pygame.K_h
mute_key = pygame.K_m
