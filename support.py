#===============================================================================
# Generic functions
#===============================================================================

import pygame
import constants

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
def message_box(msg1, msg2, surface, font_BL, font_FL, font_BS, font_FS):
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
    font_BL.render(msg1, surface, (text_x, text_y))
    font_FL.render(msg1, surface, (text_x - 2, text_y - 2))
    text_x = (x + (width//2)) - (message2_len//2)
    text_y = y + 25
    font_BS.render(msg2, surface, (text_x, text_y))
    font_FS.render(msg2, surface, (text_x - 1, text_y - 1))

