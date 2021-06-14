import streamlit as st
from tradier_data import * 
from utils import * 
from scraping import * 
from alpaca import *

option = st.sidebar.selectbox("Select Option",('home','wsb','optiondata'))
symbol = st.sidebar.text_input("Ticker",value="AAPL",max_chars=5)
wsb_df = get_wsb_analysis()
if option == 'home':
	st.header("select something in the nav bar")
	st.subheader("stocks with high short interest, low runup") 
	st.write("Runup is the maximum % difference between the 50MA and the price at any point in the last year, in my opinion a pretty good proxy for whether or not the stock has run-up already. Empirically tested a good cutoff to be 40%. Anything above 40% is pretty much a certainty the stock has already run up. The lower the runup % the more likely a runup has yet to occur, assuming all other signals check out.")
	st.write("The relative frequency column is the percentage of ticker mentions the stock has received as a proportion of all ticker mentions on the WSB subreddit. Ultimately sentiment is not considered as the specific screen we are looking at is highly shorted stocks with low market cap and poor performance. It is not unreasonable to assume bullish sentiment from a subreddit known to pump such stocks.")
	short_df = get_most_shorted_stocks()
	runup_df = get_runup_data_for_stocks(short_df["Symbol"].tolist())
	short_df = short_df.merge(runup_df,on="Symbol")
	short_df = short_df.merge(wsb_df,how='left',on='Symbol')
	st.dataframe(short_df[(short_df["Runup (%)"] < 40) & (short_df["Relative Frequency (%)"].notna())])
	st.markdown(get_table_download_link(short_df),unsafe_allow_html=True)
elif option == 'optiondata':
	st.header("Wait for the option data to render, it takes a while...")
	st.subheader("Underlying security information")
	stock_quote = get_quote_for_security(symbol)
	stock_quote
	si_data = get_short_interest_for_security(symbol)
	st.subheader("short interest data for {}".format(symbol))
	st.dataframe(si_data)
	st.subheader("option data for {}: ".format(symbol))
	chain_df = assemble_options_data_for_security(symbol)
	st.dataframe(chain_df)
	dl_link = get_table_download_link(chain_df)
	st.markdown(dl_link,unsafe_allow_html=True)
elif option == 'wsb':
	st.header("wsb data here") 
	st.dataframe(wsb_df)


