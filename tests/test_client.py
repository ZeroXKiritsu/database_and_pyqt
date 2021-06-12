import sys
sys.path.append('../')
from client import produce_presence, server_response
from shared.variables import *
import unittest
from shared.errors import ReqFieldMissingError, ServerError

class TestClass(unittest.TestCase):
     def test_def_presense(self):
         test = produce_presence('Guest')
         test[TIME] = 1.1
         self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})
    
     def test_200_ans(self):
        self.assertEqual(server_response({RESPONSE: 200}), '200 : OK')
    
     def test_400_ans(self):
         self.assertRaises(ServerError, server_response , {RESPONSE: 400, ERROR: 'Bad Request'})
    
     def test_no_response(self):
        self.assertRaises(ReqFieldMissingError, server_response, {ERROR: 'Bad Request'})

if __name__ == '__main__':
    unittest.main()