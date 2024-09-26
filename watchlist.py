# watchlist.py

import pandas as pd
import yfinance as yf

class Watchlist:
    def __init__(self):
        self.watchlist = pd.DataFrame()

    def add_contract(self, contract):
        if not self.watchlist.empty:
            if contract['contractSymbol'] in self.watchlist['contractSymbol'].values:
                # Contract already in watchlist
                return
        self.watchlist = self.watchlist.append(contract, ignore_index=True)

    def get_watchlist(self):
        return self.watchlist

    def update_prices(self):
        # Fetch the latest prices for contracts in the watchlist
        updated_watchlist = []
        for idx, contract in self.watchlist.iterrows():
            try:
                option = yf.Ticker(contract['contractSymbol'])
                data = option.history(period='1d')
                if not data.empty:
                    last_price = data['Close'].iloc[-1]
                    percent_change = ((last_price - contract['ask']) / contract['ask']) * 100
                    contract['lastPrice'] = last_price
                    contract['percentChange'] = percent_change
                    updated_watchlist.append(contract)
            except Exception:
                continue
        self.watchlist = pd.DataFrame(updated_watchlist)
