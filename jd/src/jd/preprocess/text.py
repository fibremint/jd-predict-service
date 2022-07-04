def _filter_tokenized(analyzed):
    token_elem = list()

    for elem in analyzed[0][0]:
        word, word_type, _, _ = elem

        if word_type == 'SL' and len(word) >= 3:
            token_elem.append(word)
        elif word_type in ('NNG', 'NNP') and len(word) >= 2:
            token_elem.append(word)

    return token_elem


def tokenize(data, kiwi_ctx=None, value_filter_key: list = None):
    def _validate_filter_key(_data, _value_filter_key):
        data_keys = _data.keys()

        for vfk in _value_filter_key:
            if vfk not in data_keys:
                raise AssertionError(f'invalid key \'{vfk}\'')

    def _concat_str(_data, _value_filter_key, concat_with='\n'):
        target = list()
        for k in _value_filter_key:
            value = _data[k]
            if not value:
                continue

            value = value.lower()
            target.append(value)

        return concat_with.join(target)

    if not kiwi_ctx:
        from kiwipiepy import Kiwi
        
        kiwi_ctx = Kiwi(num_workers=4)
        kiwi_ctx.prepare()

    if type(data) == str:
        analyzed = kiwi_ctx.analyze(data)

        return _filter_tokenized(analyzed)

    elif type(data) == dict:
        if not value_filter_key:
            value_filter_key = list(data.keys())
        elif value_filter_key:
            _validate_filter_key(data, value_filter_key)

            target = _concat_str(data, value_filter_key)
            analyzed = kiwi_ctx.analyze(target)

            return _filter_tokenized(analyzed)
