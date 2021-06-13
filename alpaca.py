from alpaca_trade_api.rest import REST, TimeFrame
from datetime import datetime, timedelta
import pandas as pd

def get_historical_data_for_security(ticker,start=str((datetime.today() - timedelta(days=365)).date()),end=str(datetime.today().date() - timedelta(days=1)),df=True):
    api = REST()
    
    data = api.get_bars(ticker, TimeFrame.Day, start, end)
    if df: 
        data = data.df
        data['50MA'] = data['close'].rolling(50).mean()
        return data
    return data


def get_max_runup(df):
    gap = df['gap'] = (df['close'] - df['50MA'])*100/df['close']
    return df['gap'].max()


def get_runup_data_for_stocks(stocks,df=True):
    runup = []
    for stock in stocks:
        data = get_historical_data_for_security(stock)
        runup.append(get_max_runup(data))
    if df: 
        return pd.DataFrame(list(zip(stocks,runup)),columns=["Symbol","Runup (%)"])
    return list(zip(stocks,runup))



