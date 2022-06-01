# Author: Cholian Li
# Contact: 
# cholianli970518@gmail.com
# Created at 20220601

import backtrader as bt
import talib as ta

# Create a Stratey
class DemoStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])


# Create a Stratey
class EMACrossOverStrategy(bt.Strategy):
    params = (
        ('line_a', None),
        ('line_b',None),
    )

    def log(self, txt, dt=None):
        
        # pass
    
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0)
        print('%s, %s' % (dt, txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        
        # To keep track of pending orders
        self.order = None
        self.buyprice = None
        self.buycomm = None
        
        # Add a EMA indicator
        self.ema_a = bt.talib.EMA(self.dataclose, timeperiod=self.params.line_a,plotname = 'ema_a',)
        self.ema_b = bt.talib.EMA(self.dataclose, timeperiod=self.params.line_b,plotname = 'ema_b',)
        
        
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
        
   
    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))     

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])
        self.log(f'EMA_a: {self.ema_a[0]},EMA_b: {self.ema_b[0]},')
        
        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return
        
        # If the Fast line cross over the slow line
        if self.ema_a[0] > self.ema_b[0]:
            
            # If there is already an order in a position
            if self.position:
                
                # If is has an short order, we should transfer the short position to the long position
                if self.position.size < 0:
                    # close the previous position, e.g: long
                    self.buy()
                    # buyin a new long position
                    self.buy()
                    self.log('Short --> Long  CREATE, %.2f' % self.dataclose[0])
                    
            # if there is no order in a position, we should order the position 
            # according to the current EMA singal, here we assumed the long position
            else:
                self.buy()
                self.log('Long CREATE, %.2f' % self.dataclose[0])
             
        #    Opposite to above
        elif self.ema_a[0] < self.ema_b[0]:
            
            if self.position:
                if self.position.size > 0:
                    self.sell()
                    self.sell()
                    self.log('Long --> Short  CREATE, %.2f' % self.dataclose[0])
                    
            else:
                self.sell()
                self.log('Short CREATE, %.2f' % self.dataclose[0])