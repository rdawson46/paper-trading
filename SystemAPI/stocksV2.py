import alpaca_trade_api as alpaca
from dotenv.main import load_dotenv
import os

class StockAPI:
    def __init__(self):
        load_dotenv(dotenv_path='./../.env')
        
        self.key = os.getenv('ALPACAKEY')
        self.secret = os.getenv('ALPACASECRET')
        self.url = 'https://paper-api.alpaca.markets'
        self.api = alpaca.REST(self.key, self.secret, self.url)

    def is_open(self)-> bool:
        return self.api.get_clock().is_open
    

    def getPrice(self, symbol)->float:
        return round(self.api.get_latest_bar(symbol).vw, 2)

    
    def buy_stock(self, symbol, amount) -> list[float]:
        sharePrice = self.getPrice(symbol)

        shares = sharePrice / amount

        return [shares, sharePrice]
    
if __name__ == '__main__':
    attempt = StockAPI()
    print(type(attempt.getPrice('aapl')))