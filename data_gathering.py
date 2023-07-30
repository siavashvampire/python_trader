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


def file_exist(file_name_in: str):
    files = os.listdir(main_path)
    for file in files:
        if file_name_in == file:
            return True

    return False


def get_start_time_from_file(file_path_in: str) -> datetime:
    data_temp = pd.read_csv(file_path_in)
    try:
        start_time_temp = datetime.strptime(data_temp.tail(1)['time'].values[0], time_format).replace(second=0,
                                                                                                      microsecond=0)
    except:
        start_time_temp = datetime.utcnow() - timedelta(days=93)

    return start_time_temp


for trade in trades:
    asset = trade.currency_disp()
    print(asset)

    end_time = datetime.utcnow()
    end_time = end_time.replace(second=0, microsecond=0)

    force_otc = True
    file_path = main_path + "trade_data_history_" + asset + "_" + "otc_" + candle + ".csv"

    if not file_exist("trade_data_history_" + asset + "_" + "otc_" + candle + ".csv"):
        start_time = datetime.utcnow() - timedelta(days=93)
        start_time = start_time.replace(second=0, microsecond=0)
    else:
        start_time = get_start_time_from_file(file_path)
        start_time = start_time + timedelta(minutes=1)

    df1 = data_connector.get_history(asset, start_time.strftime(time_format), end_time.strftime(time_format),
                                     candle, file_path, force_otc=force_otc)

    force_otc = False
    file_path = main_path + "trade_data_history_" + asset + "_" + candle + ".csv"

    if not file_exist("trade_data_history_" + asset + "_" + candle + ".csv"):
        start_time = datetime.utcnow() - timedelta(days=93)
        start_time = start_time.replace(second=0, microsecond=0)
    else:
        start_time = get_start_time_from_file(file_path)
        start_time = start_time + timedelta(minutes=1)

    df1 = data_connector.get_history(asset, start_time.strftime(time_format), end_time.strftime(time_format),
                                     candle, file_path, force_otc=force_otc)

    try:
        data = pd.read_csv(file_path)
    except:
        data = pd.DataFrame()

    for index, row in data.iterrows():
        temp = row['o']
        if row['o'] == temp and row['c'] == temp and row['h'] == temp and row['l'] == temp:
            data = data.drop(index)

    data.to_csv(file_path, index=False, encoding='utf-8')
