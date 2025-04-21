import backtrader as bt
from strategies.ma_strategy import MAStrategy
from utils.data_loader import fetch_data

def run_backtest():
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MAStrategy)

    # Fetch historical data
    df = fetch_data('AAPL', '2010-12-01', '2025-04-01')
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
    final_value = cerebro.broker.getvalue()
    print('Final Portfolio Value: %.2f' % final_value)

    # Buy-and-hold result
    initial_cash = 10000
    first_close = df['close'].iloc[0]
    last_close = df['close'].iloc[-1]
    shares = initial_cash // first_close
    leftover_cash = initial_cash - shares * first_close
    buy_and_hold_value = shares * last_close + leftover_cash
    print('Buy & Hold (Start to End) Value: %.2f' % buy_and_hold_value)
    print('Buy & Hold Profit/Loss: %.2f' % (buy_and_hold_value - initial_cash))

    # Calculate classic estimators
    import numpy as np
    returns = df['close'].pct_change().dropna()
    rf = 0.0  # risk-free rate
    sharpe_ratio = (returns.mean() - rf) / returns.std() * np.sqrt(252)

    # Calculate drawdown
    cum_returns = (1 + returns).cumprod()
    rolling_max = cum_returns.cummax()
    drawdown = (cum_returns - rolling_max) / rolling_max
    max_drawdown = drawdown.min()

    print('Sharpe Ratio: %.4f' % sharpe_ratio)
    print('Max Drawdown: %.2f%%' % (max_drawdown * 100))
    cerebro.plot(style='candlestick')

if __name__ == '__main__':
    run_backtest()