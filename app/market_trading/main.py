from datetime import datetime, timedelta
from threading import Thread
from time import sleep
from typing import Callable, Optional

from PyQt5.QtWidgets import QLabel

from app.data_connector.model.data_connector import DataConnector
from app.logging.api import add_log
from app.market_trading.model.trading_thread_model import TradingThreadModel
from app.ml_avidmech.model.enums import PredictNeutralEnums, PredictBuyEnums
from queue import Queue

from app.telegram_bot.api import add_message

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
    trade_log_queue: Queue[list[int, int]]

    def __init__(self, trade_threads: list[TradingThreadModel]) -> None:
        self.trade_log_queue = Queue()
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
                        self.max_trading_label.setText(" nothing")
                        self.max_trading_value_label.setText("0%")

                    self.last_check_time = datetime.now()
                except:
                    pass

            if (datetime.now() - self.last_check_time_2).seconds > 20:
                try:
                    self.balance_value_label.setText("$" + str(self.data_connector.get_balance()))
                    trading_web_id, trade_id = self.trade_log_queue.get(timeout=1)
                    check_win = self.data_connector.check_win(trading_web_id)

                    if check_win is not None:
                        # print("check win not None: ", check_win['profit'])
                        if check_win['profit'] >= 0:
                            txt = "we win " + str(check_win['profit']) + " in " + str(check_win['asset'])
                            add_log(1, trade_id, 7, txt)
                            add_message(txt)
                        else:
                            txt = "we lose " + str(check_win['profit']) + " in " + str(check_win['asset'])
                            add_log(1, trade_id, 8, txt)
                            add_message(txt)
                    else:
                        self.trade_log_queue.put([trading_web_id, trade_id])

                    self.trade_log_queue.task_done()
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

            self.trade_log_queue.put([buy_info["id"], trade.trade.id])

            if flag:
                self.buy_time = datetime.now()
            else:
                print("buy_info : ", buy_info)
