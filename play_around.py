# from os import curdir
# import MetaTrader5 as mt
# from datetime import datetime

# mt.initialize()
# # symbols_info = mt.symbol_info("Boom 500 Index").session_open
# symbols_info = mt.symbol_info_tick("Boom 500 Index")._asdict()

# # print(symbols_info)

# utc_from = datetime(2022, 8, 20)

# ohlc = mt.copy_rates_range("Boom 500 Index", mt.TIMEFRAME_M1, utc_from, datetime.now())
# print(ohlc)

# # symbol_info = mt.symbol_info("BOOM 500")
# # print(symbol_info)


# current_close = ohlc[-1][-4]
# previous_close = ohlc[-2][-4]
# # current_price = symbols_info['ask']
# print(f'current: {current_close}')
# print(f'previous: {previous_close}')
# # print(f'current price: {current_price}')


# # request =  {
# #             "action": mt.TRADE_ACTION_DEAL,
# #             "symbol": "Boom 500 Index",
# #             "volume": 0.20,
# #             "type": mt.ORDER_TYPE_BUY,
# #             "price": mt.symbol_info_tick("Boom 500 Index").ask,
# #             "sl": 0.0,
# #             "tp": 0.0,
# #             "deviation": 20,
# #         }

# # order = mt.order_send(request).order
# # print(order)



# for i in range(10):
#     for j in range(4):
        

        # 100.123

import MetaTrader5 as mt
from datetime import datetime


mt.initialize()
utc_from = datetime(2022,8,22) 
ticks_data = mt.copy_ticks_range("Boom 500 Index", utc_from, datetime.now(), mt.COPY_TICKS_ALL)
with open("ticks_data.txt", "w") as text:
    text.write(str(ticks_data))

for j in ticks_data:
    print(j)
