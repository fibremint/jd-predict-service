import json


def load_list_from_file(filepath, encoding='utf-8', remove_newline=True):
    with open(filepath, encoding=encoding) as f:
        data = f.readlines()

        if remove_newline:
            data = [d.replace('\n', '') for d in data]

    return data


def load_json(filepath, encoding='utf-8'):
    with open(filepath, encoding=encoding) as f:
        data = json.load(f)

    return data
