import time
import os
import logging
import config

# https://support.kraken.com/hc/en-us/articles/205893708-Minimum-order-size-volume-for-trading
_MINIMUM_ORDER_SIZE_VOLUME_FOR_TRADING = {'USDT': 5, 'USDC': 5, 'ZUSD': 5}
# https://support.kraken.com/hc/en-us/articles/4521313131540-Price-and-volume-decimal-precision
_PRICE_DECIMAL_PRECISION = {
    'XXBTZUSD': 1,
    'BTC/USD': 1,
    'XBTUSDT': 1,
    'BTC/USDT': 1,
    'XBTUSDC': 2,
    'BTC/USDC': 2,
    'XETHZUSD': 2,
    'ETH/USD': 2,
    'ETHUSDT': 2,
    'ETH/USDT': 2,
    'ETHUSDC': 2,
    'ETH/USDC': 2,
    'MATICUSD': 4,
    'MATIC/USD': 4,
}


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


def get_ticker_pairs(pair):
    """Return pairs string for ticker call."""
    return pair


def get_orders(ref, pair, api):
    """Order select.

    here we use pair and userref to distinguish between orders. 
    return txid and order information
    """
    # order1 = -1
    # open2 = -1
    results = []
    for order in api.query_private('ClosedOrders').get('result').get(
            'closed').values():
        if order.get('userref') == ref and order.get('descr').get(
                'pair') == pair:
            # if order1 != -1:
            #     close_k = api.query_private('CancelOrder', {'txid': open1})
            #     print("canceled", open1, close_k)
            #     time.sleep(1)
            #     continue
            results.append(order)
    return results
    # order1 = opened.get(open1)
    # open2 = open1
    # return order1, open2


def check4trade(api, pair, buyorsell, vol, price, ref, price_cell, post):
    """Check for trade this function places or updates orders."""
    return api.add_order(pair, buyorsell, vol, price, ref, price_cell, post)


def check4cancel(api, order, txid):
    """Only cancel if order exist (!=-1)."""
    return api.query_private('CancelOrder',
                             {'txid': txid}) if order != -1 else -1


def get_vol_min(asset):
    """Return Minimum Volume depending on asset."""
    return _MINIMUM_ORDER_SIZE_VOLUME_FOR_TRADING[asset]


def get_price_dec(pair):
    """Return price precision."""
    return f'%.{_PRICE_DECIMAL_PRECISION[pair]}f'
