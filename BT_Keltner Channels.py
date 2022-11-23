import pandas as pd
import numpy as np

import backtrader as bt
import backtrader.indicators as btind
from btToolbox.btDataFeed import btBinanceDataPd


class KeltnerChannel(bt.Indicator):
    lines = ('atr','kc_upper','kc_middle','kc_lower')
    params = (('tr_period', 10), ('kc_period', 20),('kc_mult', 2),)

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0)
        print('%s, %s' % (dt, txt))

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
class TestStrategy(bt.Strategy):
    params = dict(period=20)
    #* or
    lines = ('rsi',)

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0)
        print('%s, %s' % (dt, txt))

 
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
        self.kc = KeltnerChannel(self.datas[0], tr_period=10, kc_period=20, kc_mult=2)
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
        self.log('Close, %.2f' % self.datas[0].close[0])
        self.log('KC Middle, %.2f' % self.kc_middle[0])
        self.log('KC Upper, %.2f' % self.kc_upper[0])
        self.log('KC Lower, %.2f' % self.kc_lower[0])
        self.log('ATR, %.2f' % self.atr[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # stop trading if there is a high ATR value
        if self.atr[0] > 700:
            return

        if not self.position:

            # if self.kc_upper[0] - self.dataclose[0] < 0.5 * self.atr[0]:
                
            #     if (self.dataclose[0] > self.dataclose[-1] and self.dataclose[-1] > self.dataclose[-2]) and (
            #         self.l.rsi[0] < self.l.rsi[-1] and self.l.rsi[-1] < self.l.rsi[-2]):

            #         self.log('SELL CREATE, %.2f' % self.dataclose[0])
            #         self.order = self.sell()

            # elif self.dataclose[0] - self.kc_lower[0] < 0.5 * self.atr[0]:

            #     if (self.dataclose[0] < self.dataclose[-1] and self.dataclose[-1] < self.dataclose[-2]) and (
            #         self.l.rsi[0] > self.l.rsi[-1] and self.l.rsi[-1] > self.l.rsi[-2]):

            #         self.log('BUY CREATE, %.2f' % self.dataclose[0])
            #         self.order = self.buy()
            
            if self.kc_upper[0] - self.dataclose[0] < 0.5 * self.atr[0]:

                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()

            elif self.dataclose[0] - self.kc_lower[0] < 0.5 * self.atr[0]:

                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()

            else:
                self.order = self.close()

        else:
            if self.position.size < 0:
                if self.dataclose[0] < self.kc_middle[0]:
                    self.log('BUY CLOSE, %.2f' % self.dataclose[0])
                    self.order = self.close()

            elif self.position.size > 0:
                if self.dataclose[0] > self.kc_middle[0]:
                    self.log('SELL CLOSE, %.2f' % self.dataclose[0])
                    self.order = self.close()
        
    def stop(self):
        if self.position:
            self.order = self.close()
        self.log('Ending Value %.2f' %
                (self.broker.getvalue()))



if __name__ == '__main__':
    
    cerebro = bt.Cerebro(stdstats=True)
    
    cerebro.addstrategy(TestStrategy)
    # cerebro.optstrategy(TestStrategy, period=range(10, 31),test = 3)
    
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.0004)
    
    btc = btBinanceDataPd(symbol = 'BTCUSDT',interval = '1h',startTime = '2022-01-01 00:00:00',endTime = '2022-02-01 00:00:00')
    cerebro.adddata(btc, name = 'btc_day')
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='SharpeRatio')
    cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='AnnualReturn')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DrawDown')
    cerebro.addanalyzer(bt.analyzers.TimeDrawDown, _name='TimeDrawDown')
    cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='TimeReturn')

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    results = cerebro.run()
    strat = results[0]
    cerebro.plot(style = 'candlestick')
    
    SharpeRatio = strat.analyzers.SharpeRatio.get_analysis()
    print('Sharpe Ratio:', SharpeRatio)
    AnnualReturn = strat.analyzers.AnnualReturn.get_analysis()
    print('Annual Return:', AnnualReturn)
    DrawDown = strat.analyzers.DrawDown.get_analysis()
    print('DrawDown:', DrawDown)
    TimeDrawDown = strat.analyzers.TimeDrawDown.get_analysis()
    print('TimeDrawDown:', TimeDrawDown)


    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())