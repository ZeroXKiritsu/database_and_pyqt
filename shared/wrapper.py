import sys
import logs.server_log
import logs.client_log
import logging

if sys.argv[0].find('client') == -1:
    logger = logging.getLogger('server')
else:
    logger = logging.getLogger('client')


def log(func_to_log):
    def wrapper(*args , **kwargs):
        logger.debug(f'called function {func_to_log.__name__} '
                     f'with params {args} , {kwargs}. Call from'
                     f' module {func_to_log.__module__}')
        ret = func_to_log(*args , **kwargs)
        return ret
    return wrapper