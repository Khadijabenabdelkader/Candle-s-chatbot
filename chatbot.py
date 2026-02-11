import json
import random
import nltk
import numpy as np
import pickle
from nltk.stem.porter import PorterStemmer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD

stemmer = PorterStemmer()
nltk.download("punkt")

# Load intents
with open("intents.json") as file:
    data = json.load(file)
RETRAIN = True

# Load or create training data
if not RETRAIN:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
else:
    words = []
    labels = []
    docs_x = []
    docs_y = []


    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])
        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = sorted(set(stemmer.stem(w.lower()) for w in words if w.isalpha()))
    labels = sorted(labels)

    training = []
    output = []
    out_empty = [0] * len(labels)

    for x, doc in enumerate(docs_x):
        bag = []
        stemmed_words = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            bag.append(1 if w in stemmed_words else 0)

        out_row = out_empty[:]
        out_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(out_row)

    training = np.array(training)
    output = np.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

# Model
model = Sequential()
model.add(Dense(16, input_shape=(len(training[0]),), activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(16, activation="relu"))
model.add(Dense(len(output[0]), activation="softmax"))

model.compile(
    optimizer=SGD(learning_rate=0.01, momentum=0.9),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.fit(training, output, epochs=300, batch_size=8, verbose=1)
model.save("chatbot_model.keras")

# Bag of words
def bag_of_words(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [stemmer.stem(w.lower()) for w in sentence_words]
    bag = [1 if w in sentence_words else 0 for w in words]
    return np.array(bag)

def get_response(user_input):
    results = model.predict(np.array([bag_of_words(user_input)]), verbose=0)[0]
    confidence = max(results)

    if confidence < 0.5:
        return "Sorry, I didn't understand that."

    tag = labels[np.argmax(results)]

    for intent in data["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])
