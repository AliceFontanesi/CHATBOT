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
    results = [[i,r] for i,r in enumerate(res) if r > ERROR_THRESHOLD]
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
        if(i['tag']== tag): #se il tag corrisponde ottengo una risposta random
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


from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty, NumericProperty 
from kivy.core.text import LabelBase
from kivy.clock import Clock

Window.size = (350, 550)

class Command(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name = "Rajdhani-Regular"
    font_size = 17

class Response(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    font_name = "Rajdhani-Regular"
    font_size = 17


class ChatBot(MDApp):
    
    def change_screen(self, name):
        screen_manager.current = name
    
    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("Main.kv"))
        screen_manager.add_widget(Builder.load_file("Chats.kv"))
        return screen_manager
    
    def response(self, *args):
        response = ""
        ints = predict_class(value, model)
        try:
            response = getResponse(ints, intents)
        except:
            response = "Scusa, non ho capito bene, portresti spiegarti meglio?"
        if len(response) < 6:
            size = .22
        elif len(response) <11:
            size = .32
        elif len(response) < 16:
            size = .45
        elif len(response) < 21:
            size = .58
        elif len(response) < 26:
            size = .71
        else:
            size = .77
        screen_manager.get_screen('chats').chat_list.add_widget(Response(text=response, size_hint_x = size))
        
    
    def send(self):
        global size, halign, value
        if screen_manager.get_screen('chats').text_input != "":
            value = screen_manager.get_screen('chats').text_input.text
            if len(value) < 6:
                size = .22
            elif len(value) <11:
                size = .32
            elif len(value) < 16:
                size = .45
            elif len(value) < 21:
                size = .58
            elif len(value) < 26:
                size = .71
            else:
                size = .77
            halign = "left"
            screen_manager.get_screen('chats').chat_list.add_widget(Command(text=value, size_hint_x = size, halign = halign))
            Clock.schedule_once(self.response, 2)
            screen_manager.get_screen('chats').text_input.text = ""
            

ChatBot().run()