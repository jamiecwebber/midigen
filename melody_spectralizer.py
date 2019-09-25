# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 15:21:53 2019

@author: hurgdburg
"""

from mido import MidiFile

from midigen import *
from spectral_tools import *

mid = MidiFile('formidigenbasschanzero.mid')
output_midi = MidiFile()
midi_track = MidiTrack()
output_midi.tracks.append(midi_track)

class Spectralizer():
    # processes each message of the MIDI
    def __init__(self, cycle_channels = 4):
        self.dyad_note = None
        self.generator = None
        self.cycle_channels = cycle_channels
        self.current_channel = 1
        self.notes_on = {}   # dictionary of tuples
        self.backlog = []    # list of skipped-over spectral notes
        self.prev_note = 0   # not idea but this is for calculate_note to work right
    
    def handle_msg(self, msg):
        if msg.channel == 0:
            if msg.velocity > 0:
                if self.dyad_note == None:
                    self.dyad_note = msg.note
                else:
                    self.change_generator(self.dyad_note, msg.note)
                    self.prev_note = 0  # so that generators always start at the correct octave above chord
                    self.dyad_note = None
            return [msg]
        else:
            messages = self.adjust_note(msg)
            return messages
    
    def change_generator (self, note_1, note_2):
        note_1, note_2 = note_1*100, note_2*100
        if note_1 > note_2:
            note_1, note_2 = note_2, note_1
        self.generator = fib_gen_class(note_1, note_2, return_dyad=False)
        print(self.generator)
    
    def handle_channels(self, msg):
        # automatically alternates detuned notes between self.cycle_channels midi channels
        msg.channel = self.current_channel
        self.current_channel += 1
        if self.current_channel > self.cycle_channels:
            self.current_channel = 1
        return msg
    
    def adjust_note(self, msg):
        if msg.velocity == 0:
            msg.note, _, msg.channel = self.notes_on.pop(msg.note)
            return [msg]
        else:
            oldnote = msg.note
            
            msg = self.handle_channels(msg)
            
            self.notes_on[oldnote] = self.calculate_note(msg)
            self.notes_on[oldnote].append(msg.channel)
            msg.note = self.notes_on[oldnote][0] # [0] is the midi note
            print(self.notes_on)
            messages = [msg, Message('pitchwheel', channel=msg.channel, pitch=self.notes_on[oldnote][1], time=0)]
                # see how this works with pitch bend message 0 ticks AFTER pitch note. ???
            return messages
        
   
    
    def calculate_note(self, msg):
        # this bit just keeps the generator from getting too large of values,
        # not essential to the thing working
        if msg.note < self.prev_note:
            self.generator.drop_octave()
        self.prev_note = msg.note
        
        notes = self.backlog.copy()
        for note in notes:
            candidate_note = match_octave(note, msg.note*100)
            if check_interval(candidate_note, msg.note*100):
                self.backlog.pop(note)
                return mc_to_midi_and_pitchbend(candidate_note)
        while True:
            next_note = next(self.generator)
            candidate_note = match_octave(next_note, msg.note*100)
            if next_note > candidate_note:
                self.generator.drop_octave()
            if check_interval(candidate_note, msg.note*100):
                return mc_to_midi_and_pitchbend(candidate_note)
            self.backlog.append(candidate_note)
    
    def match_octave(self, spectral_note, given_note):
        while spectral_note - given_note > 600:
            spectral_note -= 1200
        while spectral_note - given_note < -600:
            spectral_note += 1200
        return spectral_note
    
    def check_interval(self, spectral_note, given_note, interval=150):
        # hardcoded value of 1.5 semitones of maximum adjustment
        return abs(spectral_note - given_note) < interval
        
    
        
        
        
    
    

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

#output_midi.save('formidigenoutspectracontourresetprevnotecyclechannelsfixed.mid')
            

