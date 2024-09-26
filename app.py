# app.py

import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
from data_fetching import get_expiration_dates, fetch_options_data
from data_processing import filter_expiration_dates, process_options_data
from watchlist import Watchlist

app = dash.Dash(__name__)
server = app.server  # For deployment

# Replace with your list of tickers
tickers = ['MMM', 'ABT', 'ABBV', 'ABMD', 'ACN', 'ATVI', 'ADBE', 'AMD', 'AAP', 'AES', 'AFL', 'A', 'APD', 'AKAM', 'ALK', 'ALB', 'ARE', 'ALXN', 'ALGN', 'ALLE', 'AGN', 'ADS', 'LNT', 'ALL', 'GOOGL', 'GOOG', 'MO', 'AMZN', 'AMCR', 'AEE', 'AAL', 'AEP', 'AXP', 'AIG', 'AMT', 'AWK', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'ANSS', 'ANTM', 'AON', 'AOS', 'APA', 'AIV', 'AAPL', 'AMAT', 'APTV', 'ADM', 'ARNC', 'ANET', 'AJG', 'AIZ', 'ATO', 'T', 'ADSK', 'ADP', 'AZO', 'AVB', 'AVY', 'BKR', 'BLL', 'BAC', 'BK', 'BAX', 'BDX', 'BRK.B', 'BBY', 'BIIB', 'BLK', 'BA', 'BKNG', 'BWA', 'BXP', 'BSX', 'BMY', 'AVGO', 'BR', 'BF.B', 'CHRW', 'COG', 'CDNS', 'CPB', 'COF', 'CPRI', 'CAH', 'KMX', 'CCL', 'CAT', 'CBOE', 'CBRE', 'CDW', 'CE', 'CNC', 'CNP', 'CTL', 'CERN', 'CF', 'SCHW', 'CHTR', 'CVX', 'CMG', 'CB', 'CHD', 'CI', 'XEC', 'CINF', 'CTAS', 'CSCO', 'C', 'CFG', 'CTXS', 'CLX', 'CME', 'CMS', 'KO', 'CTSH', 'CL', 'CMCSA', 'CMA', 'CAG', 'CXO', 'COP', 'ED', 'STZ', 'COO', 'CPRT', 'GLW', 'CTVA', 'COST', 'COTY', 'CCI', 'CSX', 'CMI', 'CVS', 'DHI', 'DHR', 'DRI', 'DVA', 'DE', 'DAL', 'XRAY', 'DVN', 'FANG', 'DLR', 'DFS', 'DISCA', 'DISCK', 'DISH', 'DG', 'DLTR', 'D', 'DOV', 'DOW', 'DTE', 'DUK', 'DRE', 'DD', 'DXC', 'ETFC', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA', 'EMR', 'ETR', 'EOG', 'EFX', 'EQIX', 'EQR', 'ESS', 'EL', 'EVRG', 'ES', 'RE', 'EXC', 'EXPE', 'EXPD', 'EXR', 'XOM', 'FFIV', 'FB', 'FAST', 'FRT', 'FDX', 'FIS', 'FITB', 'FE', 'FRC', 'FISV', 'FLT', 'FLIR', 'FLS', 'FMC', 'F', 'FTNT', 'FTV', 'FBHS', 'FOXA', 'FOX', 'BEN', 'FCX', 'GPS', 'GRMN', 'IT', 'GD', 'GE', 'GIS', 'GM', 'GPC', 'GILD', 'GL', 'GPN', 'GS', 'GWW', 'HRB', 'HAL', 'HBI', 'HOG', 'HIG', 'HAS', 'HCA', 'PEAK', 'HP', 'HSIC', 'HSY', 'HES', 'HPE', 'HLT', 'HFC', 'HOLX', 'HD', 'HON', 'HRL', 'HST', 'HPQ', 'HUM', 'HBAN', 'HII', 'IEX', 'IDXX', 'INFO', 'ITW', 'ILMN', 'IR', 'INTC', 'ICE', 'IBM', 'INCY', 'IP', 'IPG', 'IFF', 'INTU', 'ISRG', 'IVZ', 'IPGP', 'IQV', 'IRM', 'JKHY', 'J', 'JBHT', 'SJM', 'JNJ', 'JCI', 'JPM', 'JNPR', 'KSU', 'K', 'KEY', 'KEYS', 'KMB', 'KIM', 'KMI', 'KLAC', 'KSS', 'KHC', 'KR', 'LB', 'LHX', 'LH', 'LRCX', 'LW', 'LVS', 'LEG', 'LDOS', 'LEN', 'LLY', 'LNC', 'LIN', 'LYV', 'LKQ', 'LMT', 'L', 'LOW', 'LYB', 'MTB', 'M', 'MRO', 'MPC', 'MKTX', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MKC', 'MXIM', 'MCD', 'MCK', 'MDT', 'MRK', 'MET', 'MTD', 'MGM', 'MCHP', 'MU', 'MSFT', 'MAA', 'MHK', 'TAP', 'MDLZ', 'MNST', 'MCO', 'MS', 'MOS', 'MSI', 'MSCI', 'MYL', 'NDAQ', 'NOV', 'NTAP', 'NFLX', 'NWL', 'NEM', 'NWSA', 'NWS', 'NEE', 'NLSN', 'NKE', 'NI', 'NBL', 'JWN', 'NSC', 'NTRS', 'NOC', 'NLOK', 'NCLH', 'NRG', 'NUE', 'NVDA', 'NVR', 'ORLY', 'OXY', 'ODFL', 'OMC', 'OKE', 'ORCL', 'PCAR', 'PKG', 'PH', 'PAYX', 'PAYC', 'PYPL', 'PNR', 'PBCT', 'PEP', 'PKI', 'PRGO', 'PFE', 'PM', 'PSX', 'PNW', 'PXD', 'PNC', 'PPG', 'PPL', 'PFG', 'PG', 'PGR', 'PLD', 'PRU', 'PEG', 'PSA', 'PHM', 'PVH', 'QRVO', 'PWR', 'QCOM', 'DGX', 'RL', 'RJF', 'RTN', 'O', 'REG', 'REGN', 'RF', 'RSG', 'RMD', 'RHI', 'ROK', 'ROL', 'ROP', 'ROST', 'RCL', 'SPGI', 'CRM', 'SBAC', 'SLB', 'STX', 'SEE', 'SRE', 'NOW', 'SHW', 'SPG', 'SWKS', 'SLG', 'SNA', 'SO', 'LUV', 'SWK', 'SBUX', 'STT', 'STE', 'SYK', 'SIVB', 'SYF', 'SNPS', 'SYY', 'TMUS', 'TROW', 'TTWO', 'TPR', 'TGT', 'TEL', 'FTI', 'TFX', 'TXN', 'TXT', 'TMO', 'TIF', 'TJX', 'TSCO', 'TDG', 'TRV', 'TFC', 'TWTR', 'TSN', 'UDR', 'ULTA', 'USB', 'UAA', 'UA', 'UNP', 'UAL', 'UNH', 'UPS', 'URI', 'UTX', 'UHS', 'UNM', 'VFC', 'VLO', 'VAR', 'VTR', 'VRSN', 'VRSK', 'VZ', 'VRTX', 'VIAC', 'V', 'VNO', 'VMC', 'WRB', 'WAB', 'WMT', 'WBA', 'DIS', 'WM', 'WAT', 'WEC', 'WFC', 'WELL', 'WDC', 'WU', 'WRK', 'WY', 'WHR', 'WMB', 'WLTW', 'WYNN', 'XEL', 'XRX', 'XLNX', 'XYL', 'YUM', 'ZBRA', 'ZBH', 'ZION', 'ZTS']    
watchlist = Watchlist()

# App Layout
app.layout = html.Div([
    html.H1("Options Analyzer"),
    html.Div([
        html.Label("Select Option Time Frame:"),
        dcc.Dropdown(
            id='time-frame',
            options=[
                {'label': 'Weeklies', 'value': 'weeklies'},
                {'label': 'Monthlies', 'value': 'monthlies'},
                {'label': 'Long-Term', 'value': 'long-term'}
            ],
            value='weeklies'
        ),
        html.Div([
            html.Label("Enter number of months for long-term options:"),
            dcc.Input(id='long-term-months', type='number', min=1, max=24, step=1)
        ], id='long-term-input', style={'display': 'none'}),
        html.Button('Submit', id='submit-button', n_clicks=0),
    ]),
    html.Div(id='options-table'),
    html.H2("Watchlist"),
    html.Div(id='watchlist-table'),
    html.Div(id='price-change-graph'),
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # Update every minute
        n_intervals=0
    )
])

# Callback Functions

# 1. Display or Hide Long-Term Input
@app.callback(
    Output('long-term-input', 'style'),
    Input('time-frame', 'value')
)
def display_long_term_input(selected_time_frame):
    if selected_time_frame == 'long-term':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

# 2. Fetch and Display Options Data
@app.callback(
    Output('options-table', 'children'),
    Input('submit-button', 'n_clicks'),
    State('time-frame', 'value'),
    State('long-term-months', 'value')
)
def update_options_table(n_clicks, time_frame, long_term_months):
    if n_clicks == 0:
        return ""
  
    all_options_data = []

    for ticker in tickers:
        expirations = get_expiration_dates(ticker)
        if not expirations:
            continue
        filtered_expirations = filter_expiration_dates(expirations, time_frame, long_term_months)
        if not filtered_expirations:
            continue
        options_data = fetch_options_data(ticker, filtered_expirations)
        if not options_data.empty:
            processed_data = process_options_data(options_data)
            all_options_data.append(processed_data)

    if all_options_data:
        combined_df = pd.concat(all_options_data, ignore_index=True)
        # Limit to top 50 options
        combined_df = combined_df.head(50)
        table = dash_table.DataTable(
            id='options-data-table',
            columns=[{"name": i, "id": i} for i in combined_df.columns],
            data=combined_df.to_dict('records'),
            row_selectable='multi',
            selected_rows=[]
        )
        return table
    else:
        return "No options data available based on the provided criteria."

@app.callback(
    Output('watchlist-table', 'children'),
    [
        Input('options-data-table', 'derived_virtual_selected_rows'),
        Input('interval-component', 'n_intervals')
    ],
    [State('options-data-table', 'data')]
)
def update_and_refresh_watchlist(selected_rows, n_intervals, rows):
    # Adding new contracts to the watchlist
    if selected_rows and rows:
        selected_contracts = [rows[i] for i in selected_rows]
        for contract in selected_contracts:
            watchlist.add_contract(contract)

    # Refreshing watchlist prices
    watchlist.update_prices()
    watchlist_df = watchlist.get_watchlist()

    if watchlist_df.empty:
        return "No contracts in watchlist."

    table = dash_table.DataTable(
        id='watchlist-data-table',
        columns=[{"name": i, "id": i} for i in watchlist_df.columns],
        data=watchlist_df.to_dict('records')
    )
    return table

# 5. Graph Percent Change
@app.callback(
    Output('price-change-graph', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_graph(n):
    watchlist_df = watchlist.get_watchlist()
    if watchlist_df.empty:
        return ""
    fig = {
        'data': [
            {'x': watchlist_df['contractSymbol'], 'y': watchlist_df['percentChange'], 'type': 'bar'}
        ],
        'layout': {
            'title': 'Percent Change of Options Contracts Since Added to Watchlist'
        }
    }
    return dcc.Graph(figure=fig)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
