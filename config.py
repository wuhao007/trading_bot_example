# your local path to API keys and logs folder
path_key = 'pathtokeydirectory'
path_logs = 'pathtologsdirectory'

# sell_levels and buy_levels are lists of lists. It defines:
# [ [ percented of balance to trade, price level, unique userref ], [ ... ] ]
sell_levels = [[0.5, 1.008, 101], [0.5, 1.002, 102]]
buy_levels = [[0.5, 0.992, 201], [0.3, 0.996, 202], [0.2, 0.998, 203]]

# pairs is a list if list that defines tradable pairs and assets:
# [ [ base asset, quote asset, altname from AssetPairs endpoint ], [ ... ] ]
pairs = [['USDC', 'ZUSD', 'USDCUSD']]
