# CHATBOT
• intents.json: file contenente le possibili domande e le relative risposte del chatbot;

• training.py: file di allenamento della rete neurale costituita da tre strati,
1° strato con 128 neuroni, secondo con 64, 3° strato di output contenente il numero di neuroni uguale al numero intenti per predire l'output

• chatbot_model.h5: file contenente i dati di allenamento della rete neurale;

• classes.pkl: file generato da pickle (libreria python), un modulo Python che permette agli oggetti di essere serializzati a file su disco 
e deserializzati indietro nel programma in fase di runtime. Contiene un flusso di byte che rappresenta gli oggetti.
Questo file contiene i tag presenti all'interno del file json.
2 classes ['arrivederci', 'saluti']

• words.pkl: file sempre generato da pickle (libreria python) contenente le parole presenti all'interno del file json.
20 unique lemmatized words ["'", 'a', 'arrivederci', 'buona', 'buongiorno', 'c', 'ci', 'ciao', 'come', 'dopo', 'ehilã', 
'giornata', 'hey', 'qualcuno', 'qui', 'salve', 'stai', 'va', 'vediamo', 'ã¨']

• Chats.kv e Main.kv: file realizzati con kivy (framework Python gratuito e open source per lo sviluppo di app mobili), linguaggio molto simile a quello dei CSS che permette di tenere separata la gestione dell'interfaccia grafica da quello che è l'applicazione logica.

• chatguy.py: file contente l'interfaccia grafica. ESEGUIRE QUESTO FILE PER MESSAGGIARE CON IL CHATBOT






