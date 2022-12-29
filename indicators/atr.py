import yfinance as yf

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

for ticker in ohclv_data:
	ohclv_data[ticker][["ATR"]] = ATR(ohclv_data[ticker])

print(ohclv_data)