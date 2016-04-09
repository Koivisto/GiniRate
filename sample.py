from __future__ import print_function
from keras.models import Sequential
from keras.models import model_from_json
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.utils.data_utils import get_file

import numpy as np
import random
import sys
import os

startSentence = sys.argv[1];
origTemperature = sys.argv[2];

#Helper function to sample
def sample(a, temperature=origTemperature):
    a = np.log(a) / temperature
    a = np.exp(a) / np.sum(np.exp(a))
    return np.argmax(np.random.multinomial(1, a, 1))

#Load the model
if os.path.isfile('model.json') and os.path.isfile('model.h5'):
    print("Loading model")
    model = model_from_json(open('model.json').read())
    model.load_weights('model.h5')
    print("Compiling")
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
    generated = startSentence
    print("Generating with seed " + startSentence)
    for i in range(400):
        x = np.zeros((1, maxlen, len(chars)))
        for t, char in enumerate(sentence):
            x[0, t, char_indices[char]] = 1.

        preds = model.predict(x, verbose=0)[0]
        next_index = sample(preds, diversity)
        next_char = indices_char[next_index]

        generated += next_char
        sentence = sentence[1:] + next_char

        sys.stdout.write(next_char)
        sys.stdout.flush()
    print()
