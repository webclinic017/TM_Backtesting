import time
import requests
from urllib.parse import urljoin, urlencode
import datetime
import pandas as pd

class Binance():
    def __init__(self, BASE_URL = 'https://api.binance.com', url_path = '/api/v3/klines'):
        self.BASE_URL = BASE_URL
        self.url_path = url_path

    # used for sending public data request
    def send_public_request(self, url_path, payload={}):
        query_string = urlencode(payload, True)
        url = self.BASE_URL + url_path
        if query_string:
            url = url + '?' + query_string
        # print("{}".format(url))
        # response = dispatch_request('GET')(url=url)
        response = requests.get(url)
        return response.json()


    def kline_data(self, stime, etime, symbol = 'BTCUSDT', interval = '1d'):
        
        # stimestamp = int(datetime.datetime.strptime(stime, "%Y-%m-%d").timestamp()*1000)
        # etimestamp = int(datetime.datetime.strptime(etime, "%Y-%m-%d").timestamp()*1000)
        params = {
            'symbol': symbol,
            'interval': interval,
            'startTime': stime,
            'endTime': etime,
            'limit': 1000,
        }
        response = self.send_public_request(url_path=self.url_path,payload = params)
        data = pd.DataFrame(response)

        col = ['time','Open','High','Low','Close','Volume','Close_time','Quote_asset_volume','Number_of_trades',
            'Taker_buy_volume','Taker_buy_quote_asset_volume','Ignore']

        data.columns = col
        #       transfer the timestamp into time
        data['time'] = pd.to_datetime(data['time'],unit='ms',utc=True).dt.strftime('%Y-%m-%d %H:%M:%S')
        data['Close_time'] = pd.to_datetime(data['Close_time'],unit='ms',utc=True).dt.strftime('%Y-%m-%d %H:%M:%S')
        data['time'] = pd.to_datetime(data['time'])
        data['Close_time'] = pd.to_datetime(data['Close_time'])
        
        data.iloc[:,[1,2,3,4,5,7,9,10]] = data.iloc[:,[1,2,3,4,5,7,9,10]].astype(float)
        
        return data.iloc[:,:-1]


    def time_format(self, TimeString):
        TimeString = datetime.datetime.strptime(TimeString, "%Y-%m-%d %H:%M:%S")
        TimeString = datetime.datetime.timestamp(TimeString)*1000
        
        return str(int(TimeString))

    def start_end_time(self, startTime,interval,length = 1000):
    #     Due to the limit of the api, we need a function to help cut a long time into small period.
    #     The function input the start time and interval and return the start time and endtime. 
        
        startTime = int(startTime)/1000
        startTime = datetime.datetime.fromtimestamp(startTime)
        
    #     unit 
        unit = interval
    #     transfer the interval frequence
        if unit in ["1m","3m","5m","15m","30m"]:
            unit = 'm'
        elif unit in ["1h","2h","4h","6h","8h","12h"]:
            unit = 'hours'
        elif unit in ["1d","3d"]:
            unit = 'D'
        else:
            unit = 'W'
            
        endTime = pd.to_datetime(startTime)+pd.to_timedelta(length, unit = unit)

        startTime = datetime.datetime.timestamp(startTime)*1000
        endTime = datetime.datetime.timestamp(endTime)*1000
        
        return str(int(startTime)),str(int(endTime))


    def Long_data(self, pair,startTime,endTime,interval):
        data = pd.DataFrame()

        while int(endTime) > int(startTime):
            try :
                [startTime,eTime] = self.start_end_time(startTime=startTime,interval=interval)
                
                if int(eTime) >=int(endTime):
                    eTime = endTime
                    
                d = self.kline_data(stime = startTime, etime = eTime, symbol = pair, interval = interval)
                
                # log for the time
                # print(datetime.datetime.fromtimestamp(int(startTime)/1000),'finished!')
                startTime = eTime
                data = pd.concat([data,d],axis = 0)
            except :
                startTime = eTime
                time.sleep(0.1)
                continue
            time.sleep(0.1)
            
        return data

    def exchangeInfo(self, url_path):
        
        url = urljoin(self.BASE_URL, url_path)
        
        response = requests.get(url)

        data = response.json()
        data = pd.DataFrame(data['symbols'])
        return data


    def returnData(self, symbol,startTime,endTime,interval,BASE_URL, url_path):
        self.BASE_URL = BASE_URL
        self.url_path = url_path
        startTime = self.time_format(startTime)
        endTime = self.time_format(endTime)
        data = self.Long_data(pair = symbol,startTime = startTime,endTime = endTime,interval = interval)
        return data.set_index('time')

def binanceData(symbol,startTime,endTime,interval = '1d',BASE_URL = ' https://api.binance.com', url_path = '/api/v3/klines'):
    binance = Binance(BASE_URL=BASE_URL, url_path=url_path)
    data = binance.returnData(symbol,startTime,endTime,interval,BASE_URL,url_path)
    return data

if __name__ == '__main__':
    

    data = binanceData(symbol= 'BTCUSDT', interval = '1h', startTime = '2020-01-01 00:00:00', endTime = '2020-01-02 00:00:00')
    print(data.info())
    

    
    


