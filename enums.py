
#===============================================================================
# Enumerations
#===============================================================================

# tile behaviours
NO_ACTION, OBSTACLE, PLATFORM_TILE, ITEM, KILLER, DOOR = 0, 1, 2, 3, 4, 5 
# game states
RUNNING, PAUSED, OVER = 0, 1, 2
# directions
UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
# music states
UNMUTED, MUTED = 0, 1
# player states
IDLE, WALKING, JUMPING, FALLING = 0, 1, 2, 3
# enemy types (and platform)
NONE, INFECTED, PELUSOID, AVIRUS, PLATFORM_SPR, FANTY = 0, 1, 2, 3, 4, 5
# fanty enemy states
IDLE, CHASING, RETREATING = 0, 1, 2
# hotspot types
TNT, KEY, AMMO, OXYGEN, DOOR = 0, 1, 2, 3, 4
# fonts
SM_GREEN_FG, SM_GREEN_BG, LG_WHITE_FG, LG_WHITE_BG, SM_TEST = 0, 1, 2, 3, 4
# menu
START, LOAD, OPTIONS, EXIT = 0, 1, 2, 3
