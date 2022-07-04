import os

import tensorflow as tf
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from jd.data import load_tokenized_jd_data
from jd.model import load_jd_text_model, create_lstm_model
from jd.preprocess import w2v_preprocess_data, transform_jd_categories
from jd.util import load_list_from_file



SEED = 42
np.random.seed(SEED)
tf.random.set_seed(SEED)

batch_size = 32

os.environ['JD_SERVICE_PATH'] = os.getcwd()
os.environ['CUDA_VISIBLE_DEVICES'] = "-1"


def eval():
    classes = load_list_from_file('./data/jd/jd-categories.txt')

    jds, categories = load_tokenized_jd_data('./data/jd/jd-tokenized.pkl')
    word2vec_model = load_jd_text_model(model_type='word2vec')

    X = w2v_preprocess_data(word2vec_model, jds, pad_maxlen=250)
    # X = pad_sequences(X, maxlen=250, padding='pre', value=0)
    y = transform_jd_categories(categories)
    y = np.array(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=SEED)

    model = create_lstm_model(4, word2vec_model, input_maxlen=250)
    # model.load_weights('./data/model/jd_tf_lstm/checkpoint/cp-0005.ckpt')
    model.load_weights('./data/model/jd_tf_lstm/saved_manually/weight.h5')

    y_pred = model.predict(X_test, batch_size=len(X_test) // batch_size+1)
    y_pred = np.argmax(y_pred, axis=1)

    y_test_t = [classes[y_elem] for y_elem in y_test]  
    y_pred_t = [classes[y_elem] for y_elem in y_pred] 

    cm_res = confusion_matrix(y_test_t, y_pred_t)
    print(f'confusion matrix:\n{cm_res}\n')
    cr_res = classification_report(y_test, y_pred, target_names=classes)
    print(f'classification report:\n{cr_res}\n')



if __name__ == '__main__':
    eval()