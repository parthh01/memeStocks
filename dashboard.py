import streamlit as st
from tradier_data import * 


option = st.sidebar.selectbox("Select Option",('home','wsb','optiondata'))

if option == 'home':
	st.header("select something in the nav bar")
elif option == 'optiondata':
	st.header("Wait for the running man, it takes a while...")
	symbol = st.sidebar.text_input("Ticker",value="AAPL",max_chars=5)
	st.subheader("Underlying security information")
	stock_quote = get_quote_for_security(symbol)
	stock_quote
	stock_options = get_options_for_security(symbol)
	chain_df = get_quotes_for_options(stock_options,df=True)
	st.subheader("option data for {}: ".format(symbol))
	st.dataframe(chain_df)
elif option == 'wsb':
	st.header("wsb data here") 
 


