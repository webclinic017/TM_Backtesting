import pandas as pd
import numpy as np

import backtrader as bt
import backtrader.indicators as btind
from btToolbox.btDataFeed import btBinanceDataPd, PdData


class MyIndicator(bt.Indicator):
    lines = ('myline','nextline')
    params = (('period', 15),)

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0)
        print('%s, %s' % (dt, txt))

    def __init__(self):
        self.lines.myline = self.data.close(0) - self.data.close(-1)

    def next(self):
        self.lines.nextline[0] = 5


# Create a Stratey
class TestStrategy(bt.Strategy):
    params = dict(
        period=15,
    )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0)
        print('%s, %s' % (dt, txt))

    def __init__(self): 
        print(self.params.period)

    def next(self):
        self.log('Close, %.2f' % self.data.close[0])


class MyDataFeed(bt.feeds.PandasData):
    # add one more columns called quote
    lines = ('quote',)

    params = (
        ('datetime', -1),
        
        ('open', 0),
        ('high', 1),
        ('low', 2),
        ('close', 3),
        ('volume', 4),
        ('quote', -1),
    )

class MyAnalyzer(bt.Analyzer):
    params = (('riskfreerate', 0.01),)

    def __init__(self):
        print('This is my sharpe ratio analyzer')

    def start(self):
        # Not needed ... but could be used
        print('Starting sharpe ratio analyzer')

    def next(self):
        print('Next sharpe ratio analyzer')

    def stop(self):
        print('Stopping sharpe ratio analyzer')
        self.ratio = 5

    def get_analysis(self):
        return dict(MyAnalyzer=self.ratio)





class OrderObserver(bt.observer.Observer):
    lines = ('myobserver', 'expired',)

    plotinfo = dict(plot=True, subplot=True, plotlinelabels=True)

    plotlines = dict(
        myobserver=dict(marker='*', markersize=8.0, color='lime', fillstyle='full'),
        expired=dict(marker='s', markersize=8.0, color='red', fillstyle='full')
    )

    def next(self):
        self.lines.myobserver[0] = 1
        slf.lines.expired[0] = 2
        


if __name__ == '__main__':
    
    cerebro = bt.Cerebro()
    
    cerebro.addstrategy(TestStrategy)
    # cerebro.optstrategy(TestStrategy, period=range(10, 30))
    
    cerebro.broker.setcash(100000.0)
    
    
    datapath = 'data/BTC_1h.csv'
    dataframe = pd.read_csv(datapath,
                                nrows = 100,
                                parse_dates=True,
                                index_col=0)
    # print(dataframe.info())
    btc = MyDataFeed(dataname = dataframe)

    # btc = btBinanceDataPd(symbol = 'BTCUSDT',interval = '1h',startTime = '2022-01-01 00:00:00',endTime = '2022-01-01 00:07:00',BASE_URL = 'https://api.binance.us')
    # eth = btBinanceDataPd(symbol = 'DOGEUSDT',interval = '1m',startTime = '2022-01-01 00:00:00',endTime = '2022-01-01 07:00:00')
    cerebro.adddata(btc, name = 'btc')
    cerebro.addanalyzer(MyAnalyzer, _name='MyAnalyzer')

    # cerebro.resampledata(btc, timeframe=bt.TimeFrame.Weeks, compression=1, name='btc_1w')

    # cerebro.adddata(eth, name = 'eth')

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # thestrats = cerebro.run()
    # for i in thestrats: 
    #     print(i[0].p.period)
    #     print(i[0].analyzers.MyAnalyzer.get_analysis())

    
    cerebro.plot()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())