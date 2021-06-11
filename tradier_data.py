import requests
import pandas as pd

TRADIER_API_KEY = "Jta3vCKbfk5HxsN8hHqEp4HlyPku"
headers = {'Authorization': "Bearer {}".format(TRADIER_API_KEY), 'Accept': 'application/json'}


def get_options_for_security(stock):
    response = requests.get('https://sandbox.tradier.com/v1/markets/options/lookup',
        params={'underlying': stock},
        headers=headers
    )

    json_response = response.json()
    return json_response['symbols'][0]['options']


def get_quotes_for_options(options,batch_size=25,df=False):
    chains = []
    for i in range(0, len(options),batch_size):
        options_batch = options[i:i+batch_size]
        response = requests.get('https://sandbox.tradier.com/v1/markets/quotes',
            params={'symbols': ','.join(options_batch), 'greeks': 'true'},
            headers=headers
        )    
        json_response = response.json()
        chains += json_response['quotes']['quote']
    if df: return pd.DataFrame(chains).drop(["symbol","type"],axis=1)
    return chains
    

def get_quote_for_security(stock):
    response = requests.get('https://sandbox.tradier.com/v1/markets/quotes',
        params={'symbols': stock, 'greeks': 'false'},
        headers=headers
    )    
    json_response = response.json()
    return json_response['quotes']['quote']



