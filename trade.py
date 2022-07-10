import util
from config import buy_levels
from collections import namedtuple
import time

# Trade part


def trade(pair, bal, orders, api, ticker):
    # construct pair from base and quote. USDCUSD is an exception
    # print('base', base)
    # print('quote', quote)
    # print('pair', pair)
    # print('bal', bal)
    # print('orders', orders)
    # print('api', api)
    # print('ticker', ticker)

    # start logger
    base, quote, altname = pair.base_asset, pair.quote_asset, pair.altname
    logger = util.setup_logger(altname, altname)
    logger.info(
        '------------------------- New case --------------------------------')
    # assign base and quote balance variables. -0.1 is a trick to get rid
    # of rounding issues and insufficient funds error
    bal_b, bal_q = bal.get(base, 0), bal.get(quote, 0)
    # print('bal_b', base, bal_b)
    # print('bal_q', quote, bal_q)
    logger.info('%s %s %s %s', base, bal_b, quote, bal_q)
    # price_cell is a price precision variable
    price_cell = util.get_price_dec(altname)
    # print('price_cell', price_cell)
    # lever is a leverage value
    lever = 'none'

    # vol_min is a minimum order size. It depends on base currency
    vol_min = util.get_vol_min(base)

    # get best ask/bid from ticker
    ask = float(ticker.get(altname).get('a')[0])
    print('ask', ask)
    bid = float(ticker.get(altname).get('b')[0])
    print('bid', bid)

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
    buys = []
    Buy = namedtuple('Buy', 'order_size, price, userref, direction_of_trade')
    for i in buy_levels:
        # Don't cross the book. Skip buy levele if buy level >= best ask
        # if i >= ask:
        #     logger.info('%s buy level >= ask', i)
        #     continue
        # add buy level: [ order size, price, userref, direction of trade ]
        buys.append(Buy(i / ask, ask, str(int(1000 * time.time())), 'buy'))
    logger.info('buys %s', buys)

    # -------------- Check for trade @ Kraken
    # iterate through buys and sells level
    for buy in buys:
        # get order infor for particular buy/sell level
        order, txid = util.get_order(orders, buy.userref, altname, api)
        # print('txid1', txid1)
        logger.info('txid = %s', txid)
        # print('buy', buy)

        # check for minimum order size and continue
        if buy.order_size >= vol_min:
            # submit following data and place or update order:
            # ( library instance, order info, altname, direction of order,
            # size of order, price, userref, txid of existing order,
            # price precision, leverage, logger instance, oflags )
            res = util.check4trade(api, order, altname, buy.direction_of_order,
                                   buy.order_size, buy.price, buy.userref,
                                   txid, price_cell, lever, logger, 'post')
            logger.info('traded: %s', res)
        # cancel existing order if new order size is less than minimum
        else:
            res = util.check4cancel(api, order, txid)
            # print('Not enough funds to ', buy[3], altname,
            #       'or trade vol too small; canceling', res)
            logger.info(
                'Not enough funds to %s %s or trade vol too small; canceling %s',
                buy.direction_of_trade, altname, res)
        if res != -1:
            if 'error' in res and res.get('error'):
                logger.warning('%s trading error %s', altname, res)
    logger.handlers.pop()
