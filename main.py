#! /usr/bin/env python3

import krakenex
import include as inc
import include2 as inc2
import config
import time

# loading path to API keys
path = config.path_key
# getting bot trading pairs from config file
pairs_all = config.pairs


def run2(pairs):
    # starting logger
    logger_run2 = inc.setup_logger('run2', 'run2')
    # loading Kraken library and key
    k = krakenex.API()
    k.load_key(path + 'k0.key')
    # get Open Orders from API
    orders_all = k.query_private('OpenOrders')
    # print('order_all', orders_all)
    # get Balance from API
    bal_all = k.query_private('Balance')
    # print('bal_all', bal_all)
    # constructing pairs as a string to input into Ticker call
    pairs_t = inc.get_ticker_pairs(pairs)
    # print('pairs_t', pairs_t)
    # get prices with Ticker call
    ticker = k.query_public('Ticker', {'pair': pairs_t})
    # print('ticker', ticker)

    # sanity check: checking OpenOrders result and retry if needed
    if orders_all.get('error'):
        logger_run2.warning('Order error ' + str(orders_all.get('error')))
        orders = k.query_private('OpenOrders').get('result').get('open')
    else:
        orders = orders_all.get('result').get('open')

    # sanity check: checking Balance result and retry if needed
    if bal_all.get('error'):
        logger_run2.warning('Balance error ' + str(bal_all.get('error')))
        bal = k.query_private('Balance').get('result')
    else:
        bal = bal_all.get('result')

    # print('orders', orders)
    # print('bal', bal)
    # start trading algorithm for all pairs
    for i in range(len(pairs)):
        inc2.trade(pairs[i][0], pairs[i][1], pairs[i][2], bal, orders, k,
                   ticker['result'])

    # stop the logger
    logger_run2.handlers.pop()


def run():
    try:
        run2(pairs_all)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    run()
