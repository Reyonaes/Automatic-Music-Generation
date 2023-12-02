import music21
from music21 import *
import pandas as pd
import numpy as np
import random
import joblib
import streamlit as st
import tensorflow
from tensorflow import keras
import midi2audio
#from midi2audio import FluidSynth
#fs=FluidSynth()
timesteps=6
import pickle
with open('Dict1.pkl', 'rb') as fp:
    ind2note = pickle.load(fp)
st.title("Automatic Music Generation")
st.markdown("Classical music in Bach style")
index=int(st.number_input("Enter a random number from 0 to 185"))
df=pd.read_csv("Bach_dataframe.csv")
x=df.iloc[:,:-1]
x_new=np.array(x)
x_new = np.reshape(x_new,(len(x_new),timesteps,1))
music_pattern=x_new[index]
model2=keras.models.load_model("Classical_Bach.h5")
if st.button("Generate") :
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
	#fs.midi_to_audio('pred_music2.mid', 'pred3.wav')
	st.audio('pred_music1.mid')
