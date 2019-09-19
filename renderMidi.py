from mido import Message, MidiFile, MidiTrack
import midigen as mg
import os

# This file creates a new directory and fills it with MIDI files
# with a 10-note array for every dyad between C0 (1200 mc) and 
# C1 (2400 mc).
# naming: A_on_C: A1 on C1. C_on_A: C2 on A1. Root note is always
# between C1 and B1. (recall that the octave number increases on C)
# C_on_C is an octave, not a unison


# Create directory
dirName = 'SpectraWithRests_dropsecondnotebyoctave'
noteNames = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
 
try:
    # Create target Directory
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ") 
except FileExistsError:
    print("Directory " , dirName ,  " already exists")

for base in range(12):
	for interval in range(1, 13):
		mid = MidiFile()
		dyad_track = MidiTrack()
		mid.tracks.append(dyad_track)
		arp_track = MidiTrack()
		mid.tracks.append(arp_track)

		base_freq = (base + 12) * 100
		treble_freq = base_freq + interval * 100

		spectral_array = mg.create_spectral_array(base_freq, treble_freq, 10, 1, 0.5)
		print(spectral_array)
		mg.make_spectral_arpeggio_midi(mid, spectral_array, 100, 1)
		mg.add_rests_between_notes(arp_track, 100)

		base_name = noteNames[base]
		treble_name = noteNames[(base + interval) % 12]

		file_name = f"{dirName}/{treble_name}_on_{base_name}.mid"

		mid.save(file_name)








# for i, track in enumerate(mid.tracks):
# 	print('Track {}: {}'.format(i, track.name))
# 	mg.flatten_midi_channels(track)
# 	mg.cycle_midi_channels(track, 4)
# 	for msg in track:
# 		print(msg)
# 	print("end of track")

# for i, track in enumerate(mid.tracks):
# 	for msg in track:
# 		print(msg)
# 	new_file = mg.midi_channels_to_tracks(track)
# 	new_file.save(f'output/{i}.mid')

#mid.save('output/song8.mid')
