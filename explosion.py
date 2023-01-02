
#===============================================================================
# Explosion class
#===============================================================================

import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos, blast_animation):
        super().__init__()
        self.frame_index = 0 # frame number
        self.animation_speed = 0.15 # frame dwell time     
        self.frames = blast_animation # image list
        self.image = self.frames[0] # first frame
        self.rect = self.image.get_rect(center = pos) # position
        
    # loads next frame of animation or ends
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames): # end of the animation
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)] # next frame

    def update(self):
        self.animate()