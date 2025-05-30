![NMK Logo](nmk_logo.png)
# NMK Backtesting Framework

## Overview
This project provides a flexible backtesting framework using Backtrader for evaluating trading strategies on multiple stocks. It supports batch backtesting, performance analysis, and automated plot generation without requiring a GUI.

## Key Features
- **Batch Backtesting:** Run backtests for multiple stocks and date ranges in a single execution.
- **Strategy Support:** Includes Moving Average (MA) and Breakout ATR strategies (see `src/strategies/`).
- **Automated Plot Saving:** Plots are saved directly to the `plots/` folder using a non-GUI backend (matplotlib 'Agg').
- **Performance Metrics:** Calculates Sharpe Ratio, Max Drawdown, and Buy & Hold results for each stock.
- **Summary CSV:** Outputs a summary CSV (`plots/backtest_summary.csv`) with key metrics for all runs.
- **Error Handling:** Skips stocks with missing or empty data and continues processing others.

## Usage
1. **Install Requirements:**
   - Python 3.7+
   - Install dependencies:
     ```
     pip install backtrader matplotlib pandas numpy
     ```
2. **Prepare Data Loader:**
   - Ensure `src/utils/data_loader.py` provides a `fetch_data(stock, start, end)` function returning a pandas DataFrame with OHLCV columns.

3. **Configure Stocks:**
   - Edit `src/backtest_runner.py` and update the `stock_configs` list with your desired stocks and date ranges.

4. **Run Backtests:**
   - Execute:
     ```
     python src/backtest_runner.py
     ```

5. **Results:**
   - Plots are saved in the `plots/` directory.
   - A summary CSV is generated at `plots/backtest_summary.csv`.

## Example `stock_configs`
```
stock_configs = [
    {"stock": "AAPL", "start": "2025-01-01", "end": "2025-03-01"},
    {"stock": "MSFT", "start": "2025-01-01", "end": "2025-03-01"},
    # Add more as needed
]
```

## Limitations & Notes
- Only stocks with available and non-empty data are processed.
- Plots are never shown interactively; they are always saved to disk.
- The default strategy is `BreakoutATRStrategy`. You can switch to `MAStrategy` by editing the `cerebro.addstrategy` line.
- Ensure your data loader returns data in the expected format (see code comments).

## Changelog
### [Unreleased]
- Switched to batch processing for multiple stocks.
- Added automated plot saving with non-GUI backend.
- Improved error handling for missing/empty data.
- Added summary CSV output for all backtests.
- Modularized strategies for easy extension.

---
For more details, see the code in `src/backtest_runner.py` and `src/strategies/`.