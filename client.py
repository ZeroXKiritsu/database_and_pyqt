import sys
import json
import time
import re
import logging
import threading
from lib.vars import *
from lib.utils import server_settings, get_message, send_message
from lib.errors import ReqFieldMissingError, ServerError, IncorrectDataRecivedError
from lib.metaclasses import ClientVerifier
import socket

CLIENT_LOGGER = logging.getLogger('client')

class ClientSender(threading.Thread, metaclass=ClientVerifier):
    def __init__(self, account_name, sock):
        self.account_name = account_name
        self.sock = sock
        super.__init__()

    def create_exit_message(self):
        out = {ACTION: EXIT, TIME: time.time(), ACCOUNT_NAME: self.account_name}
        CLIENT_LOGGER.info(f"Выход {out}")
        return out

    def create_message(self):
        to_user = input('Получатель сообщения')
        message = input('Введите сообщение')
        message_dict = {ACTION: MSG, TIME: time.time(), SENDER: self.account_name, DESTINATION: to_user,
                        MSG_TEXT: message}
        CLIENT_LOGGER.debug(f'Сформирован словарь сообщения {message_dict}')
        try:
            send_message(self.sock, message_dict)
        except:
            CLIENT_LOGGER.error('Потеряно соединение с сервером')
            sys.exit(1)

    def create_who_message(self):
        message_dict = {ACTION: WHO, TIME: time.time(), SENDER: self.account_name, DESTINATION: self.account_name,
                        MSG_TEXT: None}
        CLIENT_LOGGER.debug(f'Сформирован словарь сообщения {message_dict}')
        try:
            send_message(self.sock, message_dict)
        except:
            CLIENT_LOGGER.error('Потеряно соединение с сервером')
            sys.exit(1)

    def run(self):
        while True:
            self.help()
            command = input('Введите команду').lower()
            if command == 'message' or command == 'm':
                self.create_message()
            elif command == 'help' or command == 'h':
                self.help()
            elif command == 'who' or command == 'w':
                CLIENT_LOGGER.debug(f"Запрос пользователей сервера")
                self.create_who_message()
            elif command == 'exit' or command == 'e' or command == 'q':
                send_message(self.sock, self.create_exit_message())
                CLIENT_LOGGER.info('Завершение работы по командле пользователя')
                time.sleep(0.5)
                break
            else:
                print('Команда не распознана, попробуйте снова.')

    def help(self):
        print('Поддерживаемые команды')
        print('message (m) - отправить сообщение. Кому и текс будет запрошены отдельно')
        print('who (w) - имена пользователей')
        print('help (h) - вывести подсказки по командам')
        print('exit (q или e) - выход из программы')


class ClientReader(threading.Thread, metaclass=ClientVerifier):
    def __init__(self, account_name, sock):
        self.account_name = account_name
        self.sock = sock
        super.__init__()

    def run(self):
        while True:
            try:
                message = get_message(self.sock)
                if ACTION in message and message[ACTION] == MSG and SENDER in message \
                    and DESTINATION in message and MSG_TEXT in message and message[
                    DESTINATION] == self.account_name:
                    print(f'Получено сообщение от пользователя {message[SENDER]}:\n{message[MSG_TEXT]}')
                    CLIENT_LOGGER.info(f'Получено сообщение от пользователя {message[SENDER]}:\n{message[MSG_TEXT]}')
                elif ACTION in message and message[ACTION] == WHO and SENDER in message \
                        and DESTINATION in message and MSG_TEXT in message and message[
                    DESTINATION] == self.account_name:
                    print(f'Получено сообщение от пользователя {message[SENDER]}:\n{message[MSG_TEXT]}')
                    CLIENT_LOGGER.info(f'Получено сообщение от пользователя {message[SENDER]}:\n{message[MSG_TEXT]}')
                else:
                    CLIENT_LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')
            except IncorrectDataRecivedError:
                CLIENT_LOGGER.error(f'Не удалось декодировать полученное сообщение.')
            except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError):
                CLIENT_LOGGER.critical(f'Потеряно соединение с сервером.')
                break

def create_presence(account_name='Guest'):
    out = {ACTION: PRESENCE, TIME: time.time(), USER: {ACCOUNT_NAME: account_name}}
    CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out

def process_handler(message):
    CLIENT_LOGGER.debug(f'Разбор приветственного сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:  # message[RESPONSE]==200:
            CLIENT_LOGGER.debug(f"{message[RESPONSE]} содержит {ERROR_200}")
            return message[MSG]  # ERR200
        elif message[RESPONSE] == ERROR_400:  # message[RESPONSE]==400:
            CLIENT_LOGGER.debug(f"{message[RESPONSE]} содержит {ERROR_400}")
            raise ServerError(f"{ERROR_400}: {message[ERROR]}")
    raise ReqFieldMissingError(RESPONSE)

def get_user():
    while True:
        account = input("введите имя пользователя >>> ")
        if not re.match(r"[A-Za-z]", account) or len(account) > 25 or len(account) < 3:
            CLIENT_LOGGER.error(f"недопустимое имя пользователя: {account}")
            print("Имя пользователя должно быть от 3 до 25 латинских символов")
        elif account.lower().strip() == 'guest':
            CLIENT_LOGGER.error(f"недопустимое имя пользователя: {account}")
            print("Недоспустимое имя пользователя")
        else:
            break
    return account

def create_action(account_name, action, msg=None):
    out = {ACTION: action, TIME: time.time(), USER: {ACCOUNT_NAME: account_name}, MSG: msg}
    CLIENT_LOGGER.debug(f'Сформировано {action} сообщение для пользователя {account_name}')
    CLIENT_LOGGER.debug(f"{out}")
    return out

def start_client():
    srv_settings = server_settings()
    server_address = srv_settings[0]
    server_port = srv_settings[1]
    print(f"start client on: {server_address}:{server_port}")
    CLIENT_LOGGER.info(f"start client on: {server_address}:{server_port}")

    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        transport.connect((server_address, server_port))
        send_message(transport, create_presence())
        answer = process_handler(get_message(transport))
        CLIENT_LOGGER.info(f"соединение с сервером {server_address}:{server_port}. Ответ: {answer}")
        print(f"соединение с сервером {server_address}:{server_port} \n {answer}")

        # авторизация
        account_name = get_user()
        CLIENT_LOGGER.info(f"Guest авторизовался как {account_name}")
        CLIENT_LOGGER.debug(
            f"отправка {AUTH} сообщения на сервер {server_address}:{server_port} от user={account_name}")
        message_to_server = create_action(account_name, action=AUTH, msg=None)
        send_message(transport, message_to_server)
        try:
            answer = process_handler(get_message(transport))
            print(answer)
        except (ValueError, json.JSONDecodeError):
            print(answer)
            CLIENT_LOGGER.error(f"{ERROR_400}. Не удалось декодировать сообшение от сервера")
            print(f"{ERROR_400}. Не удалось декодировать сообшение от сервера")

    except json.JSONDecodeError:
        CLIENT_LOGGER.error(f"не удалось декодировать JSON-строку")
        print(f"не удалось декодировать JSON-строку")
        sys.exit(1)
    except ServerError as error:
        CLIENT_LOGGER.error(f"ошибка при установке соединения: {error.text}")
        print(f"ошибка при установке соединения: {error.text}")
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f"в ответе сервера нет обязательного поля {missing_error.missing_field}")
        sys.exit(1)
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f"Не удалось подключиться к серверу {server_address}:{server_port}")
        sys.exit(1)
    else:
        receiver = ClientReader(account_name, transport)
        receiver.daemon = True
        receiver.start()


        user_interface = ClientSender(account_name, transport)
        user_interface.daemon = True
        user_interface.start()
        CLIENT_LOGGER.debug('Запущены процессы')


        while True:
            time.sleep(1)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break

if __name__ == '__main__':
    start_client()