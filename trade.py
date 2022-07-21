import util
import config
# from collections import namedtuple
import time
import coingecko
import ftxus
# import numpy as np
# import math

# BTC $1.06 10 minutes == $5 per 47.1698113208 minutes
# ETH $0.78 10 minutes == $5 per 64.1025641026 minutes
# MATIC $2 4 hours = $5 10 hours
# 1 / cost_in_second
_SLEEP_SECONDS = {
    'XXBTZUSD': 10 * 60 / 0.53,
    'BTC/USD': 10 * 60 / 0.53,
    'XETHZUSD': 10 * 60 / 0.39,
    'ETH/USD': 10 * 60 / 0.39,
    'MATICUSD': 4 * 60 * 60 / 2,
    'MATIC/USD': 4 * 60 * 60 / 2,
}


def _GetWaitTime(ahr999: float, pair: str, cost: float) -> float:
    return cost * _SLEEP_SECONDS[pair] * (0.5 + (ahr999 - 0.45) / 1.5)


def Trade(pair: str, api: ftxus.api.API):
    # construct pair from base and quote. USDCUSD is an exception
    # print('base', base)
    # print('quote', quote)
    # print('pair', pair)
    # print('bal', bal)
    # print('orders', orders)
    # print('api', api)
    # print('ticker', ticker)

    # start logger
    log_name = pair.replace('/', '')
    logger = util.setup_logger(log_name, log_name)
    logger.info(
        '------------------------- New case --------------------------------')
    # assign base and quote balance variables. -0.1 is a trick to get rid
    # of rounding issues and insufficient funds error
    # bal_b = bal.get(base, 0)
    # print('bal_b', base, bal_b)
    # print('bal_q', quote, bal_q)
    # logger.info('%s %s', base, bal_b)
    # price_cell is a price precision variable
    # price_cell = util.get_price_dec(pair)
    # print('price_cell', price_cell)
    # lever is a leverage value
    # lever = 'none'

    # vol_min is a minimum order size. It depends on base currency
    # vol_min = util.get_vol_min(base)

    # get best ask/bid from ticker
    # ask = float(ticker.get(pair).get('a')[0])
    # bid = float(ticker.get(pair).get('b')[0])
    ask, bid = api.get_ask_bid(pair)
    logger.info('ask %s, bid %s', ask, bid)
    coin_gecko = coingecko.CoinGecko(pair)
    ahr999, ahr999_120 = coin_gecko.get_coingecko()
    # logger.info('ahr999: %s, ahr999 0.45: %s, ahr999 1.2: %s, ahr999x 0.45: %s',
    #             ahr999, ahr999_045, ahr999_120, ahr999x_045)
    logger.info('ahr999: %s, ahr999 1.2: %s', ahr999, ahr999_120)

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
    # Buy = namedtuple('Buy', 'order_size, userref')
    # for i in buy_levels:
    # Don't cross the book. Skip buy levele if buy level >= best ask
    # if i >= ask:
    #     logger.info('%s buy level >= ask', i)
    #     continue
    # add buy level: [ order size, price, userref, direction of trade ]
    order_size = config.BUY_LEVELS.get(pair)
    # buy = Buy(config.BUY_LEVELS.get(pair),
    #           np.random.randint(-2147483648, 2147483647, dtype=np.int32))
    logger.info('order_size %s', order_size)

    # -------------- Check for trade @ Kraken
    # iterate through buys and sells level
    # get order infor for particular buy/sell level
    # order, txid = util.get_order(orders, buy.userref, pair, api)
    # print('txid1', txid1)
    # logger.info('txid = %s', txid)
    # print('buy', buy)

    # check for minimum order size and continue
    price = max(ask, bid)
    cost = price * order_size
    if ahr999 < 1.2 and price < ahr999_120:
        # submit following data and place or update order:
        # ( library instance, order info, pair, direction of order,
        # size of order, price, userref, txid of existing order,
        # price precision, leverage, logger instance, oflags )
        # bal_start = api.get_usd_balance()
        # bal_start = 1998.40127897
        # logger.info('before order balance: %s', bal_start)

        cost, created_at, avg_fill_price = api.add_order(pair, order_size)
        coin_gecko.add_own_data(created_at, avg_fill_price)
        # response = 'test'

        logger.info('cost: %s', cost)
        # if response.get('error'):
        #    logger.info('%s trading error %s', pair, response)

        # bal_end = api.get_usd_balance()
        # logger.info('after order balance: %s', bal_end)

        # logger.info('api.get_balances: %s', api.get_balances())
        # logger.info('api.get_coins: %s', api.get_coins())
        # logger.info('api.get_total_usd_balance: %s', api.get_total_usd_balance())
        # logger.info('api.get_all_balances: %s', api.get_all_balances())
        # logger.info('api.get_total_account_usd_balance: %s', api.get_total_account_usd_balance())

        # sleep_time = 1
        # while math.isclose(bal_start, bal_end):
        #     bal_end = api.get_total_account_usd_balance()
        #     logger.info('Wait %s second balance change.', sleep_time)
        #     time.sleep(sleep_time)
        #     sleep_time *= 2

        # cost = max(bal_start - bal_end, 0)
        # logger.info('cost: %s', cost)
        # fee = cost - order_cost
        # logger.info('fee: %s %s', fee * 100 / cost, fee * 100 / order_cost)

        # balance = api.query_private('Balance')
        # if balance.get('error'):
        #     logger.warning('Balance error %s', balance.get('error'))
        #     bal = api.query_private('Balance').get('result')
        # else:
        #     bal = balance.get('result')
        # logger.info('USD Balance %s', bal.get('ZUSD'))
        # print('bal_all', bal_all)
        # self.get_cost(ref, res)

        # print('closed_orders: ', type(closed_orders))
        # orders = []
        # sleep_time = 1
        #while not orders:
        #    orders.extend(
        #        util.get_orders(closed_orders, buy.userref, pair, api))
        #    time.sleep(sleep_time)
        #    sleep_time *= 2
        # orders = [{'cost': cost, 'fee': cost * 0.26 / 100}]
        # cost = sum(
        #     (float(order['cost']) + float(order['fee'])) for order in orders)
        # print('res ', res)
        # result = {'txid': ['O4N3YT-TE4G2-V6SR2D']}
        # if res:
        # cost = max(api.get_cost(buy.userref, res), cost)

        # if (cost / order_size) > ahr999_045:
        ahr999, ahr999_120 = coin_gecko.get_coingecko()
        sleep_time = _GetWaitTime(ahr999, pair, cost)
        logger.info('sleep %s minutes', sleep_time / 60)
        time.sleep(sleep_time)

    # cancel existing order if new order size is less than minimum
    else:
        # res = util.check4cancel(api, order, txid)
        # print('Not enough funds to ', buy[3], pair,
        #       'or trade vol too small; canceling', res)
        logger.info('Price %s too high', pair)
        time.sleep(600)

    # logger.info('sleep %s minutes', cost * _SLEEP_SECONDS.get(pair) / 60)
    # time.sleep(cost * _SLEEP_SECONDS.get(pair))
    logger.handlers.pop()
