import json
import socket
import sys
from errors import IncorrectDataRecivedError, NonDictInputError
from vars import PACKAGE_LENGTH, ENCODING, DEFAULT_PORT, DEFAULT_IP, CLIENT_LISTEN

def validate_ip(ip_str):
    tmp_str = ip_str.split('.')
    if len(tmp_str) != 4:
        return False
    for el in tmp_str:
        if not el.isdigit():
            return False
        i = int(el)
        if i < 0 or i > 255:
            return False
    return True

def validate_port(ip_port):
    try:
        ip_port = int(ip_port)
        if ip_port < 1025 or ip_port > 65535:
            return  False
        else:
            return True
    except:
        return False


def server_settings():
    client_listen = CLIENT_LISTEN
    try:
        if '-l' in sys.argv:
            client_listen = True

        if '-ip' in sys.argv:
            server_address = sys.argv[sys.argv.index('-ip') + 1]
        elif '-i' in sys.argv:
            server_address = sys.argv[sys.argv.index('-i') + 1]
        else:
            server_address = DEFAULT_IP

        if '-p' in sys.argv:
            server_port = int(sys.argv[sys.argv.index('-p') + 1])
        elif '-port' in sys.argv:
            server_port = int(sys.argv[sys.argv.index('-port') + 1])
        else:
            server_port = DEFAULT_PORT

    except ValueError:
        print('Некорректный адрес. Запуск скрипта должен быть: ****.py -i(or -ip) XXX.XXX.XXX.XXX -p(or -port) 9999')
        sys.exit(1)
    return [server_address, server_port, client_listen]

def create_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def get_message(client):
    response_bytes = client.recv(PACKAGE_LENGTH)
    if isinstance(response_bytes, bytes):
        json_response = response_bytes.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise IncorrectDataRecivedError
    raise IncorrectDataRecivedError

def send_message(sock_obj, message):
    if not isinstance(message, dict):
        raise NonDictInputError
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock_obj.send(encoded_message)

