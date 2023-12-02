import joblib
import streamlit as st
import tensorflow
from tensorflow import keras
st.title("Automatic Music Generation")
st.markdown("LSTM model which creates classical music by inputing a random number")
n=st.number_input("Enter a random number from 0 to 37")
model2=keras.load_model("Classical_Bach")
if st.button("Generate") :
	music_pattern = x_test[n]
	out_pred=[]
	for i in range(200):
		music_pattern = music_pattern.reshape(1,len(music_pattern),1)
		pred_index = np.argmax(model2.predict(music_pattern))
       		#get the note using predicted index and append to the output prediction list
		out_pred.append(ind2note[pred_index])
		music_pattern = np.append(music_pattern,pred_index)
       		#update the music pattern with one timestep ahead
       		music_pattern = music_pattern[1:]
   	output_notes = []
   	for offset,pattern in enumerate(out_pred):
		#if pattern is a chord instance
		if ('.' in pattern) or pattern.isdigit():
			#split notes from the chord
           		notes_in_chord = pattern.split('.')
           		notes = []
           		for current_note in notes_in_chord:
				i_curr_note=int(current_note)
               			#cast the current note to Note object and append the current note 
               			new_note = note.Note(i_curr_note)
               			new_note.storedInstrument = instrument.Piano()
               			notes.append(new_note)
			#cast the current note to Chord object and offset will be 1 step ahead from the previous note
           		#as it will prevent notes to stack up 
           		new_chord = chord.Chord(notes)
           		new_chord.offset = offset
           		output_notes.append(new_chord)
		else:
			#cast the pattern to Note object apply the offset and append the note
           		new_note = note.Note(pattern)
           		new_note.offset = offset
           		new_note.storedInstrument = instrument.Piano()
           		output_notes.append(new_note)
	#save the midi file
	midi_stream = stream.Stream(output_notes)
	midi_stream.write('midi', fp='pred_music2.mid')
	st.audio("pred_music2.mid",format="mid", start_time=0)
