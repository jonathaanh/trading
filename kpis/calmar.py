import yfinance as yf
import numpy as np
import pandas as pd

tickers = ["AMZN", "GOOG", "MSFT"]

ohclv_data={}

for ticker in tickers:
	temp = yf.download(ticker, period='7mo', interval='1d')
	temp.dropna(how="any", inplace=True)
	ohclv_data[ticker]= temp

def max_dd(DF):
	df= DF.copy()
	df['return'] = df['Adj Close'].pct_change()
	df['cum_return'] = (1+df['return']).cumprod()
	df['cum_roll_max'] = df['cum_return'].cummax()
	df['drawdown'] = df['cum_roll_max'] - df['cum_return']
	return (df['drawdown']/df['cum_roll_max']).max()

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

def calmar(DF):
	df = DF.copy()
	return CAGR(DF)/max_dd(DF)

for ticker in ohclv_data:
	print("max drawdown for {} = {}".format(ticker, max_dd(ohclv_data[ticker])))
	print("calmar ratio for {} = {}".format(ticker, calmar(ohclv_data[ticker])))
