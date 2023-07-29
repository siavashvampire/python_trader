import os
from datetime import datetime, timedelta

import pandas as pd

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


def get_start_time_from_file(file_path_in: str) -> datetime:
    data = pd.read_csv(file_path_in)
    return datetime.strptime(data.tail(1)['time'].values[0], time_format).replace(second=0, microsecond=0)


for trade in trades:
    asset = trade.currency_disp()
    print(asset)
    file_path = main_path + "trade_data_history_" + asset + "_" + candle + ".csv"

    end_time = datetime.utcnow()
    end_time = end_time.replace(second=0, microsecond=0)
    if not file_exist(asset):
        start_time = datetime.utcnow() - timedelta(hours=4)
        start_time = start_time.replace(second=0, microsecond=0)
    else:
        start_time = get_start_time_from_file(file_path)
        start_time = start_time + timedelta(minutes=1)

    df1 = data_connector.get_history(asset, start_time.strftime(time_format), end_time.strftime(time_format),
                                     candle, file_path)
