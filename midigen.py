from mido import Message, MidiFile, MidiTrack
import math

## frequency and midicents handling

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

## midi channel handling
## the issue is that in MIDI 1.0 pitch-bend messages are per-channel and not per-note, so
## if you have more than one note playing on a single channel, a pitch bend message will
## affect all of them. So, the solution is to have several identical instruments playing
## on multiple channels. (although this gets in the way of portamento, other effects)
    
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






