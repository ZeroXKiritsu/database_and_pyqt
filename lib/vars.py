import logging

DEFAULT_PORT = 7777
DEFAULT_IP = '127.0.0.1'
MAX_CONNECTIONS = 5
PACKAGE_LENGTH = 1024
ENCODING = 'utf-8'
SERVER_TIMEOUT = 1

ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'from'
DESTINATION = 'to'

PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
AUTH = 'auth'
ALERT = 'alert'
MSG = 'msg'
MSG_TEXT = 'msg_text'
LISTEN = 'listen'
EXIT = 'exit'
WHO = 'who'

CLIENT_LISTEN = False

ERROR_200 = '200:OK'
ERROR_400 = '400:Bad Request'
ERROR_USER_ALREADY_EXIST = 'Имя пользователя уже занято'

RESPONSE_200 = {RESPONSE: 200}
RESPONSE_400 = {RESPONSE: 400, ERROR: None}

LOG_LEVEL = logging.DEBUG
LOG_FORMATTING = '%(asctime)s %(levelname)s %(filename)s %(message)s'