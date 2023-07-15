# from datetime import datetime, timedelta
# from time import sleep
#
# import requests
#
# from app.data_connector.model.data_connector import DataConnector
# from app.logging.api import add_log
# from app.market_trading.api import get_trading, get_all_trading
# from app.ml_avidmech.model.enums import PredictSellEnums, PredictBuyEnums
# from app.ml_avidmech.model.ml_trading import MlTrading
# from app.oanda.api import get_last_candle_oanda
# from datetime import datetime, timedelta
# from time import sleep
# from time import sleep

# print(asd.empty)
# # sleep(60)
# from app.logging.api import add_log
# from app.logging.api import add_log
# from core.database.database import create_db
# from app.data_connector.model.data_connector import DataConnector


# print(get_history_quotex("EUR_USD",start_time.strftime('%Y-%m-%d %H:%M:%S'),end_time.strftime('%Y-%m-%d %H:%M:%S'),"M1"))


# print(get_history_oanda("EUR_USD",start_time.strftime('%Y-%m-%d %H:%M:%S'),end_time.strftime('%Y-%m-%d %H:%M:%S'),"M1"))


# # import logging
# #logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
# account=Quotex(set_ssid=ssid,host=host,user_agent=user_agent,websocket_cookie=weboscket_cookie)
# check_connect,message=account.connect()
# import time
# print(check_connect,message)
# if check_connect:
#     print("\n\n------get")
#     a=account.get_candle_v2("NZDUSD_otc",180)
#     print(a)


# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
# url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=1min&apikey=demo'
# r = requests.get(url)
# data = r.json()
#
# print(data)

# Example usage
# asd = {'id': '0f8e310d-1873-4c58-8035-e76552d98536', 'openTime': '2023-07-03 11:24:52',
#        'closeTime': '2023-07-03 11:26:00', 'openTimestamp': 1688383492, 'closeTimestamp': 1688383560, 'uid': 24692142,
#        'isDemo': 1, 'tournamentId': 0, 'amount': 10, 'purchaseTime': 1688383530, 'profit': 8.7, 'percentProfit': 87,
#        'percentLoss': 100, 'openPrice': 1.08983, 'copyTicket': '', 'closePrice': 0, 'command': 0, 'asset': 'EURUSD',
#        'nickname': '#24692142', 'accountBalance': 9876.7, 'requestId': '1', 'openMs': 40, 'currency': 'USD'}

# add_log(1, 3, 6, "asd")
#
# from app.quotex.api import qx_api_class
# from core.database.database import create_db
#
# print(True in asd2)


