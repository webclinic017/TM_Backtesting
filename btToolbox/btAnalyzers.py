# Author: Cholian Li
# Contact: 
# cholianli970518@gmail.com
# Created at 20220601

import operator

from backtrader.utils.py3 import map
from backtrader import Analyzer, TimeFrame
from backtrader.mathsupport import average, standarddev
from backtrader.analyzers import AnnualReturn


class MySharpeRatio(Analyzer):
    params = (('timeframe', TimeFrame.Years), ('riskfreerate', 0.01),)

    def __init__(self):
        super(MySharpeRatio, self).__init__()
        self.anret = AnnualReturn()

    def start(self):
        # Not needed ... but could be used
        pass

    def next(self):
        # Not needed ... but could be used
        pass

    def stop(self):
        retfree = [self.p.riskfreerate] * len(self.anret.rets)
        retavg = average(list(map(operator.sub, self.anret.rets, retfree)))
        retdev = standarddev(self.anret.rets)

        self.ratio = retavg / retdev

    def get_analysis(self):
        return dict(sharperatio=self.ratio)



class MyAnalyzer(bt.Analyzer):
    params = (('riskfreerate', 0.01),)

    def __init__(self):
        print('This is my sharpe ratio analyzer')

    def start(self):
        # Not needed ... but could be used
        print('Starting sharpe ratio analyzer')

    def next(self):
        print('Next sharpe ratio analyzer')

    def stop(self):
        print('Stopping sharpe ratio analyzer')
        self.ratio = 5

    def get_analysis(self):
        return dict(MyAnalyzer=self.ratio)