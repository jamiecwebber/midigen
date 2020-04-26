
from mido import Message, MidiFile, MidiTrack
from spectral_tools import *
import midigen as mg
import os

noteNames = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

for i in range (0, 25):

	A = 1200
	B = A + (i * 100);

	array1 = fibonacci_generator(0, B)
	array2 = fibonacci_generator(B, A)
	print(next(array2));

	row1 = fibonacci_generator(next(array1), next(array2))
	row2 = fibonacci_generator(next(array1), next(array2))
	row3 = fibonacci_generator(next(array1), next(array2))
	row4 = fibonacci_generator(next(array1), next(array2))
	row5 = fibonacci_generator(next(array1), next(array2))
	row6 = fibonacci_generator(next(array1), next(array2))
	row7 = fibonacci_generator(next(array1), next(array2))
	row8 = fibonacci_generator(next(array1), next(array2))

	spectral_array = [A,B]

	for y in range(8):
		spectral_array.append(next(row1))
		spectral_array.append(next(row2))
		spectral_array.append(next(row3))
		spectral_array.append(next(row4))
		spectral_array.append(next(row5))
		spectral_array.append(next(row6))
		spectral_array.append(next(row7))
		spectral_array.append(next(row8))

	print(spectral_array)


	mid = MidiFile()
	dyad_track = MidiTrack()
	mid.tracks.append(dyad_track)
	arp_track = MidiTrack()
	mid.tracks.append(arp_track)

	make_spectral_arpeggio_midi(mid, spectral_array, 100, 1)
	add_rests_between_notes(arp_track, 100)

	filename = f'diamond{i}.mid'

	mid.save('FibonacciDiamonds/' + filename)

