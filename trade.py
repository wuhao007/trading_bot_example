import util
from config import sell_levels, buy_levels
import time

# Trade part


def trade(base, quote, pair, bal, orders, k, ticker):
    # construct pair from base and quote. USDCUSD is an exception
    # print('base', base)
    # print('quote', quote)
    # print('pair', pair)
    # print('bal', bal)
    # print('orders', orders)
    # print('k', k)
    print('ticker', ticker)

    # start logger
    logger = util.setup_logger(pair, pair)
    logger.info(
        '------------------------- New case --------------------------------')
    # assign base and quote balance variables. -0.1 is a trick to get rid
    # of rounding issues and insufficient funds error
    bal_b = float(bal.get(base, 0)) - 0.1
    bal_q = float(bal.get(quote, 0)) - 0.1
    # print('bal_b', base, bal_b)
    # print('bal_q', quote, bal_q)
    logger.info(base + ' ' + str(bal_b) + ' ' + quote + ' ' + str(bal_q))
    # price_cell is a price precision variable
    price_cell = util.get_price_dec(pair)
    # lever is a leverage value
    lever = 'none'

    # vol_min is a minimum order size. It depends on base currency
    vol_min = util.get_vol_min(base)

    # get best ask/bid from ticker
    ask = float(ticker.get(pair).get('a')[0])
    print('ask', ask)
    bid = float(ticker.get(pair).get('b')[0])
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
    for i in buy_levels:
        # Don't cross the book. Skip buy levele if buy level >= best ask
        if i[1] >= ask:
            logger.info(str(i[1]) + ' buy level >= ask')
            continue
        # add buy level: [ order size, price, userref, direction of trade ]
        buys.append([i[0] / ask, ask, str(int(1000 * time.time())), 'buy'])
    logger.info('buys ' + str(buys))

    # -------------- Check for trade @ Kraken
    # iterate through buys and sells level
    for i in buys:
        # get order infor for particular buy/sell level
        order1, txid1 = util.get_order(orders, i[2], pair, k)
        # print('txid1', txid1)
        logger.info('txid1 = ' + str(txid1))
        # print('i', i)

        # check for minimum order size and continue
        if i[0] >= vol_min:
            try:
                # submit following data and place or update order:
                # ( library instance, order info, pair, direction of order,
                # size of order, price, userref, txid of existing order,
                # price precision, leverage, logger instance, oflags )
                res = util.check4trade(k, order1, pair, i[3], i[0], i[1], i[2],
                                      txid1, price_cell, lever, logger, 'post')
                print(res)
                logger.info('traded: ' + str(res))
            except Exception as e:
                print('Error occured when ', i[3], pair, e)
                logger.warning('Error occured when ' + i[3] + pair + str(e))
        # cancel existing order if new order size is less than minimum
        else:
            res = util.check4cancel(k, order1, txid1)
            # print('Not enough funds to ', i[3], pair,
            #       'or trade vol too small; canceling', res)
            logger.info('Not enough funds to ' + str(i[3]) + ' ' + pair +
                        ' or trade vol too small; canceling ' + str(res))
        if res != -1:
            if 'error' in res and res.get('error') != []:
                logger.warning(pair + ' trading error ' + str(res))
    logger.handlers.pop()
