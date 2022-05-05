"""
This python file is to create the necessary DCF valuation calculations.
This file performs the core back-end calculations.
"""

# import necessary packages
import requests
from decimal import Decimal
from WACC import wacc_func
import csv

from get_data import *


def DCF(ticker, earnings_growthrate, capex_growthrate, terminal_growthrate):
    """
    This function takes ticker, earnings_growthrate, capex_growthrate, terminal_growthrate
    as parameters, returns the DCF valuation as a dictionary with date, 
    enterprise_value, equity_value, share_price as keys, and their corresponding values as values.
    This is core function that takes almost all the following functions in its calculations.
    """
    equity_value, share_price = equity_value_func(ticker, earnings_growthrate, capex_growthrate, terminal_growthrate)
    income_statement = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{ticker}?apikey={API_KEY}').json()

    ev_statement = get_EV(ticker = ticker, apikey= API_KEY)
    enterprise_value = equity_value + ev_statement.get('enterpriseValues')[0]['+ Total Debt'] - ev_statement.get('enterpriseValues')[0]['- Cash & Cash Equivalents']
    
    # print('\nEnterprise Value for {}: ${}.'.format(ticker, '%.2E' % Decimal(str(enterprise_value))), 
    #           '\nEquity Value for {}: ${}.'.format(ticker, '%.2E' % Decimal(str(equity_value))),
    #        '\nPer share value for {}: ${}.\n'.format(ticker, '%.2E' % Decimal(str(share_price))),
    #         '-'*60)   # for testing in vscode terminal
            
    return{
        'date': income_statement[0]['date'],
        'enterprise_value': f'{enterprise_value:0.2f}',
        'equity_value': f'{equity_value:0.2f}',
        'share_price': f'{share_price:0.2f}'
        }


def FCFE(ebit, tax_rate, depre_amorti, cwc, capex):
    """
    this is a function takes ebit, tax_rate, deprec_amorti, cwc, and capex as parameters
    to derive the unlevered free cash flow to firm for forecasting
    """
    return ebit * (1-tax_rate) + depre_amorti + cwc + capex


def enterprise_value_func(ticker, earnings_growthrate, capex_growthrate, terminal_growthrate):
    """
    This function takes ticker, earnings_growthrate, capex_growthrate, terminal_growthrate
    as parameters, returns the enterprise value of the firm and 
    writes a ticker.csv file to record the generated cash flow information.
    Since this is a longer function, each section is separated using an empty line with subtitles
    """
    # procure necessary financials information
    balance_sheet = requests.get(f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?apikey={API_KEY}').json()
    income_statement = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{ticker}?apikey={API_KEY}').json()
    cashflow_statement = requests.get(f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}?apikey={API_KEY}').json()

    # perform necessary cash flow calculations
    ebit = income_statement[0]['operatingIncome']
    tax_rate = float(income_statement[0]['incomeTaxExpense']) / float(income_statement[0]['incomeBeforeTax'])
    depre_amorti = float(cashflow_statement[0]['depreciationAndAmortization'])
    cwc = float(balance_sheet[0]['totalCurrentAssets']) - float(balance_sheet[0]['totalCurrentLiabilities'])
    capex = float(cashflow_statement[0]['capitalExpenditure'])
    discount_rate = wacc_func(ticker)

    # generate empty lists to store cash flow values later
    cash_flow_lst = []
    write_dfcf = []
    write_ebit = []
    write_da = []
    write_cwc = []
    write_capex = []

    # for testing
    # print('Forecasting flows for {} years out, starting at {}.'.format(5, income_statement[0]['date']),    
        #  ('\n         DFCF   |    EBIT   |    D&A    |    CWC    |   CAPEX   | '))
        #   for testing in vscode terminal

    # generate cash flow projections using a for loop
    # append the results generated into the previously created empty lists
    for year in range(1, 6):
        ebit = ebit * (1 + (year * float(earnings_growthrate)))
        depre_amorti = depre_amorti * (1 + (year * float(earnings_growthrate)))
        cwc = cwc * 0.2
        capex = capex * (1 + (year * float(capex_growthrate)))

        cash_flow = FCFE(ebit, tax_rate, depre_amorti, cwc, capex)
        PV_cashflow = cash_flow / ((1 + discount_rate) ** year)
        cash_flow_lst.append(PV_cashflow)

        write_dfcf.append(f'{PV_cashflow:0.2f}')
        write_ebit.append(f'{ebit:0.2f}')
        write_da.append(f'{depre_amorti:0.2f}')
        write_cwc.append(f'{cwc:0.2f}')
        write_capex.append(f'{capex:0.2f}')

        # for testing
        # print(str(int(income_statement[0]['date'][0:4]) + year) + '  ',  # for testing in vscode terminal
        #       '%.2E' % Decimal(PV_cashflow) + ' | ',  # for testing in vscode terminal
        #       '%.2E' % Decimal(ebit) + ' | ',  # for testing in vscode terminal
        #       '%.2E' % Decimal(depre_amorti) + ' | ',  # for testing in vscode terminal
        #       '%.2E' % Decimal(cwc) + ' | ',  # for testing in vscode terminal
        #       '%.2E' % Decimal(capex) + ' | ')  # for testing in vscode terminal

    # Net Present Values calculations
    NPV_FCFE = sum(cash_flow_lst)

    # Terminal values calculations
    terminal_cashflow = cash_flow_lst[-1] * (1 + float(terminal_growthrate))
    terminal_value = terminal_cashflow / (discount_rate - float(terminal_growthrate))
    NPV_terminal = terminal_value / (1 + discount_rate) ** 6

    # generate the .csv file
    header = ['Year', 'DFCF', 'EBIT', 'D&A', 'CWC', 'CAPEX']
    date_lst = ['2022', '2023', '2024', '2025', '2026']
    data_dfcf = write_dfcf
    data_ebit = write_ebit
    data_da = write_da
    data_cwc = write_cwc
    data_capex = write_capex
    with open(ticker + '.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for w in range(5):
            writer.writerow([date_lst[w], data_dfcf[w], data_ebit[w], data_da[w], data_cwc[w], data_capex[w]])

    # ending enterprise value calculation using NPV of cash flow and terminal cash flow
    enterprise_value = NPV_FCFE + NPV_terminal
    return enterprise_value
    # print(NPV_FCFE + NPV_terminal)   # for testing
    # print(NPV_FCFE)   # for testing
    # print(terminal_cashflow)   # for testing
    # print(terminal_value)   # for testing
    # print(NPV_terminal)   # for testing
    # print(discount_rate)   # for testing
    # print(cash_flow_lst)   # for testing


def equity_value_func(ticker, earnings_growthrate, capex_growthrate, terminal_growthrate):
    """
    this function takes the ticker, earnings_growthrate, capex_growthrate, and terminal_growthrate
     as parameters and return the equity value of the selected firm
    """
    ev_statement = get_EV(ticker = ticker, apikey= API_KEY)   # from get_data.py
    equity_value = float(enterprise_value_func(ticker, earnings_growthrate, capex_growthrate, terminal_growthrate)) - ev_statement.get('enterpriseValues')[0]['+ Total Debt'] + ev_statement.get('enterpriseValues')[0]['- Cash & Cash Equivalents']
    share_price = equity_value / float(ev_statement.get('enterpriseValues')[0]['Number of Shares'])

    return equity_value, share_price
    # pprint(ev_statement)   # for testing


def main():
    """
    test all functions
    """
    return DCF('AAPL', 0.02, 0.01, 0.02)

    # enterprise_value('AAPL')
    # equity_value('AAPL')
    

if __name__ == '__main__':
    main()