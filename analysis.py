class Analysis:
    """
        SIGNAL:
            We check the current close vs the previous.
            We check to see if the current close is higher than the previous candle
            
        Data:
            Current close.
            List of at least 3 previous closes.
    """

    def __init__(self, live_orders, running_trades):
        self.live_orders = live_orders
        self.running_trades = running_trades
        self.is_live_order
        self.is_running_trade

    def something(self):
        return true
    def get_signal(self):
        """
            Compare previous close with current close.

            params:
                current_close
                running_trades
        """
   
        l_v = len(self.live_order)
        r_t = len(self.running_trades)


        if self.current_close > self.previous_close:
            return True

##jlsfdkjl

     
    def is_live_order(self):
        """
            Gets the length of the orders list and return a 
                boolean value if empty or not.

            params:
                numberOrders --> int
            return:
                ifLiveOrders --> boolean
        """
        # return True

    def is_running_trade(self):
        """
            Gets the length of the orders list and return a 
                boolean value if empty or not.

            params:
                numberOfRunnigTrades --> int
            return:
                ifRunnigTrades --> boolean
        """
        # return True
