import yfinance as yf

tickers = ["AMZN", "GOOG", "MSFT"]

ohclv_data={}

for ticker in tickers:
	temp = yf.download(ticker, period='1mo', interval='5m')
	temp.dropna(how="any", inplace=True)
	ohclv_data[ticker]= temp

def Bollinger_Band(DF, n=14):
	df = DF.copy()
	df['MB'] = df['Adj Close'].rolling(n).mean()
	df['UB'] = df['MB'] + 2*df['Adj Close'].rolling(n).std(ddof=0)
	df['LB'] = df['MB'] - 2*df['Adj Close'].rolling(n).std(ddof=0)
	df['BB_width'] = df['UB'] - df['LB']
	return df[["MB", "UB", "LB", "BB_width"]]

for ticker in ohclv_data:
	ohclv_data[ticker][["MB", "UB", "LB", "BB_width"]] = Bollinger_Band(ohclv_data[ticker])

print(ohclv_data)