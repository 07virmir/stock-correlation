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
    tickers = get_tickers(db_path)
    ticker_correlations = defaultdict(lambda: {'top': [], 'bottom': []})
    cache = {}

    for ticker1 in tickers:
        correlations = []
        for ticker2 in tickers:
            if ticker1 != ticker2:
                corr_value = correlation(ticker1, ticker2, start_date, end_date, cache)
                correlations.append((ticker2, corr_value))

        # Sort by correlation value
        sorted_correlations = sorted(correlations, key=lambda x: x[1])

        # Get the top 10 and bottom 10 for each ticker
        ticker_correlations[ticker1]['top'] = sorted_correlations[-10:]
        ticker_correlations[ticker1]['bottom'] = sorted_correlations[:10]

    return ticker_correlations


def write_to_file(data, file_path):
    with open(file_path, 'w') as file:
        for ticker, correlations in data.items():
            # Write the ticker
            file.write(f"'{ticker}'\n")

            # Format and write the top 10 correlations
            top_10 = ', '.join([f"({corr[0]}, {corr[1]:.4f})" for corr in correlations['top']])
            file.write(f"Top 10 Correlations: {top_10}\n")

            # Format and write the bottom 10 correlations
            bottom_10 = ', '.join([f"({corr[0]}, {corr[1]:.4f})" for corr in correlations['bottom']])
            file.write(f"Bottom 10 Correlations: {bottom_10}\n\n")


# Example usage
db_path = 'data_viz_db.sqlite'
start_date = '2019-12-23'
end_date = '2020-04-01'
file_path = 'correlations_per_stock.txt'

ticker_correlations = calculate_correlations(db_path, start_date, end_date)
write_to_file(ticker_correlations, file_path)
