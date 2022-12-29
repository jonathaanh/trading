import yfinance as yf
import numpy as np

tickers = ["AMZN", "GOOG", "MSFT"]

ohclv_data={}

for ticker in tickers:
	temp = yf.download(ticker, period='1mo', interval='5m')
	temp.dropna(how="any", inplace=True)
	ohclv_data[ticker]= temp

def ATR(DF, n=14):
	df = DF.copy()
	df["H-L"] = df["High"] - df["Low"]
	df["H-PC"] = df["High"] - df["Adj Close"].shift(1)
	df["L-PC"] = df["Low"] - df["Adj Close"].shift(1)
	df["TR"] = df[["H-L", "H-PC", "L-PC"]].max(axis=1, skipna=False)
	df["ATR"] = df["TR"].ewm(com=n, min_periods=n).mean()
	return df["ATR"]

def ADX(DF, n=20):
	df = DF.copy()
	df['atr'] = ATR(df, n)
	df['upmove'] = df['High'] - df['High'].shift(1)
	df['downmove'] = df['Low'].shift(1) - df['Low']
	df['+dm'] = np.where((df['upmove']> df['downmove']) & df['upmove']>0, df['upmove'], 0)
	df['-dm'] = np.where((df['downmove']> df['upmove']) & df['downmove']>0, df['downmove'], 0)
	df['+di'] = 100 * (df['+dm']/df['atr']).ewm(span = n, min_periods=n).mean()
	df['-di'] = 100 * (df['-dm']/df['atr']).ewm(span = n, min_periods=n).mean()
	df['adx'] = 100 * abs((df['+di'] - df['-di'])/(df['+di'] + df['-di'])).ewm(com = n, min_periods=n).mean()
	return df['adx']

for ticker in ohclv_data:
	ohclv_data[ticker][["adx"]] = ADX(ohclv_data[ticker])

print(ohclv_data)