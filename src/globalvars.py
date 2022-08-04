#===============================================================================
# Global variables
#===============================================================================

import os


dp = os.path.dirname(__file__) + "/" # exec path (+ "/" when using VS Code)
jp = os.path.join # forms the folder/file path

win_size = 800, 600 # main window size
map_scaled_size = 720, 480 # map size (scaled x3)
map_unscaled_size = 240, 160 # map size (unscaled)
sboard_scaled_size = 720, 114 # scoreboard size (scaled x3)
sboard_unscaled_size = 240, 38 # scoreboard size (unscaled)
map_number = 0 # current map number
last_map = -1 # last map loaded
game_percent = 0 # % of gameplay completed
lives = 10 # remaining player lives
oxigen = 99 # remaining player oxigen
ammo = 5 # bullets available in the gun
keys = 0 # unused keys collected
explosives = 0 # explosives collected

# configuration values
cfg_scanlines_type = 2  # 0 = none, 1 = fast, 2 = HQ

# colour palette (Pico8)
pal = {
    "BLACK":(0, 0, 0),
    "DARK_BLUE" : (35, 50, 90),
    "PURPLE" : (126, 37, 83),
    "DARK_GREEN" : (0, 135, 81),
    "BROWN" : (171, 82, 54),
    "DARK_GRAY" : (95, 87, 79),
    "GRAY" : (194, 195, 199),
    "WHITE" : (255, 241, 232),
    "RED" : (255, 0, 77),
    "ORANGE" : (255, 163, 0),
    "YELLOW" : (255, 236, 39),
    "GREEN" : (0, 228, 54),
    "CYAN" : (41, 173, 255),
    "MALVA" : (131, 118, 156),
    "PINK" : (255, 119, 168),
    "SAND" : (255, 204, 170) 
}

# screen names
map_names = {
    0  : "CONTROL CENTRE",
	1  : "SUPPLY DEPOT 1",
	2  : "CENTRAL HALL LEVEL 0",
	3  : "TOXIC WASTE STORAGE 1A",
    4  : "TOXIC WASTE STORAGE 1B",
	5  : "WEST PASSAGE LEVEL -1",
	6  : "ACCESS TO WEST PASSAGES",
	7  : "CENTRAL HALL LEVEL -1",
	8  : "ACCESS TO DUNGEONS",
	9  : "DUNGEONS",
	10 : "WEST PASSAGE LEVEL -2",
	11 : "SUPPLY DEPOT 2",
	12 : "CENTRAL HALL LEVEL -2",
	13 : "ACCESS TO SOUTHEAST EXIT",
	14 : "EXIT TO UNDERGROUND",
	15 : "PELUSOIDS LAIR",
	16 : "ALVARITOS GROTTO 2",
	17 : "ALVARITOS GROTTO 1",
	18 : "TOXIC WASTE STORAGE 2A",
	19 : "UNDERGROUND TUNNEL",
	20 : "SIDE HALL LEVEL -4",
	21 : "ARACHNOVIRUS LAIR",
	22 : "UNSTABLE CORRIDORS 1",
	23 : "UNSTABLE CORRIDORS 2",
	24 : "TOXIC WASTE STORAGE 2B",
	25 : "SIDE HALL LEVEL -5",
	26 : "ABANDONED MINE 1",
	27 : "ABANDONED MINE 2",
	28 : "ABANDONED MINE 3",
	29 : "EXPLOSIVES STOCKPILE",
    30 : "BACK TO CONTROL CENTER",
}