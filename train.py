import os

import tensorflow as tf
from tensorflow.keras import Sequential, layers
import numpy as np
from jd.data import load_tokenized_jd_data
from jd.model import load_jd_text_model, create_lstm_model
from jd.preprocess import w2v_preprocess_data, transform_jd_categories
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report



SEED = 42
np.random.seed(SEED)
tf.random.set_seed(SEED)

batch_size = 32

os.environ['JD_SERVICE_PATH'] = os.getcwd()
os.environ['CUDA_VISIBLE_DEVICES'] = "-1"


def train_eval():
    # if not tensorboard_logdir:
    #     tensorboard_logdir = get_path_from_service_root('TF_LSTM_LOGDIR')
    #     create_path_if_not_exist(tensorboard_logdir)

    # if not model_save_path:
    #     model_save_path = get_path_from_service_root('TF_LSTM_MODEL_PATH')
    #     create_path_if_not_exist(model_save_path)

    # avail_save_format = ('weights', 'saved_model')

    jds, categories = load_tokenized_jd_data('./data/jd/jd-tokenized.pkl')
    word2vec_model = load_jd_text_model(model_type='word2vec')

    X = w2v_preprocess_data(word2vec_model, jds, pad_maxlen=250)
    # X = pad_sequences(X, maxlen=250, padding='pre', value=0)
    y = transform_jd_categories(categories)
    y = np.array(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=SEED)

    model = create_lstm_model(4, word2vec_model, input_maxlen=250)

    model.fit(X_train, y_train, epochs=5, batch_size=batch_size, verbose=True)
    model.save_weights('./data/model/jd_tf_lstm/saved_manually/weight.h5')


    
if __name__ == '__main__':
    train_eval()