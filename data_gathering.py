import os
from datetime import datetime, timedelta

from core.config.Config import time_format
from core.database.database import create_db

create_db()

from app.data_connector.model.data_connector import DataConnector
from app.market_trading.api import get_all_trading

data_connector = DataConnector()

trades = get_all_trading()
candle = "M1"

main_path = "File/trade_data/"


def file_exist(asset_in):
    files = os.listdir(main_path)
    for file in files:
        if asset_in in file:
            return True

    return False


for trade in trades:
    asset = trade.currency_disp()
    print(asset)
    if not file_exist(asset):
        start_time = datetime.utcnow() - timedelta(days=93)
        end_time = datetime.utcnow()
        df1 = data_connector.get_history(asset, start_time.strftime(time_format), end_time.strftime(time_format),
                                         candle,
                                         main_path + "trade_data_history_" + asset + "_" + candle + ".csv")
