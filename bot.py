from ctypes import GetLastError
from datetime import datetime
from signal import signal
import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import time

SYMBOL = "Volatility 75 Index"
# SYMBOL = "Step Index"
TIMEFRAME = mt5.TIMEFRAME_M1
VOLUME = 0.01 # Trade Volume
DEVIATION = 20 # Deviation for Order Slippage
MAGIC = 1234
SMA_PERIOD = 20 # SMA Period for Bollinger Band
STANDARD_DEVIATIONS = 2 # Number of Deviations for calculation of bollinger bands.

TP_SD = 2
SL_SD = 32

# function to send market orders
def market_order(symbol, volume, order_type, deviation, magic, sl, tp):
    tick = mt5.symbol_info_tick(symbol)
    print(tick)

    order_dict = {"buy": mt5.ORDER_TYPE_BUY, "sell": mt5.ORDER_TYPE_SELL}
    price_dict = {"buy": tick.ask, "sell": tick.bid}

    # V75
    sl_dict = {"buy": price_dict[order_type] - 5000, "sell": price_dict[order_type] + 5000}
    tp_dict = {"buy": price_dict[order_type] + 15000, "sell": price_dict[order_type] - 15000}

    # Step Index
    # sl_dict = {"buy": price_dict[order_type] - 10, "sell": price_dict[order_type] + 10}
    # tp_dict = {"buy": price_dict[order_type] + 30, "sell": price_dict[order_type] - 30}

    request = {
        "action":mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_dict[order_type],
        "price": price_dict[order_type],
        "deviation": deviation,
        "magic": magic,
        "sl": sl_dict[order_type],
        "tp": tp_dict[order_type],
        "comment": "Python Market Order",
        "type_time": mt5.ORDER_TIME_GTC,
        # "type_filling": mt5.ORDER_FILLING_IOC,
    }

    order_result = mt5.order_send(request)
    check = mt5.order_check(request)
    print(check)

    if order_result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. order_send failed, retcode={}".format(order_result.retcode))
    


    return order_result


# function to close open trades
def close_trades(position):
    tick = mt5.symbol_info_tick(position.symbol)
    print(tick)
    

    request={
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": position.symbol,
    "volume": position.volume,
    "type": mt5.ORDER_TYPE_SELL if position.type == 0 else mt5.ORDER_TYPE_BUY,
    "position": position.ticket,
    "price": tick.ask if position.type == 1 else tick.bid,
    "deviation": DEVIATION,
    "magic": MAGIC,
    "comment": "python script close",
    "type_time": mt5.ORDER_TIME_GTC,
}

    order_result = mt5.order_send(request)
    check = mt5.order_check(request)
    print(check)

    if order_result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. order_send failed, retcode={}".format(order_result.retcode))
    


    return order_result


# def find_crossover(fast_sma, prev_fast_sma, slow_sma):
    
#     if fast_sma > slow_sma and prev_fast_sma < slow_sma:
#         return 'bullish crossover'
#     elif fast_sma < slow_sma and prev_fast_sma > slow_sma:
#         return 'bearish crossover'
    
#     return None


def get_signal():
    # bar data
    bars = mt5.copy_rates_from_pos(SYMBOL, TIMEFRAME, 1, 1000)

    # converting to dataframe
    df = pd.DataFrame(bars)


    # simple moving average
    sma = df["close"].mean()

    # print(df['close'].rolling(100).mean())


    df['fast_sma'] = df['close'].rolling(100).mean()
    df['slow_sma'] = df['close'].rolling(200).mean()


    # finding crossovers
    prev_fast_sma = df['fast_sma'].shift(1)
    df['prev_fast_sma'] = df['fast_sma'].shift(1)

    df.dropna(inplace=True)

    # print(df)

    fast_sma = df.iloc[-1]['fast_sma']
    slow_sma = df.iloc[-1]['slow_sma']
    prev_fast_sma = df.iloc[-1]['prev_fast_sma']

    # print(fast_sma[])

    # df['crossover'] = np.vectorize(find_crossover)(fast_sma, prev_fast_sma, slow_sma)


    # signal = df[df['crossover'] == 'bullish crossover'].copy()
    # print(signal)

    # standard deviation
    sd = df["close"].std()

    # lower band
    lower_band = sma - STANDARD_DEVIATIONS * sd

    # upper band
    upper_band = sma + STANDARD_DEVIATIONS * sd

    # last close_price
    last_close_price = df.iloc[-1]["close"]

    # print(last_close_price, upper_band)

    # finding signal
    # if last_close_price < lower_band:
    #     return "buy", sd
    # elif last_close_price > upper_band:
    #     return "sell", sd
    # else:
    #     return [None, None]

    # print(fast_sma)
    # print(slow_sma)
    # print(prev_fast_sma)

    # tick = mt5.symbol_info_tick(SYMBOL)
    # market_order(SYMBOL, VOLUME, "buy", DEVIATION, MAGIC, tick.bid - SL_SD * sd, tick.bid + TP_SD * sd)



    if fast_sma >  slow_sma and prev_fast_sma < slow_sma:
        print('bullish crossover')
        return "buy", sd
    elif fast_sma <  slow_sma and prev_fast_sma > slow_sma:
        print('bearish crossover')
        return "sell", sd

    return [None, None]


# connect to platform
initialized = mt5.initialize()
mt5.login(30160627, "MikeOxLong69", "Deriv-Demo")
account = mt5.account_info()
# print(account)

if initialized:
    print("Connected to MetaTrader5")
    print("Login: ", mt5.account_info().login)
    print("Server: ", mt5.account_info().server)





# Strategy Loop
while True:

    # if mt5.positions_total()
    # print(mt5.positions_total())
    # signal, sd = get_signal()
    # print(signal, sd)

    signal, sd = get_signal()
    print(signal, sd)

    open_positions = mt5.positions_get()


    # if there's a signal and there are trades open the close them to take the new signal
    if mt5.positions_total() == 5 and signal != None:
        print("Closing Trades")
        for position in open_positions:
            close_trades(position)



    # If no positions are open
    if mt5.positions_total() < 5:

        # getting signal history to avoid consecutive trades
        from_date = datetime(2022, 9, 23)
        deals = mt5.history_deals_get(from_date, datetime.now())
        deals_df = pd.DataFrame(list(deals),columns=deals[0]._asdict().keys())
        previous_history = int(deals_df['type'].iat[-1])
        # print(previous_history)

        # buy = 1
        # sell = 0

        tick = mt5.symbol_info_tick(SYMBOL)
        # if previous_history == 0:
        # print("Previous: "+str(previous_history))
        if signal == "buy":
            for i in range(5):    
                market_order(SYMBOL, VOLUME, "buy", DEVIATION, MAGIC, tick.bid - SL_SD * sd, tick.bid + TP_SD * sd)

            # sleep for a minute and 10 seconds to avoid opening and closing of trades in that 1 minute window of the signal
            time.sleep(70)

        # elif previous_history == 1:
        # print("Previous: "+str(previous_history))
        if signal == "sell" and previous_history == 1:
            for i in range(5):  
                market_order(SYMBOL, VOLUME, "sell", DEVIATION, MAGIC, (tick.bid + SL_SD) * sd, (tick.bid - TP_SD) * sd)
            
            # sleep for a minute and 10 seconds to avoid opening and closing of trades in that 1 minute window of the signal
            time.sleep(70)

        
    

    # check for signal every 1 second
    # time.sleep(1)