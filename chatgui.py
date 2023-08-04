import nltk #natural language toolkit
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

import tensorflow as tf #opensource machine learning platform
#from tensorflow.keras.models import load_model
model = tf.keras.models.load_model('chatbot_model.h5')
import json
import random

intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))


def clean_up_sentence(sentence):
    #separo le parole in un array
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

#ritorna un bag of words array: 0 se una non esiste, 1 se esiste
def bow(sentence, words):
    #separo le parole
    sentence_words = clean_up_sentence(sentence)
    #bag of words, inserisco le parole in una matrice (vocabolario)
    bag = [0]*len(words)  
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s: 
                #assegno 1 alla parola se è presente all'interno della matrice/vocabolario
                bag[i] = 1
                #if show_details:
                    #print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    #prevedo risposte in base a una certa soglia
    p = bow(sentence, words)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    #ordino in base alla probabilità
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag): #se il tag corrispoende ottengo una risposta random
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    try:
        res = getResponse(ints, intents)
    except:
        res = "Scusa, non ho capito bene la domanda, portresti spiegarti meglio?"
    return res






#creo la GUI con tkinter
from tkinter import *

def send():
    #messaggio nella entrybox
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)

    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "Io: " + msg + '\n\n')#quello che scrive l'utente
    
        res = chatbot_response(msg)
        ChatLog.insert(END, "Bot: " + res + '\n\n')#risposte del bot
            
        ChatLog.yview(END)
 
#creo un oggetto tk -> tkinter gui
app = Tk()
app.title("Chatbot")
app.geometry("400x500")#dimensione finestra
app.resizable(width=FALSE, height=FALSE)

#Dettagli finestra
ChatLog = Text(app, bd=0, bg="white", height="8", width="50", font="Bookman")

ChatLog.config(state=DISABLED)

#Imposto scrollbar
scrollbar = Scrollbar(app, command = ChatLog.yview, cursor="star")
ChatLog['yscrollcommand'] = scrollbar.set

#Bottone per inviare i messaggi
SendButton = Button(app, font=("Bookman",12,'bold'), text="Invia", width="12", height=5,
                    bd= 0, bg="#8c78f9",fg='#000000',
                    command= send)

#Creo entrybox
EntryBox = Text(app, bd = 0,bg="white", width="29", height= 5, font="Bookman")


#Posizione componenti finestra
scrollbar.place(x=376,y=6, height=386)
ChatLog.place(x=6,y=6, height=436, width=370)
EntryBox.place(x=6, y=451, height=40, width=265)
SendButton.place(x=265, y=451, height=40, width = 112)

app.mainloop()