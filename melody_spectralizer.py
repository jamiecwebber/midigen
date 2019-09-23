# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 15:21:53 2019

@author: hurgdburg
"""

from mido import MidiFile

from midigen import *
from spectral_tools import *

mid = MidiFile('formidigennosus.mid')


class Spectralizer():
    # processes each message of the MIDI
    def __init__(self):
        self.dyad_note = None
        self.generator = None
    
    
        
    def handle_msg(self, msg):
        if msg.channel == 1:
            print(msg)
            if dyad_note == None:
                dyad_note = msg.note
            else:
                self.change_generator(dyad_note, msg.note)
                dyad_note = None
        else:
            self.adjust_note(msg)
    
    def change_generator (self, note_1, note_2):
        note_1, note_2 = [note_1, note_2]*100
        print(f'{note_1}, {note_2}')
    
    def adjust_note(msg):
        print('blah')
        
    


spec = Spectralizer()

for i, track in enumerate(mid.tracks):
    dyad_note = None  # value of the first of the two notes of the dyad 
    
    print(f'Track {i}: {track.name}')
    for msg in track:
        if msg.type == 'note_on' or msg.type == 'note_off':
            spec.handle_msg(msg)
            
