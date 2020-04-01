#!/usr/bin/env python3

import sys, os
import json
import unittest
import hashlib
sys.path.append(os.path.join(sys.path[0],'..'))
from parameterized import parameterized, parameterized_class

class TestApi(unittest.TestCase):
    def setUp(self):  
        self.headers = {
            'ContentType': 'application/json',
            'dataType': 'json'
        }
 
    def test_dummy(self):
        test = 'ok'
        self.assertEqual(test, 'ok')
    
        
if __name__ == '__main__':
    unittest.main()
