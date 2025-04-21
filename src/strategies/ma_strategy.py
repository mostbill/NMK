import backtrader as bt

class MAStrategy(bt.Strategy):
    params = (
        ('fast_ma', 10),
        ('slow_ma', 30),
        ('rsi_period', 14),
        ('rsi_low', 30),
        ('rsi_high', 70),
    )

    def __init__(self):
        self.fast_ma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.p.fast_ma)
        self.slow_ma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.p.slow_ma)
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=self.p.rsi_period)

    def next(self):
        if not self.position:
            if self.fast_ma[0] > self.slow_ma[0] and self.rsi[0] > self.p.rsi_low:
                self.buy()
        else:
            if self.fast_ma[0] < self.slow_ma[0] or self.rsi[0] > self.p.rsi_high:
                self.close()