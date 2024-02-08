from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from metrics import correlation, beta, jensen_alpha, treynor_ratio, information_ratio, sortino_ratio
from indicators import bollinger_bands, simple_moving_average, exponential_moving_average, relative_strength_index
import sqlite3
from portfolio_metrics import all_portfolio_metrics, cumulative_return, sharpe_ratio, avg_daily_return, std_daily_return
import re

app = Flask(__name__)
CORS(app)

# Function to parse the file and create a mapping of tickers to their top and bottom correlations
def parse_correlation_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    correlations = {}
    current_ticker = ""
    for line in lines:
        # Check if the line contains a stock ticker
        if line.startswith("'"):
            current_ticker = line.strip().strip("'")
            correlations[current_ticker] = {'top': [], 'bottom': []}
        else:
            # Extract the correlations
            matches = re.findall(r'\(([^,]+), ([^)]+)\)', line)
            if 'Top' in line:
                correlations[current_ticker]['top'] = matches[:5]  # Top 5
            elif 'Bottom' in line:
                correlations[current_ticker]['bottom'] = matches[:5]  # Bottom 5

    return correlations

stocks_folder_path = "dataset/stocks"
sqlite_db_path = "data_viz_db.sqlite"
conn = sqlite3.connect(sqlite_db_path, check_same_thread=False)
cursor = conn.cursor()
file_path = 'correlations_per_stock.txt'
correlation_data = parse_correlation_file(file_path)

@app.route('/get_data')
# Get 100 days of data for a specific stock
def get_data():
    query = f"""
    SELECT * FROM stock_data
    WHERE Ticker = '{request.args.get('ticker')}' AND Date >= Date('2020-04-01', '-100 days') AND Date <= '2020-04-01'
    ORDER BY Date DESC;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    return jsonify(results)

@app.route('/correlation_info')
def correlation_info():
    stock1 = request.args.get('stock1')
    stock2 = request.args.get('stock2')
    sd = request.args.get('sd')
    ed = request.args.get('ed')
    corr = correlation(stock1, stock2, sd, ed)
    corr = {'correlation': corr}
    return jsonify(corr)

@app.route('/beta_info')
def beta_info():
    stock1 = request.args.get('stock1')
    sd = request.args.get('sd')
    ed = request.args.get('ed')
    res = beta(stock1, sd, ed)
    res = {'beta': res}
    return jsonify(res)

@app.route('/information_ratio')
def information_ratio_info():
    stock1 = request.args.get('stock1')
    sd = request.args.get('sd')
    ed = request.args.get('ed')
    res = information_ratio(stock1, sd, ed)
    res = {'information_ratio': res}
    return jsonify(res)

@app.route('/jensen_alpha')
def jensen_alpha_info():
    stock1 = request.args.get('stock1')
    sd = request.args.get('sd')
    ed = request.args.get('ed')
    rfr = request.args.get('rfr')
    res = jensen_alpha(stock1, sd, ed, rfr)
    res = {'jensen_alpha': res}
    return jsonify(res)

@app.route('/treynor_ratio')
def treynor_ratio_info():
    stock1 = request.args.get('stock1')
    sd = request.args.get('sd')
    ed = request.args.get('ed')
    rfr = request.args.get('rfr')
    res = treynor_ratio(stock1, sd, ed, rfr)
    res = {'treynor_ratio': res}
    return jsonify(res)

@app.route('/sortino_ratio')
def sortino_ratio_info():
    stock1 = request.args.get('stock1')
    sd = request.args.get('sd')
    ed = request.args.get('ed')
    rfr = request.args.get('rfr')
    res = sortino_ratio(stock1, sd, ed, rfr)
    res = {'sortino_ratio': res}
    return jsonify(res)

@app.route('/bollinger_bands')
def bb_info():
    stock1 = request.args.get('stock1')
    sd = request.args.get('sd')
    ed = request.args.get('ed')
    window = request.args.get('window')
    num_std = request.args.get('num_std')
    bb = bollinger_bands(stock1, sd, ed, window, num_std)
    return jsonify(bb.to_dict())

@app.route('/sma')
def sma_info():
    stock1 = request.args.get('stock1')
    sd = request.args.get('sd')
    ed = request.args.get('ed')
    window = request.args.get('window')
    sma = simple_moving_average(stock1, sd, ed, window)
    sma = {'sma': sma.to_json()}
    return jsonify(sma)

@app.route('/ema')
def ema_info():
    stock1 = request.args.get('stock1')
    sd = request.args.get('sd')
    ed = request.args.get('ed')
    window = request.args.get('window')
    ema = exponential_moving_average(stock1, sd, ed, window)
    ema = {'ema': ema.to_json()}
    return jsonify(ema)

@app.route('/rsi')
def rsi_info():
    stock1 = request.args.get('stock1')
    sd = request.args.get('sd')
    ed = request.args.get('ed')
    window = request.args.get('window')
    rsi = relative_strength_index(stock1, sd, ed, window)
    rsi = {'rsi': rsi.to_json()}
    return jsonify(rsi)

@app.route('/portfolio_metrics')
def portfolio_metrics():
    # Get parameters from request args
    stocks = request.args.getlist('stocks')
    allocations = list(map(float, request.args.getlist('allocations')))
    sd = request.args.get('sd')
    ed = request.args.get('ed')
    
    # Call all_portfolio_metrics function
    metrics = all_portfolio_metrics(stocks, allocations, sd, ed)
    
    # Convert metrics to JSON
    metrics_json = {
        'cum_return': metrics['cum_return'],
        'avg_daily_return': metrics['avg_daily_return'],
        'std_daily_return': metrics['std_daily_return'],
        'sharpe_ratio': metrics['sharpe_ratio']
    }
    
    return jsonify(metrics_json)

@app.route('/cumulative_return')
def get_cumulative_return():
    # Get parameters from request args
    stocks = request.args.getlist('stocks')
    allocations = list(map(float, request.args.getlist('allocations')))
    sd = request.args.get('sd')
    ed = request.args.get('ed')
    
    # Call cumulative_return function
    result = cumulative_return(stocks, allocations, sd, ed)
    
    return jsonify({'cumulative_return': result})

@app.route('/avg_daily_return')
def get_avg_daily_return():
    # Get parameters from request args
    stocks = request.args.getlist('stocks')
    allocations = list(map(float, request.args.getlist('allocations')))
    sd = request.args.get('sd')
    ed = request.args.get('ed')
    
    # Call avg_daily_return function
    result = avg_daily_return(stocks, allocations, sd, ed)
    
    return jsonify({'avg_daily_return': result})

@app.route('/std_daily_return')
def get_std_daily_return():
    # Get parameters from request args
    stocks = request.args.getlist('stocks')
    allocations = list(map(float, request.args.getlist('allocations')))
    sd = request.args.get('sd')
    ed = request.args.get('ed')
    
    # Call std_daily_return function
    result = std_daily_return(stocks, allocations, sd, ed)
    
    return jsonify({'std_daily_return': result})

@app.route('/sharpe_ratio')
def get_sharpe_ratio():
    # Get parameters from request args
    stocks = request.args.getlist('stocks')
    allocations = list(map(float, request.args.getlist('allocations')))
    sd = request.args.get('sd')
    ed = request.args.get('ed')
    
    # Call sharpe_ratio function
    result = sharpe_ratio(stocks, allocations, sd, ed)
    
    return jsonify({'sharpe_ratio': result})

@app.route('/correlated_stocks')
def correlated_stocks():
    ticker = request.args.get('ticker')
    if ticker not in correlation_data:
        return jsonify({'error': 'Ticker not found'}), 404

    top_correlations = correlation_data[ticker]['top']
    bottom_correlations = correlation_data[ticker]['bottom']

    result = {
        'ticker': ticker,
        'top_correlated_stocks': top_correlations,
        'bottom_correlated_stocks': bottom_correlations
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
    conn.close()
