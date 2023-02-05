
#===============================================================================
# Jukebox class
#===============================================================================

import pygame
import random

class Jukebox():
    def __init__(self, path, base_filename, tracks, loop_list):
        self.tracks = tracks
        self.track_list = list(range(0,self.tracks))
        self.track_index = 0 # nº de tema actual
        self.loop_list = loop_list # repeticiones por tema
        self.path = path
        self.base_filename = base_filename

    # genera una nueva lista aleatoria de los x temas disponibles
    def shuffle(self):
        random.shuffle(self.track_list)

    # load the next track from the playlist
    def load_next(self):
        pygame.mixer.music.load(self.path + self.base_filename + 
            str(self.track_list[self.track_index]) + '.ogg')
        self.track_index += 1
        if self.track_index == self.tracks: 
            self.track_index = 0

    def update(self):
        if not pygame.mixer.music.get_busy():
            self.load_next()
            pygame.mixer.music.play(self.loop_list[self.track_list[self.track_index]])