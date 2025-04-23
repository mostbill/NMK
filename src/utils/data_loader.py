import requests
import pandas as pd
import os

def fetch_data(ticker, start_date, end_date):
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    if not api_key:
        raise ValueError("Alpha Vantage API key not found. Set ALPHA_VANTAGE_API_KEY environment variable.")
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch data: HTTP {response.status_code}")
    data_json = response.json()
    if 'Time Series (Daily)' not in data_json:
        raise ValueError(f"Unexpected response format or API limit reached: {data_json}")
    ts_data = data_json['Time Series (Daily)']
    df = pd.DataFrame.from_dict(ts_data, orient='index')
    df.index = pd.to_datetime(df.index)
    df = df.loc[(df.index >= pd.to_datetime(start_date)) & (df.index <= pd.to_datetime(end_date))]
    df = df.rename(columns={
        '1. open': 'open',
        '2. high': 'high',
        '3. low': 'low',
        '4. close': 'close',
        '5. volume': 'volume'
    })
    df = df[['open', 'high', 'low', 'close', 'volume']]
    df = df.astype(float)
    df = df.sort_index()
    if df.empty:
        raise ValueError("No data fetched from Alpha Vantage.")
    return df