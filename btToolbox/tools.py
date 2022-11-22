from .. import BinanceDataFormat


def binanceData(symbol,startTime,endTime,interval = '1d',BASE_URL = 'https://api.binance.com', url_path = '/api/v3/klines'):
    binance = Binance()
    data = binance.returnData(symbol,startTime,endTime,interval,BASE_URL,url_path)
    return data