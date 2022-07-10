from collections import namedtuple
# your local path to API keys and logs folder
path_key = '/Users/sunny/key'
path_logs = '/Users/sunny/trading_bot_example/logs'

# sell_levels and buy_levels are lists of lists. It defines:
# [ [ percented of balance to trade, price level, unique userref ], [ ... ] ]
buy_levels = [1.06]

# {'XXBT': '0.0000097500', 'DAI': '0.0000000000', 'XETC': '0.0000039000',
# 'DOT': '0.0020759200', 'DOT.S': '0.0000000000', 'USDT': '0.00004210',
# 'BCH': '0.0000000000', 'XLTC': '0.0000000000', 'EOS': '0.0000000000',
# 'LINK': '0.0000000000', 'ZUSD': '0.0060', 'XETH': '0.0000000000'}
# pairs is a list if list that defines tradable pairs and assets:
# [ [ base asset, quote asset, altname from AssetPairs endpoint ], [ ... ] ]
Pair = namedtuple('Pair', 'base_asset altname')
pairs = [Pair('ZUSD', 'XXBTZUSD')]
