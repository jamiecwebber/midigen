# midigen
does spectral calculations to output microtonal midi files

midigen is a set of tools I have developed for my own use - it uses the python library mido to create and edit MIDI files where the pitches do not fall on the 12 notes of the traditional western scale. This project is in active development and I am using python because I plan to integrate TensorFlow and use the midi output to model the internal dynamics of the neural networks as they are processing information. For art AND for science!

todo 
- set it up so you can assign midi items their time in absolute terms relative to the start of the piece, rather than relative to the most recent event. Be able to convert from one to the other
- set up generators to give the next note in a series indefinitely 