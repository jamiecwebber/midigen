# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 15:21:53 2019

@author: hurgdburg
"""

from mido import MidiFile
from collections import deque

from midigen import *
from spectral_tools import *

filename = 'dpliRLsaw'

mid = MidiFile(f'{filename}.mid')
output_midi = MidiFile(ticks_per_beat=960)
midi_track = MidiTrack()
output_midi.tracks.append(midi_track)

class Spectralizer():
    # processes each message of the MIDI
    def __init__(self, cycle_channels = 4, n_back = 4):
        self.dyad_note = None
        self.generator = None
        self.current_dyad = [None,None]
        self.cycle_channels = cycle_channels
        self.current_channel = 1
        self.last_n = deque(maxlen=n_back) # deque of ints
        self.notes_on = {}   # dictionary of tuples
        self.values = {}     # dictionary of values of notes, used for n_back
        self.backlog = []    # list of skipped-over spectral notes
        self.prev_note = 0   # not idea but this is for calculate_note to work right
    
    def __repr__(self):
        return f'Spectralizer(cycle_channels={self.cycle_channels})'
    
    def handle_msg(self, msg):
        if msg.channel == 0:
            if msg.velocity > 0:
                if self.dyad_note == None:
                    if msg.note not in self.current_dyad:
                        self.dyad_note = msg.note
                else:
                    self.current_dyad = [self.dyad_note, msg.note]
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
        self.generator = fib_gen_class(note_1, note_2, return_dyad=False, factor_1=1)
        self.backlog = [] # clear backlog
        print(self.generator)
    
    def handle_channels(self, msg):
        # automatically alternates detuned notes between self.cycle_channels midi channels
        msg.channel = self.current_channel
        self.current_channel += 1
        if self.current_channel > self.cycle_channels:
            self.current_channel = 1
        return msg
    
    def adjust_note(self, msg):
        if msg.velocity == 0 or msg.type == 'note_off':
            if msg.note in self.notes_on.keys():
                print(self.notes_on[msg.note])
                msg.note, _, msg.channel = self.notes_on.pop(msg.note)
            return [msg]
        else:
            oldnote = msg.note
            
            msg = self.handle_channels(msg)
            
            if oldnote in self.last_n:
                # move note back to end of list
                self.last_n.remove(oldnote)
                self.last_n.append(oldnote)
                self.notes_on[oldnote] = self.values[oldnote]
            else:  
                self.notes_on[oldnote] = self.calculate_note(msg)
                self.values[oldnote] = self.notes_on[oldnote]
                self.last_n.append(oldnote)
            if len(self.notes_on[oldnote]) == 3:
                self.notes_on[oldnote][2] = msg.channel
            else:
                self.notes_on[oldnote].append(msg.channel)
            msg.note = self.notes_on[oldnote][0] # [0] is the midi note
            # print(self.notes_on)
            messages = [msg, Message('pitchwheel', channel=msg.channel, pitch=self.notes_on[oldnote][1], time=0)]
            return messages
        
   
    
    def calculate_note(self, msg):
        # this bit just keeps the generator from getting too large of values,
        # not essential to the thing working
        if msg.note < self.prev_note:
            self.generator.drop_octave()
        self.prev_note = msg.note
        
        notes = self.backlog.copy()
        for note in notes:
            candidate_note = self.match_octave(note, msg.note*100)
            if self.check_interval(candidate_note, msg.note*100):
                self.backlog.remove(note)
                return mc_to_midi_and_pitchbend(candidate_note)
        while True:
            next_note = next(self.generator)
            candidate_note = self.match_octave(next_note, msg.note*100)
            if next_note > candidate_note:
                self.generator.drop_octave()
            if self.check_interval(candidate_note, msg.note*100):
                return mc_to_midi_and_pitchbend(candidate_note)
            self.backlog.append(candidate_note)
            # print(self.backlog)
    
    def match_octave(self, spectral_note, given_note):
        while spectral_note - given_note > 600:
            spectral_note -= 1200
        while spectral_note - given_note < -600:
            spectral_note += 1200
        return spectral_note
    
    def check_interval(self, spectral_note, given_note, interval=100):
        # hardcoded value of +/- 1 semitone of maximum adjustment
        #if given_note > spectral_note:
        #    return False
        return abs(spectral_note - given_note) < interval
        
    
        
        
        
    
    

spec = Spectralizer()

for i, track in enumerate(mid.tracks):
    dyad_note = None  # value of the first of the two notes of the dyad 
    
    print(f'Track {i}: {track.name}')
    for msg in track:
        print(f'in : {msg}')
        messages = [msg]
        if msg.type == 'note_on' or msg.type == 'note_off':
            messages = spec.handle_msg(msg)
        for message in messages:
            print(f'out: {message}')
            midi_track.append(message)

output_midi.save(f'{filename}-spec.mid')
            

