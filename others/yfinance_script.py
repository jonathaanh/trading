import yfinance as yf
import datetime as dt
import pandas as pd

stocks=['AAPL', 'GOOG', 'MSFT', 'FB']
start_date = dt.datetime.today().date()-dt.timedelta(30)
end_date = dt.datetime.today().date()
cl_price = pd.DataFrame()

#for ticker in stocks:
# data = yf.download("SPY AAPL",start=start_date, end=end_date,interval='1d')
# print(data)
ohlcv_data = {}

for ticker in stocks:
	ohlcv_data[ticker] = yf.download(ticker, period='1mo', interval='1d')

# print(cl_price)
print(ohlcv_data)