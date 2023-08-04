import tensorflow as tf
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
import pickle

import numpy as np
#from tf.keras.models import Sequential
#from tensorflow.keras.layers import Dense, Activation, Dropout
#from tensorflow.keras.optimizers import SGD
import random

words=[]
classes = []
documents = []
ignore_words = ['?', '!', '@', '&']
data_file = open('intents.json').read() #leggo il file con gli intenti
intents = json.loads(data_file)


for intent in intents['intents']:
    for pattern in intent['patterns']:

        #tokenize ogni parola
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w, intent['tag']))

        #aggiungo alla lista classes
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

#lemmatize, parole in minuscolo e rimuove duplicati
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
#ordino le parole
words = sorted(list(set(words)))
#ordino le classi
classes = sorted(list(set(classes)))

#stampo dati
print (len(documents), "documenti")
print (len(classes), "classes", classes)# -> intenti
print (len(words), "unique lemmatized words", words)# -> vocabolario


pickle.dump(words,open('words.pkl','wb')) 
pickle.dump(classes,open('classes.pkl','wb'))

#creo allenamento reti reurali
training = []
#creo array vuoto
output_empty = [0] * len(classes)

#allenamento
for doc in documents:
    #bag of words
    bag = []
    #lista di tokenized words per i pattern
    pattern_words = doc[0]
    #lemmatize ogni parola
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    #creo una bag of words array con 1 se la parola viene trovata nel modello corrente
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)
    
    #output è '0' per ogni tag e '1' per ogni tag corrente
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    
    training.append([bag, output_row])
#mescolo i dati e li inserisco all'interno di un array
random.shuffle(training)
training = np.array(training)
#creo liste per allenamento -> X = patterns, Y = intents
train_x = list(training[:,0])
train_y = list(training[:,1])
print("Training data created")


#modello a tre strati
#1° strato con 128 neuroni, secondo con 64, 3° strato di output contenente il numero di neuroni uguale al numero
#intenti per predire l'output
#utilizzo funzione softmax (funzione esponenziale normalizzata)
model = tf.keras.Sequential()
#primo strato
model.add(tf.keras.layers.Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))
#secondo strato
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))
#terzo strato
model.add(tf.keras.layers.Dense(len(train_y[0]), activation='softmax'))

#discesa stocastica del gradiente [Nesterov accelerated gradient(è una tecnica di ottimizzazione)]
sgd = tf.keras.optimizers.legacy.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

#salvataggio modello
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('chatbot_model.h5', hist)

print("Modello creato")
