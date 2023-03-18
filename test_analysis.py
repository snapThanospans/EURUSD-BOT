import MetaTrader5 as mt
import analysis as a
from datetime import datetime as dt

def get_data():
    mt.initialize()

    utc_from = dt(2022, 8, 20) 
    ohlc = mt.copy_rates_range("Boom 500 Index", mt.TIMEFRAME_M1, utc_from, dt.now())

    print(ohlc)

# get_data()
mock_data_list = [
    10, 9, 8, 7, 4, 
    2, 8, 7, 4, 3,
    2, 4, 3, 2, 1, 0]

openPositions = []

for i in range(len(mock_data_list)):
    previous_close = mock_data_list[i]
    current_close = mock_data_list[i+1]
    current_price = current_close
    

    analysed_data = a.Analysis(current_close, previous_close, current_price)      

    if analysed_data.get_signal() and len(openPositions) == 0:
        print("took a sell")
        openPositions.append(current_close)
    elif analysed_data.take_profit() and len(openPositions) > 0:
        print("closed")
        openPositions = []





# current_close = 10
# previous_close = 9
# current_price = 9
# openPositions = [1]
# vol = 0.0

# analysed_data = a.Analysis(current_close, previous_close, current_price)      

# if analysed_data.get_signal() and len(openPositions) == 0:
#     print('we in')
#     # openPositions = open_trades(vol, 0.0)
# elif analysed_data.take_profit() and len(openPositions) > 0:
#     print('we in again')