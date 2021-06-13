import requests
import pandas as pd
import numpy as np
import py_vollib_vectorized as vollib
from datetime import datetime, timedelta
from config import *


def get_options_for_security(stock):
    response = requests.get('{}/v1/markets/options/lookup'.format(BASE_URL),
        params={'underlying': stock},
        headers=headers
    )

    json_response = response.json()
    return json_response['symbols'][0]['options']


def get_quotes_for_options(options,batch_size=25,df=True):
    chains = []
    for i in range(0, len(options),batch_size):
        options_batch = options[i:i+batch_size]
        response = requests.get('{}/v1/markets/quotes'.format(BASE_URL),
            params={'symbols': ','.join(options_batch), 'greeks': 'true'},
            headers=headers
        )    
        json_response = response.json()
        chains += json_response['quotes']['quote']
    if df: return pd.DataFrame(chains).drop(["symbol","type"],axis=1)
    return chains
    

def get_quote_for_security(stock):
    response = requests.get('{}/v1/markets/quotes'.format(BASE_URL),
        params={'symbols': stock, 'greeks': 'false'},
        headers=headers
    )    
    json_response = response.json()
    return json_response['quotes']['quote']


def assemble_options_data_for_security(stock):
    quote = get_quote_for_security(stock)
    options = get_options_for_security(stock)
    chain_df = get_quotes_for_options(options,df=True)
    chain_df['flag'] = np.where(chain_df['option_type'] == 'put','p','c')
    chain_df['t_to_exp'] = (pd.to_datetime(chain_df['expiration_date']) - pd.to_datetime(datetime.today())).dt.days/365
    chain_df['Implied Volatility (%)'] = vollib.vectorized_implied_volatility_black(price=chain_df['last'],F=quote['last'],K=chain_df['strike'],t=chain_df['t_to_exp'],r=.3,flag=chain_df['flag'],return_as='series')*100
    return chain_df
