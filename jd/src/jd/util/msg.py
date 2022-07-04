def get_warn_msg_path_not_set_use_default(name: str, action: str = ''):
    if action:
        return f'{action}: path of the {name} is not set. set to the default value.'
    return f'path of the {name} is not set. set to the default value.'
