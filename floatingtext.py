
#===============================================================================
# FloatingText class
#===============================================================================

import constants
from font import Font

class FloatingText():
    def __init__(self, surface):
        # attributes
        self.surface = surface    
        self.font = Font('images/fonts/small_font.png', constants.PALETTE['YELLOW'], True)
        self.font2 = Font('images/fonts/small_font.png', constants.PALETTE['BROWN'], True) 
        self.acceleration = 0.05 
        self.x = 0
        self.y = 0    
        self.speed = 0
        self.text = ''

    # update the xy position (only if drawn inside the screen)
    def update(self):
        if self.y > 0:
            self.speed += self.acceleration
            self.y -= self.speed
            self.font2.render(self.text, self.surface, (self.x+1, self.y+1))
            self.font.render(self.text, self.surface, (self.x, self.y))
        else:
            self.speed = 0
