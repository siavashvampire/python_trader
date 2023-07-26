# from app.data_connector.model.data_connector import DataConnector
# from app.logging.api import add_log
# from app.ml_avidmech.model.ml_trading import MlTrading
# from app.logging.api import get_log_by_trading, get_log_by_title, get_log_by_title_by_trading
# from app.country.api import get_country
# from app.market_trading.api import get_all_trades_by_country_id
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
# url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=1min&apikey=demo'
# r = requests.get(url)
# data = r.json()
#
# print(data)
# from app.logging.api import get_log_by_title_by_trading,get_log_by_title,get_log_by_trading
# from app.market_trading.api import get_trading
# from app.ml_avidmech.model.ml_trading import MlTrading
# Example usage
# asd = {'id': '0f8e310d-1873-4c58-8035-e76552d98536', 'openTime': '2023-07-03 11:24:52',
#        'closeTime': '2023-07-03 11:26:00', 'openTimestamp': 1688383492, 'closeTimestamp': 1688383560, 'uid': 24692142,
#        'isDemo': 1, 'tournamentId': 0, 'amount': 10, 'purchaseTime': 1688383530, 'profit': 8.7, 'percentProfit': 87,
#        'percentLoss': 100, 'openPrice': 1.08983, 'copyTicket': '', 'closePrice': 0, 'command': 0,
#        'asset': 'EURUSD' or CADCHF_otc,'nickname': '#24692142', 'accountBalance': 9876.7, 'requestId': '1',
#        'openMs': 40, 'currency': 'USD'}
from datetime import datetime, timedelta

from core.config.Config import time_format
from core.database.database import create_db

create_db()

from app.data_connector.model.data_connector import DataConnector
from app.market_trading.api import get_all_trading, get_trading

data_connector = DataConnector()

trades = get_all_trading()
candle = "M1"

# trade_data_history_CAD_CHF_M1

for trade in trades:
    asset = trade.currency_disp()
    start_time = datetime.utcnow() - timedelta(hours=8)
    end_time = datetime.utcnow()
    df1 = data_connector.get_history(asset, start_time.strftime(time_format), end_time.strftime(time_format), candle,
                                     "File/trade_data/trade_data_history_" + asset + "_" + candle + ".csv")
