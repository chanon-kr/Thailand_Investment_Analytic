import starfishX as sx
import pythainav as nav

import pandas as pd
import numpy as np
from datetime import datetime

# stock_type = 'Mutual fund'
# target_name  = 'SCBDV'
# start_date = "2022-05-01"
# end_date = "2022-07-13"

def get_invest_data(stock_type, target_name, start_date, end_date) :
    if stock_type == 'Mutual fund' : 
        # pass
        backward_range = (datetime.now() - datetime.strptime(start_date,'%Y-%m-%d')).total_seconds()/3600/24/365
        if backward_range >= 10 : back_ = 'MAX'
        elif backward_range >= 5 : back_ = '10Y'
        elif backward_range >= 3 : back_ = '5Y'
        elif backward_range >= 1 : back_ = '3Y'
        else : back_ = '1Y'
        df = nav.get_all(target_name, range =back_, asDataFrame=True)[['updated', 'value']]
        if type(df) != type(pd.DataFrame()) : raise ("No Data Found")
        df.columns = ['Date','close_value']
        df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)].set_index('Date')
    else : 
        # pass
        df = sx.loadHistData_v2(target_name,start=start_date, end = end_date)
        if type(df) != type(pd.DataFrame()) : raise ("No Data Found")
        df = df[['Close']]
        df.columns = ['close_value']
        
    df['week_day'] = df.index.day_name()
    df['day'], df['month'], df['year'] = df.index.day, df.index.month,  df.index.year
    df['month_period'] = np.where(df['day'] <= 10, 'early', np.where(df['day'] <= 20, 'mid', 'late'))
    df['month_period'] = pd.Categorical(df['month_period'], ["early", "mid", "late"])
    df['week_day'] = pd.Categorical(df['week_day'], ["Monday", "Tuesday", "Wednesday", 'Thursday', 'Friday'])
    df['year-month'] = df['year'].astype(str) + '-' + df['month'].astype(str)
    df = df.reset_index()
    df = df[['Date','year','month', 'year-month', 'month_period','day','week_day','close_value']]
    return df

def format_df(df) :
    for i in ['day','month','year'] : df[i] = df[i].astype(int)
    for i in ['close_value'] : df[i] = df[i].astype(float)

def filter_df(df, filter_year, filter_month, filter_month_year) :
    df_plot = df.copy()
    if len(filter_year) > 0 : 
        df_plot = df_plot[df_plot['year'].astype(int).isin([int(x) for x in filter_year])]
    if len(filter_month) > 0 : 
        df_plot = df_plot[df_plot['month'].astype(int).isin([int(x) for x in filter_month])]
    if len(filter_month_year) > 0 : 
        df_plot = df_plot[df_plot['year-month'].isin([x for x in filter_month_year])]
    return df_plot