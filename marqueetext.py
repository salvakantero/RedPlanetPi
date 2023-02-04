
#===============================================================================
# MarqueeText class
#===============================================================================

import pygame
import constants

class MarqueeText():
    def __init__(self, surface, font, y, speed, text, text_width):
        # attributes
        self.surface = surface    
        self.font = font
        self.x = surface.get_width() # to the far right
        self.y = y  
        self.speed = speed # in pixels
        self.text = text
        self.text_width = text_width # in pixels

    # update the xy position
    def update(self):
        # draws the text in the new position       
        self.x -= self.speed
        self.font.render(self.text, self.surface, (self.x, self.y))
        # resets when a certain number of pixels are shifted
        if self.x < -self.text_width: self.x = self.surface.get_width()