
# ==============================================================================
# .::Jukebox class::.
# Create a playlist with the tracks randomly shuffled and repeated 
# a certain number of times according to their duration.
# ==============================================================================
#
#  This file is part of "Red Planet Pi". Copyright (C) 2023 @salvakantero
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ==============================================================================

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
