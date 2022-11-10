# Author: Cholian Li
# Contact: 
# cholianli970518@gmail.com
# Created at 20220601

import backtrader.feeds as btfeeds

class CSVData(btfeeds.GenericCSVData):
    # add one more columns called quote
    lines = ('quote',)

    params = (
        ('nullvalue', 0.0),
        ('dtformat', ('%Y-%m-%d')),
        # ('tmformat',('%H:%M:%S')),


        ('datetime', 0),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        ('volume', 5),
        ('quote', 6),
    )
    
class PdData(btfeeds.PandasData):
    # add one more columns called quote
    lines = ('quote',)

    params = (
        ('datetime', None),
        
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        ('volume', 5),
        ('quote', 6),
    )
    
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


class TM_API_data(GenericCSVData):
    # add only three columns called date, Bitcoin, Ethereum
    lines = ('btc','eth')

    params = (
        ('nullvalue', float('NaN')),
        ('dtformat', '%Y-%m-%d'),
        ('tmformat', '%H:%M:%S'),

        ('datetime', 0),
        ('time', -1),
        ('open', -1),
        ('high', -1),
        ('low', -1),
        ('close', -1),
        ('volume', -1),
        ('openinterest', -1),
        ('btc',1),
        ('eth',2)
    )