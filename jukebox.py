
#===============================================================================
# Jukebox class
#===============================================================================

import pygame
import random

class Jukebox():
    def __init__(self, path, base_filename, tracks, loop_list):
        self.tracks = tracks # number of music tracks available
        self.track_list = list(range(0,self.tracks)) # sorted playlist
        self.track_index = 0 # current theme song number
        self.loop_list = loop_list # list of repetitions assigned to each track
        self.path = path # path to the folder with the music tracks
        self.base_filename = base_filename # common name of the files

    # generates a new random list of the x available tracks
    def shuffle(self):
        random.shuffle(self.track_list)
        self.track_index = 0

    # load the next track from the playlist
    # for example: 'sounds/music/'+'mus_ingame_'+'9' + '.ogg'
    def load_next(self):
        pygame.mixer.music.load(self.path + self.base_filename + 
            str(self.track_list[self.track_index]) + '.ogg')
        # next number in the playlist         
        self.track_index += 1
        # or restart if it has reached the end of the list
        if self.track_index == self.tracks: 
            self.track_index = 0

    def update(self):
        if not pygame.mixer.music.get_busy(): # if a track is not playing...
            self.load_next() # obviously load in memory the following track
            # applies the number of repetitions assigned to the track and plays it
            pygame.mixer.music.play(self.loop_list[self.track_list[self.track_index]])
