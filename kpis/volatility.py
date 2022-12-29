import yfinance as yf
import numpy as np

tickers = ["AMZN", "GOOG", "MSFT"]

ohclv_data={}

for ticker in tickers:
	temp = yf.download(ticker, period='7mo', interval='1d')
	temp.dropna(how="any", inplace=True)
	ohclv_data[ticker]= temp


def volatility(DF):
	df = DF.copy()
	df['return'] = df['Adj Close'].pct_change()
	vol = df['return'].std() *  np.sqrt(252)
	return vol

for ticker in ohclv_data:
	print("Volatility of {} is {}".format(ticker, volatility(ohclv_data[ticker])))
