# Author: Chao Li
# Contact: 
# cholianli970518@gmail.com
# Created at 20220604


import backtrader as bt
import pandas as pd

import backtrader.feeds as btfeeds
    
    

class TM_strategy(btfeeds.GenericCSVData):
    # add one more columns called quote
    lines = ('datetime','frama','ema','trend','signal')

    params = (
        ('nullvalue', 0.0),
        ('dtformat', ('%Y-%m-%d')),
        # ('tmformat',('%H:%M:%S')),

        ('open', -1),
        ('high', -1),
        ('low', -1),
        ('volume', -1),
        ('quote', -1),
        
        # ('token_id', 0),
        # ('symbol', 1),
        ('datetime', 2),
        ('close', 3),
        ('frama', 4),
        ('ema', 5),
        ('trend', 6),
        ('signal', 7),
    )

# Create a Stratey
class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
    
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt, txt))
        
    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.close = self.datas[0].close
        self.frama = self.datas[0].frama
        self.ema = self.datas[0].ema
        self.trend = self.datas[0].trend
        self.signal = self.datas[0].signal
        
        
        # To keep track of pending orders
        self.order = None
        self.buyprice = None
        self.buycomm = None
        
    def next(self):
        # self.log(f'Close: {self.close[0]}')
        self.log(self.data.close[0])
        
        if self.order:
            return 
        
if __name__ == '__main__':
    
    cerebro = bt.Cerebro()
    
    cerebro.addstrategy(TestStrategy)
    
    cerebro.broker.setcash(100000.0)
    
    datapath = ('TM_strategyEMA.csv')
    
    data = TM_strategy(dataname=datapath)
    cerebro.adddata(data)
    
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
    # cerebro.plot()