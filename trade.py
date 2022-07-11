import util
import config
from collections import namedtuple
import time
import coingecko
import numpy as np


# BTC $1.06 10 minutes == $5 per 47.1698113208 minutes
# ETH $0.78 10 minutes == $5 per 64.1025641026 minutes
# MATIC $2 4 hours = $5 10 hours
_SLEEP_SECONDS = {
    'XXBTZUSD': 10 * 60 / 1.06,
    'XETHZUSD': 10 * 60 / 0.78,
    'MATICUSD': 4 * 60 * 60 / 4,
}


def trade(pair, api, ticker):
    # construct pair from base and quote. USDCUSD is an exception
    # print('base', base)
    # print('quote', quote)
    # print('pair', pair)
    # print('bal', bal)
    # print('orders', orders)
    # print('api', api)
    # print('ticker', ticker)

    # start logger
    base, altname = pair.base_asset, pair.altname
    logger = util.setup_logger(altname, altname)
    logger.info(
        '------------------------- New case --------------------------------')
    # assign base and quote balance variables. -0.1 is a trick to get rid
    # of rounding issues and insufficient funds error
    # bal_b = bal.get(base, 0)
    # print('bal_b', base, bal_b)
    # print('bal_q', quote, bal_q)
    # logger.info('%s %s', base, bal_b)
    # price_cell is a price precision variable
    price_cell = util.get_price_dec(altname)
    # print('price_cell', price_cell)
    # lever is a leverage value
    # lever = 'none'

    # vol_min is a minimum order size. It depends on base currency
    # vol_min = util.get_vol_min(base)

    # get best ask/bid from ticker
    ask = float(ticker.get(altname).get('a')[0])
    logger.info('ask %s', ask)
    bid = float(ticker.get(altname).get('b')[0])
    logger.info('bid %s', bid)
    ahr999_045, ahr999_120, ahr999x_045 = coingecko.GetCoinGecko(altname)
    logger.info('ahr999 0.45: %s, ahr999 1.2: %s, ahr999x 0.45: %s',
                ahr999_045, ahr999_120, ahr999x_045)

    # sells is an array of sell orders data
    # sells = []
    # for i in sell_levels:
    # Don't cross the book. Skip sell levele if sell level <= best bid
    #     if i[1] <= bid:
    #         logger.info(str(i[1]) + ' sell level <= bid')
    #         continue
    # add sell level: [ order size, price, userref, direction of trade ]
    #     sells.append([i[0] * bal_b, i[1], i[2], 'sell'])
    # logger.info('sells ' + str(sells))

    # buys is an array of buy orders data
    Buy = namedtuple('Buy', 'order_size, price, userref, direction_of_trade')
    # for i in buy_levels:
    # Don't cross the book. Skip buy levele if buy level >= best ask
    # if i >= ask:
    #     logger.info('%s buy level >= ask', i)
    #     continue
    # add buy level: [ order size, price, userref, direction of trade ]
    buy = Buy(config.BUY_LEVELS[altname], ask, np.random.randint(-2147483648, 2147483647, dtype=np.int32),
              'buy')
    logger.info('buy %s', buy)

    # -------------- Check for trade @ Kraken
    # iterate through buys and sells level
    # get order infor for particular buy/sell level
    # order, txid = util.get_order(orders, buy.userref, altname, api)
    # print('txid1', txid1)
    # logger.info('txid = %s', txid)
    # print('buy', buy)

    # check for minimum order size and continue
    cost = buy.price * buy.order_size
    if buy.price < ahr999_120:
        # submit following data and place or update order:
        # ( library instance, order info, altname, direction of order,
        # size of order, price, userref, txid of existing order,
        # price precision, leverage, logger instance, oflags )
        res = util.check4trade(api, altname, buy.direction_of_trade,
                               buy.order_size, buy.price, buy.userref,
                               price_cell, 'post')
        logger.info('traded: %s', res)
        if res != -1:
            if 'error' in res and res.get('error'):
                logger.warning('%s trading error %s', altname, res)

        closed_orders = api.query_private('ClosedOrders').get('result').get(
            'closed')
        # print('closed_orders: ', type(closed_orders))
        orders = []
        sleep_time = 1
        # while not orders:
        #     orders.extend(
        #         util.get_orders(closed_orders, buy.userref, altname, api))
        #     time.sleep(sleep_time)
        #     sleep_time *= 2
        orders = [{'cost': cost, 'fee': cost * 0.26 / 100}]
        cost = sum(
            (float(order['cost']) + float(order['fee'])) for order in orders)

        # TODO(haowu) change to use closed order
        # print('sleep for ', cost * _SLEEP_SECONDS[altname] / 60, 'minutes')
        if buy.price > ahr999_045:
            time.sleep(cost * _SLEEP_SECONDS[altname])

    # cancel existing order if new order size is less than minimum
    else:
        # res = util.check4cancel(api, order, txid)
        # print('Not enough funds to ', buy[3], altname,
        #       'or trade vol too small; canceling', res)
        logger.info('Not enough funds to %s %s or trade vol too small',
                    buy.direction_of_trade, altname)
    # time.sleep(cost * _SLEEP_SECONDS[altname])
    logger.handlers.pop()
