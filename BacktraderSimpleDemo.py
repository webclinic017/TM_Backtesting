import backtrader as bt
import pandas as pd

# Create a Stratey
class TestStrategy(bt.Strategy):

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
        
if __name__ == '__main__':
    
    cerebro = bt.Cerebro()
    
    cerebro.addstrategy(TestStrategy)
    
    cerebro.broker.setcash(100000.0)
    
    datapath = ('data/BTC_1d.csv')
    
    dataframe = pd.read_csv(datapath,
                        # nrows=1000,
                        # skiprows = range(1,1500),
                        parse_dates=True,
                        index_col=0)
    
    data = bt.feeds.PandasData(dataname=dataframe)
    cerebro.adddata(data)
    
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())