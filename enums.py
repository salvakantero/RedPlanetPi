
# ==============================================================================
# .::Enumerations::.
# Values that are named to clarify the source code.
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
