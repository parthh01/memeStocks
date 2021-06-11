import requests
import pandas as pd
from config import *


def get_options_for_security(stock):
    response = requests.get('{}/v1/markets/options/lookup'.format(BASE_URL),
        params={'underlying': stock},
        headers=headers
    )

    json_response = response.json()
    return json_response['symbols'][0]['options']


def get_quotes_for_options(options,batch_size=25,df=False):
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



