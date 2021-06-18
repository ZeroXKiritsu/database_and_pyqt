import logging
import logs.client_log
import argparse
import sys
from PyQt5.QtWidgets import QApplication

from shared.variables import *
from shared.errors import ServerError
from shared.wrapper import log
from client.database import ClientStorage
from client.transport import ClientTransport
from client.main_window import ClientMainWindow
from client.start_dialog import UserNameDialog

logger = logging.getLogger('client')

@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name

    if not 1023 < server_port < 65536:
        logger.critical(
            f'Attempt to launch console with incorrect port number: {server_port}. '
            f'Allowed values in ragne 1024 to 65535. Console closing.')
        exit(1)

    return server_address, server_port, client_name

if __name__ == '__main__':
    server_address, server_port, client_name = arg_parser()

    client_app = QApplication(sys.argv)

    if not client_name:
        start_dialog = UserNameDialog()
        client_app.exec_()
        if start_dialog.ok_pressed:
            client_name = start_dialog.client_name.text()
            del start_dialog
        else:
            exit(0)

    logger.info(
        f'console launched: server address: {server_address} ,'
        f' port: {server_port}, name of user: {client_name}')

    database = ClientStorage(client_name)

    try:
        transport = ClientTransport(server_port, server_address, database, client_name)
    except ServerError as error:
        print(error.text)
        exit(1)
    transport.setDaemon(True)
    transport.start()

    main_window = ClientMainWindow(database, transport)
    main_window.make_connection(transport)
    main_window.setWindowTitle(f'chat program (alpha release) - {client_name}')
    client_app.exec_()

    transport.transport_shutdown()
    transport.join()