import requests
import json
data_dict = {}

def get_correlation(stock1, stock2, sd = "2019-12-22", ed = "2020-04-01"):
    url = "http://127.0.0.1:5000/correlation_info"
    params = {
        "stock1": stock1,
        "stock2": stock2,
        "sd": sd,
        "ed": ed
    }

    # Make the request to the localhost server
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the response data
        response = response.json()
        # print(response)
    else:
        print("Error making request:", response)
    
    return response["correlation"]


def get_top_ten(ticker):
    url = "http://127.0.0.1:5000/correlated_stocks"
    params = {
        "ticker": ticker
    }

    # Make the request to the localhost server
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the response data
        response = response.json()
    else:
        print("Error making request:", response)

    
    data_dict[ticker] = {}
    data_dict[ticker]["correlations"] = {}

    for tick, corr in response["bottom_correlated_stocks"]:
        data_dict[tick] = {}
        data_dict[tick]["correlations"] = {}
    for tick, corr in response["top_correlated_stocks"]:
        data_dict[tick] = {}
        data_dict[tick]["correlations"] = {}

    # print(data_dict)


def get_portfolio_metrics(ticker, sd = "2019-12-22", ed = "2020-04-01"):
    url = "http://127.0.0.1:5000/portfolio_metrics"
    params = {
        "stocks": [ticker],
        "sd": sd,
        "ed": ed,
        "allocations": [1]
    }

    # Make the request to the localhost server
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the response data
        response = response.json()
        print(response)
    else:
        print("Error making request:", response)

    data_dict[ticker]["portfolio_metrics"] = response
    # print(data_dict)


def get_advanced_metrics(ticker, sd = "2019-12-22", ed = "2020-04-01", rfr = "0.02"):
    url = "http://127.0.0.1:5000/jensen_alpha"
    params = {
        "stock1": ticker,
        "sd": sd ,
        "ed": ed,
        "rfr": "0.02"
    }

    # Make the request to the localhost server
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the response data
        response = response.json()
    else:
        print("Error making request:", response)

    data_dict[ticker]["jensen_alpha"] = response['jensen_alpha']

    url = "http://127.0.0.1:5000/information_ratio"
    params = {
        "stock1": ticker,
        "sd": sd ,
        "ed": ed,
        "rfr": "0.02"
    }

    # Make the request to the localhost server
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the response data
        response = response.json()
    else:
        print("Error making request:", response)

    data_dict[ticker]["information_ratio"] = response['information_ratio']

    url = "http://127.0.0.1:5000/treynor_ratio"
    params = {
        "stock1": ticker,
        "sd": sd ,
        "ed": ed,
        "rfr": "0.02"
    }

    # Make the request to the localhost server
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the response data
        response = response.json()
    else:
        print("Error making request:", response)

    data_dict[ticker]["treynor_ratio"] = response['treynor_ratio']

def get_pairwise_correlations():
    tickers = list(data_dict.keys())
    print(tickers)
    for i in range(len(tickers)):
        for j in range(i + 1, len(tickers)):
            corr = get_correlation(tickers[i], tickers[j])
            print(corr)
            data_dict[tickers[i]]["correlations"][tickers[j]] = corr
            data_dict[tickers[j]]["correlations"][tickers[i]] = corr
            
    # print(data_dict)

    
def write_to_JSON(name):
    file_path = name+"-correlations.json"

    # Use the json.dump() function to write the dictionary to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(data_dict, json_file)

def populate_metrics():
    tickers = list(data_dict.keys())
    for tick in tickers:
        get_portfolio_metrics(tick)
        # get_pairwise_correlations()
        get_advanced_metrics(tick)



if __name__ == "__main__":
    tlist = ["PFE", "UNH", "COST"]
    for ticker in tlist:
        get_top_ten(ticker)
        # get_portfolio_metrics(ticker)
        get_pairwise_correlations()
        # get_advanced_metrics(ticker)
        populate_metrics()
        print(data_dict)
        write_to_JSON(ticker)
        data_dict = {}
