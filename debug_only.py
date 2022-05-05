"""
This python file is created for the sole purpose of debugging individual functions
and make neccessary changes and test them so that functions in other files are not affected.
Please do not grade functions in this file as a part of the overall grade.
"""


# import requests
# import pandas_datareader as web
# from pprint import pprint
# import datetime
# from decimal import Decimal

# from get_data import API_KEY, get_json, get_EV
# from WACC import wacc_func
# from get_data import get_earnings_growth, get_capex_growth, get_terminal_growth
# from DCF_old import FCFE

# def interest_coverage_ratio_func(ticker):
#     """
#     this function takes the stock ticker as a parameter and returns the interest coverage ratio
#     """
#     income_statement = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{ticker}?apikey={API_KEY}').json()
#     year1 = income_statement[0]
#     ebit = year1['operatingIncome']
#     interest_expense = year1['interestExpense']
#     interest_coverage_ratio = float(ebit / interest_expense)

#     return interest_coverage_ratio
#     # print(type(income_statement))
#     # pprint(income_statement)
#     # pprint(interest_expense)

# # interest_coverage_ratio_func('AAPL')   # for testing




# def cost_of_equity(ticker):
#     """
#     this function takes the ticker as a parameter, and returns the cost of equity of the company
#     """
#     url = f'https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={API_KEY}'
#     data = get_json(url)
#     beta = data[0]['beta']
#     # start = datetime.datetime(2021, 4, 21)
#     # end = datetime.datetime.today().strftime('%Y-%m-%d')
#     # sp500 = web.DataReader(['sp500'], 'fred', start, end)
#     # sp500.dropna(inplace = True)
#     # sp500_return = (sp500['sp500'].iloc[-1] / sp500['sp500'].iloc[-252]) - 1
#     # Rf = risk_free()
#     # ke = Rf + (beta * (sp500_return - Rf))
#     # return ke
#     return beta

# pprint(cost_of_equity('AAPL'))



# def enterprise_value_func(ticker, period):
#     """
#     This function takes ticker, ev_statement, income_statement, balance_sheet, cashflow_statement, discount_rate, forecast, earnings_growthrate, capex_growthrate, terminal_growthrate
#     as parameters, returns the enterprise value of the firm.
#     """
#     balance_sheet = requests.get(f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?apikey={API_KEY}').json()
#     income_statement = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{ticker}?apikey={API_KEY}').json()
#     cashflow_statement = requests.get(f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}?apikey={API_KEY}').json()

#     ebit = income_statement[0]['operatingIncome']
#     tax_rate = float(income_statement[0]['incomeTaxExpense']) / float(income_statement[0]['incomeBeforeTax'])
#     depre_amorti = float(cashflow_statement[0]['depreciationAndAmortization'])
#     cwc = float(balance_sheet[0]['totalCurrentAssets']) - float(balance_sheet[0]['totalCurrentLiabilities'])
#     capex = float(cashflow_statement[0]['capitalExpenditure'])
#     discount_rate = wacc_func(ticker)

#     cash_flow_lst = []

#     earnings_growthrate = get_earnings_growth()
#     capex_growthrate = get_capex_growth()
#     terminal_growthrate = get_terminal_growth()

#     print('Forecasting flows for {} years out, starting at {}.'.format(period, income_statement[0]['date']),    
#          ('\n         FCFE   |    EBIT   |    D&A    |    CWC     |   CAP_EX   | '))

#     for year in range(1, period + 1):
#         ebit = ebit * (1 + (year * earnings_growthrate))
#         depre_amorti = depre_amorti * (1 + (year * earnings_growthrate))
#         cwc = cwc * 0.2  ### what to evaluate?
#         capex = capex * (1 + (year * capex_growthrate))

#         cash_flow = FCFE(ebit, tax_rate, depre_amorti, cwc, capex)
#         PV_cashflow = cash_flow / ((1 + discount_rate) ** year)
#         cash_flow_lst.append(PV_cashflow)

#         print(str(int(income_statement[0]['date'][0:4]) + year) + '  ',
#               '%.2E' % Decimal(PV_cashflow) + ' | ',
#               '%.2E' % Decimal(ebit) + ' | ',
#               '%.2E' % Decimal(depre_amorti) + ' | ',
#               '%.2E' % Decimal(cwc) + ' | ',
#               '%.2E' % Decimal(capex) + ' | ')

#     NPV_FCFE = sum(cash_flow_lst)

#     terminal_cashflow = cash_flow_lst[-1] * (1 + terminal_growthrate)
#     terminal_value = terminal_cashflow / (discount_rate - terminal_growthrate)
#     NPV_terminal = terminal_value / (1 + discount_rate) ** (1 + period)

#     pprint(income_statement[0]['operatingIncome'])
#     print(len(income_statement))
#     return NPV_FCFE + NPV_terminal
#     # print(NPV_FCFE + NPV_terminal)
#     # print(NPV_FCFE)
#     # print(terminal_cashflow)
#     # print(terminal_value)
#     # print(NPV_terminal)
#     # print(discount_rate)
#     # print(cash_flow_lst)

#     # number is 1 digit bigger

# # enterprise_value_func('AAPL', 5)

# def equity_value_func(ticker):
#     """
#     this function takes the enterprice_value and ev_statement as parameters and return the equity value of the selected firm
#     """
#     ev_statement = get_EV(ticker = ticker, apikey= API_KEY)
#     equity_value = float(enterprise_value_func(ticker, period=5)) - ev_statement.get('enterpriseValues')[0]['+ Total Debt'] + ev_statement.get('enterpriseValues')[0]['- Cash & Cash Equivalents']
#     share_price = equity_value / float(ev_statement.get('enterpriseValues')[0]['Number of Shares'])

#     # pprint(ev_statement)
#     print(equity_value, share_price)

# # equity_value('AAPL')