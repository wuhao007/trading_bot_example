import time
import os
import logging
import config

_TR = {'USDT': 5, 'USDC': 5}

# ---------------- Set up logger for writing logs


def setup_logger(name, log_file, level=logging.INFO, add_time=True):
    """Function setup as many loggers as you want"""

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.Formatter.converter = time.gmtime

    if add_time:
        hour = time.strftime("%m-%d_%H", time.gmtime(time.time()))
    else:
        hour = '001'

    handler = logging.FileHandler(
        os.path.join(config.path_logs, f'{hour}_{log_file}.log'))
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


# -------------- Return pairs string for ticker call


def get_ticker_pairs(pairs):
    return ','.join(pair.altname for pair in pairs)


# -------------- Order select


# here we use pair and userref to distinguish between orders
# return txid and order information
def get_order(opened, ref, pair, k):
    order1 = -1
    open2 = -1
    for open1 in opened:
        if opened.get(open1).get('userref') == ref and opened.get(open1).get(
                'descr').get('pair') == pair:
            if order1 != -1:
                close_k = k.query_private('CancelOrder', {'txid': open1})
                print("canceled", open1, close_k)
                time.sleep(1)
                continue
            order1 = opened.get(open1)
            open2 = open1
    return order1, open2


# -------------- Check for trade
# this function places or updates orders


def check4trade(k, order, pair, buyorsell, vol, price, ref, txid, price_cell,
                lever, logger, post):
    trade = -1
    # if order does not currently exist, we place it. Order size and price is
    # truncated to meet precesion requirements
    if order == -1:
        trade = k.query_private(
            'AddOrder', {
                'pair': pair,
                'type': buyorsell,
                'ordertype': 'limit',
                'volume': str('%.8f' % vol),
                'price': str(price_cell % price),
                'userref': ref,
                'oflags': post
            })
    else:
        # if an order currently exists at this price level, we check if it has
        # to be updated. We use 0.02% price tolerance and 2% size tolerance
        if abs(1 - float(order.get('descr').get('price')) /
               float(price_cell % price)) > 0.0002 or abs(
                   1 - vol / float(order.get('vol'))) > 0.02:
            close_k = k.query_private('CancelOrder', {'txid': txid})
            logger.info('close result ' + str(close_k))
            close_res = -1
            try:
                close_res = int(close_k.get('result').get('count'))
            except:
                pass
            if close_res == 1:
                trade = k.query_private(
                    'AddOrder', {
                        'pair': pair,
                        'type': buyorsell,
                        'ordertype': 'limit',
                        'volume': str('%.8f' % vol),
                        'price': str(price_cell % price),
                        'userref': ref,
                        'oflags': post
                    })
        else:
            print('Order not changed', txid)
            logger.info('Order not changed ' + str(txid))
    return trade


# --------------- Only cancel if order exist (!=-1)


def check4cancel(api, order, txid):
    close_api = -1
    if order != -1:
        close_api = api.query_private('CancelOrder', {'txid': txid})
    return close_api


# --------------- Return Minimum Volume depending on asset


def get_vol_min(asset):
    return _TR.get(asset, 5)


# ---------------- Return price precision


def get_price_dec(pair):
    res = 1  # USD, EUR to XBT is included here
    if pair in ['USDTZUSD', 'USDCUSD']:
        res = 4
    return f'%.{res}f'
