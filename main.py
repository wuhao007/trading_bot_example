#! /usr/bin/env python3

import krakenex
import util
import os
import trade
import config
import sys


def main(coin):
    # starting logger
    pair = config.PAIRS[coin]
    logger = util.setup_logger('main', 'main')
    # loading Kraken library and key
    api = krakenex.API()
    # loading path to API keys
    api.load_key(os.path.join(config.path_key, 'k0.key'))
    # get Open Orders from API
    # orders = api.query_private('OpenOrders')
    # print('order_all', orders_all)
    # get Balance from API
    balance = api.query_private('Balance')
    # print('bal_all', bal_all)
    # constructing pairs as a string to input into Ticker call
    pairs_ticker = util.get_ticker_pairs(pair)
    # print('pairs_t', pairs_t)
    # get prices with Ticker call
    ticker = api.query_public('Ticker', {'pair': pairs_ticker})
    # print('ticker', ticker)
    # asset_pairs = api.query_public('AssetPairs', {'pair': 'XXBTZUSD'})
    # print('asset_pairs', json.dumps(asset_pairs, indent=4))

    # sanity check: checking OpenOrders result and retry if needed
    # if orders.get('error'):
    #     logger.warning('Order error %s', orders.get('error'))
    #     orders = api.query_private('OpenOrders').get('result').get('open')
    # else:
    #     orders = orders.get('result').get('open')

    # sanity check: checking Balance result and retry if needed
    if balance.get('error'):
        logger.warning('Balance error %s', balance.get('error'))
        bal = api.query_private('Balance').get('result')
    else:
        bal = balance.get('result')

    # print('orders', orders)
    # print('bal', bal)
    # start trading algorithm for all pairs
    trade.trade(pair, bal, api, ticker['result'])

    # stop the logger
    logger.handlers.pop()


if __name__ == "__main__":
    # getting bot trading pairs from config file
    main(sys.argv[1])
    
