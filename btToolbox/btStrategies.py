# Author: Cholian Li
# Contact: 
# cholianli970518@gmail.com
# Created at 20220601

import backtrader as bt
import talib as ta

#################################### Note ###########################################
# // Note
"""
1. Method to add the signal based on the simple calculate of the data

- Could be calculate directly in the `__init__()` of the Strategy

E.g
```
def __init__(self):
    self.signal = self.datas[0].trader_grade(0) > self.datas[0].trader_grade(-1)
```

"""

#################################### concepts ###########################################

# // Concept
'''
self.data targets self.datas[0]
self.dataX targets self.datas[X]

'''

#################################### Examples ###########################################


# Create a Stratey
class DemoStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.quote = self.datas[0].quote

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])
        self.log('Quote, %.2f' % self.quote[0])


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
                
                
class KeltnerChannel(bt.Indicator):
    lines = ('atr','kc_upper','kc_middle','kc_lower')
    params = (('tr_period', 10), ('kc_period', 20),('kc_mult', 2),)

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0)
        # print('%s, %s' % (dt, txt))

    def __init__(self):

        self.tr1 = self.data.high - self.data.low
        self.tr2 = abs(self.data.high - self.data.close(-1))
        self.tr3 = abs(self.data.low - self.data.close(-1))
        self.tr = btind.Max(self.tr1, self.tr2, self.tr3)
        self.lines.atr = btind.EMA(self.tr, period=self.params.tr_period)
        self.lines.kc_middle = btind.EMA(self.data.close, period=self.params.kc_period)
        self.lines.kc_upper = self.lines.kc_middle + self.lines.atr * self.params.kc_mult
        self.lines.kc_lower = self.lines.kc_middle - self.lines.atr * self.params.kc_mult
        
    def next(self):
        pass

# Create a Stratey
class KeltnerChannelStrategy(bt.Strategy):
    params = dict(tr_period=10, kc_period=20, kc_mult=2)
    #* or
    lines = ('rsi',)

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0)
        # print('%s, %s' % (dt, txt)) 

 
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
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
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

    def __init__(self): 
        # for data
        self.dataclose = self.data.close

        # for indicators
        self.kc = KeltnerChannel(self.datas[0], tr_period=self.p.tr_period, kc_period=self.p.kc_period, kc_mult=self.p.kc_mult)
        self.kc.plotinfo.subplot = False

        self.kc_middle = self.kc.lines.kc_middle
        self.kc_upper = self.kc.lines.kc_upper
        self.kc_lower = self.kc.lines.kc_lower
        self.atr = self.kc.lines.atr
        self.rsi = btind.RSI(self.datas[0], period=14)
        bt.LinePlotterIndicator(self.atr, name='ATR')

        # To keep track of pending orders
        self.order = None
        self.buyprice = None
        self.buycomm = None

    def next(self):
        cash = self.broker.get_cash()
        size = cash/self.dataclose[0]

        self.log('Close, %.2f' % self.datas[0].close[0])
        # self.log('KC Middle, %.2f' % self.kc_middle[0])
        # self.log('KC Upper, %.2f' % self.kc_upper[0])
        # self.log('KC Lower, %.2f' % self.kc_lower[0])
        # self.log('ATR, %.2f' % self.atr[0])
        self.log('Position, %.2f' % self.position.size)
            
        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if not self.position:
            if self.atr[0] > 700:
                return
            else:
            
                if  (self.dataclose[0] < self.kc_upper[0]) and (self.dataclose[-1]) and (self.kc_upper[-1] - self.dataclose[0] < 0.5 * self.atr[0]):
                    # if self.dataclose[0] < self.dataclose[-1]:
                    self.log('SELL CREATE, %.2f' % self.dataclose[0])
                    self.order = self.sell(size=size)


                elif  (self.dataclose[0] > self.kc_lower[0]) and (self.dataclose[-1] > self.kc_lower[-1])  and (self.dataclose[0] - self.kc_lower[0] < 0.5 * self.atr[0]):
                    # if self.dataclose[0] > self.dataclose[-1]:

                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order = self.buy(size=size)

                else:
                    return

        # sell
        elif self.position.size < 0:
            # stop profit
            if self.dataclose[0] - self.kc_lower[0] < 0.5 * self.atr[0]:
                self.log('Stop Profit on Sell, %.2f' % self.dataclose[0])
                self.order = self.close()

            # stop loss
            elif self.dataclose[0] > self.kc_upper[0] :
                self.log('Stop Loss on Sell, %.2f' % self.dataclose[0])
                self.order = self.close()

        elif self.position.size > 0:
            if self.kc_upper[0] - self.dataclose[0] < 0.5 * self.atr[0]:
                self.log('Stop Profit on Buy, %.2f' % self.dataclose[0])
                self.order = self.close()

            elif self.dataclose[0] < self.kc_lower[0] :
                self.log('Stop Loss on Buy, %.2f' % self.dataclose[0])
                self.order = self.close()
        
    def stop(self):
        if self.position:
            self.order = self.close()
        self.log('Ending Value %.2f' %
                (self.broker.getvalue()))
