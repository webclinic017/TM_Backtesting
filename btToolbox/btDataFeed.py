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