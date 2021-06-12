import streamlit as st
from tradier_data import * 
from utils import * 
from scraping import * 

option = st.sidebar.selectbox("Select Option",('home','wsb','optiondata'))

if option == 'home':
	st.header("select something in the nav bar")
	st.subheader("Highest shorted stocks right now") 
	short_df = get_most_shorted_stocks()
	st.dataframe(short_df)
elif option == 'optiondata':
	st.header("Wait for the option data to render, it takes a while...")
	symbol = st.sidebar.text_input("Ticker",value="AAPL",max_chars=5)
	st.subheader("Underlying security information")
	stock_quote = get_quote_for_security(symbol)
	stock_quote
	si_data = get_short_interest_for_security(symbol)
	st.subheader("short interest data for {}".format(symbol))
	st.dataframe(si_data)
	stock_options = get_options_for_security(symbol)
	chain_df = get_quotes_for_options(stock_options,df=True)
	st.subheader("option data for {}: ".format(symbol))
	st.dataframe(chain_df)
	dl_link = get_table_download_link(chain_df)
	st.markdown(dl_link,unsafe_allow_html=True)
elif option == 'wsb':
	st.header("wsb data here") 
 


