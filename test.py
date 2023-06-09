import requests

from app.market_trading.api import get_trading
from app.ml_avidmech.model.ml_trading import MlTrading
from app.oanda.api import get_last_candle_oanda

# # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
# url = 'https://www.alphavantage.co/query?function=STOCHF&symbol=IBM&interval=daily&apikey=demo'
# r = requests.get(url)
# data = r.json()
#
# print(data)

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
# url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=1min&apikey=demo'
# r = requests.get(url)
# data = r.json()
#
# print(data)


# Example usage
trade = get_trading(3)
asd = MlTrading(trade)
asd.preprocess()
print(asd.predict())



# model = joblib.load('model_1min_EUR_USD.pkl')
# trading = Trading(country1, country2, last_candle, model)
