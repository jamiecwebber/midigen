# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 16:33:12 2019

@author: hurgdburg
"""
from midigen import *

## Spectral tools

def fibonacci_generator(note_1, note_2, factor_1=1, factor_2=1, return_dyad=True):
    # generates a series of notes through frequency addition - these will be a subset
    # of a harmonic series of which the two given notes are a part. With default settings
    # this series converges to a ratio of 1.618, the golden mean.
    # When converting back to midicents this will look like a repeating stack of 633c intervals.
    # factor_1 and factor_2 allow you to scale the two notes during addition, this
    # changes the interval that the series converges to.
    freq_1 = mc_to_f(note_1)
    freq_2 = mc_to_f(note_2)
    if return_dyad:
        yield note_1
        yield note_2
    while True:
        new_freq = freq_1*factor_1 + freq_2*factor_2
        yield f_to_mc(new_freq)
        freq_1 = freq_2
        freq_2 = new_freq

class fib_gen_class:
    def __init__(self, note_1, note_2, factor_1=1, factor_2=1, return_dyad=True):
        self.note_1 = note_1
        self.note_2 = note_2
        self.freq_1 = mc_to_f(self.note_1)
        self.freq_2 = mc_to_f(self.note_2)
        self.factor_1 = factor_1
        self.factor_2 = factor_2
        self.return_dyad = return_dyad
    
    def __next__(self):
        new_freq = self.freq_1*self.factor_1 + self.freq_2*self.factor_2
        self.freq_1, self.freq_2 = self.freq_2, new_freq
        return f_to_mc(new_freq)
    
    def drop_octave(self):
        self.freq_1 = self.freq_1 / 2
        self.freq_2 = self.freq_2 / 2
    

        
        
        
def create_spectral_array(generator, number_of_overtones):
	# note_1 and note_2 are in midicents
    spectral_array = []
    for _ in range(number_of_overtones):
        spectral_array.append(next(generator))
    return spectral_array


def make_spectral_arpeggio_midi(midi_file, spectral_array, time_step, repetitions):
	# midi_file must be pre-defined with two tracks

	dyad_note_1 = mc_to_midi_and_pitchbend(spectral_array[0])
	dyad_note_2 = mc_to_midi_and_pitchbend(spectral_array[1])
	dyad_duration = (len(spectral_array)-2)*time_step*repetitions
	dyad_track = midi_file.tracks[0]
	arp_track = midi_file.tracks[1]
	dyad_track.append(Message('note_on', note=dyad_note_1[0], time=0))
	dyad_track.append(Message('note_on', note=dyad_note_2[0], time=0))
	dyad_track.append(Message('note_off', note=dyad_note_1[0], time=dyad_duration))
	dyad_track.append(Message('note_off', note=dyad_note_2[0], time=0))

	for repetition in range(0, repetitions):
		for note in range(2, len(spectral_array)):
			new_note = mc_to_midi_and_pitchbend(spectral_array[note])
			arp_track.append(Message('pitchwheel', channel=note - 1, pitch=new_note[1], time=0))
			arp_track.append(Message('note_on', channel=note - 1, note=new_note[0], time=0))
			arp_track.append(Message('note_off', channel=note - 1, note=new_note[0], time=time_step))

def add_rests_between_notes(midi_track, rest_time):
	first_note = True
	for msg in midi_track:
		if not msg.is_meta:
			if msg.type == 'pitchwheel':
				if not first_note:
					msg.time = rest_time
				else:
					first_note = False






