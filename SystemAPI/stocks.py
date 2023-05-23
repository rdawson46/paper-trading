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
        
        # self.url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey={self.key}'
        # self.r = requests.get(self.url)
        # self.data = self.r.json()
    
    def getPrice(self, symbol):
        pass


attempt = StockAPI()
# print(attempt.data)