import sys
import os
from datetime import datetime
import logging.handlers

sys.path.append('../')
from lib.vars import LOG_LEVEL, ENCODING, LOG_FORMATTING

SERVER_FORMATTING = logging.Formatter(LOG_FORMATTING)

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'server_' + datetime.now().strftime("%Y%m%d_%H%M%S") + '.log')

LOG_FILE = logging.handlers.TimedRotatingFileHandler(PATH, encoding=ENCODING, interval=1, when='midnight')
LOG_FILE.setFormatter(SERVER_FORMATTING)

LOGGER = logging.getLogger('server')
LOGGER.addHandler(LOG_FILE)
LOGGER.setLevel(LOG_LEVEL)

if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Отладка')
    LOGGER.info('Информация')