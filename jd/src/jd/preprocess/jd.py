from itertools import zip_longest

from kiwipiepy import Kiwi

from .text import tokenize
from jd.util import load_list_from_file, split_dict_by_key, get_path_from_service_root


def tokenize_jd_data(jd_data,
                     kiwi_ctx=None, 
                     kiwi_jd_dictionary_fullpath='',
                     verbose=False):
    """
    is_concat_words: set True, if tokenized data would be used for `Tokenizer` from keras.
                     or False, if this would be used for `Word2Vec`
    """
    content_keys = load_list_from_file(
        get_path_from_service_root('JD_DATA_PATH', 'JD_METADATA_CONTENT_TYPE_FILENAME'))

    category_classes = load_list_from_file(
        get_path_from_service_root('JD_DATA_PATH', 'JD_METADATA_CATEGORIES_FILENAME'))

    if not kiwi_ctx:
        kiwi_ctx = Kiwi(num_workers=4)
    
        if kiwi_jd_dictionary_fullpath:
            print(f'load kiwi jd dictionary: {kiwi_jd_dictionary_fullpath}')
            kiwi_ctx.load_user_dictionary(kiwi_jd_dictionary_fullpath)
    
        kiwi_ctx.prepare()

    if type(jd_data) == dict:
        jd_data = [jd_data]

    if verbose:
        print('tokenization started')

    split_res = [split_dict_by_key(jd, split_keys=['category']) for jd in jd_data]
    jds, categories = list(zip(*split_res))
    categories = [v for c in categories for v in c.values()]
    tokenized_jds = list()
    for jd, category in zip_longest(jds, categories, fillvalue=None):
        if categories and not category:
            raise AssertionError(f'all of jd data seems to have category.\n'
                                 f'but category not exist on wd_id: {jd["wd_id"]}')

        if category:
            if category not in category_classes:
                print(f'unknown category: \'{category}\', this would be ignored\n'
                      f'jd: wd_id: {jd["wd_id"]}, category: {category}')
                continue

        tokenized_jd = tokenize(jd, kiwi_ctx=kiwi_ctx, value_filter_key=content_keys)
        tokenized_jds.append(tokenized_jd)
       

    if categories:
        return tokenized_jds, categories

    return tokenized_jds


def transform_jd_categories(categories):
    avail_category = load_list_from_file(get_path_from_service_root('JD_DATA_PATH', 'JD_METADATA_CATEGORIES_FILENAME'))

    return [avail_category.index(c) for c in categories]