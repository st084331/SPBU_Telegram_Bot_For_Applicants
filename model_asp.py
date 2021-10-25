import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy
import tflearn
import tensorflow as tf
import json
import random
import pickle


with open('intents_asp.json') as file:
    data = json.load(file)


try:
    with open('testdata_asp.pickle', 'rb') as f:
        words, labels, training, output = pickle.load(f)
except:
    # Prepare Data
    ###################################################
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data['intents']:
        for pattern in intent['patterns']:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent['tag'])

        if intent['tag'] not in labels:
            labels.append(intent['tag'])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))
    labels = sorted(labels)

    training = []
    output = []

    out_empty  = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)

    with open('testdata_asp.pickle', 'wb') as f:
       pickle.dump((words,labels,training,output), f)
###################################################

tf.compat.v1.reset_default_graph()
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 10)
net = tflearn.fully_connected(net, 10)
net = tflearn.fully_connected(net, len(output[0]), activation='softmax')
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
   model.load('Model_asp.tflearn')
except:
    model.fit(training, output, n_epoch=10000, show_metric=True)
    model.save('Model_asp.tflearn')

def bag_of_words(sentence, words):
    bag = [0 for _ in range(len(words))]
    sent_words = [stemmer.stem(word.lower()) for word in nltk.word_tokenize(sentence)]
    for se in sent_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    return numpy.array(bag)

def chat_AI(message):
    results = model.predict([bag_of_words(message, words)])
    results_index = numpy.argmax(results)
    tag = labels[results_index]
    if results[0][results_index] < 0.3:
        return "Sorry, I cannot answer this question. Reformulate it or contact the applicable commission. Thank you for understanding."
    for tg in data['intents']:
        if tg['tag'] == tag:
            responses = tg['responses']
    return random.choice(responses)


