import sys
import os
from datetime import datetime
import logging

sys.path.append('../')
from lib.vars import LOG_LEVEL, ENCODING, LOG_FORMATTING

CLIENT_FORMATTING = logging.Formatter(LOG_FORMATTING)

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'client_' + datetime.now().strftime("%Y%m%d_%H%M%S") + '.log')

LOG_FILE = logging.FileHandler(PATH, encoding=ENCODING)
LOG_FILE.setFormatter(CLIENT_FORMATTING)

LOGGER = logging.getLogger('client')
LOGGER.addHandler(LOG_FILE)
LOGGER.setLevel(LOG_LEVEL)

if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Отладка')
    LOGGER.info('Информация')