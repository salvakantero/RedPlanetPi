
#===============================================================================
# Jukebox class
#===============================================================================

import pygame
import random

class Jukebox():
    def __init__(self, path, base_filename, tracks, loop_list):
        self.tracks = tracks
        self.track_list = list(range(1,self.tracks+1))
        self.track_index = 0 # nº de tema actual
        self.loop_list = loop_list # repeticiones por tema
        self.path = path
        self.base_filename = base_filename

    # genera una nueva lista aleatoria de los x temas disponibles
    def shuffle(self):
        random.shuffle(self.track_list)

    # loads next frame of animation or ends
    def load(self):
        pass

    def update(self):
        pass