import unittest
import trade


class TestTradeMethods(unittest.TestCase):

    def test_get_wait_time(self):
        self.assertEqual(trade._GetWaitTime(1.2, 'ETH/USD', 0.39), 600)
        self.assertEqual(trade._GetWaitTime(1.2, 'XETHZUSD', 0.39), 600)
        self.assertEqual(trade._GetWaitTime(0.45, 'ETH/USD', 0.39), 300)
        self.assertEqual(trade._GetWaitTime(0.45, 'XETHZUSD', 0.39), 300)

        self.assertEqual(trade._GetWaitTime(1.2, 'BTC/USD', 0.53), 600)
        self.assertEqual(trade._GetWaitTime(1.2, 'XXBTZUSD', 0.53), 600)
        self.assertEqual(trade._GetWaitTime(0.45, 'BTC/USD', 0.53), 300)
        self.assertEqual(trade._GetWaitTime(0.45, 'XXBTZUSD', 0.53), 300)

        self.assertEqual(trade._GetWaitTime(1.2, 'MATICUSD', 2), 60 * 60 * 4)
        self.assertEqual(trade._GetWaitTime(1.2, 'MATIC/USD', 2), 60 * 60 * 4)
        self.assertEqual(trade._GetWaitTime(0.45, 'MATIC/USD', 2), 60 * 60 * 2)
        self.assertEqual(trade._GetWaitTime(0.45, 'MATICUSD', 2), 60 * 60 * 2)
