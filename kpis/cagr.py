import yfinance as yf
import numpy as np

tickers = ["AMZN", "GOOG", "MSFT"]

ohclv_data={}

for ticker in tickers:
	temp = yf.download(ticker, period='7mo', interval='1d')
	temp.dropna(how="any", inplace=True)
	ohclv_data[ticker]= temp


def CAGR(DF):
	df = DF.copy()
	#finding the effectiveness of buy/hold strategy
	# df = ohclv_data['AMZN'].copy()
	df['return'] = df['Adj Close'].pct_change()
	df['cum_return'] = (1+df['return']).cumprod()

	#number of trading days in a year
	n = len(df)/252
	CAGR = (df['cum_return'][-1])**(1/n) - 1
	return CAGR

for ticker in ohclv_data:
	print("CAGR for {} = {}".format(ticker, CAGR(ohclv_data[ticker])))
