#! /usr/bin/env python3

import kraken
import ftxus
import util
# import os
import trade
# import config
import sys


def Run(pair: str, exchange: str, key_path: str) -> None:
    # starting logger
    # pair = config.PAIRS[coin]
    # logger = util.setup_logger('run', 'run')
    # loading Kraken library and key
    # loading path to API keys
    key, secret = util.load_key(key_path)
    #    os.path.join(config.path_key, exchange, 'k0.key'))
    api = getattr(sys.modules[__name__], exchange).API(key, secret)
    # if exchange == 'kraken':
    #     key, secret = util.load_key(
    #         os.path.join(config.kraken_path_key, 'k0.key'))
    #     api = kraken.API(key, secret)
    # else:
    #     key, secret = util.load_key(
    #         os.path.join(config.ftxus_path_key, 'k0.key'))
    #     api = ftxus.FtxClient(key, secret)
    # get Open Orders from API
    # orders = api.query_private('OpenOrders')
    # print('order_all', orders_all)
    # get Balance from API
    # balance = api.query_private('Balance')
    # print('bal_all', bal_all)
    # constructing pairs as a string to input into Ticker call
    # pairs_ticker = util.get_ticker_pairs(pair)
    # print('pairs_t', pairs_t)
    # get prices with Ticker call
    # ticker = api.query_public('Ticker', {'pair': pairs_ticker})
    # print('ticker', ticker)
    # asset_pairs = api.query_public('AssetPairs', {'pair': 'XXBTZUSD'})
    # print('asset_pairs', json.dumps(asset_pairs, indent=4))
    # closed_orders = api.query_private('ClosedOrders').get('result').get('closed')
    # print('closed_orders: ', json.dumps(closed_orders, indent=4, sort_keys=True))

    # sanity check: checking OpenOrders result and retry if needed
    # if orders.get('error'):
    #     logger.warning('Order error %s', orders.get('error'))
    #     orders = api.query_private('OpenOrders').get('result').get('open')
    # else:
    #     orders = orders.get('result').get('open')

    # sanity check: checking Balance result and retry if needed
    # if balance.get('error'):
    #     logger.warning('Balance error %s', balance.get('error'))
    #     bal = api.query_private('Balance').get('result')
    # else:
    #     bal = balance.get('result')

    # print('orders', orders)
    # print('bal', bal)
    # start trading algorithm for all pairs
    # order_history = api.get_order_history(pair)
    # logger.info('order_history: %s', order_history)
    # open_orders = api.get_open_orders(pair)
    # logger.info('open orders: %s', open_orders)
    while True:
        trade.Trade(pair, api)

    # stop the logger
    # logger.handlers.pop()


if __name__ == "__main__":
    # getting bot trading pairs from config file
    Run(sys.argv[1], sys.argv[2], sys.argv[3])
