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
	midi_values = (midi_note, int(pitchbend))   # if this is broken change this back to a list
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

