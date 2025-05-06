from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
from backtest_runner import run_backtests
from strategies.ma_strategy import MAStrategy
from strategies.breakout_atr_strategy import BreakoutATRStrategy

app = Flask(__name__)

STRATEGY_MAP = {
    'BreakoutATRStrategy': BreakoutATRStrategy,
    'MAStrategy': MAStrategy
}

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    plot_url = None
    if request.method == 'POST':
        stock = request.form['stock']
        start = request.form['start']
        end = request.form['end']
        strategy_name = request.form['strategy']
        strategy = STRATEGY_MAP.get(strategy_name, BreakoutATRStrategy)
        # Prepare config for backtest_runner
        stock_configs = [{
            'stock': stock,
            'start': start,
            'end': end
        }]
        # Patch run_backtests to use selected strategy
        def run_with_strategy(stock_configs, plot_folder="plots"):
            import backtrader as bt
            import csv
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            from utils.data_loader import fetch_data
            import numpy as np
            results = []
            if not os.path.exists(plot_folder):
                os.makedirs(plot_folder)
            for config in stock_configs:
                stock = config['stock']
                start = config['start']
                end = config['end']
                cerebro = bt.Cerebro()
                cerebro.addstrategy(strategy)
                df = fetch_data(stock, start, end)
                if df is None or df.empty:
                    continue
                data = bt.feeds.PandasData(dataname=df)
                cerebro.adddata(data)
                cerebro.broker.set_cash(10000)
                cerebro.addsizer(bt.sizers.FixedSize, stake=10)
                cerebro.broker.setcommission(commission=0.001)
                cerebro.run()
                final_value = cerebro.broker.getvalue()
                initial_cash = 10000
                first_close = df['close'].iloc[0]
                last_close = df['close'].iloc[-1]
                shares = initial_cash // first_close
                leftover_cash = initial_cash - shares * first_close
                buy_and_hold_value = shares * last_close + leftover_cash
                returns = np.array([final_value / initial_cash - 1])
                rf = 0.0
                sharpe_ratio = (returns.mean() - rf) / returns.std() * np.sqrt(252) if returns.std() != 0 else 0
                cum_returns = np.cumprod(1 + returns)
                rolling_max = np.maximum.accumulate(cum_returns)
                drawdown = (cum_returns - rolling_max) / rolling_max
                max_drawdown = drawdown.min() if len(drawdown) > 0 else 0
                fig = cerebro.plot(style='candlestick', iplot=False, volume=False)[0][0]
                filename = f"{stock}_{start}_to_{end}_{strategy_name}.png".replace(":", "-")
                filepath = os.path.join(plot_folder, filename)
                fig.savefig(filepath)
                plt.close(fig)
                results.append({
                    "stock": stock,
                    "start": start,
                    "end": end,
                    "final_portfolio_value": final_value,
                    "buy_and_hold_value": buy_and_hold_value,
                    "sharpe_ratio": sharpe_ratio,
                    "max_drawdown": max_drawdown,
                    "plot": filename
                })
            return results
        results = run_with_strategy(stock_configs)
        if results and len(results) > 0:
            result = results[0]
            plot_url = url_for('plot_file', filename=result['plot'])
    return render_template('index.html', result=result, plot_url=plot_url, strategies=list(STRATEGY_MAP.keys()))

@app.route('/plots/<filename>')
def plot_file(filename):
    return send_from_directory(os.path.join(os.getcwd(), 'plots'), filename)

if __name__ == '__main__':
    app.run(debug=True)