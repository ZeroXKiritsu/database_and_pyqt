import sys
import logging
import inspect

if sys.argv[0].rfind('server') > 0:
    DEC_LOGGER = logging.getLogger('server')
else:
    DEC_LOGGER = logging.getLogger('client')

def log(func):
    def wrapper(*args, **kwargs):
        ret_wrapper = func(*args, **kwargs)
        DEC_LOGGER.debug(f'Called function:{func.__module__}.{func.__name__}:({args}, {kwargs}).'
                         f'Called from function: {inspect.stack()[1][3]}')
        return ret_wrapper
    return wrapper