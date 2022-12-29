import alpaca_trade_api as alpaca
from alpaca_trade_api.rest import REST, TimeFrame
from alpaca_trade_api.stream import Stream
import backtrader as bt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 150

ALPACA_ENDPOINT = 'https://paper-api.alpaca.markets'
KEY = 'PK699XC4CAMW43FP43MO'
SECRET = 'lcb8O8oAECEMCZ6A31LDU95Wz4ZJV6mh5Ga1918F'
API =  alpaca.REST(KEY, SECRET, ALPACA_ENDPOINT)

def run_backtest(strategy, symbols, start, end, timeframe=TimeFrame.Day, cash=10000):
	"""params:
		strategy: the strategy you wish to backtest, an instance of backtrader.Strategy
		symbols: the symbol (str) or list of symbols List[str] you wish to backtest on
		start: start date of backtest in format 'YYYY-MM-DD'
		end: end date of backtest in format: 'YYYY-MM-DD'
		timeframe: the timeframe the strategy trades on (size of bars) -
				1 min: TimeFrame.Minute, 1 day: TimeFrame.Day, 5 min: TimeFrame(5, TimeFrameUnit.Minute)
		cash: the starting cash of backtest
	"""

	# initialize backtrader broker
	cerebro = bt.Cerebro(stdstats=True)
	cerebro.broker.setcash(cash)

	# add strategy
	cerebro.addstrategy(strategy)

	# add analytics
	# cerebro.addobserver(bt.observers.Value)
	# cerebro.addobserver(bt.observers.BuySell)
	cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mysharpe')
	# historical data request
	if type(symbols) == str:
		symbol = symbols
		alpaca_data = API.get_crypto_bars(symbol, timeframe, start, end).df
		data = bt.feeds.PandasData(dataname=alpaca_data, name=symbol)
		cerebro.adddata(data)
	elif type(symbols) == list or type(symbols) == set:
		for symbol in symbols:
			alpaca_data = API.get_crypto_bars(symbol, timeframe, start, end).df
			data = bt.feeds.PandasData(dataname=alpaca_data, name=symbol)
			cerebro.adddata(data)
	# run
	initial_portfolio_value = cerebro.broker.getvalue()
	print(f'Starting Portfolio Value: {initial_portfolio_value}')
	results = cerebro.run()
	final_portfolio_value = cerebro.broker.getvalue()
	print(f'Final Portfolio Value: {final_portfolio_value} ---> Return: {(final_portfolio_value/initial_portfolio_value - 1)*100}%')

	strat = results[0]
	print('Sharpe Ratio:', strat.analyzers.mysharpe.get_analysis()['sharperatio'])
	cerebro.plot(iplot= False)


#optimal for dull days with no major news 
class SMAScross(bt.Strategy):

	# list of parameters which are configurable for the strategy
	params = dict(
		pfast=13,  # period for the fast moving average
		pslow=25   # period for the slow moving average
	)

	def __init__(self):
		sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
		sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
		self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal
  
	def next(self):
		if not self.position and self.crossover > 0:  # not in the market
			self.buy()
   
		elif self.position and self.crossover < 0:  # in the market & cross to the downside
			self.close()  # close long position


if __name__ == "__main__":
	run_backtest(SMAScross, 'BTCUSD', '2019-01-01', '2021-11-01', TimeFrame.Day, 10000)

