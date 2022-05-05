"""
This python file is to calculate the weighted average cost of capital (WACC) for the selected company.
"""


# import necessary packages
import requests
import pandas_datareader as web
from pprint import pprint
import datetime

from get_data import API_KEY

def interest_coverage_ratio_func(ticker):
    """
    this function takes the stock ticker as a parameter and returns the interest coverage ratio
    """
    income_statement = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{ticker}?apikey={API_KEY}').json()
    ebit = income_statement[0]['operatingIncome']
    interest_expense = income_statement[0]['interestExpense']
    interest_coverage_ratio = float(ebit / interest_expense)

    return interest_coverage_ratio
    # print(type(income_statement))   # for testing
    # pprint(income_statement)   # for testing
    # pprint(interest_expense)   # for testing


def risk_free():
    """
    this function returns the risk free rate in the US stock market
    """
    start = datetime.datetime(2021, 4, 21)
    end = datetime.datetime.today().strftime('%Y-%m-%d')
    treasury = web.DataReader(['GS10'], 'fred', start, end)
    Rf = float(treasury.iloc[-1]) / 100    
    return Rf


def cost_of_debt(Rf, interest_coverage_ratio):
    """
    this function takes the risk free rate, and the interest coverage ratio as parameters, and return the cost of debt for the selected company.
    the credit rating is adapted based on: http://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ratings.htm
    """
    if interest_coverage_ratio > 12.5:
        credit_spread = 0.0067 #Rating is AAA
    elif interest_coverage_ratio > 9.5 & interest_coverage_ratio <= 12.5:
        credit_spread = 0.0082 # Rating is AA
    elif interest_coverage_ratio > 7.5 & interest_coverage_ratio <= 9.5:
        credit_spread = 0.0103 # Rating is A+
    elif interest_coverage_ratio > 6 & interest_coverage_ratio <= 7.5:
        credit_spread = 0.0114 # Rating is A
    elif interest_coverage_ratio > 4.5 & interest_coverage_ratio <= 6:
        credit_spread = 0.0129 # Rating is A-
    elif interest_coverage_ratio > 4 & interest_coverage_ratio <= 4.5:
        credit_spread = 0.0159 # Rating is BBB
    elif interest_coverage_ratio > 3.5 & interest_coverage_ratio <= 4:
        credit_spread = 0.0193 # Rating is BB+
    elif interest_coverage_ratio > 3 & interest_coverage_ratio <= 3.5:
        credit_spread = 0.0215 # Rating is BB
    elif interest_coverage_ratio > 2.5 & interest_coverage_ratio <= 3:
        credit_spread = 0.0315 # Rating is B+
    elif interest_coverage_ratio > 2 & interest_coverage_ratio <= 2.5:
        credit_spread = 0.0378 # Rating is B
    elif interest_coverage_ratio > 1.5 & interest_coverage_ratio <= 2:
        credit_spread = 0.0462 # Rating is B-
    elif interest_coverage_ratio > 1.25 & interest_coverage_ratio <= 1.5:
        credit_spread = 0.0778 # Rating is CCC
    elif interest_coverage_ratio > 0.8 & interest_coverage_ratio <= 1.25:
        credit_spread = 0.088 # Rating is CC
    elif interest_coverage_ratio > 0.5 & interest_coverage_ratio <= 0.8:
        credit_spread = 0.1076 # Rating is C
    else:
        credit_spread = 0.1434 # Rating is D

    cost_of_debt = Rf + credit_spread
    return cost_of_debt


def cost_of_equity(ticker):
    """
    this function takes the ticker as a parameter, and returns the cost of equity of the company
    """
    data = requests.get(f'https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={API_KEY}').json()
    beta = data[0]['beta']
    start = datetime.datetime(2021, 4, 21)
    end = datetime.datetime.today().strftime('%Y-%m-%d')
    sp500 = web.DataReader(['sp500'], 'fred', start, end)
    sp500.dropna(inplace = True)
    sp500_return = (sp500['sp500'].iloc[-1] / sp500['sp500'].iloc[-252]) - 1
    Rf = risk_free()
    ke = Rf + (beta * (sp500_return - Rf)) + 0.1   # wacc adjustment
    return ke
    

def wacc_func(ticker):
    """
    this function takes the ticker as a parameter and return the weighted average cost of capital 
    by using the cost of debt function and cost of equity function
    """
    data = requests.get(f'https://financialmodelingprep.com/api/v3/ratios/{ticker}?apikey={API_KEY}').json()
    etr = data[0]['effectiveTaxRate']

    balance_sheet = requests.get(f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?apikey={API_KEY}').json()
    debt = balance_sheet[0]['totalDebt'] / (balance_sheet[0]['totalDebt'] + balance_sheet[0]['totalStockholdersEquity'])
    equity = balance_sheet[0]['totalStockholdersEquity'] / (balance_sheet[0]['totalDebt'] + balance_sheet[0]['totalStockholdersEquity'])

    kd = cost_of_debt(risk_free(), interest_coverage_ratio_func('AAPL'))
    ke = cost_of_equity(ticker)
    wacc = (kd * (1 - etr) * debt) + (ke * equity)
    return wacc


def main():
    """
    test all functions
    """
    Rf = risk_free()
    interest_coverage_ratio = interest_coverage_ratio_func('AAPL')
    ke = cost_of_equity('AAPL')
    kd = cost_of_debt(risk_free(), interest_coverage_ratio_func('AAPL'))
    print(Rf, interest_coverage_ratio, ke, kd)
    wacc = wacc_func('AAPL')
    print('wacc is ' + str((f'{wacc*100:0.2f}')) + '%')


if __name__ == '__main__':
    main()


# does not use get_json() because of httperror: 429 -- too many web request