from datetime import datetime, timedelta
from time import sleep

import requests

from app.data_connector.model.data_connector import DataConnector
from app.logging.api import add_log
from app.market_trading.api import get_trading, get_all_trading
from app.ml_avidmech.model.enums import PredictSellEnums, PredictBuyEnums
from app.ml_avidmech.model.ml_trading import MlTrading
from app.oanda.api import get_last_candle_oanda
from core.database.database import create_db

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
# create_db()
#
# add_log(1, 3, 4, "we are open buying " + "asdasd")
# add_log(1, 3, 4, "we are open buying " + "asdas12d")
# add_log(1, 3, 4, "we are open buying " + "asd47asd")
# add_log(1, 3, 4, "we are open buying " + "asd21asd")

# asd.update()
# asd.update()
# # sleep(70)
# # asd.update()
# print(asd.predict())
# data_connector = DataConnector()
# asd = data_connector.create_order("EUR_USD", unit=-1000)


# start_time = "2023-06-13 03:00"
# end_time = "2023-06-14 10:00"
# asd = data_connector.get_history(name="EUR_CHF", start_time=start_time.strftime('%Y-%m-%d %H:%M:%S'), end_time=end_time.strftime('%Y-%m-%d %H:%M:%S'), candle="M1")

# {'id': '204', 'time': '2023-06-14T10:33:01.523387207Z', 'userID': 25830786, 'accountID': '101-001-25830786-001',
#  'batchID': '204', 'requestID': '79132289255640649', 'type': 'MARKET_ORDER', 'instrument': 'CAD_CHF', 'units': '1000.0',
#  'timeInForce': 'FOK', 'positionFill': 'DEFAULT', 'reason': 'CLIENT_ORDER',
#  'stopLossOnFill': {'distance': '0.1', 'timeInForce': 'GTC'}}

# trades = get_all_trading()
# for trade in trades:
#     print(trade.currency_disp("_"))
# data_connector.open_trade_window()
# print(asd)
# api.create_order(instrument="EUR_USD", units=1000, sl_distance=0.1)
# model = joblib.load('model_1min_EUR_USD.pkl')
# trading = Trading(country1, country2, last_candle, model)
