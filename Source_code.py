from music21 import *
import glob
from tqdm import tqdm
import numpy as np
import random
from tensorflow.keras.layers import LSTM, Dense, Input, Dropout
from tensorflow.keras.models import Sequential, Model, load_model
from sklearn.model_selection import train_test_split
def read_files(file) :
    notes=[]
    chords=[]
    notes_to_parse=None
    # Parse the midi file
    midi=converter.parse(file)
    #Separate all instruments from the file
    instrmnts= instrument.partitionByInstrument(midi)
    for part in instrmnts.parts :
        # Fetch data of Piano instrument only
        if "Piano" in str(part) :
            notes_to_parse=part.recurse()
            # Iterate over all the parts of the sub stream elements and check if elements type is note or chord
            # If it is chord split them into notes
            for element in notes_to_parse :
                if type(element)==note.Note :
                    notes.append(str(element.pitch))
                elif type(element)==chord.Chord :
                    notes.append('.'.join(str(n) for n in element.normalOrder))
    return notes
# Retrieve the paths directly from inside the directories / files
file_path=["bach"]
all_files=glob.glob(r"C:\Users\Ryona Elza Sabu\Desktop\BE AI - 3rd Year\NNDL\Automatic Music Generation\Classical Music\\"+file_path[0]+ "\*.mid",recursive=True)
# Reading each midi file
#notes_array = np.array([read_files(i) for i in tqdm(all_files,position=0,leave=True)])
for i in tqdm(all_files, position=0, leave=True) :
    notes=read_files(i)
notes_array = np.array(notes)
unique_notes=[]
for i in notes_array :
    if i not in unique_notes :
        unique_notes.append(i)
freq={}
for i in unique_notes :
    count=0
    for j in notes_array :
        if i==j :
            count=count+1
    freq[i]=count
# Dictionary having key as note index and value as note
ind2note=dict(enumerate(freq))
# Dictionary having key as note and value as note index
note2ind=dict(map(reversed,ind2note.items()))
# Timestep
timesteps=6
# Store values for input and output
x=[]
y=[]
start=0
inp=[]
while start<len(notes_array) :
    if start%(timesteps+1)==0 :
        out=notes_array[start]
        x.append(inp)
        y.append(note2ind[out])
        inp=[]
    else :
        inp.append(note2ind[notes_array[start]])
    start=start+1
x.pop(0)
y.pop(0)
x_new=np.array(x)
y_new=np.array(y)
# Reshape input and output for the model
x_new = np.reshape(x_new,(len(x_new),timesteps,1))
y_new = np.reshape(y_new,(-1,1))
# Split the input and value into training and testing sets, 80% for training and 20% for testing sets
x_train,x_test,y_train,y_test = train_test_split(x_new,y_new,test_size=0.2,random_state=42)
st.title("Automatic Music Generation")
st.markdown("Classical music in Bach style")
index=int(st.number_input("Enter a number from 0 to 37"))
model2=keras.models.load_model("Classical_Bach.h5")
music_pattern = x_test[index]
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
	st.audio("pred_music2.mid",format="mid", start_time=0)
