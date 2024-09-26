# data_processing.py

import pandas as pd
from datetime import datetime, timedelta

def filter_expiration_dates(expirations, choice, long_term_months=None):
    today = datetime.today().date()
    filtered_dates = []

    if choice == 'weeklies':
        end_date = today + timedelta(days=7)
        filtered_dates = [date for date in expirations if today <= datetime.strptime(date, '%Y-%m-%d').date() <= end_date]

    elif choice == 'monthlies':
        start_date = today + timedelta(days=8)
        end_date = today + timedelta(days=30)
        filtered_dates = [date for date in expirations if start_date <= datetime.strptime(date, '%Y-%m-%d').date() <= end_date]

    elif choice == 'long-term' and long_term_months:
        target_date = today + timedelta(days=long_term_months * 30)
        start_date = target_date - timedelta(days=15)
        end_date = target_date + timedelta(days=15)
        filtered_dates = [date for date in expirations if start_date <= datetime.strptime(date, '%Y-%m-%d').date() <= end_date]

    return filtered_dates

def process_options_data(df):
    df = df[df['openInterest'] > 200]
    df = df.assign(volume_oi_ratio = df['volume'] / df['openInterest'])
    df = df[df['volume_oi_ratio'] > 0.5]
    return df.sort_values('volume_oi_ratio', ascending=False)
