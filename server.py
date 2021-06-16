import socket
import sys
import os
import argparse
import json
import logging
import select
import time
import threading
import configparser
import logs.server_log
from shared.errors import *
from shared.variables import *
from shared.utils import *
from shared.wrapper import log
from shared.descriptors import Port
from shared.metaclasses import ServerVerifier
from server_database import ServerStorage
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer
from gui import MainWindow, create_model, HistoryWindow, create_static_model, ConfigWindow
from PyQt5.QtGui import QStandardItemModel, QStandardItem

LOGGER = logging.getLogger('server')

NEW_CONNECTION = False
CONFLAG_LOCK = threading.Lock()


@log
def argument_parser(default_port, default_address):
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=default_port, type=int, nargs='?')
    parser.add_argument('-a', default=default_address, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    return listen_address, listen_port


class Server(threading.Thread, metaclass=ServerVerifier):
    port = Port()


    def __init__(self, listen_address, listen_port, database):
        self.addr = listen_address
        self.port = listen_port
        self.database = database
        self.clients = []
        self.messages = []
        self.names = dict()
        super().__init__()


    def init_socket(self):
        LOGGER.info(
            f'server launched, port to connect: {self.port}, '
            f'connections from: {self.addr}. '
            f'If address not specified, all connections '
            f'will be available')
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((self.addr, self.port))
        transport.settimeout(0.5)

        self.sock = transport
        self.sock.listen()

    def run(self):
        self.init_socket()
        while True:
            try:
                client, client_address = self.sock.accept()
            except OSError:
                pass
            else:
                LOGGER.info(f'connection with address {client_address} stabilized')
                self.clients.append(client)

            income_list = []
            outcome_list = []
            err_lst = []
            try:
                if self.clients:
                    income_list, outcome_list, err_lst = \
                        select.select(self.clients, self.clients, [], 0)
            except OSError as err:
                LOGGER.error(f'error in relation with sockets: {err}')

            if income_list:
                for client_with_message in income_list:
                    try:
                        self.income_message(get_message(
                            client_with_message), client_with_message)

                    except (OSError):
                        LOGGER.info(
                            f'user {client_with_message.getpeername()} '
                            f'logged out')
                        for name in self.names:
                            if self.names[name] == client_with_message:
                                self.database.user_logout(name)
                                del self.names[name]
                                break
                        self.clients.remove(client_with_message)

            for message in self.messages:
                try:
                    self.outcome_message(message, outcome_list)

                except (
                        ConnectionAbortedError,
                        ConnectionError,
                        ConnectionResetError,
                        ConnectionRefusedError
                ):
                    LOGGER.info(f'connection with user '
                                f'{message[DESTINATION]} is over')
                    self.clients.remove(self.names[message[DESTINATION]])
                    self.database.user_logout(message[DESTINATION])
                    del self.names[message[DESTINATION]]
            self.messages.clear()


    def outcome_message(self, message, listen_socks):

        if message[DESTINATION] in self.names and \
                self.names[message[DESTINATION]] in listen_socks:
            send_message(self.names[message[DESTINATION]], message)

            LOGGER.info(
                f'message to user {message[DESTINATION]} '
                f'by user {message[SENDER]}.')

        elif message[DESTINATION] in self.names and \
                self.names[message[DESTINATION]] not in listen_socks:
            raise ConnectionError

        else:
            LOGGER.error(
                f'user {message[DESTINATION]} not logged, '
                f'sending is unavailable.')


    def income_message(self, message, client):
        global NEW_CONNECTION
        LOGGER.debug(f'Parsing a message from a client : {message}')
        if ACTION in message and message[ACTION] == PRESENCE and \
                TIME in message and USER in message:

            if message[USER][ACCOUNT_NAME] not in self.names.keys():
                self.names[message[USER][ACCOUNT_NAME]] = client
                client_ip, client_port = client.getpeername()
                self.database.user_login(
                    message[USER][ACCOUNT_NAME], client_ip, client_port)
                send_message(client, RESPONSE_200)
                with CONFLAG_LOCK:
                    NEW_CONNECTION = True

            else:
                response = RESPONSE_400
                response[ERROR] = 'User name is occupied.'
                send_message(client, response)
                self.clients.remove(client)
                client.close()
            return

        elif ACTION in message and message[ACTION] == MESSAGE and \
                DESTINATION in message and TIME in message and SENDER\
                in message and MESSAGE_TEXT in message and \
                self.names[message[SENDER]] == client:
            self.messages.append(message)
            self.database.process_message(
                message[SENDER], message[DESTINATION])
            return

        elif ACTION in message and message[ACTION] == EXIT and \
                ACCOUNT_NAME in message and \
                self.names[message[ACCOUNT_NAME]] == client:
            self.database.user_logout(message[ACCOUNT_NAME])
            LOGGER.info(
                f'client {message[ACCOUNT_NAME]} correctly leave program')
            self.clients.remove(self.names[message[ACCOUNT_NAME]])
            self.names[message[ACCOUNT_NAME]].close()
            del self.names[message[ACCOUNT_NAME]]
            with CONFLAG_LOCK:
                NEW_CONNECTION = True
            return

        elif ACTION in message and message[ACTION] == GET_CONTACTS and \
                USER in message and self.names[message[USER]] == client:
            response = RESPONSE_202
            response[LIST_INFO] = self.database.get_contacts(message[USER])
            send_message(client, response)

        elif ACTION in message and message[ACTION] == ADD_CONTACT and \
                ACCOUNT_NAME in message and USER in message and \
                self.names[message[USER]] == client:
            self.database.add_contact(message[USER], message[ACCOUNT_NAME])
            send_message(client, RESPONSE_200)

        elif ACTION in message and message[ACTION] == REMOVE_CONTACT and \
                ACCOUNT_NAME in message and USER in message and \
                self.names[message[USER]] == client:
            self.database.remove_contact(message[USER], message[ACCOUNT_NAME])
            send_message(client, RESPONSE_200)

        elif ACTION in message and message[ACTION] == USERS_REQUEST and \
                ACCOUNT_NAME in message and \
                self.names[message[ACCOUNT_NAME]] == client:
            response = RESPONSE_202
            response[LIST_INFO] = [user[0]
                                   for user in self.database.users_list()]
            send_message(client, response)

        else:
            response = RESPONSE_400
            response[ERROR] = 'Incorrect request.'
            send_message(client, response)
            return


def server_launcher():
    config = configparser.ConfigParser()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config.read(f"{dir_path}/{'server.ini'}")
    listen_address, listen_port = argument_parser(
        config['SETTINGS']['Default_port'], config['SETTINGS']['Listen_Address']
    )
    database = ServerStorage(
        os.path.join(
            config['SETTINGS']['Database_path'],
            config['SETTINGS']['Database_file'])
    )
    server = Server(listen_address, listen_port, database)
    server.daemon = True
    server.start()

    server_app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.statusBar().showMessage('Server Working')
    main_window.active_clients_table.setModel(create_model(database))
    main_window.active_clients_table.resizeColumnsToContents()
    main_window.active_clients_table.resizeRowsToContents()

    def list_update():
        global NEW_CONNECTION
        if NEW_CONNECTION:
            main_window.active_clients_table.setModel(
                create_model(database))
            main_window.active_clients_table.resizeColumnsToContents()
            main_window.active_clients_table.resizeRowsToContents()
            with CONFLAG_LOCK:
                NEW_CONNECTION = False

    def show_statistics():
        global stat_window
        stat_window = HistoryWindow()
        stat_window.history_table.setModel(create_static_model(database))
        stat_window.history_table.resizeColumnsToContents()
        stat_window.history_table.resizeRowsToContents()
        stat_window.show()

    def server_config():
        global config_window
        config_window = ConfigWindow()
        config_window.db_path.insert(config['SETTINGS']['Database_path'])
        config_window.db_file.insert(config['SETTINGS']['Database_file'])
        config_window.port.insert(config['SETTINGS']['Default_port'])
        config_window.ip.insert(config['SETTINGS']['Listen_Address'])
        config_window.save_button.clicked.connect(save_server_config)

    def save_server_config():
        global config_window
        message = QMessageBox()
        config['SETTINGS']['Database_path'] = config_window.db_path.text()
        config['SETTINGS']['Database_file'] = config_window.db_file.text()
        try:
            port = int(config_window.port.text())
        except ValueError:
            message.warning(config_window, 'Error', 'Port shall be a number')
        else:
            config['SETTINGS']['Listen_Address'] = config_window.ip.text()
            if 1023 < port < 65536:
                config['SETTINGS']['Default_port'] = str(port)
                print(port)
                with open('server.ini', 'w') as conf:
                    config.write(conf)
                    message.information(
                        config_window, 'Ok', 'settings succesfully updated!')
            else:
                message.warning(
                    config_window,
                    'Error',
                    'Port shall be in diaposon between 1024 and 65536')

    timer = QTimer()
    timer.timeout.connect(list_update)
    timer.start(1000)

    main_window.refresh_button.triggered.connect(list_update)
    main_window.show_history_button.triggered.connect(show_statistics)
    main_window.config_button.triggered.connect(server_config)

    server_app.exec_()


if __name__ == '__main__':
    server_launcher()