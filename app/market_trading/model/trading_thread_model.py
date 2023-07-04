from datetime import datetime
from threading import Thread
from time import sleep
from typing import Callable, Union

from PyQt5.QtWidgets import QLabel

from app.data_connector.model.data_connector import DataConnector
from app.market_trading.model.trading_model import TradingModel
from app.ml_avidmech.model.enums import PredictEnums, PredictNeutralEnums, PredictBuyEnums, PredictSellEnums
from app.ml_avidmech.model.ml_trading import MlTrading
from core.theme.color.color import trade_on_bg_color, trade_on_text_color, trade_off_text_color, trade_off_bg_color


class TradingThreadModel:
    q_label_name: QLabel
    q_label_value: QLabel
    q_label_accuracy: QLabel
    q_label_predict: QLabel
    thread: Thread
    name: str
    accuracy: float = 0
    predict: Union[PredictNeutralEnums, PredictBuyEnums, PredictSellEnums]
    state: Union[PredictNeutralEnums, PredictBuyEnums, PredictSellEnums]

    def __init__(self, trade: TradingModel, q_label_name: QLabel, q_label_value: QLabel,
                 q_label_accuracy: QLabel, q_label_predict: QLabel) -> None:
        self.predict = PredictEnums().neutral
        self.trade = trade
        self.q_label_name = q_label_name
        self.q_label_value = q_label_value
        self.q_label_accuracy = q_label_accuracy
        self.q_label_predict = q_label_predict
        self.stop_thread = False
        self.last_update_time = datetime.now()
        self.state = PredictEnums().neutral
        self.state_unit = 0

        self.name = self.trade.currency_disp()
        self.data_connector = DataConnector()

        self.get_real_time_data = lambda: self.data_connector.get_real_time_data(self.name)

        self.q_label_name.setText(self.name)
        self.ml_trading = MlTrading(trade)

        self.Thread = Thread(target=self.getting_data_thread, args=(lambda: self.stop_thread,))
        # self.Thread.start()

    def change_color(self, state: bool = False):
        if state:
            css = "background-color:" + trade_on_bg_color + ";color: rgba(" + trade_on_text_color + ");"
        else:
            css = "background-color: " + trade_off_bg_color + ";color: rgba(" + trade_off_text_color + ");"

        self.q_label_name.setStyleSheet(css)
        self.q_label_value.setStyleSheet(css)
        self.q_label_accuracy.setStyleSheet(css)
        self.q_label_predict.setStyleSheet(css)

    def getting_data_thread(self, stop_thread: Callable[[], bool]) -> None:
        self.ml_trading.preprocess()

        while True:
            sleep(1)

            if (datetime.now() - self.last_update_time).seconds > 5:
                try:
                    self.ml_trading.update()
                    self.predict, self.accuracy = self.ml_trading.predict()
                    # value = str(self.get_real_time_data())
                    value = str(0)
                    self.q_label_value.setText(value)

                    self.q_label_accuracy.setText(str(round(self.accuracy * 100, 2)) + "%")
                    self.q_label_predict.setText(self.predict.__repr__())
                    self.last_update_time = datetime.now()
                except Exception as e:
                    sleep(1)
                    print("error in trading thread : " + str(e))
                    # add_log(1, self.trade.id, 1, str(e))
            if stop_thread():
                print("Main Rendering Thread", "Stop")
                break

    def create_order_from_predict(self, predict: Union[PredictNeutralEnums, PredictBuyEnums, PredictSellEnums]):
        if predict != PredictNeutralEnums:
            # TODO:vaghti mikhare v mifroshe neveshte mide serfan bayad y True False bede
            self.data_connector.create_order(self.name, predict.get_unit())

    def check(self) -> None:
        if not (self.Thread.is_alive()):
            self.stop_thread = False
            self.restart_thread()

    def start_thread(self):
        self.stop_thread = False
        self.Thread = Thread(target=self.getting_data_thread, args=(lambda: self.stop_thread,))
        self.Thread.start()

    def restart_thread(self) -> None:
        if not (self.Thread.is_alive()):
            self.stop_thread = False
            self.Thread = Thread(target=self.getting_data_thread, args=(lambda: self.stop_thread,))
            self.Thread.start()
