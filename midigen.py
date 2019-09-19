from mido import Message, MidiFile, MidiTrack
import math

def mc_to_f(midicents):
	# converts midicents value to frequency
	# assumes A440 @ 6900 midicents
	frequency = 440 * 2.**((midicents-6900.)/1200.)
	return frequency

def f_to_mc(frequency):
	#converts frequency to midicents
	midicents = 1200 * math.log(frequency/440.) / math.log(2) + 6900
	return int(midicents)

def mc_to_midi_and_pitchbend(midicents):
	# assuming standard pitch bend range of +- 2 semitones
	# assuming +8192/-8191 pitch bend unites, so 1 midicent = 40.96 pbu
	midi_note = int((midicents + 50) / 100)
	pitchbend = (midicents - (midi_note * 100))*40.96
	midi_values = [midi_note, int(pitchbend)]
	return midi_values

def fibonacci_generator(note_1, note_2, factor_1=1, factor_2=1, return_dyad=True):
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

#def create_spectral_array(generator, number_of_overtones):
	# note_1 and note_2 are in midicents
    
    
    
	#freq_1 = mc_to_f(note_1)
	#freq_2 = mc_to_f(note_2)
	#spectral_array = [note_1, note_2]
	#for x in range(0, number_of_overtones):
	#	freq_new = factor1 * freq_1 + factor2 * freq_2
	#	midicents_new = f_to_mc(freq_new)
	#	spectral_array.append(midicents_new)
	#	freq_1 = freq_2
	#	freq_2 = freq_new
	#return spectral_array


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

def cycle_midi_channels(midi_track, n = 2):
	# changes the midi channel with each pitchwheel message to avoid unintended pitch bends.
	# a quirk - starts pitchbend track on second track
	channel = 0
	for msg in midi_track:
		if not msg.is_meta:
			if msg.type == 'pitchwheel':
				if channel == n:
					channel = 0
				channel += 1

			msg.channel = channel 


def flatten_midi_channels(midi_track):
	for msg in midi_track:
		if not msg.is_meta:
			msg.channel = 0

def increase_midi_channels(midi_track, n = 1):
	for msg in midi_track:
		if not msg.is_meta:
			msg.channel += n

def midi_channels_to_tracks(midi_track):
	new_file = MidiFile(type=1)
	max_channel = 0
	for msg in midi_track:
		if not msg.is_meta:
			if msg.channel > max_channel:
				max_channel = msg.channel
	for channel in range(max_channel):
		new_track = MidiTrack()
		new_file.tracks.append(new_track)
		new_time = 0
		for msg in midi_track:
			if not msg.is_meta:
				if msg.channel == channel:
					new_track.append(msg.copy(channel=0, time=new_time))
					new_time = 0
				else:
					new_time += msg.time
	return new_file

def add_rests_between_notes(midi_track, rest_time):
	first_note = True
	for msg in midi_track:
		if not msg.is_meta:
			if msg.type == 'pitchwheel':
				if not first_note:
					msg.time = rest_time
				else:
					first_note = False






