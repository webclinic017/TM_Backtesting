# Author: Cholian Li
# Contact: 
# cholianli970518@gmail.com
# Created at 20220601

'''
############################## Possible BUG ##########################################
#! Bug: the matplotlib has crash to the backtrader
#? method 1: 
# degrade the matplotlib to 3.2.2:
# pip install matplotlib==3.2.2

#? method 2 (could not install matplotlib==3.2.2 with python 3.9):
# pip uninstall backtrader
# pip install git+https://github.com/mementum/backtrader.git@0fa63ef4a35dc53cc7320813f8b15480c8f85517#egg=backtrader

# refer: https://stackoverflow.com/questions/63471764/importerror-cannot-import-name-warnings-from-matplotlib-dates
########################################################################
'''

############################ body ####################################

import backtrader as bt
import pandas as pd
import talib as ta

from btToolbox.btStrategies import EMACrossOverStrategy, DemoStrategy
from btToolbox.btDataFeed import CSVData, PdData
from btToolbox.btObervers import OrderObserver
from btToolbox.btAnalyzers import MySharpeRatio
from btToolbox.btDataFeed import btBinanceDataPd
from btToolbox.btIndicators import SMACloseSignal, SMAExitSignal
    



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
        self.lines.nextline[0] = self.data.close[0] - self.data.close[-1]
     
class DemoStrategy(bt.Strategy):
    params = (
        ('period1', None),
        ('period1',None),
    )
    # or
    params = dict(line_a=None, line_b=None)

    lines = ('sma',)

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        smadays = bt.ind.SMA(self.dnames.btc.close, period=self.p.period1)  # or self.dnames['days'], self.params.period1
        cmpval = self.data.close(-1) > self.sma # DELAYED indexing
        LinePlotterIndicator(cmpval, name='Close_over_SMA') # plot the indicator
        self.test = MyIndicator(self.datas[0], period=15) # Access the Indicators. Note: All the lines in Indicator will be ploted automatically.

    def next(self):
        # data
        self.log('Close, %.2f' % self.dnames.btc.close[0])
        self.log('Quote, %.2f' % self.data.close[0]) # -> self.data targets self.datas[0], self.dataX targets self.datas[X]
        self.log('Quote, %.2f' % self.data_btc.close[0])
        self.log('Quote, %.2f' % self.data1_close[0])
        self.log('Quote, %.2f' % self.datas[0].lines.close[0])

        myslice = self.data.close.get(ago=0, size=1)  # default values show

        # lines
        self.log('SMA, %.2f' % self.lines.sma[0])

        myslice = self.data.close.get(ago=0, size=1)  # default values show
        '''
        xxx.lines -> xxx.l
        xxx.lines.name -> xxx.lines_name
        self.data_name -> self.data.lines.name  (Strategies, Indicators)
        self.data1_name -> self.data1.lines.name  (Strategies, Indicators)
        self.lines[0] points to self.lines.sma
        self.line points to self.lines[0]
        self.lineX point to self.lines[X]
        self.line_X point to self.lines[X]
        self.dataY points to self.data.lines[Y]
        self.dataX_Y points to self.dataX.lines[X] which is a full shorthard version of self.datas[X].lines[Y]
        '''

        # Others
        self.data.close.buflen() # buflen reports the total number of bars which have been loaded for the Data Feed
        len(self.data.close) # len reports the number of bars which have been loaded for the Data Feed


    def prenext(self):
        pass
    def start(self):
        pass
    def stop(self):
        pass
    def nextstart(self):
        pass
    def notify_order(self, order):
        pass
    def notify_trade(self, trade):
        pass
    def notify_cashvalue(cash, value):
        pass
    def notify_fund(self, cash, value, fundvalue, shares):
        pass
    def notify_store(self, msg, *args, **kwargs):
        pass


def runstart(line_a,line_b,datapath):
    
    # TODO // Create a Cerebro
    cerebro = bt.Cerebro() # default observers: Broker,traders
    
    # TODO // Add observers
    # cerebro = bt.Cerebro(stdstats=False) # uncomment for deleting the default observers(broker, trades, BuySell)
    
    #* self-defined observers
    # cerebro.addobserver(OrderObserver)
    
    #* default Observers
    # cerebro.addobserver(bt.observers.Broker)
    # cerebro.addobserver(bt.observers.Trades)
    # cerebro.addobserver(bt.observers.BuySell)
    cerebro.addobserver(bt.observers.DrawDown)
    
    # TODO // Add a Data
    #* method 1: default pandas data frame
    # dataframe = pd.read_csv(datapath,
    #                             # nrows=1000, # uncomment for large dataset
    #                             parse_dates=True,
    #                             index_col=0)
    # data = bt.feeds.PandasData(dataname=dataframe)
    
    #* method 2: self-define CSV file (recommended)
    data = CSVData(dataname=datapath)
    
    #* method 3: self-pandas dataframe
    # dataframe = pd.read_csv(datapath,
    #                             # nrows=1000, # uncomment for large dataset
    #                             parse_dates=True,
    #                             index_col=0)
    # # print(dataframe.info())
    # data = PdData(dataname = dataframe)
    
    #* method 4: self-define binance data
    # data = btBinanceDataPd(symbol = 'ETHUSDT',interval = '1d',startTime = '2021-01-01 00:00:00',endTime = '2022-12-31 00:00:00')

    #* add to cerebro
    cerebro.adddata(data)
    # cerebro.adddata(data, name = 'eth')
    # cerebro.resampledata(data, timeframe=bt.TimeFrame.Minutes, compression=60, name='eth')


    # TODO // Add a strategy
    # cerebro.addstrategy(EMACrossOverStrategy,line_a = line_a,line_b=line_b)
    cerebro.addstrategy(DemoStrategy)

    # TODO // Add Indicators (compared with the strategy)
    # cerebro.add_signal(bt.SIGNAL_LONG, SMACloseSignal, period=10)
    # cerebro.add_signal(bt.SIGNAL_LONGEXIT, SMAExitSignal, p1=5, p2=30)
    
    # TODO // Analyzer
    # * method 1: self-defined analyzers
    cerebro.addanalyzer(MySharpeRatio, _name='MySharpeRatio')
    
    # * method 2: default analyzers
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='SharpeRatio')
    
    ######################### e.g start ###############################################
    # cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='AnnualReturn')
    # cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DrawDown')
    # cerebro.addanalyzer(bt.analyzers.TimeDrawDown, _name='TimeDrawDown')
    # cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='TimeReturn')
    ######################### e.g end ###############################################
    
    # * method 3 outsourced to the Pyfolio package: 
    # cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
    
    # TODO // Cash
    cerebro.broker.setcash(1000.0)

    # TODO // Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.FixedSize, stake=.02)
    
    # TODO // Set the commission - 0.1% ... divide by 100 to remove the %
    cerebro.broker.setcommission(commission=0.0004)

    # TODO // For storing the analytical indicators result
    Myown_result = []

    # TODO // Run over everything
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    Myown_result.append(cerebro.broker.getvalue()) # (Initial portfolio value) save to the list
    results = cerebro.run()
    
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    Myown_result.append(cerebro.broker.getvalue()) # (Final portfolio value) save to the list
    Myown_result.append(Myown_result[1]/Myown_result[0]-1) #  (cumulative return) save to the list

    # TODO // Plot the result
    cerebro.plot()
    
    # TODO // Collect the Analyzer result
    strat = results[0]
    
    # * method 1
    # SharpeRatio = strat.analyzers.SharpeRatio.get_analysis()
    # print('Default Sharpe Ratio:', SharpeRatio)
    
    # SharpeRatio = strat.analyzers.MySharpeRatio.get_analysis()
    # print('MySharpe Ratio:', SharpeRatio)
    
    # * method 2 (recommended)
    SharpeRatio = strat.analyzers.getbyname('SharpeRatio')
    Myown_result.append(SharpeRatio.get_analysis()['sharperatio'])
    print('Default Sharpe Ratio:', SharpeRatio.get_analysis()['sharperatio'])
    
    SharpeRatio = strat.analyzers.getbyname('MySharpeRatio')
    Myown_result.append(SharpeRatio.get_analysis()['sharperatio'])
    print('MySharpe Ratio:', SharpeRatio.get_analysis()['sharperatio'])
    
    ######################### e.g start ###############################################
    # AnnualReturn = strat.analyzers.getbyname('AnnualReturn')
    # Myown_result.append(AnnualReturn.get_analysis())
    
    # DrawDown = strat.analyzers.getbyname('DrawDown')
    # print(DrawDown.get_analysis())
    # Myown_result.append(DrawDown.get_analysis())
    
    # TimeDrawDown = strat.analyzers.getbyname('TimeDrawDown')
    # print(TimeDrawDown.get_analysis())
    
    # TimeReturn = strat.analyzers.getbyname('TimeReturn')
    # print(TimeReturn.get_analysis())
    ######################### e.g end ###############################################

    # * method 3 Pyfolio package
    
    # pyfoliozer = strat.analyzers.getbyname('pyfolio')
    # returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
    
    # import pyfolio as pf
    # pf.create_full_tear_sheet(
    #     returns,
    #     positions=positions,
    #     transactions=transactions,
    #     gross_lev=gross_lev,
    #     live_start_date='2018-05-01',  # This date is sample specific
    #     round_trips=True)
    
    
    # TODO // Collect other information
    
    # * self-defined information
    Myown_result.append(line_a)
    Myown_result.append(line_b)
    
    print(Myown_result)
    
    return Myown_result

def validation_runstart(datapath):
    
    column_names = [
        "starting cash", 
        "ending cash", 
        "return",
        'sharp ratio',
        # 'annual return'
        'line_a',
        'line_b'
        ]
    
    # result_table = pd.DataFrame(columns=column_names)
    result_table = []
    
    for i in range(10,100):
        for j in range(i,100):
            if i != j:
                res = runstart(i,j,datapath)
                result_table.append(res)
                print(i,j,'finished')
    
    result_table = pd.DataFrame(result_table,columns = column_names)
    result_table.to_csv('Validation_future_6h_train.csv',encoding='utf-8')
    

if __name__ == '__main__':

    datapath = ('data/BTC_1d.csv')
    # validation_runstart(datapath)
    runstart(36,60,datapath)
            