import requests
import pandas as pd
from bs4 import BeautifulSoup



def get_most_shorted_stocks(df=True):
    table_cols = ['Symbol\nSymbol',
                 'Company Name',
                 'Price',
                 'Chg% (1D)',
                 'Chg% (YTD)',
                 'Short Interest',
                 'Short Date',
                 'Float',
                 'Float Shorted (%)']
    url = "https://www.marketwatch.com/tools/screener/short-interest"
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    si_table = soup.findAll('table')[0]
    si_cols =  [col.text.strip('\n') for col in si_table.find('thead').find('tr').findAll('th')]
    assert(si_cols == table_cols)
    rows = si_table.findAll('tr')[1:]
    data = []
    for row in rows: data.append([val.text.strip('\n') for val in row.findAll('td')])
    if df: return pd.DataFrame(data,columns=si_cols)
    return data


