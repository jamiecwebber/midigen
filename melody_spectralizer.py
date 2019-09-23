# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 15:21:53 2019

@author: hurgdburg
"""

from mido import MidiFile

from midigen import *
from spectral_tools import *

mid = MidiFile('formidigennosus.mid')


dyad_note = None  # value of the first of the two notes of the dyad 

def handle_msg(msg):
    # processes each message of the MIDI
    if msg.channel == 1:
        if dyad_note == None:
            dyad_note = msg.note
        else:
            change_generator(dyad_note, msg.note)
    else:
        adjust_note()



for i, track in enumerate(mid.tracks):
    print(f'Track {i}: {track.name}')
    for msg in track:
        if not msg.type == 'control_change':
            handle_msg(msg)
            

