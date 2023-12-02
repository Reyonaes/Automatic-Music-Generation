import joblib
import streamlit as st
st.title("Automatic Music Generation")
st.markdown("LSTM model which creates classical music by inputing a random number")
n=st.number_input("Enter a random number from 0 to 37")
music_pattern = x_test[n]
out_pred=[] # It will store predicted notes
# Iterate till 200 note is generated
for i in range(200):
   # if i%5==0 :
        #music_pattern=np.append(music_pattern,x_test[np.random.randint(0,len(x_test)-1)])
    # Reshape the music pattern
    music_pattern = music_pattern.reshape(1,len(music_pattern),1)
    #get the maximum probability value from the predicted output
    pred_index = np.argmax(model2.predict(music_pattern))
    #get the note using predicted index and append to the output prediction list
    out_pred.append(ind2note[pred_index])
    music_pattern = np.append(music_pattern,pred_index)
    #update the music pattern with one timestep ahead
    music_pattern = music_pattern[1:]
