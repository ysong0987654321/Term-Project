"""
This python file is to get financials data from financialmodelingprep.com with their API.
This file was the first one to be created. 
But in the end, functions in this file were largely unused because the server does not
allow for my requests to access data using functions in this file (httperror: 429)
and therefore, urls needed to be built into the specific functions, instead of the intended use here.
"""

# import necessary packages
import urllib.request
import json
from pprint import pprint


# API Keys
API_KEY = '3de996f877c8cf825ebcb3ce8178db04'


# Base URL from FinancialModelingPrep
FMP_base_url = 'https://financialmodelingprep.com/api/v3/'


def get_url(request_data, ticker, apikey):
    """
    this function takes in three parameters: the kind of data requested, stock ticker, and the apikey to financialmodelingprep.com and return the corresponding url
    """
    url = FMP_base_url + f'{request_data}/{ticker}?apikey={apikey}'.format(request_data = request_data, ticker = ticker, apikey = apikey)
    return url


# get json data from the base url
def get_json(url):
    """
    this function takes a parameter url and get the json data
    """
    f = urllib.request.urlopen(url)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)
    return response_data
    # pprint(response_data)   # for testing


# get income statement using url
def get_income_statement(ticker, apikey):
    """
    this function takes the stock ticker and the apikey as parameters, return the income statement for the selected company
    """
    url = get_url('income-statement', ticker = ticker, apikey = apikey)
    return get_json(url)


# get balance sheet using url
def get_balance_sheet(ticker, apikey):
    """
    this function takes the stock ticker and the apikey as parameters, return the balance sheet for the selected company
    """
    url = get_url('balance-sheet-statement', ticker = ticker, apikey = apikey)
    return get_json(url)


# get cash flow statement using url
def get_cash_flow_statement(ticker, apikey):
    """
    this function takes the stock ticker and the apikey as parameters, return the cash flow statement for the selected company
    """
    url = get_url('cash-flow-statement', ticker = ticker, apikey = apikey)
    return get_json(url)


# get stock price using url
def get_stock_price(ticker, apikey):
    """
    this function takes the stock ticker and the apikey as parameters, return the stock price for the selected company
    """
    url = get_url('stock/real-time-price', ticker = ticker, apikey = apikey)
    return get_json(url)


# get enterprise value statement using url
def get_EV(ticker, apikey):
    """
    this function takes the stock ticker and the apikey as parameters, return the stock shares outstanding information for the selected company
    """
    url = get_url('enterprise-value', ticker = ticker, apikey = apikey)
    return get_json(url)


def get_earnings_growth():
    """
    this function prompts the user to input a earnings growth rate and returns the corresponding rate as a float
    """
    earnings_growth = float(input('Please enter a earnings growth rate: '))
    return earnings_growth


def get_capex_growth():
    """
    this function prompts the user to input a capex growth rate and returns the corresponding rate as a float
    """
    capex_growth = float(input('Please enter a capex growth rate: '))
    return capex_growth


def get_terminal_growth():
    """
    this function prompts the user to input a terminal growth rate and returns the corresponding rate as a float
    """
    terminal_growth = float(input('Please enter a terminal growth rate: '))
    return terminal_growth


def main():
    """
    test all functions
    """
    # pprint(get_income_statement('AAPL', API_KEY))  # for testing
    # pprint(get_balance_sheet('AAPL', API_KEY))  # for testing
    # pprint(get_cash_flow_statement('AAPL', API_KEY))  # for testing
    # pprint(get_stock_price('AAPL', API_KEY))  # for testing
    # pprint(get_EV('AAPL', API_KEY))  # for testing
    # get_earnings_growth()  # for testing
    # get_capex_growth()  # for testing
    # get_terminal_growth()  # for testing

if __name__ == '__main__':
    main()