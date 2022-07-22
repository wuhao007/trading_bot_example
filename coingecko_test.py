import unittest
import coingecko


class TestCoinGeckoMethods(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.coin_gecko = coingecko.CoinGecko('ETH/USD')
        self.coin_gecko.update()

    def test_get_coingecko(self) -> None:

        # print('last price', self.coin_gecko.prices)
        ahr999, ahr999_120 = self.coin_gecko.get_coingecko()
        self.assertEqual(ahr999 < 1.2, True)
        # self.assertEqual(1000 < ahr999_045 < 2000, True)
        self.assertEqual(2000 < ahr999_120 < 6000, True)
        # self.assertEqual(6000 < ahr999x_045 < 10000, True)

    def test_add_own_data(self) -> None:
        # print('prices', self.coin_gecko.prices)
        # print('last price', self.coin_gecko.prices[-1])
        num_days = self.coin_gecko.prices.shape[0]
        # date_time = '2022-07-14T01:56:57.092580+00:00'
        self.coin_gecko.add_own_data(1657763817.09258, 1109.7)
        last_price = self.coin_gecko.prices[-1]
        # print(coingecko._Date2Timestamp(date_time))
        self.assertEqual(last_price[0], 1657763817.09258 * 1000)
        self.assertEqual(last_price[1], 1109.7)
        self.assertEqual(num_days + 1, self.coin_gecko.prices.shape[0])

        ahr999, ahr999_120 = self.coin_gecko.get_coingecko()
        self.assertEqual(ahr999 < 1.2, True)
        self.assertEqual(2000 < ahr999_120 < 6000, True)
