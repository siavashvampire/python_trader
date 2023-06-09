import pandas as pd

from app.data_connector.model.enums import APIUsed
from app.oanda.api import get_real_time_data_oanda, get_history_oanda, get_last_candle_oanda, create_order_oanda
from core.config.Config import api_used


class DataConnector:
    api_enums: APIUsed

    def __init__(self):
        self.api_enums = APIUsed()

        if api_used == self.api_enums.oanda:
            self.get_real_time_data = get_real_time_data_oanda
            self.get_history = get_history_oanda
            self.get_last_candle = get_last_candle_oanda
            self.create_order = create_order_oanda

    @staticmethod
    def get_history_from_file(name:str)->pd.DataFrame:
        df = pd.read_csv(name)
        return df
