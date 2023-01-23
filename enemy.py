
#===============================================================================
# Enemy class
#===============================================================================

import pygame
import math
import enums
import constants


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_data, player_rect):
        # enemy_data = (x1, y1, x2, y2, mx, my, type)
        super().__init__()
        self.player = player_rect # player's current position
        # from/to xy values
        self.x = self.x1 = enemy_data[0]
        self.y = self.y1 = enemy_data[1]
        self.x2 = enemy_data[2]
        self.y2 = enemy_data[3]
        # movement (pixels per frame)
        self.mx = enemy_data[4]
        self.my = enemy_data[5]
        # enemy type
        self.type = enemy_data[6]
        if self.type == enums.INFECTED:
            enemy_name = 'infected'
        elif self.type == enums.PELUSOID:
            enemy_name = 'pelusoid'
        elif self.type == enums.AVIRUS:
            enemy_name = 'avirus'
        elif self.type == enums.PLATFORM_SPR:
            enemy_name = 'platform'
        elif self.type == enums.FANTY:
            enemy_name = 'fanty'  
            self.state = enums.IDLE          
            self.sight_distance = 1 # *64 pixels/frame
            self.acceleration = 0.075 # pixels/frame
            self.max_speed = 2 # pixels/frame
        # images
        self.image_list = []
        for i in range(2): # 2 frames per enemy
            # image for the frame
            self.image_list.append(pygame.image.load(
                'images/sprites/' + enemy_name + str(i) + '.png'))
            self.image_list[i].convert_alpha()
        self.frame_index = 0 # frame number
        self.animation_timer = 12 # timer to change frame
        self.animation_speed = 12 # frame dwell time
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()

    def animate(self):
        self.animation_timer += 1
        # exceeded the frame time?
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0 # reset the timer
            self.frame_index += 1 # next frame
        # exceeded the number of frames?
        if self.frame_index > len(self.image_list) - 1:
            self.frame_index = 0 # reset the frame number
        # assigns the original or inverted image
        if self.mx > 0 or (self.mx == 0 and self.player.rect.x >= self.x):
            self.image = self.image_list[self.frame_index]
        elif self.mx < 0 or (self.mx == 0 and self.player.rect.x < self.x):
            self.image = pygame.transform.flip(
                self.image_list[self.frame_index], True, False)

    # changes a sign value according to the sign of another value
    def addsign (self, n, value):
        if n >= 0: return value
        else: return -value

    # calculates the distance between two points
    def distance (self, x1, y1, x2, y2):
        return math.hypot(x2 - x1, y2 - y1)

    # maintains a value within limits
    def limit(self, val, min, max):
        if val < min: return min
        elif val > max: return max
        return val

    def update(self):
        # movement
        if self.type != enums.FANTY: # no fanty  
            self.x += self.mx
            self.y += self.my
            if self.x == self.x1 or self.x == self.x2:
                self.mx = -self.mx
            if self.y == self.y1 or self.y == self.y2:
                self.my = -self.my
        else: # fanty
            gpx = self.player.rect.x / 64
            gpy = self.player.rect.y / 64  
            gpen_cx = self.x / 64
            gpen_cy = self.y / 64      
            if self.state == enums.IDLE:
                if self.distance (gpx, gpy, gpen_cx, gpen_cy) <= self.sight_distance:
                    self.state = enums.CHASING
            elif self.state == enums.CHASING:
                if self.distance (gpx, gpy, gpen_cx, gpen_cy) > self.sight_distance:
                    self.state = enums.RETREATING
                else:
                    self.mx = self.limit(self.mx + self.addsign(
                        self.player.rect.x - self.x, self.acceleration), 
                        -self.max_speed, self.max_speed)
                    self.my = self.limit(self.my + self.addsign(
                        self.player.rect.y - self.y, self.acceleration), 
                        -self.max_speed, self.max_speed)
                    self.x = self.limit(self.x + self.mx, 0, constants.MAP_UNSCALED_SIZE[0])
                    self.y = self.limit(self.y + self.my, 0, constants.MAP_UNSCALED_SIZE[1])
            else: # retreating
                self.x += self.addsign(self.x1 - self.x, 1)
                self.y += self.addsign(self.y1 - self.y, 1)
                if self.distance(gpx, gpy, gpen_cx, gpen_cy) <= self.sight_distance:
                    self.state = enums.CHASING		
            # in its original position?
            if self.state == enums.RETREATING \
            and self.x == self.x1 and self.y == self.y1:
                self.state = enums.IDLE

        self.rect.x = self.x
        self.rect.y = self.y
        self.animate()
