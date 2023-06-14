from datetime import datetime
from threading import Thread
from time import sleep
from typing import Callable, Union

from PyQt5.QtWidgets import QLabel

from app.data_connector.model.data_connector import DataConnector
from app.logging.api import add_log
from app.market_trading.model.trading_model import TradingModel
from app.ml_avidmech.model.enums import PredictEnums, PredictNeutralEnums, PredictBuyEnums, PredictSellEnums
from app.ml_avidmech.model.ml_trading import MlTrading


class TradingThreadModel:
    thread: Thread
    name: str
    state: Union[PredictNeutralEnums, PredictBuyEnums, PredictSellEnums]

    def __init__(self, trade: TradingModel, q_label_name: QLabel, q_label_value: QLabel) -> None:
        self.trade = trade
        self.q_label_name = q_label_name
        self.q_label_value = q_label_value
        self.stop_thread = False
        self.last_update_time = datetime.now()
        self.state = PredictEnums().neutral
        self.state_unit = 0

        self.name = self.trade.currency_disp("_")
        self.data_connector = DataConnector()

        self.get_real_time_data = lambda: self.data_connector.get_real_time_data(self.name)

        self.q_label_name.setText(self.name)
        self.ml_trading = MlTrading(trade)

        self.Thread = Thread(target=self.getting_data_thread, args=(lambda: self.stop_thread,))
        # self.Thread.start()

    def getting_data_thread(self, stop_thread: Callable[[], bool]):
        self.ml_trading.preprocess()

        while True:
            response = self.get_real_time_data()
            value = str(response.asks[0].dict()['price'])
            self.q_label_value.setText(value)
            sleep(1)

            if (datetime.now() - self.last_update_time).seconds > 10:
                try:
                    predict = self.ml_trading.predict()

                    # for test
                    # if isinstance(self.state, PredictNeutralEnums):
                    #     predict = PredictSellEnums()
                    # elif isinstance(self.state, PredictSellEnums):
                    #     predict = PredictBuyEnums()

                    if isinstance(self.state, PredictNeutralEnums):
                        if not isinstance(predict, PredictNeutralEnums):
                            self.create_order_from_predict(predict)
                            print("we are ", predict, self.name)
                            if isinstance(predict, PredictBuyEnums):
                                add_log(1, self.trade.id, 4, "we are open buying " + self.name)
                            elif isinstance(predict, PredictSellEnums):
                                add_log(1, self.trade.id, 2, "we are open selling " + self.name)
                            # TODO:inja bayad ba TRUE False k az order migire moshakhas kone state ro
                            self.state = predict

                    elif isinstance(self.state, PredictBuyEnums):
                        if not isinstance(predict, PredictBuyEnums):
                            self.create_order_from_predict(PredictSellEnums())
                            add_log(1, self.trade.id, 5, "we are close buying " + self.name)
                            print("we are ", PredictNeutralEnums())
                            self.state = PredictNeutralEnums()

                    elif isinstance(self.state, PredictSellEnums):
                        if not isinstance(predict, PredictSellEnums):
                            self.create_order_from_predict(PredictBuyEnums())
                            add_log(1, self.trade.id, 3, "we are close selling " + self.name)
                            print("we are ", PredictNeutralEnums())
                            self.state = PredictNeutralEnums()

                    self.last_update_time = datetime.now()
                except Exception as e:
                    add_log(1, self.trade.id, 1, str(e))
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

    def restart_thread(self) -> None:
        if not (self.Thread.is_alive()):
            self.stop_thread = False
            self.Thread = Thread(target=self.getting_data_thread, args=(lambda: self.stop_thread,))
            self.Thread.start()
