# -*- coding: utf-8 -*-
"""coingecko.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fjxQk-7-XGqgGxlq_8l062FTGmPLPgIb
"""

import math
import time
import json
import datetime
import requests
from sklearn.linear_model import LinearRegression
import numpy as np
from typing import Optional, Dict, Any, List, Tuple

_SECONDS_IN_A_DAY = 24 * 60 * 60 * 1000
_BTC_START_DATE = '2009-01-03T00:00:00'

_AHR999_W = 5.84
_AHR999_B = -17.01
_AHR999_DAYS = 200

# def _Symbol2Id(symbol):
#     coins_list = requests.get(
#         'https://api.coingecko.com/api/v3/coins/list').json()
#    return [coin for coin in coins_list if coin['symbol'] == symbol]

# def _GetMarkets(vs_currency):
#     coins_list = requests.get(
#         f'https://api.coingecko.com/api/v3/coins/markets?vs_currency={vs_currency}&order=market_cap_desc'
#     ).json()
#     return [coin['id'] for coin in coins_list]


def _GetMarketChart(coin: str, vs_currency: str) -> List[Tuple[float, float]]:
    market_chart = requests.get(
        f'https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency={vs_currency}&days=36500&interval=hourly'
    ).json()
    return [price for price in market_chart['prices'] if price[1]]


# def _GetPrice(coin, vs_currency):
#     price = requests.get(
#         f'https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies={vs_currency}'
#     ).json()
#    return price[coin][vs_currency]

# def _ParseDate(item):
#    return datetime.datetime.fromtimestamp(item / 1000)


def _Date2Timestamp(item: str) -> float:
    return datetime.datetime.timestamp(
        datetime.datetime.fromisoformat(item)) * 1000


# A script that generates ahr999 index data into a JSON file.
def _GetAvgHelper(items: np.array) -> float:
    return sum(1 / item[1] for item in items)


def _GetAvg(items: np.array) -> float:
    # return stats.gmean(list(map(lambda item: item[1], items)))
    return len(items) / _GetAvgHelper(items)


def _GetCoinDays(timestamp: float, start_date: str) -> float:
    return (timestamp - _Date2Timestamp(start_date)) / _SECONDS_IN_A_DAY


def _GetLogPrice(timestamp: float, w: float, b: float,
                 start_date: str) -> float:
    return 10**(w * math.log(_GetCoinDays(timestamp, start_date), 10) + b)


def _GetAhr999(items: np.array, w: float, b: float, start_date: str) -> float:
    end_item = items[-1]
    return end_item[1]**2 / (_GetAvg(items) *
                             _GetLogPrice(end_item[0], w, b, start_date))


# def _GetAhr999x(items, w, b, start_date):
#    end_item = items[-1]
#    return _GetAvg(items) * _GetLogPrice(end_item[0], w, b,
#                                         start_date) * 3 / (end_item[1]**2)


def _GetAhr999Prices(prices: np.array) -> np.array:
    ahr999_prices = prices[-_AHR999_DAYS - 1:][:_AHR999_DAYS]
    assert len(ahr999_prices) == _AHR999_DAYS, f'{_AHR999_DAYS} items'
    return ahr999_prices


# def _GetPastAhr999(coin, w, b, start_date, vs_currency):
#     ahr999_prices = _GetAhr999Prices(coin, vs_currency)
# print(f'Date: {_ParseDate(ahr999_prices[-1][0])}')
# print(f'200 days average price: {_GetAvg(ahr999_prices)} {vs_currency}')
# print(
#     f'Log price: {_GetLogPrice(ahr999_prices[-1][0], w, b, start_date)} {vs_currency}'
# )
# print(f'Days: {_GetCoinDays(ahr999_prices[-1][0], start_date)} days')
# print(f'Yesterday price: {ahr999_prices[-1][1]} {vs_currency}')
# print(f'ahr999: {_GetAhr999(ahr999_prices, w, b, start_date)}')
# print(f'ahr999x: {_GetAhr999x(ahr999_prices, w, b, start_date)}')


def _GetAns(ratio, array, w: float, b: float, start_date: str) -> float:
    a_ = _GetAvgHelper(array[-_AHR999_DAYS + 1:])
    b_ = 1
    c_ = -200 * _GetLogPrice(array[-1][0], w, b, start_date)
    return (-b_ + math.sqrt(b_**2 - 4 * a_ * c_ * ratio)) / (2 * a_)


# def _GetTodayAhr999(coin, w, b, start_date, vs_currency, prices):
#    ahr999_prices = _GetAhr999Prices(prices)
# price = _GetPrice(coin, vs_currency)
#    ratio = 0.45
#    ahr999_045 = _GetAns(ratio, ahr999_prices, w, b, start_date)
#    print(f'ahr999={ratio}: {ahr999_045} {vs_currency}')
#    ratio = 1.2
#    ahr999_120 = _GetAns(ratio, ahr999_prices, w, b, start_date)
#    print(f'ahr999={ratio}: {ahr999_120} {vs_currency}')
#    ratio = 0.45
#    ahr999x_045 = _GetAns(3 / ratio, ahr999_prices, w, b, start_date)
#    print(f'ahr999x={ratio}: {ahr999x_045} {vs_currency}')
# print(f'Current price: {price} {vs_currency}')
#    print(f'\033[31m{coin}/{vs_currency}\033[0m')
# if price < ahr999_045:
#     print('\033[31mBasically a Fire Sale\033[0m')
# elif price < ahr999_120:
#     print('\033[31mAccumulate\033[0m')
# elif price < ahr999x_045:
#     print('\033[31mHOLD!\033[0m')
# else:
#     print('\033[31mFOMO intensifies\033[0m')
#    return ahr999_045, ahr999_120, ahr999x_045

# https://www.lookintobitcoin.com/charts/pi-cycle-top-indicator/
# def _GetMa(items, days):
#     return sum(item[1] for item in items[-days:]) / days

# def _GetPiIndicator(coin):
#     pi_prices = _GetMarketChart(coin, 'usd')[-351:][:350]
#     print(_GetMa(pi_prices, 350) * 2, _GetMa(pi_prices, 111))

# https://www.tradingview.com/symbols/CRYPTOCAP-BTC.D/
# def _GetMarketCap(coin):
#     page = 1
#     total_coins_market = 0
#
#     sleep = 1
#     while page == 1 or markets:
#         try:
#             markets = requests.get(
#                 f'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page={page}&sparkline=false'
#             ).json()
#         except:
#             time.sleep(sleep)
#             sleep *= 2
#             continue
#
#         for market in markets:
#             if market['market_cap'] is not None:
#                 total_coins_market += market['market_cap']
#             if market['id'] == coin:
#                 bitcoin_market = market['market_cap']
#         else:
#             page += 1
#
#     print(f'{bitcoin_market*100/total_coins_market}%')

# def _GetJzr(coin):
#     jzr_prices = _GetMarketChart(coin, 'usd')[-62:][:61]
#     print(
#         f'{sum((jzr_prices[i][1]/jzr_prices[i-1][1] - 1) for i in range(1, len(jzr_prices))) * 100}%'
#    )


def _GetWb(start_date: str, prices: np.array) -> Tuple[float, float]:
    xdata = np.log10(_GetCoinDays(prices[:, 0], start_date)).reshape(-1, 1)
    ydata = np.log10(prices[:, 1])

    reg = LinearRegression().fit(xdata, ydata)
    w, b = reg.coef_[0], reg.intercept_
    # if w <= 0:
    #   return w, b

    #timestamp = _Date2Timestamp('2022-02-22T00:00:00')
    #print(10 ** reg.predict(np.array([[np.log10(_GetCoinDays(timestamp, start_date))]])))

    # dates = [_ParseDate(price) for price in prices[:, 0]]
    print(f'Score:\033[31m{reg.score(xdata, ydata)}\033[0m')
    print(f'w: {w}, b: {b}')
    return w, b


# def _GetStartDate(market_chart):
#     return (_ParseDate(market_chart[0][0]) -
#             datetime.timedelta(days=1)).isoformat()


def _GetHaowu999(prices: np.array,
                 start_date: str = None) -> Tuple[float, float]:
    # market_chart = _GetMarketChart(coin, vs_currency)
    # if not start_date:
    #     start_date = _GetStartDate(market_chart)
    #     print(f'DEBUG: {start_date}')

    # prices = np.array(_GetMarketChart(coin, vs_currency))

    # np.delete(prices, -1)
    w, b = _GetWb(start_date, prices)
    # if w <= 0:
    #   return

    # _GetPastAhr999(coin, w, b, start_date, vs_currency)
    ahr999_prices = _GetAhr999Prices(prices)

    ahr999 = _GetAhr999(ahr999_prices, w, b, start_date)
    # ahr999x = _GetAhr999x(ahr999_prices, w, b, start_date)
    print(f'ahr999: {ahr999}')
    # print(f'ahr999x: {ahr999x}')

    # ratio = 0.45
    # ahr999_045 = _GetAns(ratio, ahr999_prices, w, b, start_date)
    # print(f'ahr999={ratio}: {ahr999_045} {vs_currency}')
    ratio = 1.2
    ahr999_120 = _GetAns(ratio, ahr999_prices, w, b, start_date)
    print(f'ahr999={ratio}: {ahr999_120} USD')
    # ratio = 0.45
    # ahr999x_045 = _GetAns(3 / ratio, ahr999_prices, w, b, start_date)
    # print(f'ahr999x={ratio}: {ahr999x_045} {vs_currency}')
    # print(f'Current price: {price} {vs_currency}')
    # print(f'\033[31m{coin}/{vs_currency}\033[0m')
    # if price < ahr999_045:
    #     print('\033[31mBasically a Fire Sale\033[0m')
    # elif price < ahr999_120:
    #     print('\033[31mAccumulate\033[0m')
    # elif price < ahr999x_045:
    #     print('\033[31mHOLD!\033[0m')
    # else:
    #     print('\033[31mFOMO intensifies\033[0m')
    return ahr999, ahr999_120


# def _GetRainbowWb(coin, start_date=_BTC_START_DATE, vs_currency='usd'):
#     haowu_prices = np.array(_GetMarketChart(coin, vs_currency))
#     #(haowu_prices, -1)
#     start_date = '2009-01-09T00:00:00'
#     xdata = np.log(_GetCoinDays(haowu_prices[:, 0], start_date)).reshape(-1, 1)
#     ydata = np.log10(haowu_prices[:, 1])
#
#     reg = LinearRegression().fit(xdata, ydata)
#
#     print(reg.score(xdata, ydata))
#     print(reg.coef_)
#     print(reg.intercept_)
#     #timestamp = _Date2Timestamp('2022-02-21T00:00:00')
#     #print(10 ** reg.predict(np.array([[np.log(_GetCoinDays(timestamp, start_date))]])))
#
#     return reg

#_BTC_START_DATE = '2013-04-27T00:00:00'
_BTC_START_DATE = '2009-01-03T00:00:00'
# _GetHaowu999('bitcoin', 'usd', _BTC_START_DATE)

#_ETH_START_DATE = '2015-07-30T00:00:00'
_ETH_START_DATE = '2014-06-01T00:00:00'
# _GetHaowu999('ethereum', 'usd', _ETH_START_DATE)
# _GetHaowu999('ethereum', 'btc', _ETH_START_DATE)

_RUNE_START_DATE = '2019-07-20T00:00:00'

# _GetHaowu999('thorchain', 'usd', _RUNE_START_DATE)
# _GetHaowu999('thorchain', 'btc', _RUNE_START_DATE)
# _GetHaowu999('thorchain', 'eth', _RUNE_START_DATE)

# _BNB_START_DATE = '2017-09-15T00:00:00'
_BNB_START_DATE = '2017-07-01T00:00:00'
# _GetHaowu999('binancecoin', 'usd', _BNB_START_DATE)
# _GetHaowu999('binancecoin', 'btc', _BNB_START_DATE)
# _GetHaowu999('binancecoin', 'eth', _BNB_START_DATE)

_MATIC_START_DATE = '2019-04-24T00:00:00'

# _GetHaowu999('matic-network', 'usd', _MATIC_START_DATE)
# _GetHaowu999('matic-network', 'btc', _MATIC_START_DATE)
# _GetHaowu999('matic-network', 'eth', _MATIC_START_DATE)

# _LINK_START_DATE = '2017-11-08T00:00:00'
_LINK_START_DATE = '2017-09-19T00:00:00'
# _GetHaowu999('chainlink', 'usd', _LINK_START_DATE)
# _GetHaowu999('chainlink', 'btc', _LINK_START_DATE)
# _GetHaowu999('chainlink', 'eth', _LINK_START_DATE)

# _FTT_START_DATE = '2019-07-29T00:00:00'
_FTT_START_DATE = '2019-05-08T00:00:00'
# _GetHaowu999('ftx-token', 'usd', _FTT_START_DATE)
# _GetHaowu999('ftx-token', 'btc', _FTT_START_DATE)
# _GetHaowu999('ftx-token', 'eth', _FTT_START_DATE)

# _DOT_START_DATE = '2020-08-18T00:00:00'
_DOT_START_DATE = '2017-10-14T00:00:00'

# _GetHaowu999('polkadot', 'usd', _DOT_START_DATE)
# _GetHaowu999('polkadot', 'btc', _DOT_START_DATE)

# _CRO_START_DATE = '2019-01-01T00:00:00'
_CRO_START_DATE = '2017-05-18T00:00:00'
# _GetHaowu999('crypto-com-chain', 'usd', _CRO_START_DATE)
# _GetHaowu999('crypto-com-chain', 'btc', _CRO_START_DATE)

_LTC_START_DATE = '2013-04-27T00:00:00'

# _GetHaowu999('litecoin', 'usd', _LTC_START_DATE)
# _GetHaowu999('litecoin', 'btc', _LTC_START_DATE)
# _GetHaowu999('litecoin', _LTC_START_DATE, 'eth')

# _FTM_START_DATE = '2018-10-29T00:00:00'
_FTM_START_DATE = '2018-06-15T00:00:00'

# _GetHaowu999('fantom', 'usd', _FTM_START_DATE)
#_GetHaowu999('fantom', 'btc', _FTM_START_DATE)

# _BAT_START_DATE = '2017-06-07T00:00:00'
_BAT_START_DATE = '2017-05-31T00:00:00'

# _GetHaowu999('basic-attention-token', 'usd', _BAT_START_DATE)
# _GetHaowu999('basic-attention-token', 'btc', _BAT_START_DATE)

_START_DATE = {
    'bitcoin': _BTC_START_DATE,
    'ethereum': _ETH_START_DATE,
    'thorchain': _RUNE_START_DATE,
    'binancecoin': _BNB_START_DATE,
    'matic-network': _MATIC_START_DATE,
    'chainlink': _LINK_START_DATE,
    'ftx-token': _FTT_START_DATE,
    'polkadot': _DOT_START_DATE,
    'crypto-com-chain': _CRO_START_DATE,
    'litecoin': _LTC_START_DATE,
    'fantom': _FTM_START_DATE,
    'basic-attention-token': _BAT_START_DATE,
}

_API2COINGECKO = {
    'XXBTZUSD': 'bitcoin',
    'BTC/USD': 'bitcoin',
    'XETHZUSD': 'ethereum',
    'ETH/USD': 'ethereum',
    'MATICUSD': 'matic-network',
    'MATIC/USD': 'matic-network',
}


class CoinGecko(object):

    def __init__(self, coin: str) -> None:
        self.coin = _API2COINGECKO[coin]
        self.start_date = _START_DATE[self.coin]

    def update(self):
        self.prices = np.array(_GetMarketChart(self.coin, 'usd'))

    def get_coingecko(self) -> Tuple[float, float]:
        return _GetHaowu999(self.prices, self.start_date)

    def add_own_data(self, price: float) -> None:
        # sdata = np.log10(_GetCoinDays(prices[:, 0], start_date)).reshape(-1, 1)
        # ydata = np.log10(prices[:, 1])
        self.prices = np.append(self.prices, [[time.time() * 1000, price]],
                                axis=0)
        # print(self.prices[-2:])
