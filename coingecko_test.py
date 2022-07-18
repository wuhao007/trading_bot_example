import unittest
import coingecko


class TestCoinGeckoMethods(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.coin_gecko = coingecko.CoinGecko('ETH/USD')

    def test_get_coingecko(self):

        ahr999, ahr999_120 = self.coin_gecko.get_coingecko()
        self.assertEqual(ahr999 < 1.2, True)
        # self.assertEqual(1000 < ahr999_045 < 2000, True)
        self.assertEqual(2000 < ahr999_120 < 6000, True)
        # self.assertEqual(6000 < ahr999x_045 < 10000, True)
