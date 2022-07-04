def split_dict_by_key(target, split_keys: list):
    a, b = dict(), dict()

    for k, v in target.items():
        if k in split_keys:
            b[k] = v
        else:
            a[k] = v

    return a, b
