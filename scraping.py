import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_first_val_in_table(table):
    first_row = table.find('tr')
    if first_row:
        first_field = first_row.find('td')
        if first_field:
            enclosed = first_field.find('div')
            if enclosed:
                return enclosed.text
    return ''

def get_si_data_from_table(table,df=True):
    data = []
    cols = []
    rows = table.findAll('tr')
    for row in rows:
        col,val = row.findAll('td')
        cols.append(col.find('div').text.strip())
        data.append(val.text.strip())
    if df: return pd.DataFrame([data[2:]],columns=cols[2:]) # first 2 fields are bs
    return cols,data
        

def get_short_interest_for_security(ticker):
    response = requests.get("https://shortsqueeze.com/?symbol={}&submit=Short+Quote%E2%84%A2".format(ticker))
    soup = BeautifulSoup(response.text,'html.parser')
    si_table = [table for table in soup.findAll('table') if get_first_val_in_table(table) == 'Short Squeeze Ranking™'][0]
    return get_si_data_from_table(si_table)

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
    if df: 
        data =  pd.DataFrame(data,columns=si_cols).rename(columns={si_cols[0]:"Symbol"})
        data["Symbol"] = data["Symbol"].str.split(n=1).map(lambda x:x[0])
    return data


