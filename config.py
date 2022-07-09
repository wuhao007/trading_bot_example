# your local path to API keys and logs folder
path_key = '/Users/sunny/key/'
path_logs = '/tmp/'

# sell_levels and buy_levels are lists of lists. It defines:
# [ [ percented of balance to trade, price level, unique userref ], [ ... ] ]
buy_levels = [0.5]

# pairs is a list if list that defines tradable pairs and assets:
# [ [ base asset, quote asset, altname from AssetPairs endpoint ], [ ... ] ]
pairs = [('BTC', 'USD', 'XXBTZUSD')]