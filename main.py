#! /usr/bin/env python3

import krakenex
import util
import trade
import config


def Trade(pairs):
    # starting logger
    logger = util.setup_logger('trade', 'trade')
    # loading Kraken library and key
    api = krakenex.API()
    # loading path to API keys
    api.load_key(config.path_key + 'k0.key')
    # get Open Orders from API
    orders_all = api.query_private('OpenOrders')
    # print('order_all', orders_all)
    # get Balance from API
    bal_all = api.query_private('Balance')
    # print('bal_all', bal_all)
    # constructing pairs as a string to input into Ticker call
    pairs_t = util.get_ticker_pairs(pairs)
    # print('pairs_t', pairs_t)
    # get prices with Ticker call
    ticker = api.query_public('Ticker', {'pair': pairs_t})
    # print('ticker', ticker)
    # asset_pairs = api.query_public('AssetPairs', {'pair': 'XXBTZUSD'})
    # print('asset_pairs', json.dumps(asset_pairs, indent=4))

    # sanity check: checking OpenOrders result and retry if needed
    if orders_all.get('error'):
        logger.warning('Order error %s', orders_all.get('error'))
        orders = api.query_private('OpenOrders').get('result').get('open')
    else:
        orders = orders_all.get('result').get('open')

    # sanity check: checking Balance result and retry if needed
    if bal_all.get('error'):
        logger.warning('Balance error %s', bal_all.get('error'))
        bal = api.query_private('Balance').get('result')
    else:
        bal = bal_all.get('result')

    # print('orders', orders)
    # print('bal', bal)
    # start trading algorithm for all pairs
    for i in range(len(pairs)):
        trade.trade(pairs[i][0], pairs[i][1], pairs[i][2], bal, orders, api,
                   ticker['result'])

    # stop the logger
    logger.handlers.pop()


def Run():
    try:
        # getting bot trading pairs from config file
        Trade(config.pairs)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    Run()
