import sys
import os
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))
from lib.vars import *
from server import Server

class TestServer(unittest.TestCase):
    def test_fail_message_object(self):
        self.assertEqual(Server.client_message_handler('AUTH_USER'), self.failed_dict)

    def test_no_key_action(self):
        self.assertEqual(Server.client_message_handler({TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.failed_dict)

    def test_no_key_time(self):
        self.assertEqual(Server.client_message_handler({ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}), self.failed_dict)

    def test_no_key_user(self):
        self.assertEqual(Server.client_message_handler({ACTION: PRESENCE, TIME: '2'}), self.failed_dict)

    def test_wrong_action_value(self):
        self.assertEqual(Server.client_message_handler(
            {ACTION: 'abrakadabra', TIME: '2', USER: {ACCOUNT_NAME: 'Guest'}}), self.failed_dict)

    def test_Guest_with_AUTH(self):
        self.assertEqual(Server.client_message_handler(
            {ACTION: AUTH, TIME: '2', USER: {ACCOUNT_NAME: 'Guest'}}), self.failed_dict)

    def test_Guest_with_MSG(self):
        self.assertEqual(Server.client_message_handler(
            {ACTION: MSG, TIME: '2', USER: {ACCOUNT_NAME: 'Guest'}}), self.failed_dict)

    def test_Success_PRESENCE_Guest(self):
        self.assertEqual(Server.client_message_handler(
            {ACTION: PRESENCE, TIME: '2', USER: {ACCOUNT_NAME: 'Guest'}}), self.success_dict_guest)

    def test_Success_PRESENCE_not_Guest(self):
        self.assertEqual(Server.client_message_handler(
            {ACTION: PRESENCE, TIME: '2', USER: {ACCOUNT_NAME: 'AUTH_USER'}}), self.success_dict_guest)

    def test_Success_AUTH_not_Guest(self):
        self.assertEqual(Server.client_message_handler(
            {ACTION: AUTH, TIME: '2', USER: {ACCOUNT_NAME: 'AUTH_USER'}}), self.success_dict_auth_user)

    def test_Success_MSG_not_Guest(self):
        self.assertEqual(Server.client_message_handler(
            {ACTION: AUTH, TIME: '2', USER: {ACCOUNT_NAME: 'AUTH_USER'}}), self.success_dict_auth_user)


if __name__ == '__main__':
    unittest.main()


