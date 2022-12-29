import yfinance as yf
import numpy as np
import pandas as pd

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

def sharpe(DF,rf):
	df = DF.copy()
	sharpe = (CAGR(df) - rf)/volatility(df)
	return sharpe

def sortino(DF, rf):
	df = DF.copy()
	df['return'] = df['Adj Close'].pct_change()
	neg_return = np.where(df['return']>0 ,0,df['return'])
	neg_vol = pd.Series(neg_return[neg_return!=0]).std()*np.sqrt(252)
	return (CAGR(df) - rf)/neg_vol



for ticker in ohclv_data:
	print("Sharpe of {} is {}".format(ticker, sharpe(ohclv_data[ticker], 0.03)))
	print("Sortino of {} is {}".format(ticker, sortino(ohclv_data[ticker], 0.03)))
