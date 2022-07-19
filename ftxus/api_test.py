import unittest
from unittest.mock import MagicMock
import api


class TestApiMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.api = api.API()

    def test_get_ask_bid(self) -> None:
        self.api._get = MagicMock(return_value={
            "bids": [[20512.0, 5.3274]],
            "asks": [[20514.0, 0.365]]
        })
        # print(self.api._get())
        ask, bid = self.api.get_ask_bid('BTC/USD')
        self.assertEqual(ask, 20514.0)
        self.assertEqual(bid, 20512.0)

    def test_add_order(self) -> None:
        self.api.place_order = MagicMock(
            return_value={
                'id': 6315360489,
                'clientId': '1043601791',
                'market': 'ETH/USD',
                'type': 'market',
                'side': 'buy',
                'price': None,
                'size': 0.001,
                'status': 'new',
                'filledSize': 0.0,
                'remainingSize': 0.001,
                'reduceOnly': False,
                'liquidation': False,
                'avgFillPrice': None,
                'postOnly': False,
                'ioc': True,
                'createdAt': '2022-07-14T01:56:57.092580+00:00',
                'future': None
            })
        self.api._get = MagicMock(
            return_value={
                'id': 6315360489,
                'clientId': '1043601791',
                'market': 'ETH/USD',
                'type': 'market',
                'side': 'buy',
                'price': None,
                'size': 0.001,
                'status': 'closed',
                'filledSize': 0.001,
                'remainingSize': 0.0,
                'reduceOnly': False,
                'liquidation': False,
                'avgFillPrice': 1109.7,
                'postOnly': False,
                'ioc': True,
                'createdAt': '2022-07-14T01:56:57.092580+00:00',
                'future': None
            })
        cost, created_at, avg_fill_price = self.api.add_order('ETH/USD', 0.001)
        self.assertEqual(cost, 1.1119194000000001)
        self.assertEqual(avg_fill_price, 1109.7)
        self.assertEqual(created_at, '2022-07-14T01:56:57.092580+00:00')
