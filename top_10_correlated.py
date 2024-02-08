import sqlite3
import itertools
import pandas as pd
from metrics import correlation
from collections import defaultdict

def get_tickers(db_path):
    """Retrieve a list of unique tickers from the SQLite database."""
    conn = sqlite3.connect(db_path)
    query = "SELECT DISTINCT Ticker FROM stock_data"  # Adjust the query based on your table structure
    tickers = pd.read_sql_query(query, conn)
    conn.close()
    return tickers['Ticker'].tolist()

def calculate_correlations(db_path, start_date, end_date):
    """Calculate correlations between all pairs of stocks and return the top 10 and bottom 10."""
    tickers = get_tickers(db_path)
    pairs = itertools.combinations(tickers, 2)

    correlations = []
    prev = defaultdict(list)
    cache = {}

    for ticker1, ticker2 in pairs:
        if ticker2 in prev[ticker1]:
            continue
        corr_value = correlation(ticker1, ticker2, start_date, end_date, cache)
        correlations.append((ticker1, ticker2, corr_value))
        prev[ticker1].append(ticker2)
        prev[ticker2].append(ticker1)

    # Sort by correlation value
    sorted_correlations = sorted(correlations, key=lambda x: x[2])

    # Get the top 10 and bottom 10
    top_correlations = sorted_correlations[-10:]
    bottom_correlations = sorted_correlations[:10]

    return top_correlations, bottom_correlations

def write_to_file(data, file_path):
    """Write the data to a text file."""
    with open(file_path, 'w') as file:
        for row in data:
            file.write(f"{row[0]}, {row[1]}, {row[2]}\n")

# Example usage
db_path = 'data_viz_db.sqlite'
start_date = '2019-12-23'
end_date = '2020-04-01'
file_path_top = 'top_correlations.txt'
file_path_bottom = 'bottom_correlations.txt'

top_correlations, bottom_correlations = calculate_correlations(db_path, start_date, end_date)
write_to_file(top_correlations, file_path_top)
write_to_file(bottom_correlations, file_path_bottom)
