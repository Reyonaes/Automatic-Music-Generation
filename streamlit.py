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
str=st.text_input("Enter a musical note (Letters A to G)").upper()
musical_note=[]
for char in str :
	musical_note.append(char)
model2=keras.models.load_model("Classical_Bach.h5")
if st.button("Generate") :
	music_pattern = np.array(musical_note)
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
