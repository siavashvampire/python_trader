from datetime import datetime, timedelta
from threading import Thread
from time import sleep
from typing import Callable, Optional

from PyQt5.QtWidgets import QLabel

from app.data_connector.model.data_connector import DataConnector
# from app.logging.api import add_log
from app.market_trading.model.trading_thread_model import TradingThreadModel
from app.ml_avidmech.model.enums import PredictNeutralEnums, PredictBuyEnums

Force2Trade = False


class MainTradingThreadModel:
    """
        the main thread class
    """
    thread: Thread
    trade_threads: list[TradingThreadModel]
    time: int
    amount: int
    max_trading_label: QLabel = None
    max_trading_value_label: QLabel = None
    balance_value_label: QLabel = None
    trading: bool = False
    buy_time: datetime = datetime.now() - timedelta(minutes=8)

    def __init__(self, trade_threads: list[TradingThreadModel]) -> None:
        self.trade_threads = trade_threads
        self.stop_thread = False
        self.last_check_time = datetime.now()
        self.last_check_time_2 = datetime.now()
        self.data_connector = DataConnector()

        self.thread = Thread(target=self.main_thread, args=(lambda: self.stop_thread,))
        # self.Thread.start()

    def main_thread(self, stop_thread: Callable[[], bool]) -> None:
        """
            the main thread
        """
        while True:
            sleep(0.1)
            if (datetime.now() - self.last_check_time).seconds > 2:
                try:
                    self.make_all_trade_off_color()
                    max_trade = self.find_max_trade()
                    if max_trade is not None:
                        self.max_trading_label.setText(max_trade.name)
                        self.max_trading_value_label.setText(str(round(max_trade.accuracy * 100, 2)) + "%")
                        max_trade.change_color(True)
                        self.create_order_from_trade(max_trade)
                        self.make_all_trade_invalid()
                    else:
                        self.max_trading_label.setText("nothing")
                        self.max_trading_value_label.setText("0%")

                    self.last_check_time = datetime.now()
                except:
                    pass

            if (datetime.now() - self.last_check_time_2).seconds > 20:
                try:
                    self.balance_value_label.setText("$" + str(self.data_connector.get_balance()))

                except:
                    pass

                self.last_check_time_2 = datetime.now()

            if stop_thread():
                # print("Main Rendering Thread", "Stop")
                break

    def start_thread(self):
        """
            start the main thread
        """
        self.stop_thread = False
        self.thread = Thread(target=self.main_thread, args=(lambda: self.stop_thread,))
        self.thread.start()

    def stop_main_thread(self):
        """
            stop the main thread
        """
        self.stop_thread = True
        self.thread.join()

    def check(self) -> None:
        """
            check the tread if it's dead, restart thread
        """
        if not (self.thread.is_alive()):
            self.stop_thread = False
            self.restart_thread()

    def restart_thread(self) -> None:
        """
            restart thread
        """
        if not (self.thread.is_alive()):
            self.stop_thread = False
            self.thread = Thread(target=self.main_thread, args=(lambda: self.stop_thread,))
            self.thread.start()

    def find_max_trade(self) -> Optional[TradingThreadModel]:
        """
            find trade that has max accuracy
        :return:
            return trade or None if cant find any trade
        """
        temp_accuracy = 0.80
        temp_trade = None
        for trade in self.trade_threads:
            if trade.valid_predict:
                if temp_accuracy < trade.accuracy and not isinstance(trade.predict, PredictNeutralEnums):
                    temp_accuracy = trade.accuracy
                    temp_trade = trade

        if Force2Trade:
            temp_trade = self.trade_threads[1]
            temp_trade.predict = PredictBuyEnums
            temp_trade.accuracy = 0.90

        return temp_trade

    def make_all_trade_off_color(self):
        """
            make all trades off color
        """
        for trade in self.trade_threads:
            trade.change_color()

    def make_all_trade_invalid(self):
        """
            make all trades invalid
        """
        for trade in self.trade_threads:
            trade.valid_predict = False

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
        if not isinstance(trade.predict, PredictNeutralEnums) and (datetime.now() - self.buy_time).seconds > 65:
            # TODO: in aslan ham doros nis v bayad prop ham tosh check beshe
            flag, buy_info = self.data_connector.create_order(trade.name, trade.predict.get_unit(self.amount),
                                                              self.time)

            if flag:
                self.buy_time = datetime.now()
            else:
                print("buy_info : ", buy_info)
            # print("Get: ", self.qx_api.check_win(buy_info["id"]))
