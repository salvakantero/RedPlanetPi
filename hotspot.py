
#===============================================================================
# Hotspot class
#===============================================================================

import pygame

class Hotspot(pygame.sprite.Sprite):
    def __init__(self, hotspot_data, image):
        super().__init__()
        self.type = hotspot_data[0] # TNT, ammo, key, oxygen 
        # hotspot_data = [type, x, y, available]
        self.x = hotspot_data[1]
        self.y = hotspot_data[2]
        self.y_offset = 0 # to animate the hotspot (up and down)
        self.going_up = True # going up?
        self.animation_timer = 2 # timer to change position
        # image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * self.rect.width, self.y * self.rect.height)   

    def update(self):
        # movement
        #if self.animation_timer > 1: # time to change the offset
            #self.animation_timer = 0
        if self.going_up: # goinnnng up
            if self.y_offset < 5: self.y_offset += 1
            else: self.going_up = False
        else: # going down
            if self.y_offset > 0: self.y_offset -= 1                
            else: self.going_up = True            
        # apply the offset
        self.rect.y = (self.y * self.rect.height) - self.y_offset
        #self.animation_timer += 1