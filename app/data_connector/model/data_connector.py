import pandas as pd
from selenium.webdriver.chrome.webdriver import WebDriver

from app.data_connector.model.enums import APIUsed
from app.oanda.api import get_real_time_data_oanda, get_history_oanda, get_last_candle_oanda, create_order_oanda, \
    trade_window_url_oanda, prepare_api_oanda, close_api_oanda
from app.quotex.api import trade_window_url_quotex, prepare_api_quotex, create_order_quotex, get_balance_quotex, \
    close_api_quotex, get_real_time_data_quotex
from core.config.Config import api_used


class DataConnector:
    driver: WebDriver
    api_enums: APIUsed

    def __init__(self):
        self.api_enums = APIUsed()

        if api_used == self.api_enums.oanda:
            self.trade_window_url = trade_window_url_oanda
            self.prepare_api = prepare_api_oanda
            self.get_real_time_data = get_real_time_data_oanda
            self.get_history = get_history_oanda
            self.get_last_candle = get_last_candle_oanda
            self.create_order = create_order_oanda
            # self.get_balance = get_balance_quotex
            self.close_api = close_api_oanda

        if api_used == self.api_enums.quotex:
            self.trade_window_url = trade_window_url_quotex
            self.prepare_api = prepare_api_quotex
            self.get_real_time_data = get_real_time_data_quotex
            # self.get_last_candle = get_last_candle_oanda
            self.create_order = create_order_quotex
            self.get_balance = get_balance_quotex
            # self.get_history = get_history_oanda
            self.close_api = close_api_quotex

    @staticmethod
    def get_history_from_file(name: str) -> pd.DataFrame:
        df = pd.read_csv(name)
        return df

    def open_trade_window(self):
        self.get_real_time_data(name="EURUSD")
        # self.create_order(name="EURUSD", unit=-1)
