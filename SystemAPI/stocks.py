from dotenv.main import load_dotenv
import os
import requests


"""
API documentation @ https://www.alphavantage.co/documentation/
"""
class StockAPI:
    def __init__(self):
        load_dotenv(dotenv_path='./../.env')
        self.key = os.getenv('STOCKAPI')
        
        if self.key is None:
            raise ValueError
        
        self.url = 'https://www.alphavantage.co/'
        # r = requests.get(url)
        # data = r.json()
    
    def getPrice(self, symbol):
        query = f'query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={self.key}'

        r= requests.get(self.url+query)
        data = r.json()

        print(data['Global Quote']['05. price'])

    def buyStock(self, symbol, money):
        # gets the price and then math
        sharePrice = self.getPrice(symbol)

        shares = money / sharePrice

        return [shares, sharePrice]


attempt = StockAPI()
attempt.getPrice('crox')