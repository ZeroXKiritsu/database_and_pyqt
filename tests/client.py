import sys
import os
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))
from lib.vars import *
from client import get_user, create_presence, create_action, process_handler

class TestClient(unittest.TestCase):
    def test_get_user_success(self):
        self.assertEqual("NEW_USER", "NEW_USER")

    def test_presense_guest(self):
        test = create_presence()
        test[TIME] = 2
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 2, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_presense_user(self):
        test = create_presence(account_name='NEW_USER')
        test[TIME] = 2
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 2, USER: {ACCOUNT_NAME: 'NEW_USER'}})

    def test_create_action(self):
        test = create_action(account_name='NEW_USER', action='action', msg='New_Message')
        test[TIME] = 2
        self.assertEqual(test, {ACTION: 'action', TIME: 2, USER: {ACCOUNT_NAME: 'NEW_USER'}, MSG: "New_Message"})

    def test_create_action_none_msg(self):
        test = create_action(account_name='NEW_USER', action='action')
        test[TIME] = 2
        self.assertEqual(test, {ACTION: 'action', TIME: 2, USER: {ACCOUNT_NAME: 'NEW_USER'}, MSG: None})

    def test_process_handler_not_200ok(self):
        self.assertEqual(process_handler({MSG: 'msg_srv'}), '400:Bad request')

    def test_process_handler_ok(self):
        self.assertEqual(process_handler({RESPONSE: 200, MSG: 'msg_srv'}), "msg_srv")


if __name__ == '__main__':
    unittest.main()