#===============================================================================
# Font functions
#===============================================================================

import os
from support import *



# draws text with border
def outlined_text(bg_font, fg_font, t, surf, pos):
    bg_font.render(t, surf, [pos[0] - 1, pos[1]])
    bg_font.render(t, surf, [pos[0] + 1, pos[1]])
    bg_font.render(t, surf, [pos[0], pos[1] - 1])
    bg_font.render(t, surf, [pos[0], pos[1] + 1])
    fg_font.render(t, surf, [pos[0], pos[1]])



# generates the letters (and letter spacing) from the font image
def load_font_img(path, font_color, is_transparent):
    fg_color = (255, 0, 0) # original red
    bg_color = (0, 0, 0) # black
    font_img = pygame.image.load(
        os.path.join(os.path.dirname(__file__) + "/",path)).convert() # load font image
    font_img = swap_color(font_img, fg_color, font_color) # apply the requested font colour
    last_x = 0
    letters = []
    letter_spacing = []
    for x in range(font_img.get_width()): # for the entire width of the image
        if font_img.get_at((x, 0))[0] == 127: # gray separator
            # saves in the array the portion of the image with the letter we are interested in.
            letters.append(clip(font_img, last_x, 0, x - last_x, font_img.get_height()))
            # saves the width of the letter
            letter_spacing.append(x - last_x)
            last_x = x + 1
        x += 1
    if is_transparent:
        # erases the background colour of each letter in the array
        for letter in letters:
            letter.set_colorkey(bg_color) 

    return letters, letter_spacing, font_img.get_height()



# creates a new font from an image path and a colour
class Font():
    def __init__(self, path, color, transparent):
        self.letters, self.letter_spacing, self.line_height = load_font_img(path, color, transparent)
        self.font_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
        'N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e',
        'f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w',
        'x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5',
        '6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';']
        self.space_width = self.letter_spacing[0]
        self.base_spacing = 1
        self.line_spacing = 2

    # draw the text
    def render(self, text, surf, loc):
        x_offset = 0
        y_offset = 0
        for char in text:
            if char not in ['\n', ' ']:
                # draw the letter and add the width
                surf.blit(self.letters[self.font_order.index(char)], (loc[0] + x_offset, loc[1] + y_offset))
                x_offset += self.letter_spacing[self.font_order.index(char)] + self.base_spacing
            elif char == ' ':
                x_offset += self.space_width + self.base_spacing
            else: # line feed
                y_offset += self.line_spacing + self.line_height
                x_offset = 0
