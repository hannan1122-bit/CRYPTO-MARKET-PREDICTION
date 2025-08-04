import requests
import pandas as pd
import numpy as np

def get_klines(symbol="BTCUSDT", interval="1h", limit=1000, start_time=None):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    if start_time:
        params["endTime"] = start_time

    response = requests.get(url, params=params)
    response.raise_for_status()  # raise error if any
    return response.json()


def RSI_CALCULATE(dataframe, periods=14):
    difference = dataframe["close"].diff()
    gain = difference.clip(lower=0)
    loss = -difference.clip(upper=0)  # Make losses positive

    avg_gain = gain.rolling(window=periods).mean()
    avg_loss = loss.rolling(window=periods).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

    # Get the open time of the earliest candle in first batch
    # earliest_open_time = data1[0][0]
    
    # Second request - 1000 candles before that
    # data2 = get_klines(start_time=earliest_open_time - 1)
    
    # Combine
    # all_data = data2 + data1  # older first
    
def get_pre_process_data():
    data1 = get_klines()
    all_data = data1

    df = pd.DataFrame(all_data, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_vol", "taker_buy_quote_vol", "ignore"
    ])

    df["close_time"] = pd.to_datetime(df["close_time"], unit="ms", utc=True).dt.tz_convert("Asia/Karachi")

    df.sort_values("close_time", inplace=True)

    df["target"] = df["close"].shift(-1)
    df["close"] = pd.to_numeric(df["close"], errors='coerce')
    df["SMA_12"] = df["close"].rolling(window=12).mean()
    df["SMA_12"].fillna(df["SMA_12"].iloc[12], inplace=True)
    df["SMA_26"] = df["close"].rolling(window=26).mean()
    df["SMA_26"].fillna(df["SMA_26"].iloc[26], inplace=True)
    df["RSI_14"] = RSI_CALCULATE(df, 14)
    df["RSI_14"].fillna(0, inplace=True)

    for col in df.columns:
        if col != 'close_time':
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df.drop(["ignore", "open_time", "taker_buy_quote_vol"], axis=1, inplace=True)
    df.set_index("close_time", inplace=True)
    df.dropna(inplace=True)

    return df

df=get_pre_process_data()
# print(df)