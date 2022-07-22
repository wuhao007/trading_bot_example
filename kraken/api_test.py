import unittest
from unittest.mock import MagicMock
import api


class TestApiMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.api = api.API()

    def test_get_ask_bid(self) -> None:
        ask, bid = self.api.get_ask_bid('XETHZUSD')
        self.assertEqual(100 < ask < 10000, True)
        self.assertEqual(100 < bid < 10000, True)

        ask, bid = self.api.get_ask_bid('XXBTZUSD')
        self.assertEqual(10000 < ask < 100000, True)
        self.assertEqual(10000 < bid < 100000, True)

    def test_add_order(self) -> None:
        def side_effect_func(command, _):
            if command == 'AddOrder':
                return {'error': [], 'result': {'txid': ['O4N3YT-TE4G2-V6SR2D']}}
            elif command == 'QueryOrders':
                return {'error': [], 'result': {'O4N3YT-TE4G2-V6SR2D': {'refid': None, 'userref': None, 'status': 'closed', 'opentm': 1641055525.29437, 'starttm': 0, 'expiretm': 0, 'descr': {'pair': 'USDTUSD', 'type': 'buy', 'ordertype': 'market', 'price': '0', 'price2': '0', 'leverage': 'none', 'order': 'buy 752.20000000 USDTUSD @ market', 'close': ''}, 'vol': '752.20000000', 'vol_exec': '752.20000000', 'cost': '752.35044000', 'fee': '1.50470088', 'price': '1.0002', 'stopprice': '0.00000000', 'limitprice': '0.00000000', 'misc': '', 'oflags': 'fciq', 'reason': None, 'closetm': 1641055525.2955}}}
        self.api.query_private = MagicMock(side_effect=side_effect_func)
        cost, price = self.api.add_order('pair', -1)
        self.assertEqual(cost, 753.85514088)
        self.assertEqual(price, 1.0002)
        # self.api.query_private = MagicMock(side_effect=side_effect_func)

