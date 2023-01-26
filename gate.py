
#===============================================================================
# Gate class
#===============================================================================

import pygame
import constants

class Gate(pygame.sprite.Sprite):
    def __init__(self, gate_data, gate_image):
        super().__init__()
        # gate_data = [x, y, visible?]
        self.x = gate_data[0]
        self.y = gate_data[1]
        # image
        self.image = gate_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x*constants.TILE_SIZE, self.y*constants.TILE_SIZE)