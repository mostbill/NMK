import backtrader as bt
from strategies.ma_strategy import MAStrategy
from strategies.breakout_atr_strategy import BreakoutATRStrategy
from utils.data_loader import fetch_data
import os
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend to prevent plot windows from opening
import matplotlib.pyplot as plt


def run_backtests(stock_configs, plot_folder="plots"):
    """
    Runs backtests for a list of stock configurations and saves performance plots.
    Args:
        stock_configs (list): List of dicts with 'stock', 'start', 'end' keys.
        plot_folder (str): Directory to save plots.
    """
    import csv
    results = []
    if not os.path.exists(plot_folder):
        os.makedirs(plot_folder)

    for config in stock_configs:
        stock = config['stock']
        start = config['start']
        end = config['end']

        print(f"\nRunning backtest for {stock} from {start} to {end}")

        # Initialize Backtrader engine
        cerebro = bt.Cerebro()
        cerebro.addstrategy(BreakoutATRStrategy)

        # Fetch historical data
        df = fetch_data(stock, start, end)
        if df is None or df.empty:
            print(f"No data for {stock} {start} to {end}")
            continue

        # Add data feed to Cerebro
        data = bt.feeds.PandasData(dataname=df)
        cerebro.adddata(data)

        # Set initial cash and trading parameters
        cerebro.broker.set_cash(10000)
        cerebro.addsizer(bt.sizers.FixedSize, stake=10)
        cerebro.broker.setcommission(commission=0.001)

        print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

        # Run the backtest
        cerebro.run()
        final_value = cerebro.broker.getvalue()
        print('Final Portfolio Value: %.2f' % final_value)

        # Calculate Buy & Hold performance
        initial_cash = 10000
        first_close = df['close'].iloc[0]
        last_close = df['close'].iloc[-1]
        shares = initial_cash // first_close
        leftover_cash = initial_cash - shares * first_close
        buy_and_hold_value = shares * last_close + leftover_cash
        print('Buy & Hold (Start to End) Value: %.2f' % buy_and_hold_value)
        print('Buy & Hold Profit/Loss: %.2f' % (buy_and_hold_value - initial_cash))

        # Calculate Sharpe Ratio and Max Drawdown
        import numpy as np
        returns = np.array([final_value / initial_cash - 1])
        rf = 0.0  # Risk-free rate
        sharpe_ratio = (returns.mean() - rf) / returns.std() * np.sqrt(252)
        cum_returns = np.cumprod(1 + returns)
        rolling_max = np.maximum.accumulate(cum_returns)
        drawdown = (cum_returns - rolling_max) / rolling_max
        max_drawdown = drawdown.min()
        print('Sharpe Ratio: %.4f' % sharpe_ratio)
        print('Max Drawdown: %.2f%%' % (max_drawdown * 100))

        # Save plot to file (never show with GUI)
        fig = cerebro.plot(style='candlestick', iplot=False, volume=False)[0][0]
        filename = f"{stock}_{start}_to_{end}.png".replace(":", "-")
        filepath = os.path.join(plot_folder, filename)
        fig.savefig(filepath)
        plt.close(fig)
        print(f"Plot saved to {filepath}")

        # Collect results for CSV
        results.append({
            "stock": stock,
            "start": start,
            "end": end,
            "final_portfolio_value": final_value,
            "buy_and_hold_value": buy_and_hold_value,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": max_drawdown
        })

    # Write summary CSV after all backtests
    csv_path = os.path.join(plot_folder, "backtest_summary.csv")
    with open(csv_path, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["stock", "start", "end", "final_portfolio_value", "buy_and_hold_value", "sharpe_ratio", "max_drawdown"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)
    print(f"Summary CSV saved to {csv_path}")

if __name__ == '__main__':
    # Example usage: add your stocks and date ranges here
    # Set global start and end dates for all stocks
    start_date = "2024-06-01"
    end_date = "2025-04-01"
    stock_configs = [
        {"stock": "AAPL", "start": start_date, "end": end_date},
        # {"stock": "MSFT", "start": start_date, "end": end_date},
        # {"stock": "TSLA", "start": start_date, "end": end_date},
        # {"stock": "AMZN", "start": start_date, "end": end_date},
        # {"stock": "GOOG", "start": start_date, "end": end_date},
        # {"stock": "META", "start": start_date, "end": end_date},
        # {"stock": "NVDA", "start": start_date, "end": end_date},
        # {"stock": "BRK-B", "start": start_date, "end": end_date},
        # {"stock": "JNJ", "start": start_date, "end": end_date},
        # {"stock": "PG", "start": start_date, "end": end_date},
        # {"stock": "UNH", "start": start_date, "end": end_date},
        # {"stock": "V", "start": start_date, "end": end_date},
        # {"stock": "XOM", "start": start_date, "end": end_date},
        # {"stock": "CVX", "start": start_date, "end": end_date},
    ]
    run_backtests(stock_configs)