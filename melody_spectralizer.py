# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 15:21:53 2019

@author: hurgdburg
"""

from mido import MidiFile

from midigen import *
from spectral_tools import *

mid = MidiFile('formidigen.mid')
output_midi = MidiFile()
midi_track = MidiTrack()
output_midi.tracks.append(midi_track)

class Spectralizer():
    # processes each message of the MIDI
    def __init__(self):
        self.dyad_note = None
        self.generator = None
        self.notes_on = {}   # dictionary of tuples
    
    def handle_msg(self, msg):
        if msg.channel == 1:
            if msg.velocity > 0:
                if self.dyad_note == None:
                    self.dyad_note = msg.note
                else:
                    self.change_generator(self.dyad_note, msg.note)
                    self.dyad_note = None
        else:
            msg = self.adjust_note(msg)
        return 
    
    def change_generator (self, note_1, note_2):
        note_1, note_2 = note_1*100, note_2*100
        if note_1 > note_2:
            note_1, note_2 = note_2, note_1
        self.generator = fib_gen_class(note_1, note_2, return_dyad=False)
        print(self.generator)
    
    def adjust_note(self, msg):
        if msg.velocity == 0:
            msg.note = self.notes_on.pop(msg.note)
        else:
            self.notes_on[msg.note] = self.calculate_note(msg)
            msg.note = 
            
    def calculate_note(self, msg):
        print('calculate note')
        midicents = msg.note * 100 - 50
        return mc_to_midi_and_pitchbend(midicents)
    

spec = Spectralizer()

for i, track in enumerate(mid.tracks):
    dyad_note = None  # value of the first of the two notes of the dyad 
    
    print(f'Track {i}: {track.name}')
    for msg in track:
        messages = [msg]
        if msg.type == 'note_on' or msg.type == 'note_off':
            messages = spec.handle_msg(msg)
        for message in messages:
            midi_track.append(message)

output_midi.save('formidigenout.mid')
            

