from datetime import datetime
from threading import Thread
from time import sleep
from typing import Callable

from PyQt5.QtWidgets import QLabel

from app.data_connector.model.data_connector import DataConnector
from app.market_trading.model.trading_model import TradingModel
from app.ml_avidmech.model.ml_trading import MlTrading


class TradingThreadModel:
    thread: Thread
    name: str

    def __init__(self, trade: TradingModel, q_label_name: QLabel, q_label_value: QLabel) -> None:
        self.trade = trade
        self.q_label_name = q_label_name
        self.q_label_value = q_label_value
        self.stop_thread = False
        self.last_update_time = datetime.now()

        self.name = self.trade.currency_disp("_")
        self.data_connector = DataConnector()

        self.get_real_time_data = lambda: self.data_connector.get_real_time_data(self.name)

        self.q_label_name.setText(self.name)
        self.ml_trading = MlTrading(trade)
        self.ml_trading.preprocess()

        self.Thread = Thread(target=self.getting_data_thread,
                             args=(lambda: self.stop_thread,))
        self.Thread.start()

    def getting_data_thread(self, stop_thread: Callable[[], bool]):
        while True:
            response = self.get_real_time_data()
            value = str(response.asks[0].dict()['price'])
            self.q_label_value.setText(value)
            sleep(1)

            if (datetime.now() - self.last_update_time).seconds > 60:
                predict = self.ml_trading.predict()
                self.last_update_time = datetime.now()

            if stop_thread():
                print("Main Rendering Thread", "Stop")
                break
