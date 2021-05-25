import sys
import os
import unittest
import json

sys.path.append(os.path.join(os.getcwd(), '..'))
from lib.vars import *
from lib.utils import *

class TestSocket:
    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.receved_message = None

    def send(self, message_to_send):
        json_test_message = json.dumps(self.test_dict)
        self.encoded_message = json_test_message.encode(ENCODING)
        self.receved_message = message_to_send

    def recv(self, max_len):
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)

class Tests(unittest.TestCase):
    test_dict_send = {ACTION: PRESENCE, TIME: 2, USER: {ACCOUNT_NAME: 'NEW_USER'}}
    test_dict_recv_ok = {RESPONSE: 200}
    test_dict_recv_err = {RESPONSE: 400, ERROR: ERROR_400}

    def test_validate_ip_success(self):
        self.assertEqual(validate_ip('127.0.0.1'), True)

    def test_validate_ip_fail_str_is_long(self):
        self.assertEqual(validate_ip('127.0.0.1.1.1.1'), False)

    def test_validate_ip_fail_str_is_not_digit(self):
        self.assertEqual(validate_ip('127.0.Q.1'), False)

    def test_validate_ip_fail_ipport(self):
        self.assertEqual(validate_ip('127.0.0.1:8080'), False)

    def test_validate_ip_fail_incorrect_number(self):
        self.assertEqual(validate_ip('127.555.0.0'), False)

    def test_validate_port_ok(self):
        self.assertEqual(validate_port('8080'), True)

    def test_validate_port_forbidden(self):
        self.assertEqual(validate_port('1010'), False)

    def test_validate_port_not_number(self):
        self.assertEqual(validate_port('port'), False)

    def test_server_settings_default(self):
        self.assertEqual(server_settings(), [DEFAULT_IP, DEFAULT_PORT])

    def test_send_message(self):
        test_socket = TestSocket(self.test_dict_send)
        send_message(test_socket, self.test_dict_send)
        self.assertEqual(test_socket.encoded_message, test_socket.receved_message)
        with self.assertRaises(Exception):
            send_message(test_socket, test_socket)

    def test_get_message(self):
        test_sock_ok = TestSocket(self.test_dict_recv_ok)
        test_sock_err = TestSocket(self.test_dict_recv_err)
        self.assertEqual(get_message(test_sock_ok), self.test_dict_recv_ok)
        self.assertEqual(get_message(test_sock_err), self.test_dict_recv_err)


if __name__ == '__main__':
    unittest.main()