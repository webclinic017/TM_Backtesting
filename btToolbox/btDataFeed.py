# Author: Cholian Li
# Contact: 
# cholianli970518@gmail.com
# Created at 20220601

import backtrader.feeds as btfeeds
from btToolbox.DataSource.BinanceData import binanceData
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

class TM_API_data(btfeeds.GenericCSVData):
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

class BtBinanceDataPD(btfeeds.PandasData):
    lines = ()

    params = (
        # ('nullvalue', float('NaN')),
        ('dtformat', '%Y-%m-%d %H:%M:%S'),
        # ('tmformat', '%H:%M:%S'),

        ('datetime', -1),
        ('open', 0),
        ('high', 1),
        ('low', 2),
        ('close', 3),
        ('volume', 4),
        ('openinterest', -1),
    )


def btBinanceDataPd(symbol,startTime,endTime,interval = '1d',BASE_URL = 'https://api.binance.com', url_path = '/api/v3/klines'):
    class PdDataBinance(btfeeds.PandasData):
        lines = ('quoteVolume', 'numTrades', 'takerVol', 'takerQuoteVol')

        params = (
            # ('nullvalue', float('NaN')),
            ('dtformat', '%Y-%m-%d %H:%M:%S'),
            # ('tmformat', '%H:%M:%S'),

            ('datetime', -1),
            ('open', 0),
            ('high', 1),
            ('low', 2),
            ('close', 3),
            ('volume', 4),
            ('quoteVolume', 6),
            ('numTrades', 7),
            ('takerVol', 8),
            ('takerQuoteVol', 9),
            ('openinterest', -1),
        )

    df = binanceData(symbol,startTime,endTime,interval,BASE_URL,url_path)
    return PdDataBinance(dataname = df)

