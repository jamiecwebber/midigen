# midigen
does spectral calculations to output microtonal midi files

midigen is a set of tools I have developed for my own use - it uses the python library mido to create and edit MIDI files where the pitches do not fall on the 12 notes of the traditional western scale. This project is in active development and I am using python because I plan to integrate TensorFlow and use the midi output to model the internal dynamics of the neural networks as they are processing information. For art AND for science!

currently it can take as an input a midi file in two channels : channel 1 is the "bass notes" which will not be detuned, but which are taken two at a time to decide the tuning of the other notes. Channel 2 is all the rest of the notes that will be detuned. Midigen returns a new file where the notes from channel 2 are spread out onto several channels, to avoid artifacts with the pitch-bend messages. These channels need to be routed to separate identical instruments in a DAW (I use Reaper).

Please let me know if you are having a poke at the code, and I'm happy to receive constructive feedback. 

todo:
- set it up so you can assign midi items their time in absolute terms relative to the start of the piece, rather than relative to the most recent event. Be able to convert from one to the other
