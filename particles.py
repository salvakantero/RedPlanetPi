import pygame

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self,pos, dust_animation):
        super().__init__()
        self.frame_index = 0 # nº de frame
        self.animation_speed = 0.5 # velocidad de animación        
        self.frames = dust_animation # carga la lista de imágenes
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    # carga el frame siguiente de la animación o termina
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    # actualiza y hace scroll
    def update(self):
        self.animate()