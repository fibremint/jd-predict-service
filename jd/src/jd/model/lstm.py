from enum import Enum

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Sequential, layers
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import numpy as np

from jd.data import load_tokenized_jd_data
from jd.model import load_jd_text_model
from jd.preprocess import w2v_preprocess_data, transform_jd_categories
from jd.util import create_path_if_not_exist, get_path_from_service_root

from .opts import opt


# ref: https://www.kaggle.com/guichristmann/lstm-classification-model-with-word2vec
# ref: https://teddylee777.github.io/tensorflow/word2vec-%EA%B3%BC-keras%EC%9D%98-Embedding-layer-%ED%99%9C%EC%9A%A9%EB%B2%95
def create_lstm_model(num_categories, word2vec_model, input_maxlen):
    w2v_weights = word2vec_model.wv.vectors
    vocab_size, embedding_size = w2v_weights.shape

    model = Sequential()
    model.add(layers.Embedding(input_dim=vocab_size,
                               output_dim=embedding_size,
                               weights=[w2v_weights],
                               input_length=input_maxlen,
                               mask_zero=True,
                               trainable=False,
                               name='embedding'))

    model.add(layers.Bidirectional(layers.LSTM(100)))
    model.add(layers.Dense(num_categories, activation='softmax', name='prediction'))

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    return model


def create_trained_lstm_model(tokenized_jd_save_fullpath='',
                              model_save_path='', 
                              model_save_checkpoint_path='',
                              tensorboard_logdir='',
                              is_save_checkpoint=True,
                              is_log_tensorboard=True,
                              seed=None,
                              verbose=True):

    if is_log_tensorboard and not tensorboard_logdir:
        tensorboard_logdir = get_path_from_service_root('TF_LSTM_LOGPATH')
        create_path_if_not_exist(tensorboard_logdir)

    if is_save_checkpoint and not model_save_checkpoint_path:
        model_save_checkpoint_path = get_path_from_service_root('TF_LSTM_MODEL_PATH', 'TF_LSTM_CHECKPOINT_PATH')
        create_path_if_not_exist(model_save_checkpoint_path)

    if not model_save_path:
        model_save_path = get_path_from_service_root('TF_LSTM_MODEL_PATH', 'TF_LSTM_SAVED_MODEL_PATH')
        create_path_if_not_exist(model_save_path)

    jds, categories = load_tokenized_jd_data(tokenized_jd_save_fullpath)
    w2v_model = load_jd_text_model(model_type='word2vec')

    X = w2v_preprocess_data(w2v_model, jds, pad_maxlen=opt.w2v_data_maxlen)
    y = transform_jd_categories(categories)
    y = np.array(y)

    if seed:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed)
    else:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    lstm_model = create_lstm_model(num_categories=opt.num_categories,
                                   word2vec_model=w2v_model,
                                   input_maxlen=opt.w2v_data_maxlen)

    keras_callbacks = list()

    if is_log_tensorboard:
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=tensorboard_logdir)
        keras_callbacks.append(tensorboard_callback)

    if is_save_checkpoint:
        save_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(filepath=model_save_checkpoint_path,
                                                                      save_weights_only=True,
                                                                      verbose=True)

        keras_callbacks.append(save_checkpoint_callback)

    lstm_model.fit(X_train, y_train, epochs=opt.lstm_epochs, batch_size=opt.lstm_batch_size,
                  validation_data=(X_test, y_test), verbose=verbose, callbacks=keras_callbacks)

    lstm_model.save(model_save_path)
    
    print(f'saved lstm model successfully')
