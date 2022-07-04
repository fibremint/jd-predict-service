import os


# ref: https://stackoverflow.com/questions/43570838/how-do-you-use-python-decouple-to-load-a-env-file-outside-the-expected-paths
def _build_path_from_env(*args, env_root_path):
    from decouple import Config, RepositoryEnv
    
    env_config = Config(RepositoryEnv(os.path.join(env_root_path, '.env')))
    paths = [env_config(env) for env in args]

    try:
        path = os.path.join(*paths)
        
    except TypeError as e:
        print(e)
        raise KeyError('failed to read environment variable from .env')
    
    return path


def get_path_from_service_root(*args):
    try:
        service_root_path = os.environ['JD_SERVICE_PATH']

    except KeyError:
        raise AttributeError('environment variable \'JD_SERVICE_PATH\' is not set')

    sub_path = _build_path_from_env(*args, env_root_path=service_root_path)

    return os.path.join(service_root_path, sub_path)


def create_path_if_not_exist(path):
    if not os.path.isdir(path):
        path = os.path.dirname(path)
        
    if not os.path.exists(path):
        os.makedirs(path)
