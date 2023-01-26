
#===============================================================================
# FloatingText class
#===============================================================================

import pygame
import constants
import enums

class FloatingText():
    def __init__(self, surface, font):
        # attributes
        self.surface = surface    
        self.font = font  
        self.acceleration = 0.1 
        self.x = 0
        self.y = 0    
        self.text = ''

    # update the xy position
    def update(self):
        if self.y > 0:
            self.y -= self.acceleration
            self.font.render(self.text, self.surface, (self.x, self.y))
