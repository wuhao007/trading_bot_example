import unittest
import util


class TestUtilMethods(unittest.TestCase):
    def test_load_key(self):
        key, secret = util.load_key('key')
        self.assertEqual(key, 'key')
        self.assertEqual(secret, 'secret')

