#===============================================================================
# Global variables
#===============================================================================

import os # path()

dp = os.path.dirname(__file__) + '/' # exec path (+ '/' when using VS Code)
jp = os.path.join # forms the folder/file path

map_number = 0 # current map number
last_map = -1 # last map loaded
game_percent = 0 # % of gameplay completed

tilemap_rect_list = [] # list of tile rects
tilemap_behaviour_list = [] # list of tile behaviours
anim_tiles_list = [] # (frame_1, frame_2, x, y, num_frame)

