from mido import Message, MidiFile, MidiTrack
import midigen as mg

mid = MidiFile(type=1)
dyad_track = MidiTrack()
mid.tracks.append(dyad_track)
arp_track = MidiTrack()
mid.tracks.append(arp_track)


spectral_array = mg.create_spectral_array(3300, 5100, 4)
mg.make_spectral_arpeggio_midi(mid, spectral_array, 100, 4)

spectral_array = mg.create_spectral_array(4500, 5100, 4)
mg.make_spectral_arpeggio_midi(mid, spectral_array, 100, 4)

spectral_array = mg.create_spectral_array(3100, 5400, 4)
mg.make_spectral_arpeggio_midi(mid, spectral_array, 100, 4)


spectral_array = mg.create_spectral_array(4300, 5400, 4)
mg.make_spectral_arpeggio_midi(mid, spectral_array, 100, 4)

spectral_array = mg.create_spectral_array(3400, 5300, 4)
mg.make_spectral_arpeggio_midi(mid, spectral_array, 100, 4)

spectral_array = mg.create_spectral_array(4600, 5300, 4)
mg.make_spectral_arpeggio_midi(mid, spectral_array, 100, 4)


spectral_array = mg.create_spectral_array(3300, 5000, 4)
mg.make_spectral_arpeggio_midi(mid, spectral_array, 100, 4)

spectral_array = mg.create_spectral_array(4500, 5000, 4)
mg.make_spectral_arpeggio_midi(mid, spectral_array, 100, 4)


mid.save('output/song7.mid')
