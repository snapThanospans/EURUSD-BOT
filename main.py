import analysis as a
from datetime import datetime
import take_trade as t_t
import close_trade as c_t
import MetaTrader5 as mt


def open_trades(vol, sl):

    openPositions = []
    request = t_t.TakeTrade(vol, mt.ORDER_TYPE_SELL, sl)

    while len(openPositions) < 2:
        orders = mt.order_send(request.place()).order
        openPositions.append(orders)

    return openPositions


def close_trades(openPositions, vol, sl):
    
    request = c_t.CloseTrade(vol, mt.ORDER_TYPE_BUY, sl)
    for i in openPositions:
        mt.order_send(request.close(i))

    return


def get_open_close():

    date = str(datetime.today().date())
    dateSplit = date.split("-")

    dd = int(dateSplit[2])
    mm = int(dateSplit[1][1])
    yy = int(dateSplit[0])


    utc_from = datetime(yy,mm,dd,00,1)
    ohlc = mt.copy_rates_range("Boom 500 Index", mt.TIMEFRAME_M1, utc_from, datetime.now())
    current_close = ohlc[-2][-5]
    previous_close = ohlc[-3][-5]
    return previous_close, current_close


def get_current_prince():
    symbols_info = mt.symbol_info_tick("Boom 500 Index")._asdict()
    current_price = symbols_info['ask']
    return current_price

def main():

    openPositions = []
    vol = 0.20

    mt.initialize()

    while True:
        previous_close, current_close = get_open_close()
        current_price = get_current_prince()

        analysed_data = a.Analysis(current_close, previous_close, current_price)      

        if analysed_data.get_signal() and len(openPositions) == 0:
            openPositions = open_trades(vol, 0.0)
        elif analysed_data.take_profit() and len(openPositions) > 0:
            close_trades(openPositions, vol, 0.0)
            openPositions = []
        
        print(f'current price: {current_price}')


if __name__ == '__main__':
    main()
    # print(datetime.today().time().minute - 27)