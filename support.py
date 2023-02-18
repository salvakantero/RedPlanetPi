
#===============================================================================
# .::Generic functions::.
# Stand-alone utilities to be called from any part of the code
#===============================================================================
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
import math
import sys
import constants
import enums

# draws scanlines
def scanlines(surface, height, from_x, to_x, rgb):
    j = constants.V_MARGIN # Y axis
    while j < height:
        j+=3
        pygame.draw.line(surface, (rgb, rgb, rgb), (from_x, j), (to_x, j))

# applies scanlines according to the configuration
def make_scanlines(surface, surface_hq, config):
    if config.scanlines_type == 2: # HQ
        scanlines(surface_hq, constants.WIN_SIZE[1]-30, constants.H_MARGIN, 
            constants.WIN_SIZE[0]-constants.H_MARGIN-1, 200)
        surface.blit(surface_hq, (0, 0))
    elif config.scanlines_type == 1: # fast
        scanlines(surface, constants.WIN_SIZE[1]-30, constants.H_MARGIN, 
            constants.WIN_SIZE[0]-constants.H_MARGIN-1, 15)

# draws a centred message box erasing the background
def message_box(msg1, msg2, surface, font):
    height = 36
    # calculates the width of the box
    message1_len = len(msg1) * 7 # approximate length of text 1 in pixels
    message2_len = len(msg2) * 4 # approximate length of text 2 in pixels
    # width = length of the longest text + margin
    if message1_len > message2_len:
        width = message1_len + constants.V_MARGIN
    else:
        width = message2_len + constants.V_MARGIN
    # calculates the position of the box
    x = (constants.MAP_UNSCALED_SIZE[0]//2) - (width//2)
    y = (constants.MAP_UNSCALED_SIZE[1]//2) - (height//2)
    # black window
    pygame.draw.rect(surface, constants.PALETTE['BLACK'],(x, y, width, height))
    # blue border
    pygame.draw.rect(surface, constants.PALETTE['DARK_BLUE'],(x, y, width, height), 1)
    # draws the text centred inside the window (Y positions are fixed)
    text_x = (x + (width//2)) - (message1_len//2)
    text_y = y + 5
    font[enums.LG_WHITE_BG].render(msg1, surface, (text_x, text_y))
    font[enums.LG_WHITE_FG].render(msg1, surface, (text_x - 2, text_y - 2))
    text_x = (x + (width//2)) - (message2_len//2)
    text_y = y + 25
    font[enums.SM_GREEN_BG].render(msg2, surface, (text_x, text_y))
    font[enums.SM_GREEN_FG].render(msg2, surface, (text_x - 1, text_y - 1))

# leaves the programme entirely
def exit():
    pygame.quit()
    sys.exit()

# changes a sign value according to the sign of another value
def addsign (n, value):
    if n >= 0: return value
    else: return -value

# calculates the distance between two points
def distance (x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

# maintains a value within limits
def limit(val, min, max):
    if val < min: return min
    elif val > max: return max
    return val

# change one colour for another
def swap_color(image, old_color, new_color):
    image.set_colorkey(old_color)
    surf = image.copy()
    surf.fill(new_color)
    surf.blit(image,(0,0))
    return surf

# returns a part of the surface
def clip(surf, x, y, x_size, y_size):
    handle_surf = surf.copy()
    handle_surf.set_clip(pygame.Rect(x, y, x_size, y_size))
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()

# draws a text with its shadow
def shaded_text(font_BG, font_FG, text, surface, x, y, offset):           
    font_BG.render(text, surface, (x, y))  # shadow
    font_FG.render(text, surface, (x-offset, y-offset))

# the ESC, RETURN or SPACE key has been pressed.
def main_key_pressed():
    for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return True