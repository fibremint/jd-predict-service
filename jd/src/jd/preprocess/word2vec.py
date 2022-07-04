from tensorflow.keras.preprocessing.sequence import pad_sequences


def _w2v_word_to_token(w2v_model, word):
    try:
        return w2v_model.wv.key_to_index[word]

    except KeyError:
        return 0


def w2v_preprocess_data(w2v_model, data, pad_maxlen):
    data = [[_w2v_word_to_token(w2v_model, elem) for elem in row] for row in data]

    return pad_sequences(data, maxlen=pad_maxlen, padding='pre', value=0)
