import pandas as pd
from utils import get_data
import numpy as np

def cumulative_return(stocks, allocations, sd, ed):
    prices = get_data(stocks[0], sd, ed, add_spy=False)
    for i in range(1, len(stocks)):
        stock = stocks[i]
        prices = prices.join(get_data(stock, sd, ed, add_spy=False))
    
    start_prices = prices.iloc[0]
    normalized_prices = prices / start_prices			 		  		  		    	 		 		   		 		  
    normalized_weighted_prices = normalized_prices * allocations
    port_val = normalized_weighted_prices.sum(axis=1)
    cum_return = port_val.iloc[-1] - port_val.iloc[0]
    return cum_return

def avg_daily_return(stocks, allocations, sd, ed):
    prices = get_data(stocks[0], sd, ed, add_spy=False)
    for i in range(1, len(stocks)):
        stock = stocks[i]
        prices = prices.join(get_data(stock, sd, ed, add_spy=False))
    
    start_prices = prices.iloc[0]
    normalized_prices = prices / start_prices			 		  		  		    	 		 		   		 		  
    normalized_weighted_prices = normalized_prices * allocations
    port_val = normalized_weighted_prices.sum(axis=1)
    daily_returns = port_val.pct_change().iloc[1:]
    average_daily_return = daily_returns.mean()
    return average_daily_return

def std_daily_return(stocks, allocations, sd, ed):
    prices = get_data(stocks[0], sd, ed, add_spy=False)
    for i in range(1, len(stocks)):
        stock = stocks[i]
        prices = prices.join(get_data(stock, sd, ed, add_spy=False))
    
    start_prices = prices.iloc[0]
    normalized_prices = prices / start_prices			 		  		  		    	 		 		   		 		  
    normalized_weighted_prices = normalized_prices * allocations
    port_val = normalized_weighted_prices.sum(axis=1)
    daily_returns = port_val.pct_change().iloc[1:]
    std = daily_returns.std()
    return std

def sharpe_ratio(stocks, allocations, sd, ed):
    prices = get_data(stocks[0], sd, ed, add_spy=False)
    for i in range(1, len(stocks)):
        stock = stocks[i]
        prices = prices.join(get_data(stock, sd, ed, add_spy=False))
    
    start_prices = prices.iloc[0]
    normalized_prices = prices / start_prices			 		  		  		    	 		 		   		 		  
    normalized_weighted_prices = normalized_prices * allocations
    port_val = normalized_weighted_prices.sum(axis=1)
    daily_returns = port_val.pct_change().iloc[1:]
    average_daily_return = daily_returns.mean()
    std_daily_return = daily_returns.std()
    sharpe_ratio = np.sqrt(252) * (average_daily_return/std_daily_return)
    return sharpe_ratio

def all_portfolio_metrics(stocks, allocations, sd, ed):
    prices = get_data(stocks[0], sd, ed, add_spy=False)
    for i in range(1, len(stocks)):
        stock = stocks[i]
        prices = prices.join(get_data(stock, sd, ed, add_spy=False))
    
    start_prices = prices.iloc[0]
    normalized_prices = prices / start_prices			 		  		  		    	 		 		   		 		  
    normalized_weighted_prices = normalized_prices * allocations
    port_val = normalized_weighted_prices.sum(axis=1)
    cum_return = port_val.iloc[-1] - port_val.iloc[0]
    daily_returns = port_val.pct_change().iloc[1:]
    average_daily_return = daily_returns.mean()
    std_daily_return = daily_returns.std()
    sharpe_ratio = np.sqrt(252) * (average_daily_return/std_daily_return)
    metrics = {
        'cum_return': cum_return,
        'avg_daily_return': average_daily_return,
        'std_daily_return': std_daily_return,
        'sharpe_ratio': sharpe_ratio
    }

    return metrics

all_portfolio_metrics(['IBM', 'JPM', 'AAPL'], [0.3, 0.3, 0.4], "2009-01-01", "2010-01-01")