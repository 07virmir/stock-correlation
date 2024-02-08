#test script to verify the flask_server endpoints are working
import requests

url = 'http://127.0.0.1:5000/get_data'
args = {'ticker': 'AAPL'}
r = requests.get(url, params=args).json()
print(r)

url = 'http://127.0.0.1:5000/correlation_info'
args = {'stock1': 'AAPL', 'stock2': 'MSFT', 'sd': '2019-01-01', 'ed': '2019-12-31'}
r = requests.get(url, params=args).json()
print(r)

url = 'http://127.0.0.1:5000/beta_info'
args = {'stock1': 'AAPL', 'sd': '2019-01-01', 'ed': '2019-12-31'}
r = requests.get(url, params=args).json()
print(r)

url = 'http://127.0.0.1:5000/information_ratio'
args = {'stock1': 'AAPL', 'sd': '2019-01-01', 'ed': '2019-12-31'}
r = requests.get(url, params=args).json()
print(r)

url = 'http://127.0.0.1:5000/jensen_alpha'
args = {'stock1': 'AAPL', 'sd': '2019-01-01', 'ed': '2019-12-31', 'rfr': 0.02}
r = requests.get(url, params=args).json()
print(r)

url = 'http://127.0.0.1:5000/treynor_ratio'
args = {'stock1': 'AAPL', 'sd': '2019-01-01', 'ed': '2019-12-31', 'rfr': 0.02}
r = requests.get(url, params=args).json()
print(r)

url = 'http://127.0.0.1:5000/sortino_ratio'
args = {'stock1': 'AAPL', 'sd': '2019-01-01', 'ed': '2019-12-31', 'rfr': 0.02}
r = requests.get(url, params=args).json()
print(r)

url = 'http://127.0.0.1:5000/bollinger_bands'
args = {'stock1': 'AAPL', 'sd': '2019-01-01', 'ed': '2019-12-31', 'window': 20, 'num_std': 2}
r = requests.get(url, params=args).json()
print(r)

url = 'http://127.0.0.1:5000/sma'
args = {'stock1': 'AAPL', 'sd': '2019-01-01', 'ed': '2019-12-31', 'window': 20}
r = requests.get(url, params=args).json()
print(r)

url = 'http://127.0.0.1:5000/ema'
args = {'stock1': 'AAPL', 'sd': '2019-01-01', 'ed': '2019-12-31', 'window': 20}
r = requests.get(url, params=args).json()
print(r)

url = 'http://127.0.0.1:5000/rsi'
args = {'stock1': 'AAPL', 'sd': '2019-01-01', 'ed': '2019-12-31', 'window': 20}
r = requests.get(url, params=args).json()
print(r)

url = 'http://127.0.0.1:5000/correlated_stocks'
args = {'ticker': 'AAPL'}
r = requests.get(url, params=args).json()
print(r)