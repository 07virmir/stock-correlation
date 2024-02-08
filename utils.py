import os
import pandas as pd
import sqlite3

def read_stock_data_db(symbol, sd, ed, column = 'Adj_Close'):
    conn = sqlite3.connect('data_viz_db.sqlite')
    query = f"SELECT Date, {column} FROM stock_data WHERE Ticker = '{symbol}' AND Date BETWEEN '{sd}' AND '{ed}';"
    df = pd.read_sql_query(query, conn)
    df.set_index('Date', inplace=True)
    df.rename(columns={column: symbol}, inplace=True)
    conn.close()
    return df

def get_data(symbol, sd, ed, add_spy=False, colname="Adj_Close"):
    df = read_stock_data_db(symbol, sd, ed)

    if add_spy:
        spy = read_stock_data_db('SPY', sd, ed)
        df = df.join(spy)
        
    return df
