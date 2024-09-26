# data_fetching.py

import yfinance as yf
import pandas as pd

def get_expiration_dates(ticker):
    stock = yf.Ticker(ticker)
    return stock.options

def fetch_options_data(ticker, expirations):
    stock = yf.Ticker(ticker)
    all_data = []

    for expiration_date in expirations:
        try:
            options = stock.option_chain(expiration_date)
            calls = options.calls
            puts = options.puts

            calls['optionType'] = 'call'
            puts['optionType'] = 'put'

            calls['expirationDate'] = expiration_date
            puts['expirationDate'] = expiration_date

            calls['ticker'] = ticker
            puts['ticker'] = ticker

            all_data.append(calls)
            all_data.append(puts)
        except Exception:
            continue

    if all_data:
        return pd.concat(all_data, ignore_index=True)
    else:
        return pd.DataFrame()
