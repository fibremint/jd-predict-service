from decouple import config
from fastapi import FastAPI
import tensorflow as tf
from kiwipiepy import Kiwi
import numpy as np 
from jd.preprocess import tokenize_jd_data, w2v_preprocess_data
from jd.model import load_jd_text_model
from jd.model.opts import opt
from jd.util import load_list_from_file, get_path_from_service_root

from . import schemas


categories = load_list_from_file(
    get_path_from_service_root('JD_DATA_PATH', 'JD_METADATA_CATEGORIES_FILENAME'))
                               
kiwi_ctx = Kiwi(num_workers=4)
kiwi_ctx.prepare()

w2v_model = load_jd_text_model(model_type='word2vec')
lstm_model = tf.saved_model.load(get_path_from_service_root('TF_LSTM_MODEL_PATH',
                                                            'TF_LSTM_SAVED_MODEL_PATH'))

app = FastAPI(root_path=config('SERVE_TF_ROOT_PATH'), version='0.3.7')


@app.post('/jd/predict')
def predict_jd(jd: schemas.JD):
    jd = dict(jd)
    jd_tokenized = tokenize_jd_data(jd, kiwi_ctx=kiwi_ctx)
    jd_tokenized = w2v_preprocess_data(w2v_model=w2v_model,
                                       data=jd_tokenized,
                                       pad_maxlen=opt.w2v_data_maxlen)
    jd_tokenized = tf.convert_to_tensor(jd_tokenized, dtype=tf.float32)

    res = lstm_model.signatures['serving_default'](embedding_input=jd_tokenized)

    predicted_category_idx = np.argmax(res['prediction'].numpy())
    predicted_category = categories[predicted_category_idx]

    return {
        'prediction': predicted_category
    }
