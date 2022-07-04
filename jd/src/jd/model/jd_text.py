from enum import Enum
import pickle

from tensorflow.keras.preprocessing.text import Tokenizer
from gensim.models import Word2Vec

from jd.data import load_tokenized_jd_data
from jd.util import create_path_if_not_exist, get_path_from_service_root, get_warn_msg_path_not_set_use_default



class _ModelType(Enum):
    W2V = 'word2vec'
    KERAS_TOKENIZER = 'keras_tokenizer'

_avail_model_type = tuple([e.value for e in _ModelType])
_default_model_type = _ModelType.W2V.value


def _save_jd_keras_tokenizer_model(tokenized_jds,
                                   categories,
                                   model_save_path,
                                   keras_tokenizer_jd_data_save_path,
                                   is_save_keras_tokenized_jd_data=False):

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(tokenized_jds)

    with open(model_save_path, 'wb') as f_td:
        pickle.dump(tokenizer, f_td, protocol=pickle.HIGHEST_PROTOCOL)  

    # if is_save_keras_tokenized_jd_data:
    #     X = tokenizer.texts_to_sequences(tokenized_jds)

    #     with open(keras_tokenizer_jd_data_save_path, 'wb') as f_td:
    #         pickle.dump({
    #             'X': X,
    #             'y': categories
    #         }, f_td, protocol=pickle.HIGHEST_PROTOCOL)

    #     print('saved tokenized jd data')


def _save_jd_word2vec_model(tokenized_jds, model_save_path):
    model = Word2Vec(sentences=tokenized_jds, vector_size=100, window=5, min_count=5, workers=4, sg=0)
    model.save(model_save_path)


def _validate_model_type(model_type):
    if model_type not in _avail_model_type:
        raise AssertionError(f'invalid model type. given: \'{model_type}\'\n'
                             f'available model type: {_avail_model_type}')


def create_trained_jd_text_model(model_type='',
                                 is_save_keras_tokenized_jd_data=False,
                                 tokenized_jd_data_path='',
                                 keras_tokenizer_path='',
                                 keras_tokenizer_jd_data_path='',
                                 word2vec_model_path=''):

    def _resolve_path():
        nonlocal tokenized_jd_data_path, keras_tokenizer_path, keras_tokenizer_jd_data_path, word2vec_model_path
        
        curr_action = 'save jd text model'
        
        if not tokenized_jd_data_path:
            print(f"{get_warn_msg_path_not_set_use_default('tokenized jd data', action=curr_action,)}")

            tokenized_jd_data_path = get_path_from_service_root('JD_DATA_PATH', 'JD_TOKENIZED_DATA_FILENAME')
            create_path_if_not_exist(tokenized_jd_data_path)

        if model_type == _ModelType.KERAS_TOKENIZER.value and not keras_tokenizer_path:
            print(f"{get_warn_msg_path_not_set_use_default('keras tokenizer', action=curr_action)}")

            keras_tokenizer_path = get_path_from_service_root('KERAS_TOKENIZER_PATH', 'KERAS_TOKENIZER_JD_FILENAME')
            create_path_if_not_exist(keras_tokenizer_path)

        if model_type == _ModelType.KERAS_TOKENIZER.value \
            and is_save_keras_tokenized_jd_data \
            and not keras_tokenizer_jd_data_path:
            print(f"{get_warn_msg_path_not_set_use_default('keras tokenizer jd data', action=curr_action)}")

            keras_tokenizer_jd_data_path = get_path_from_service_root('KERAS_TOKENIZER_PATH', 'KERAS_TOKENIZER_JD_DATA_FILENAME')
            create_path_if_not_exist(keras_tokenizer_jd_data_path)

        if model_type == _ModelType.W2V.value and not word2vec_model_path:
            print(f"{get_warn_msg_path_not_set_use_default('Word2Vec model', action=curr_action)}")

            word2vec_model_path = get_path_from_service_root('W2V_PATH', 'W2V_JD_MODEL_FILENAME')
            create_path_if_not_exist(word2vec_model_path)

    if not model_type:
        print(f'type of the model is not set. set to default value \'{_default_model_type}\'')
        model_type = _default_model_type

    _validate_model_type(model_type)

    _resolve_path()

    tokenized_jds, categories =  \
        load_tokenized_jd_data(tokenized_jd_data_path)

    if model_type == _ModelType.W2V.value:
        _save_jd_word2vec_model(tokenized_jds,
                                model_save_path=word2vec_model_path)
   
    elif model_type == _ModelType.KERAS_TOKENIZER.value:
        _save_jd_keras_tokenizer_model(tokenized_jds, categories,
                                       model_save_path=keras_tokenizer_path,
                                       keras_tokenizer_jd_data_save_path=keras_tokenizer_jd_data_path)

    print(f'model \'{model_type}\' saved successfully')


def load_jd_text_model(model_type='',
                       keras_tokenizer_path='',
                       keras_tokenizer_jd_data_path='',
                       word2vec_model_path='',
                       is_load_keras_tokenized_jd_data=False):
    '''
    load tokenizer and word2vec model which fit to jd
    '''

    def _resolve_path():
        nonlocal keras_tokenizer_path, keras_tokenizer_jd_data_path, word2vec_model_path

        curr_action = 'load jd text model'

        if model_type == _ModelType.KERAS_TOKENIZER.value and not keras_tokenizer_path:
            print(f"{get_warn_msg_path_not_set_use_default('keras tokenizer', action=curr_action)}")
            keras_tokenizer_path = get_path_from_service_root('KERAS_TOKENIZER_PATH', 'KERAS_TOKENIZER_JD_FILENAME')

        if model_type == _ModelType.KERAS_TOKENIZER.value \
            and is_load_keras_tokenized_jd_data \
            and not keras_tokenizer_jd_data_path:

            print(f"{get_warn_msg_path_not_set_use_default('keras tokenizer jd data', action=curr_action)}")
            keras_tokenizer_jd_data_path = get_path_from_service_root('KERAS_TOKENIZER_PATH', 'KERAS_TOKENIZER_JD_DATA_FILENAME')

        if model_type == _ModelType.W2V.value and not word2vec_model_path:
            print(f"{get_warn_msg_path_not_set_use_default('Word2Vec model', action=curr_action)}")
            word2vec_model_path = get_path_from_service_root('W2V_PATH', 'W2V_JD_MODEL_FILENAME')

    if not model_type:
        model_type = _default_model_type
        
    _validate_model_type(model_type)

    _resolve_path()

    if model_type == 'word2vec':
        model = Word2Vec.load(word2vec_model_path)

    elif model_type == 'keras_tokenizer':
        with open(keras_tokenizer_path, 'rb') as f_t:
            model = pickle.load(f_t)

    print(f'load \'{model_type}\' model successfully')

    return model
