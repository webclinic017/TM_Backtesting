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
        
        # signal = +1
        if self.signal[0] == 1:
            self.buy()
        
        # signal = -1
        elif self.signal[0] == -1:
            self.sell()
            
        # signal = 0
        else:
            pass
        
        # # already have a position
        # if self.position:
        #     # support we already have short position (-1 : sell 1 coins)
        #     if self.position.size < 0:
        #         # signal = +1
        #         if self.signal[0] == 1:
        #             self.close() # we close the short position
        #             # self.sell()
        #             self.buy() # we open a new long position
        
                
        #     elif self.position.size > 0:
        #         # signal = -1
        #         if self.signal[0] == -1:
        #             self.close()
        #             self.sell()
                           
        # else:
        #     # signal = +1
        #     if self.signal[0] == 1:
        #         self.buy()
            
        #     # signal = -1
        #     elif self.signal[0] == -1:
        #         self.sell()
                
        #     # signal = 0
        #     else:
        #         pass
        
            
    def stop(self):
        
        self.close()
        print('Close the order')
        
if __name__ == '__main__':
    
    cerebro = bt.Cerebro()
    
    cerebro.addstrategy(TestStrategy)
    cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
    
    cerebro.broker.setcash(10000.0)

    datapath = ('data/TM_strategyEMA2.csv')
    data = TM_strategy(dataname=datapath)
    dataframe = pd.read_csv('data/ETH_1d.csv',
                                # nrows=1000, # uncomment for large dataset
                                parse_dates=True,
                                index_col=0)
    data1 = bt.feeds.PandasData(dataname=dataframe)
    
    cerebro.adddata(data, name = 'BTC')
    # cerebro.adddata(data1, name='ETH')
    
    # * Benchmarking-observer modules
    # cerebro.addobserver(bt.observers.TimeReturn, 
    #                 timeframe=bt.TimeFrame.NoTimeFrame)
    
    # cerebro.addobserver(bt.observers.Benchmark, data = data1,
    #                 timeframe=bt.TimeFrame.NoTimeFrame)
    
    # * Benchmarking-analyzer modules
    # cerebro.addanalyzer(bt.analyzers.TimeReturn, timeframe=bt.TimeFrame.Years, data=data1, _name='datareturns')
    # cerebro.addanalyzer(bt.analyzers.TimeReturn, timeframe=bt.TimeFrame.Years, _name='timereturns')
    
    cerebro.addsizer(bt.sizers.FixedSize, stake=.5)
    cerebro.broker.setcommission(commission=0.0004)
    
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    strats = cerebro.run()
    
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
    cerebro.plot()
    strat = strats[0]
    
    # * Collecting the benchmark results
    tret_analyzer = strat.analyzers.getbyname('timereturns')
    print(f"Time return: {tret_analyzer.get_analysis()}")
    
    tdata_analyzer = strat.analyzers.getbyname('datareturns')
    print(f"Benchmarking return: {tdata_analyzer.get_analysis()}")

    # # * Save results for analyzing via pyfolio
    # pyfoliozer = strat.analyzers.getbyname('pyfolio')
    # returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
    # returns.to_csv('result/returns.csv')
    # positions.to_csv('result/positions.csv')
    # transactions.to_csv('result/transactions.csv')
    # gross_lev.to_csv('result/gross_lev.csv')
    