import MetaTrader5 as mt


class TakeTrade:

    def __init__(self, vol, order_type, stop_loss):
        self.vol = vol
        self.order_type = order_type
        self.stop_loss = stop_loss


    def place(self):
        return {
            "action": mt.TRADE_ACTION_DEAL,
            "symbol": "Boom 500 Index",
            "volume": self.vol,
            "type": self.order_type,
            "price": mt.symbol_info_tick("Boom 500 Index").ask,
            "sl": self.stop_loss,
            "tp": 0.0,
            "deviation": 20,
        }


