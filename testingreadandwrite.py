# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 14:33:40 2019

@author: hurgdburg
"""


from mido import MidiFile

from midigen import *
from spectral_tools import *


filename = 'improvnohold'

mid = MidiFile('blah.mid' )
output_midi = MidiFile(ticks_per_beat=960)
midi_track = MidiTrack()
output_midi.tracks.append(midi_track)


for i, track in enumerate(mid.tracks):
    dyad_note = None  # value of the first of the two notes of the dyad 
    
    print('Track ')
    for msg in track:
        midi_track.append(msg)
        print('in : {msg}', msg)

output_midi.save('testing.mid')
