"""
A Website created using Flask and prompt user to enter a stock ticker, his/her estimated
earnings growth rate, capex growth rate, and terminal growth rate and
return the corresponding DCF valuation (enterprise value, equity value, and per share value),
displays the corresponding cash flows in a table and a line chart.

The DCF.html has red underlines from VScode highlighting a potential error.
The error is from the highlight extensions in VScode and thus does not interfere with the code itself.
The code is correct and thus the errors highlighted can be ignored.
"""

from flask import Flask, request, render_template
import pandas as pd
from DCF import DCF
import json
import plotly
import plotly.express as px


app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def DCF_app():
    if request.method == 'POST':
        try:
            ticker = request.form['ticker_name']
            earnings_growthrate = request.form['earnings']
            capex_growthrate = request.form['capex']
            terminal_growthrate = request.form['terminal']
            result = DCF(ticker, earnings_growthrate, capex_growthrate, terminal_growthrate)
            date = result['date']
            enterprise_value = result['enterprise_value']
            equity_value = result['equity_value']
            share_price = result['share_price']
            data = pd.read_csv(ticker + '.csv')
            fig = px.line(data, x='Year', y=['DFCF', 'EBIT', 'D&A', 'CWC', 'CAPEX'], title='Cash Flow Valuation in USD vs. Year')
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('DCF.html', ticker_name = ticker, date = date, enterprise_value = enterprise_value, equity_value = equity_value, share_price = share_price, tables=[data.to_html()], titles=[''], graphJSON=graphJSON)
        except Exception:
            return render_template('error.html') 
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)