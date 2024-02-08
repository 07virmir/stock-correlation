import pandas as pd
from utils import get_data

def bollinger_bands(symbol, sd, ed, window=20, num_std=2):
    window = int(window)
    num_std = int(num_std)
    stock_prices = get_data(symbol, sd, ed)
    stock_prices['Norm_Price'] = stock_prices[symbol]/stock_prices.iloc[0][symbol]

    bollinger_bands = pd.DataFrame(index=stock_prices.index, columns=['SMA', 'STD', 'Upper_Band', 'Lower_Band', 'Stock_Price'])
    bollinger_bands = bollinger_bands.fillna(0.0)

    bollinger_bands['SMA'] = stock_prices[symbol].rolling(window=window).mean()
    bollinger_bands['STD'] = stock_prices[symbol].rolling(window=window).std()
    bollinger_bands['Upper_Band'] = bollinger_bands['SMA'] + (bollinger_bands['STD'] * num_std)
    bollinger_bands['Lower_Band'] = bollinger_bands['SMA'] - (bollinger_bands['STD'] * num_std)
    bollinger_bands['Stock_Price'] = stock_prices[symbol]
    bollinger_bands['%B'] = (stock_prices[symbol] -  bollinger_bands['Lower_Band']) / (bollinger_bands['Upper_Band'] - bollinger_bands['Lower_Band'])
    bollinger_bands['Overbought'] = 1.0
    bollinger_bands['Oversold'] = 0.0

    bollinger_bands.drop(bollinger_bands.index[:window-1], inplace=True)

    # This prevents errors on the frontend
    bollinger_bands.fillna(0, inplace=True)

    return bollinger_bands

def simple_moving_average(symbol, sd, ed, window=20):
    window = int(window)
    stock_prices = get_data(symbol, sd, ed)

    sma = pd.DataFrame(index=stock_prices.index, columns=['Price', 'SMA'])
    sma = sma.fillna(0.0)

    sma['Price'] = stock_prices[symbol]
    sma['SMA'] = stock_prices[symbol].rolling(window=window).mean()
    sma['P/S'] = stock_prices[symbol] / sma['SMA']
    
    sma.drop(sma.index[:window-1], inplace=True)
    return sma

def exponential_moving_average(symbol, sd, ed, window=20):
    window = int(window)
    stock_prices = get_data(symbol, sd, ed)

    ema = pd.DataFrame(index=stock_prices.index, columns=['Price', 'EMA'])
    ema = ema.fillna(0.0)

    ema['Price'] = stock_prices[symbol]
    ema['EMA'] = stock_prices[symbol].ewm(span=window, adjust=False).mean()
    ema['P/E'] = stock_prices[symbol] / ema['EMA']

    ema.drop(ema.index[:window-1], inplace=True)
    return ema

def relative_strength_index(symbol, sd, ed, window=14):
    window = int(window)
    stock_prices = get_data(symbol, sd, ed)

    rsi = pd.DataFrame(index=stock_prices.index, columns=['Price_Diff', 'Signal'])
    rsi['Price_Diff'] = stock_prices[symbol].diff()

    rsi['Gain'] = rsi['Price_Diff'].apply(lambda x: x if x > 0 else 0)
    rsi['Loss'] = rsi['Price_Diff'].apply(lambda x: -x if x < 0 else 0)

    rsi['Avg_Gain'] = rsi['Gain'].rolling(window=window).mean()
    rsi['Avg_Loss'] = rsi['Loss'].rolling(window=window).mean()

    rsi['RS'] = rsi['Avg_Gain'] / rsi['Avg_Loss']
    rsi['RSI'] = 100 - (100 / (1 + rsi['RS']))

    rsi['Signal'] = 0  
    rsi['Signal'][rsi['RSI'] >= 70] = -1
    rsi['Signal'][rsi['RSI'] <= 30] = 1

    rsi.dropna(inplace=True)

    rsi['Overbought'] = 70
    rsi['Oversold'] = 30
    
    return rsi

# Example Use Cases
bb = bollinger_bands('IBM', "2008-01-01", "2009-01-01")
sma = simple_moving_average('IBM', "2008-01-01", "2009-01-01")
ema = exponential_moving_average('IBM', "2008-01-01", "2009-01-01")
rsi = relative_strength_index('AAPL', "2008-01-01", "2009-01-01")

