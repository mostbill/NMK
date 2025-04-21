import backtrader as bt

class BreakoutATRStrategy(bt.Strategy):
    params = (
        ('breakout_period', 20),
        ('atr_period', 14),
        ('risk_atr', 2.0),
        ('reward_atr', 3.0),
    )

    def __init__(self):
        self.highest = bt.indicators.Highest(self.data.high, period=self.p.breakout_period)
        self.lowest = bt.indicators.Lowest(self.data.low, period=self.p.breakout_period)
        self.atr = bt.indicators.ATR(self.data, period=self.p.atr_period)
        self.order = None
        self.entry_price = None
        self.stop_price = None
        self.take_profit = None

    def next(self):
        if self.order:
            return  # waiting for pending order

        if not self.position:
            # Breakout long
            if self.data.close[0] > self.highest[-1]:
                self.entry_price = self.data.close[0]
                self.stop_price = self.entry_price - self.p.risk_atr * self.atr[0]
                self.take_profit = self.entry_price + self.p.reward_atr * self.atr[0]
                self.order = self.buy()
            # Breakout short
            elif self.data.close[0] < self.lowest[-1]:
                self.entry_price = self.data.close[0]
                self.stop_price = self.entry_price + self.p.risk_atr * self.atr[0]
                self.take_profit = self.entry_price - self.p.reward_atr * self.atr[0]
                self.order = self.sell()
        else:
            # Manage long position
            if self.position.size > 0:
                if self.data.close[0] <= self.stop_price or self.data.close[0] >= self.take_profit:
                    self.close()
                    self.order = None
            # Manage short position
            elif self.position.size < 0:
                if self.data.close[0] >= self.stop_price or self.data.close[0] <= self.take_profit:
                    self.close()
                    self.order = None

    def notify_order(self, order):
        if order.status in [order.Completed, order.Canceled, order.Margin, order.Rejected]:
            self.order = None