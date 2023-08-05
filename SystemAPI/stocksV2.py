import alpaca_trade_api as alpaca
from dotenv.main import load_dotenv
import os
from datetime import datetime, timedelta

class StockAPI:
    def __init__(self):
        load_dotenv(dotenv_path='./../.env')
        
        self.key = os.getenv('ALPACAKEY')
        self.secret = os.getenv('ALPACASECRET')
        self.url = 'https://paper-api.alpaca.markets'
        self.api = alpaca.REST(self.key, self.secret, self.url)

    def is_open(self)-> bool:
        """
        returns if the market is open or not
        """
        return self.api.get_clock().is_open
    

    def getPrice(self, symbol)->float:
        """
        current price of an individual stock for SYMBOL
        """
        return round(self.api.get_latest_bar(symbol).vw, 2)
    
    def getWeekPrice(self, symbol)->list[float]:
        """
        returns a list of the most accurate prices
        """
        date = (datetime.now() - timedelta(weeks=2)).strftime('%Y-%m-%d')
        week = self.api.get_bars(symbol,timeframe='1day', start=date, limit=14)
        for index, value in enumerate(week):
            week[index] = [str(value.t)[:10], round(value.vw, 2)]
        return week
    
    def buy_stock(self, symbol, amount) -> list[float]:
        """
        Symbol -> stock\n
        Amount -> amount of money\n
        returns [number of shares, at share price]
        """
        sharePrice = self.getPrice(symbol)

        shares = sharePrice / amount

        return [shares, sharePrice]

    def sell_stock(self, symbol, shares) -> list[float]:
        """
        Symbol -> stock\n
        Shares -> number of shares\n
        returns [dollar amount, at share price]
        """
        sharePrice = self.getPrice(symbol)

        amount = shares * sharePrice

        return [amount, sharePrice]
    
    def getBar(self, symbol):
        return self.api.get_latest_bar(symbol)
    
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    attempt = StockAPI()
    week = attempt.getWeekPrice('aapl')

    # plt.figure(figsize=(10, 8))
    # plt.plot(train['date'], train['price'])
    # plt.plot(test['date'], test[['price', 'predictions']])
    # plt.title("AAPL Predictions")
    # plt.xlabel('Date')
    # plt.ylabel('Price')
    # plt.legend(['Train', "Test", "Predictions"])
    # plt.show()

    plt.figure(figsize=(10,8))
    plt.plot([i[0] for i in week], [i[1] for i in week])
    plt.show()