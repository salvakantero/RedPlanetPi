
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
NONE, INFECTED, AVIRUS, PELUSOID, PLATFORM_SPR, FANTY = 0, 1, 2, 3, 4, 6