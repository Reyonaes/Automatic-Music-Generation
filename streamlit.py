import music21
from music21 import *
import glob
import numpy as np
import random
import joblib
import streamlit as st
import tensorflow
from tensorflow import keras
st.title("Automatic Music Generation")
st.markdown("Classical music in Bach style")
unique_notes=['D3', 'D5', 'E5', 'F#5', 'A4', 'D4', 'A5', 'F#3', 'G5', 'E3', 'B4', 'C#5', 'A3', 'C#4', 'G#5', 'G#3', 'C#3', 'F#4', 'B2', 'G#4', 'E4', 'A2', 'G4', 'E-5', 'E-3', 'G2', 'B-4', 'F#2', 'F4', 'F5', 'B5', 'E2', 'C5', 'D2', 'C4', 'B3', 'C3', 'E-4', 'G3', 'B-3', 'F3', 'B-5', 'B-2', 'G#2', '2.5.8.9', '2.5.8.11', '11.1', '8.9', '4.6', '6.8', '9.11', '1.2', '4.5', '2.4', '1.4.7.10', '4.9', '9', '2.6.9', '6.7', '2.6', '9.1', '4.6.7', '11.1.2', '7.9', '6.9', '2.4.6', '4.7', '1.2.4', '11.2', '11.0', '7.11', '3.4', '9.0', '1.4']
musical_note=st.text_input("Enter a musical note (Letters A to G)").upper()
pattern=[]
for i, ele in enumerate(unique_notes) :
	 if musical_note in ele :
		 pattern=unique_notes[i : i+6]
model2=keras.models.load_model("Classical_Bach.h5")
if st.button("Generate") :
	music_pattern = np.array(pattern)
	out_pred=[]
	for i in range(200):
		music_pattern = music_pattern.reshape(1,len(music_pattern),1)
		pred_index = np.argmax(model2.predict(music_pattern))
		out_pred.append(ind2note[pred_index])
		music_pattern = np.append(music_pattern,pred_index)
		music_pattern = music_pattern[1:]
	output_notes = []
	for offset,pattern in enumerate(out_pred):
		if ('.' in pattern) or pattern.isdigit():
			notes_in_chord = pattern.split('.')
			notes = []
			for current_note in notes_in_chord:
				i_curr_note=int(current_note)
				new_note = note.Note(i_curr_note)
				new_note.storedInstrument = instrument.Piano()
				notes.append(new_note)
			new_chord = chord.Chord(notes)
			new_chord.offset = offset
			output_notes.append(new_chord)
		else:
			new_note = note.Note(pattern)
			new_note.offset = offset
			new_note.storedInstrument = instrument.Piano()
			output_notes.append(new_note)
	#save the midi file
	midi_stream = stream.Stream(output_notes)
	midi_stream.write('midi', fp='pred_music2.mid')
	st.audio("pred_music2.mid",format="mid", start_time=0)
