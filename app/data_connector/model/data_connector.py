import pandas as pd

from app.data_connector.model.enums import APIUsed

from core.config.Config import api_used


class DataConnector:
    api_enums: APIUsed

    def __init__(self):
        self.api_enums = APIUsed()

        if api_used == self.api_enums.oanda:
            from app.oanda.api import get_real_time_data_oanda, get_history_oanda, get_last_candle_oanda, \
                create_order_oanda, trade_window_url_oanda, prepare_api_oanda, close_api_oanda, get_balance_oanda, \
                open_trade_window_oanda
            self.trade_window_url = trade_window_url_oanda
            self.prepare_api = prepare_api_oanda
            self.get_real_time_data = get_real_time_data_oanda
            self.get_history = get_history_oanda
            self.get_last_candle = get_last_candle_oanda
            self.create_order = create_order_oanda
            self.get_balance = get_balance_oanda
            self.close_api = close_api_oanda
            self.open_trade_window = open_trade_window_oanda
            # self.check_asset = check_asset_oanda

        if api_used == self.api_enums.quotex:
            from app.quotex.api import trade_window_url_quotex_main, qx_api_class

            self.trade_window_url = trade_window_url_quotex_main
            self.prepare_api = qx_api_class.prepare_api_quotex
            self.get_real_time_data = qx_api_class.get_real_time_data_quotex
            self.get_last_candle = qx_api_class.get_last_candle_quotex
            self.create_order = qx_api_class.create_order_quotex
            self.get_balance = qx_api_class.get_balance_quotex
            self.get_history = qx_api_class.get_history_quotex
            self.close_api = qx_api_class.close_api_quotex
            self.open_trade_window = qx_api_class.open_trade_window_quotex
            self.start_candles_stream = qx_api_class.start_candles_stream_quotex
            self.stop_candles_stream = qx_api_class.stop_candles_stream_quotex
            self.check_asset = qx_api_class.check_asset

    @staticmethod
    def get_history_from_file(name: str) -> pd.DataFrame:
        df = pd.read_csv(name)
        return df
