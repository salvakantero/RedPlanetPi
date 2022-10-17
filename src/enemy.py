#===============================================================================
# Enemy class
#===============================================================================

import pygame
from globalvars import jp, dp

# calculates the distance between two points
def distance (x1, y1, x2, y2):
    dx = abs(x2-x1)
    dy = abs(y2-y1)
    if dx < dy:
        mn = dx
    else:
        mn = dy
    return(dx + dy - (mn >> 1) - (mn >> 2) + (mn >> 4))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_data): # x1, y1, x2, y2, mx, my, type
        super(Enemy, self).__init__()
        # max/min xy values
        self.x = self.x1 = enemy_data[0]
        self.y = self.y1 = enemy_data[1]
        self.x2 = enemy_data[2]
        self.y2 = enemy_data[3]
        # movement
        self.mx = enemy_data[4] / 2
        self.my = enemy_data[5] / 2
        # enemy type
        self.type = enemy_data[6]
        if self.type == 1:
            enemy_name = 'infected'
        elif self.type == 2:
            enemy_name = 'pelusoid'
        elif self.type == 3:
            enemy_name = 'avirus'
        elif self.type == 4:
            enemy_name = 'platform'
        elif self.type == 6:
            enemy_name = 'fanty'
            self.state = 0 # 0=idle  1=pursuing  2=retreating
            self.sight_distance = 64
            self.acceleration = 16
            self.max_speed = 256
        # images
        num_frames = 2
        self.images = []
        for i in range(num_frames):
            # image for the frame
            self.images.append(pygame.image.load(
                jp(dp, 'images/sprites/' + enemy_name + str(i) + '.png')).convert())
            # mask
            self.images[i].set_colorkey((255, 0, 255))
        self.animation_index = 0
        self.animation_speed = 0.08
        self.image = self.images[self.animation_index]
        self.rect = self.image.get_rect()

    def update(self):
        # animation
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.images):
            self.animation_index = 0
        self.image = self.images[int(self.animation_index)]
        # movement
        if self.type != 6: # no fanty  
            self.x += self.mx
            self.y += self.my
            if self.x == self.x1 or self.x == self.x2:
                self.mx = -self.mx
            if self.y == self.y1 or self.y == self.y2:
                self.my = -self.my
        else: # fanty
            if self.state == 0: # idle
                if distance(0, 0, self.x, self.y) <= self.sight_distance:
                    self.state = 1 # pursuing
            elif self.state == 1: # pursuing
                if distance(0, 0, self.x, self.y) > self.sight_distance:
                    self.state = 2 # retreating
                else:
                    #en_an [gpit].vx = limit(en_an [gpit].vx + addsign (player.x - en_an [gpit].x, FANTY_A),-FANTY_MAX_V, FANTY_MAX_V)
                    #en_an [gpit].vy = limit(en_an [gpit].vy + addsign (player.y - en_an [gpit].y, FANTY_A),-FANTY_MAX_V, FANTY_MAX_V)                        
                    #en_an [gpit].x = limit(en_an [gpit].x + en_an [gpit].vx, 0, 14336)
                    #en_an [gpit].y = limit(en_an [gpit].y + en_an [gpit].vy, 0, 9216) 
                    pass               
            else: # retreating
                #en_an [gpit].x += addsign(malotes [enoffsmasi].x - gpen_cx, 64)
                #en_an [gpit].y += addsign(malotes [enoffsmasi].y - gpen_cy, 64)                
                if distance (0, 0, self.x, self.y) <= self.sight_distance:
                    self.state = 1 # pursuing					
                        				
            #gpen_cx = en_an [gpit].x >> 6;
            #gpen_cy = en_an [gpit].y >> 6;
            if self.state == 2 and self.x == self.x1 and self.y == self.y1:
                self.state = 0 # idle

        self.rect.x = self.x
        self.rect.y = self.y
