from functools import wraps


def errmsghandler(e):
    def _decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print('{}: {}'.format(e.__class__.__name__, e))
            print('---')
            func()
            print('---')
            exit(1)
        return wrapper
    return _decorator
