from alpha_vantage.timeseries import TimeSeries
import pandas

key_path = 'key.txt'
ts = TimeSeries(key=open(key_path, 'r').read(), output_format='pandas')
data = ts.get_daily_adjusted(symbol='EURUSD', outputsize='full')[0]
print(data)