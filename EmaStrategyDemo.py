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
    
                
def runstart(line_a,line_b,datapath):
    
    # TODO // Create a Cerebro
    cerebro = bt.Cerebro() # default observers: Broker,traders
    
    # TODO // Add observers
    # cerebro = bt.Cerebro(stdstats=False) # uncomment for deleting the default observers(broker, trades, BuySell)
    
    #* self-defined observers
    cerebro.addobserver(OrderObserver)
    
    #* default Observers
    # cerebro.addobserver(bt.observers.Broker)
    # cerebro.addobserver(bt.observers.Trades)
    # cerebro.addobserver(bt.observers.BuySell)
    # cerebro.addobserver(bt.observers.DrawDown)
    
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
    
    #* add to cerebro
    cerebro.adddata(data)

    # TODO // Add a strategy
    cerebro.addstrategy(EMACrossOverStrategy,line_a = line_a,line_b=line_b)
    # cerebro.addstrategy(DemoStrategy)
    
    # TODO // Analyzer
    
    # * method 1: self-defined analyzers
    cerebro.addanalyzer(MySharpeRatio, _name='MySharpeRatio')
    
    # * method 2: default analyzers
    # cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='SharpeRatio')
    
    ######################### e.g start ###############################################
    # cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='AnnualReturn')
    # cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DrawDown')
    # cerebro.addanalyzer(bt.analyzers.TimeDrawDown, _name='TimeDrawDown')
    # cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='TimeReturn')
    ######################### e.g end ###############################################
    
    # * method 3: 
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
    Myown_result.append(SharpeRatio.get_analysis()['mysharperatio'])
    print('MySharpe Ratio:', SharpeRatio.get_analysis()['mysharperatio'])
    
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
    
    # TODO // Collect other information
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
            