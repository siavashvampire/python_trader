from datetime import datetime
from threading import Thread
from time import sleep
from typing import Callable, Optional

from PyQt5.QtWidgets import QLabel

from app.data_connector.model.data_connector import DataConnector
from app.market_trading.model.trading_thread_model import TradingThreadModel
from app.ml_avidmech.model.enums import PredictNeutralEnums, PredictBuyEnums, PredictSellEnums, PredictEnums


class MainTradingThreadModel:
    thread: Thread
    trade_threads: list[TradingThreadModel]
    time: int
    amount: int
    max_trading_label: QLabel = None
    max_trading_value_label: QLabel = None
    balance_value_label: QLabel = None
    trading: bool = False

    def __init__(self, trade_threads: list[TradingThreadModel]) -> None:
        self.trade_threads = trade_threads
        self.stop_thread = False
        self.last_check_time = datetime.now()
        self.data_connector = DataConnector()

        self.Thread = Thread(target=self.main_thread, args=(lambda: self.stop_thread,))
        # self.Thread.start()

    def main_thread(self, stop_thread: Callable[[], bool]) -> None:
        while True:
            sleep(1)

            if (datetime.now() - self.last_check_time).seconds > 10:
                try:
                    self.make_all_trade_off_color()
                    max_trade = self.find_max_trade()
                    if max_trade is not None:
                        self.max_trading_label.setText(max_trade.name)
                        self.max_trading_value_label.setText(str(round(max_trade.accuracy * 100, 2)) + "%")
                        max_trade.change_color(True)
                        self.create_order_from_trade(max_trade)
                        # print(max_trade.accuracy)
                    else:
                        self.max_trading_label.setText("nothing")
                        self.max_trading_value_label.setText("0%")

                    self.balance_value_label.setText("$" + str(self.data_connector.get_balance()))
                    self.last_check_time = datetime.now()
                except:
                    sleep(1)

            if stop_thread():
                # print("Main Rendering Thread", "Stop")
                break

    def start_thread(self):
        self.stop_thread = False
        self.Thread = Thread(target=self.main_thread, args=(lambda: self.stop_thread,))
        self.Thread.start()

    def stop_main_thread(self):
        self.stop_thread = True
        self.Thread.join()

    def check(self) -> None:
        if not (self.Thread.is_alive()):
            self.stop_thread = False
            self.restart_thread()

    def restart_thread(self) -> None:
        if not (self.Thread.is_alive()):
            self.stop_thread = False
            self.Thread = Thread(target=self.main_thread, args=(lambda: self.stop_thread,))
            self.Thread.start()

    def find_max_trade(self) -> Optional[TradingThreadModel]:
        """
            find trade that has max accuracy
        :return:
            return trade or None if cant find any trade
        """
        temp_accuracy = 0.80
        temp_trade = None
        for trade in self.trade_threads:
            if temp_accuracy < trade.accuracy and not isinstance(trade.predict, PredictNeutralEnums):
                temp_accuracy = trade.accuracy
                temp_trade = trade

        return temp_trade

    def make_all_trade_off_color(self):
        for trade in self.trade_threads:
            trade.change_color()

    def set_time(self, time: int):
        """
        set time
        :param time:
        """
        self.time = time

    def set_amount(self, amount: int):
        """
        set amount
        :param amount:
        """
        self.amount = amount

    def create_order_from_trade(self, trade: TradingThreadModel):
        """
            create order from trade
        :param trade:
        """
        self.trading = True
        if not isinstance(trade.predict, PredictNeutralEnums):
            # TODO:vaghti mikhare v mifroshe neveshte mide serfan bayad y True False bede v in aslan ham doros nis v
            #  bayad prop ham tosh check beshe
            buy_info = self.data_connector.create_order(trade.name,
                                                        trade.predict.get_unit(self.amount), self.time)
            sleep(65)
            # print("Get: ", self.qx_api.check_win(buy_info["id"]))

        # for test
        # if isinstance(self.state, PredictNeutralEnums):
        #     predict = PredictSellEnums()
        # elif isinstance(self.state, PredictSellEnums):
        #     predict = PredictBuyEnums()

        # if isinstance(self.state, PredictNeutralEnums):
        #     if not isinstance(predict, PredictNeutralEnums):
        #         self.create_order_from_predict(predict)
        #         print("we are ", predict, self.name)
        #         if isinstance(predict, PredictBuyEnums):
        #             add_log(1, self.trade.id, 4, "we are open buying " + self.name)
        #         elif isinstance(predict, PredictSellEnums):
        #             add_log(1, self.trade.id, 2, "we are open selling " + self.name)
        #         # TODO:inja bayad ba TRUE False k az order migire moshakhas kone state ro
        #         self.state = predict
        #
        # elif isinstance(self.state, PredictBuyEnums):
        #     if not isinstance(predict, PredictBuyEnums):
        #         self.create_order_from_predict(PredictSellEnums())
        #         add_log(1, self.trade.id, 5, "we are close buying " + self.name)
        #         print("we are ", PredictNeutralEnums())
        #         self.state = PredictNeutralEnums()
        #
        # elif isinstance(self.state, PredictSellEnums):
        #     if not isinstance(predict, PredictSellEnums):
        #         self.create_order_from_predict(PredictBuyEnums())
        #         add_log(1, self.trade.id, 3, "we are close selling " + self.name)
        #         print("we are ", PredictNeutralEnums())
        #         self.state = PredictNeutralEnums()
