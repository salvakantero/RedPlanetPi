
#===============================================================================
# Constants
#===============================================================================

WIN_SIZE = 800, 640 # main window size
MAP_SCALED_SIZE = 720, 480 # map size (scaled x3)
MAP_UNSCALED_SIZE = 240, 160 # map size (unscaled)
SBOARD_SCALED_SIZE = 720, 114 # scoreboard size (scaled x3)
SBOARD_UNSCALED_SIZE = 240, 38 # scoreboard size (unscaled)
H_MARGIN = 40 # horizontal distance between the edge and the playing area
V_MARGIN = 20 # vertical distance between the edge and the playing area
JUMP_VALUE = -3.2 # value of the initial jump for the player
GRAVITY = 0.180 # acceleration of gravity for the player
MAX_Y_SPEED = 2.9 # maximum limit for vertical speed

# animated tiles
ANIM_TILES = {
    # frame_1   frame_2
    'T4.png' : 'T80.png',   # computer 1
    'T8.png' : 'T81.png',   # computer 2
    'T9.png' : 'T82.png',   # corpse
    'T70.png' : 'T83.png',  # toxic waste
    'T71.png' : 'T84.png'   # lava
}

# colour palette (Pico8)
PALETTE = {
    'BLACK': (0, 0, 0),
    'DARK_BLUE' : (35, 50, 90),
    'PURPLE' : (126, 37, 83),
    'DARK_GREEN' : (0, 135, 81),
    'BROWN' : (171, 82, 54),
    'DARK_GRAY' : (95, 87, 79),
    'GRAY' : (194, 195, 199),
    'WHITE' : (255, 241, 232),
    'RED' : (255, 0, 77),
    'ORANGE' : (255, 163, 0),
    'YELLOW' : (255, 236, 39),
    'GREEN' : (0, 228, 54),
    'CYAN' : (41, 173, 255),
    'MALVA' : (131, 118, 156),
    'PINK' : (255, 119, 168),
    'SAND' : (255, 204, 170)
}

# screen names
MAP_NAMES = {
    # level 1
    0  : 'CONTROL CENTRE',
    1  : 'SUPPLY DEPOT 1',
    2  : 'CENTRAL HALL',
    3  : 'TOXIC WASTE STORAGE 1A',
    4  : 'TOXIC WASTE STORAGE 1B',
    5  : 'WEST CORRIDOR',
    6  : 'ACCESS TO WEST CORRIDORS',
    7  : 'CENTRAL HALL',
    8  : 'ACCESS TO DUNGEONS',
    9  : 'DUNGEONS',
    10 : 'WEST CORRIDOR',
    11 : 'SUPPLY DEPOT 2',
    12 : 'CENTRAL HALL',
    13 : 'ACCESS TO SOUTHEAST EXIT',
    14 : 'EXIT TO UNDERGROUND',
    # level 2
    15 : 'WAREHOUSE ACCESS',
    16 : 'CONVECTION CORRIDOR',
    17 : 'SEWER MAINTENANCE',
    18 : 'COLD ZONE ACCESS CORRIDOR',
    19 : 'COLD ZONE ACCESS CORRIDOR',
    20 : 'FROZEN WAREHOUSE 1',
    21 : 'CONVECTION CORRIDOR',
    22 : 'TOXIC SEWERS 1',
    23 : 'ICE CAVE',
    24 : 'ACCESS TO ICE CAVE',
    25 : 'FROZEN WAREHOUSE 2',
    26 : 'CONVECTION CORRIDOR',
    27 : 'TOXIC SEWERS 1',
    28 : 'ACCESS TO THE WARM ZONE',
    29 : 'EXIT TO THE WARM ZONE',
    # level 3
    30 : 'PELUSOIDS LAIR',
    31 : 'ALVARITOS GROTTO 2',
    32 : 'ALVARITOS GROTTO 1',
    33 : 'TOXIC WASTE STORAGE 2A',
    34 : 'UNDERGROUND TUNNEL',
    35 : 'SIDE HALL',
    36 : 'ARACHNOVIRUS LAIR',
    37 : 'UNSTABLE CORRIDORS 1',
    38 : 'UNSTABLE CORRIDORS 2',
    39 : 'TOXIC WASTE STORAGE 2B',
    40 : 'SIDE HALL',
    41 : 'ABANDONED MINE 1',
    42 : 'ABANDONED MINE 2',
    43 : 'ABANDONED MINE 3',
    44 : 'EXPLOSIVES STOCKPILE',
    45 : 'BACK TO CONTROL CENTER',
}

# enemies per map (x1, y1, x2, y2, mx, my, type)
# types:
#	1) Infected
#	2) Pelusoid
#	3) Arachnovirus
#	4) Mobile platform
#	6) Fanty

ENEMIES_DATA = [
    #-----------LEVEL 1-------------
    # 0 CONTROL CENTRE
    [128, 112, 32, 112, -2, 0, 1],
	[16, 16, 224, 48, 2, 2, 2],
	[0, 0, 0, 0, 0, 0, 0],
    # 1 SUPPLY DEPOT 1
	[192, 112, 32, 112, -4, 0, 1],
	[208, 16, 144, 64, -1, 1, 2],
	[80, 64, 80, 16, 0, -2, 3],
    # 2 CENTRAL HALL  
	[112, 144, 112, 32, 0, -2, 4],
	[208, 112, 16, 80, -2, -2, 2],
	[0, 0, 0, 0, 0, 0, 0],
    # 3 TOXIC WASTE STORAGE 1A
	[160, 48, 32, 48, -4, 0, 1],
	[16, 80, 208, 112, 4, 4, 3],
	[0, 0, 0, 0, 0, 0, 0],
    # 4 TOXIC WASTE STORAGE 1B
	[64, 80, 64, 16, 0, -2, 3],
	[144, 16, 144, 128, 0, 2, 3],
	[208, 112, 208, 96, 0, -2, 6],
    # 5 WEST CORRIDOR
	[32, 48, 192, 48, 2, 0, 1],
	[192, 80, 32, 80, -2, 0, 1],
	[144, 128, 160, 128, 2, 0, 6],
    # 6 ACCESS TO THE WEST CORRIDORS
	[96, 48, 48, 16, -2, -2, 3],
	[144, 80, 144, 16, 0, -2, 3],
	[16, 112, 16, 96, 0, -2, 6],
    # 7 CENTRAL HALL
	[112, 144, 112, 16, 0, -2, 4],
	[208, 96, 16, 96, -2, 0, 3],
	[16, 32, 192, 64, 1, 1, 2],
    # 8 ACCESS TO DUNGEONS
	[208, 64, 192, 64, -2, 0, 6],
	[64, 64, 64, 32, 0, -1, 3],
	[0, 0, 0, 0, 0, 0, 0],
    # 9 DUNGEONS
	[144, 128, 144, 16, 0, -4, 3],
	[80, 16, 80, 128, 0, 4, 3],
	[192, 128, 208, 128, 2, 0, 6],
    # 10 WEST CORRIDOR
	[128, 128, 144, 128, 2, 0, 6],
	[176, 64, 160, 16, -2, -2, 3],
	[32, 16, 16, 64, -2, 2, 3],
    # 11 SUPPLY DEPOT 2
	[192, 80, 32, 80, -4, 0, 1],
	[32, 48, 192, 48, 4, 0, 1],
	[192, 16, 32, 16, -4, 0, 1],
    # 12 CENTRAL HALL
	[112, 128, 112, 16, 0, -2, 4],
	[208, 96, 32, 96, -2, 0, 2],
	[16, 48, 208, 48, 2, 0, 2],
    # 13 ACCESS TO SOUTHEAST EXIT
	[128, 112, 144, 112, 2, 0, 6],
	[144, 128, 208, 128, 2, 0, 1],
	[16, 80, 48, 16, 2, -2, 2],
    # 14 EXIT TO UNDERGROUND
	[112, 128, 112, 16, 0, -4, 3],
	[48, 16, 48, 128, 0, 4, 3],
	[96, 16, 96, 128, 0, 2, 3],
    
    #-----------LEVEL 2-------------
    # 15 WAREHOUSE ACCESS
    [32, 96, 32, 112, 0, 1, 6],
	[192, 16, 128, 128, -2, 2, 2],
	[0, 0, 0, 0, 0, 0, 0],
    # 16 CONVECTION CORRIDOR
    [176, 48, 64, 48, -1, 0, 1],
	[48, 128, 32, 16, -2, -2, 3],
	[64, 48, 176, 48, 2, 0, 1],
    # 17 SEWER MAINTENANCE
    [64, 16, 80, 128, 2, 2, 2],
	[96, 32, 160, 32, 2, 0, 1],
	[16, 96, 16, 16, 0, -2, 3],
    # 18 COLD ZONE ACCESS CORRIDOR
    [48, 112, 208, 80, 2, -2, 2],
	[192, 48, 48, 16, -2, -2, 2],
	[16, 80, 16, 16, 0, -1, 3],
    # 19 COLD ZONE ACCESS CORRIDOR
	[32, 48, 192, 48, 2, 0, 1],
	[160, 112, 112, 112, -2, 0, 1],
    [0, 0, 0, 0, 0, 0, 0],
    # 20 FROZEN WAREHOUSE 1
	[112, 48, 32, 48, -2, 0, 1],
	[144, 128, 144, 80, 0, -2, 3],
	[64, 128, 64, 80, 0, -2, 3], 
    # 21 CONVECTION CORRIDOR
	[112, 112, 112, 16, 0, -4, 4],
	[208, 128, 144, 16, -2, -2, 2],
	[80, 16, 32, 128, -2, 2, 2],  
    # 22 TOXIC SEWERS 1
	[48, 112, 48, 16, 0, -2, 4],
	[144, 32, 192, 32, 2, 0, 1],
	[80, 16, 80, 112, 0, 4, 3],
    # 23 ICE CAVE
	[160, 112, 80, 32, -2, -2, 2],
	[160, 32, 80, 112, -2, 2, 2],
	[48, 48, 64, 96, 2, 2, 3],    
    # 24 ACCESS TO ICE CAVE
	[144, 32, 144, 112, 0, 4, 3],
	[80, 96, 80, 48, 0, -2, 3],
	[176, 128, 176, 16, 0, -4, 3],
    # 25 FROZEN WAREHOUSE 2
	[80, 32, 80, 16, 0, -1, 6],
	[96, 128, 96, 96, 0, -2, 3],
	[160, 64, 176, 16, 2, -2, 3],
    # 26 CONVECTION CORRIDOR
	[48, 112, 176, 112, 2, 0, 4],
	[32, 32, 208, 32, 4, 0, 3],
	[192, 64, 48, 64, -4, 0, 3],
    # 27 TOXIC SEWERS 1
	[144, 128, 144, 16, 0, -4, 3],
	[80, 16, 80, 112, 0, 4, 3],
	[96, 32, 128, 32, 1, 0, 1],
    # 28 ACCESS TO THE WARM ZONE
	[160, 80, 208, 16, 2, -2, 2],
	[144, 32, 80, 16, -2, -2, 3],
	[64, 80, 32, 16, -2, -2, 2],
    # 29 EXIT TO THE WARM ZONE
	[112, 16, 160, 128, 4, 4, 2],
	[64, 32, 32, 128, -2, 2, 2],
	[16, 48, 16, 16, 0, -1, 3],

    #-----------LEVEL 3-------------
    # 30 PELUSOIDS LAIR
	[80, 128, 112, 128, 2, 0, 6],
	[112, 112, 144, 112, 2, 0, 2],
	[0, 0, 0, 0, 0, 0, 0],
    # 31 ALVARITOS GROTTO 2
	[192, 64, 32, 32, -2, -2, 2],
	[48, 128, 224, 112, 2, -2, 2],
	[16, 64, 32, 64, 2, 0, 6],
    # 32 ALVARITOS GROTTO 1
	[160, 128, 160, 16, 0, -4, 3],
	[112, 32, 112, 128, 0, 4, 3],
	[64, 128, 16, 16, -4, -4, 2],
    # 33 TOXIC WASTE STORAGE 2A
	[192, 96, 32, 96, -4, 0, 1],
	[32, 64, 192, 64, 2, 0, 1],
	[192, 32, 32, 32, -4, 0, 1],
    # 34 UNDERGROUND TUNNEL
	[64, 16, 64, 128, 0, 4, 3],
	[112, 128, 112, 16, 0, -4, 3],
	[16, 112, 16, 16, 0, -4, 3],
    # 35 SIDE HALL
	[112, 144, 112, 16, 0, -2, 4],
	[208, 144, 16, 48, -1, -1, 3],
	[128, 16, 128, 144, 0, 4, 3],
    # 36 ARACHNOVIRUS LAIR
	[160, 128, 96, 128, -2, 0, 3],
	[208, 128, 208, 96, 0, -1, 3],
	[80, 112, 128, 112, 1, 0, 0],
    # 37 UNSTABLE CORRIDORS 1
	[64, 128, 48, 32, -2, -2, 2],
	[208, 128, 208, 32, 0, -4, 3],
	[128, 32, 160, 112, 2, 2, 2],
    # 38 UNSTABLE CORRIDORS 2
	[16, 32, 32, 128, 2, 2, 2],
	[128, 128, 128, 32, 0, -4, 3],
	[160, 32, 160, 128, 0, 4, 3],
    # 39 TOXIC WASTE STORAGE 2B
	[48, 32, 192, 64, 4, 4, 2],
	[48, 128, 192, 128, 4, 0, 1],
	[192, 96, 64, 96, -2, 0, 1],
    # 40 SIDE HALL
	[112, 128, 112, 16, 0, -2, 4],
	[208, 48, 16, 48, -2, 0, 3],
	[16, 96, 208, 96, 4, 0, 3],
    # 41 ABANDONED MINE 1
	[192, 128, 32, 128, -4, 0, 1],
	[80, 32, 192, 32, 4, 0, 1],
	[16, 32, 32, 32, 2, 0, 6],
    # 42 ABANDONED MINE 2
	[160, 32, 160, 128, 0, 4, 3],
	[192, 128, 96, 128, -1, 0, 1],
	[112, 32, 112, 128, 0, 2, 0],
    # 43 ABANDONED MINE 3
	[112, 128, 128, 128, 2, 0, 6],
	[32, 32, 32, 128, 0, 2, 3],
	[96, 48, 176, 48, 4, 0, 1],
    # 44 EXPLOSIVES STOCKPILE
	[128, 32, 128, 48, 0, 2, 6],
	[0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0]
]
