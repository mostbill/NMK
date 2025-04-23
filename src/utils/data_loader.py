import yfinance as yf

def fetch_data(ticker, start_date, end_date):
    try:
        df = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            auto_adjust=False,
            multi_level_index=False,
            progress=False
        )
        if df.empty:
            raise ValueError("No data fetched from Yahoo Finance.")
        
        # Rename columns to match Backtrader's expected format
        df.rename(columns={
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume'
        }, inplace=True)
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None