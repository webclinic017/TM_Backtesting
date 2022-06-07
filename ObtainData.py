# Author: Cholian Li
# Contact: 
# cholianli970518@gmail.com
# Created at 20220601

import hmac
import time
import hashlib
import requests
from urllib.parse import urlencode
import pandas as pd
import datetime


# used for sending public data request
def send_public_request(url_path, payload={}):
    query_string = urlencode(payload, True)
    url = BASE_URL + url_path
    if query_string:
        url = url + '?' + query_string
    # print("{}".format(url))
    # response = dispatch_request('GET')(url=url)
    response = requests.get(url)
    return response.json()

def kline_data(stime, etime, symbol = 'BTCUSDT', interval = '1d'):
    
    stimestamp = int(datetime.datetime.strptime(stime, "%Y-%m-%d").timestamp()*1000)
    etimestamp = int(datetime.datetime.strptime(etime, "%Y-%m-%d").timestamp()*1000)
    params = {
        'symbol': symbol,
        'interval': interval,
        'startTime': stimestamp,
        'endTime': etimestamp,
        'limit': 1000,
    }
    url_path = '/fapi/v1/klines'
    response = send_public_request(url_path, params)
    data = pd.DataFrame(response)

    col = ['time','Open','High','Low','Close','Volume','Close time','Quote asset volume','Number of trades',
        'Taker buy volume','Taker buy quote asset volume','Ignore']

    data.columns = col
    #       transfer the timestamp into time
    data['time'] = pd.to_datetime(data['time'],unit='ms',utc=True).dt.strftime('%Y-%m-%d')
    data['Close time'] = pd.to_datetime(data['Close time'],unit='ms',utc=True).dt.strftime('%Y-%m-%d')
    
    data.iloc[:,[1,2,3,4,5,7,9,10]] = data.iloc[:,[1,2,3,4,5,7,9,10]].astype(float)
    
    return data.iloc[:,[0,1,2,3,4,5,7,9,10]]
    
if __name__ == '__main__':
    
    stime = "2021-01-02"
    etime = "2022-06-02"
    symbol = 'BTCUSDT'
    interval = '1d'
    
    # for future market
    global BASE_URL
    BASE_URL = 'https://fapi.binance.com' # production base url
    
    data = kline_data(stime, etime, symbol = 'ETHUSDT', interval = '1d')
    data.to_csv('data/ETH_1d.csv',index = False)