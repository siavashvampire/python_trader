from threading import Thread
from time import sleep
from typing import Callable

from PyQt5.QtWidgets import QLabel

from app.market_trading.model.trading_model import TradingModel
from app.oanda.api import get_real_time_data


class TradingThreadModel:
    thread: Thread
    name: str

    def __init__(self, trade: TradingModel, q_label_name: QLabel, q_label_value: QLabel):
        self.trade = trade
        self.q_label_name = q_label_name
        self.q_label_value = q_label_value
        self.stop_thread = False

        self.name = self.trade.currency_disp("_")

        q_label_name.setText(self.name)

        self.Thread = Thread(target=self.getting_data,
                             args=(lambda: self.stop_thread,))
        self.Thread.start()

    def getting_data(self, stop_thread: Callable[[], bool]):
        while True:
            response = get_real_time_data(self.name)
            value = str(response.asks[0].dict()['price'])
            self.q_label_value.setText(value)
            sleep(1)
            if stop_thread():
                print("Main Rendering Thread", "Stop")
                break
