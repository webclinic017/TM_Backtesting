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

        ('open', 8),
        ('high', 9),
        ('low', 10),
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
        # self.frama = self.datas[0].frama
        # self.ema = self.datas[0].ema
        # self.trend = self.datas[0].trend
        self.signal = self.datas[0].signal
        
        # To keep track of pending orders
        self.order = None
        self.buyprice = None
        self.buycomm = None
    
    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))   
        
    def notify_order(self, order):
        
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
                
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
                
            elif order.issell() : # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

            elif order.isclose():
                self.log('Order closed EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None
        
    def next(self):
        self.log(self.close[0])
        self.log(self.signal[0])
        if self.position:
            if self.position.size < 0:
                # signal = +1
                if self.signal[0] == 1:
                    self.buy()
                    self.buy()
        
                
            elif self.position.size > 0:
                # signal = +1
                if self.signal[0] == -1:
                    self.sell()
                    self.sell()
                           
        else:
            # signal = +1
            if self.signal[0] == 1:
                self.buy()
            
            # signal = -1
            elif self.signal[0] == -1:
                self.sell()
                
            # signal = 0
            else:
                pass
        
            
    def stop(self):
        
        self.close()
        print('Close the order')
        
if __name__ == '__main__':
    
    cerebro = bt.Cerebro()
    
    cerebro.addstrategy(TestStrategy)
    
    cerebro.broker.setcash(100000.0)

        
    datapath = ('TM_strategyEMA2.csv')
    
    data = TM_strategy(dataname=datapath)
    cerebro.adddata(data)
    
    cerebro.addsizer(bt.sizers.FixedSize, stake=.2)
    cerebro.broker.setcommission(commission=0.0004)
    
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
    cerebro.plot()