import pandas as pd
import numpy as np

import backtrader as bt
import backtrader.indicators as btind
from btToolbox.btDataFeed import btBinanceDataPd

# Create a Stratey
class TestStrategy(bt.Strategy):
    params = dict(period=20)
    #* or

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0)
        print('%s, %s' % (dt, txt))

    def __init__(self):
        pass

    def next(self):
        self.log(self.datas[0].close[0])
        # self.log(self.datas[1].close[0])


if __name__ == '__main__':
    
    cerebro = bt.Cerebro()
    
    cerebro.addstrategy(TestStrategy)
    # cerebro.optstrategy(TestStrategy, period=range(10, 31),test = 3)
    
    cerebro.broker.setcash(100000.0)
    
    btc = btBinanceDataPd(symbol = 'BTCUSDT',interval = '1h',startTime = '2021-01-01 00:00:00',endTime = '2022-12-31 00:00:00')
    # eth = btBinanceDataPd(symbol = 'ETHUSDT',interval = '1d',startTime = '2021-01-01 00:00:00',endTime = '2022-12-31 00:00:00')
    cerebro.adddata(btc, name = 'btc')
    # cerebro.adddata(eth, name = 'eth')

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()
    # cerebro.plot(type='candlestick')

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())