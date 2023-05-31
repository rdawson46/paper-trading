from dotenv.main import load_dotenv
import os
import requests
from time import sleep


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

        r = requests.get(self.url+query)
        data = r.json()

        if 'Note' in data:
            sleep(3)
            value = self.getPrice(symbol)
            return value

        return data['Global Quote']['05. price']

    def buyStock(self, symbol, money)-> list[float]:
        # gets the price and then math
        sharePrice = self.getPrice(symbol)

        shares = money / sharePrice

        return [shares, sharePrice]


if __name__ == '__main__':
    attempt = StockAPI()
    print(attempt.getPrice('aapl'))