from typing import Optional
import pandas as pd
from utils import get_data

def beta(symbol, sd, ed):
    stock_data = get_data(symbol, sd, ed, add_spy=True)
    stock_data['stock_pct_chg'] = stock_data[symbol].pct_change()
    stock_data['mkt_pct_chg'] = stock_data['SPY'].pct_change()

    cov = stock_data['stock_pct_chg'].cov(stock_data['mkt_pct_chg'])
    mkt_var = stock_data['mkt_pct_chg'].var()

    return cov/mkt_var

def jensen_alpha(symbol, sd, ed, risk_free_rate = 0.02):
    risk_free_rate = float(risk_free_rate)
    stock_data = get_data(symbol, sd, ed, add_spy=True)
    stock_data['stock_pct_chg'] = stock_data[symbol].pct_change()
    stock_data['mkt_pct_chg'] = stock_data['SPY'].pct_change()

    b = beta(symbol, sd, ed)
    stock_data['alpha'] = (stock_data['stock_pct_chg'] - (risk_free_rate + b * (stock_data['mkt_pct_chg'] - risk_free_rate))).mean()

    return stock_data['alpha'].mean()

def treynor_ratio(symbol, sd, ed, risk_free_rate = 0.02):
    risk_free_rate = float(risk_free_rate)
    stock_data = get_data(symbol, sd, ed)
    stock_data['stock_pct_chg'] = stock_data[symbol].pct_change()

    b = beta(symbol, sd, ed)

    return (stock_data['stock_pct_chg'].mean() - risk_free_rate) / b

def information_ratio(symbol, sd, ed):
    stock_data = get_data(symbol, sd, ed, add_spy=True)

    stock_returns = stock_data[symbol].pct_change().dropna()
    benchmark_returns = stock_data['SPY'].pct_change().dropna()

    excess_returns = stock_returns - benchmark_returns
    mean_excess_return = excess_returns.mean()
    std_dev_excess_return = excess_returns.std()

    information_ratio = mean_excess_return / std_dev_excess_return

    return information_ratio

def sortino_ratio(symbol, sd, ed, risk_free_rate=0.02):
    risk_free_rate = float(risk_free_rate)
    stock_data = get_data(symbol, sd, ed, add_spy=True)
    stock_returns = stock_data[symbol].pct_change().dropna()
    benchmark_returns = stock_data['SPY'].pct_change().dropna()
    excess_returns = stock_returns - benchmark_returns

 
    downside_returns = excess_returns.copy()
    downside_returns[excess_returns > risk_free_rate] = 0
    downside_deviation = downside_returns.std()

    mean_excess_return = excess_returns.mean()

    sortino_ratio = mean_excess_return / downside_deviation

    return sortino_ratio

def correlation(symbol_1, symbol_2, sd, ed, cache = Optional[dict]):
    # if symbol_1 not in cache:
    #     stock_data_1 = get_data(symbol_1, sd, ed)
    #     returns_1 = stock_data_1[symbol_1].pct_change()
    #     cache[symbol_1] = returns_1
    # else:
    #     returns_1 = cache[symbol_1]
    # if symbol_2 not in cache:
    #     stock_data_2 = get_data(symbol_2, sd, ed)
    #     returns_2 = stock_data_2[symbol_2].pct_change()
    #     cache[symbol_2] = returns_2
    # else:
    #     returns_2 = cache[symbol_2]
    
    # return returns_1.corr(returns_2)
    
    stock_data_1 = get_data(symbol_1, sd, ed)
    returns_1 = stock_data_1[symbol_1].pct_change()
    stock_data_2 = get_data(symbol_2, sd, ed)
    returns_2 = stock_data_2[symbol_2].pct_change()

    return returns_1.corr(returns_2)

# Example Use Cases
b = beta('IBM', "2009-01-01", "2010-01-01")
ja = jensen_alpha('IBM', "2008-01-01", "2009-01-01")
tr = treynor_ratio('IBM', "2008-01-01", "2009-01-01")
ir = information_ratio('IBM', "2008-01-01", "2009-01-01")
sr = sortino_ratio('IBM', "2008-01-01", "2009-01-01")
cor = correlation('IBM', 'JPM', "2009-01-01", "2010-01-01")

