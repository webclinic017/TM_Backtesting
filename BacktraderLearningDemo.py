import pandas as pd
import numpy as np

import backtrader as bt
import backtrader.indicators as btind
from btToolbox.btDataFeed import btBinanceDataPd


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
    params = dict(period=20)
    #* or
    lines = ('strategy_line',)

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0)
        print('%s, %s' % (dt, txt))

    def __init__(self): 
        cross_close = self.datas[0].close(-1) - self.datas[0].close(-2)
        bt.LinePlotterIndicator(cross_close, name='cross_close')
        self.my_ind = MyIndicator(self.datas[0], period=15)

    def next(self):
        self.log(self.dnames.btc_day.lines.close[0])
        self.log(self.my_ind.lines.nextline[0])
        pass



if __name__ == '__main__':
    
    cerebro = bt.Cerebro()
    
    cerebro.addstrategy(TestStrategy)
    # cerebro.optstrategy(TestStrategy, period=range(10, 31),test = 3)
    
    cerebro.broker.setcash(100000.0)
    
    btc = btBinanceDataPd(symbol = 'BTCUSDT',interval = '1d',startTime = '2022-01-01 00:00:00',endTime = '2022-03-01 00:00:00')
    # eth = btBinanceDataPd(symbol = 'DOGEUSDT',interval = '1m',startTime = '2022-01-01 00:00:00',endTime = '2022-01-01 07:00:00')
    cerebro.adddata(btc, name = 'btc_day')
    # cerebro.resampledata(btc, timeframe=bt.TimeFrame.Weeks, compression=1, name='btc_1w')

    # cerebro.adddata(eth, name = 'eth')

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()
    # cerebro.plot(type='candlestick')

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())