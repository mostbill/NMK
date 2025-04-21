import backtrader as bt
from strategies.ma_strategy import MAStrategy
from utils.data_loader import fetch_data

def run_backtest():
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MAStrategy)

    # Fetch historical data
    df = fetch_data('AAPL', '2021-01-01', '2023-01-01')
    if df is None:
        return

    # Feed the data into Backtrader
    data = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(data)

    # Set up broker and sizer
    cerebro.broker.set_cash(10000)
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.broker.setcommission(commission=0.001)

    # Run the backtest
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot(style='candlestick')

if __name__ == '__main__':
    run_backtest()