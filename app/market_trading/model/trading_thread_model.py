"""
    TradingThreadModel
"""
import traceback
from datetime import datetime, timedelta
from threading import Thread
from time import sleep
from typing import Callable, Union, Optional

from PyQt5.QtWidgets import QLabel

from app.data_connector.model.data_connector import DataConnector
from app.data_gathering.main import data_gathering
from app.market_trading.model.trading_model import TradingModel
from app.ml_avidmech.model.enums import PredictEnums, PredictNeutralEnums, PredictBuyEnums, PredictSellEnums
from app.ml_avidmech.model.ml_trading import MlTrading
from core.theme.style.style import trade_none_style, trade_on_style, trade_off_style


class TradingThreadModel:
    """
        TradingThreadModel
    """
    q_label_name: QLabel
    q_label_value: QLabel
    q_label_accuracy: QLabel
    q_label_predict: QLabel
    thread: Thread
    model_thread: Thread
    name: str
    accuracy: float = 0
    predict: Union[PredictNeutralEnums, PredictBuyEnums, PredictSellEnums]
    state: Union[PredictNeutralEnums, PredictBuyEnums, PredictSellEnums]
    valid_predict: bool = False
    update_time: int = 5  # update thread in second
    model_update_time: int = 720 * 60  # model update thread in second
    check_asset: Optional[bool] = None
    last_check_asset: Optional[bool] = None

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
        self.last_model_update_time = datetime.now() - timedelta(days=2)
        self.state = PredictEnums().neutral
        self.state_unit = 0

        self.name = self.trade.currency_disp()
        self.data_connector = DataConnector()

        self.get_real_time_data = lambda: self.data_connector.get_real_time_data(self.name)

        if self.q_label_name is not None:
            self.q_label_name.setText(self.name)
        self.ml_trading = MlTrading(trade)

        self.thread = Thread(target=self.getting_data_thread, args=(lambda: self.stop_thread,))
        self.model_thread = Thread(target=self.update_model_thread, args=(lambda: self.stop_thread,))
        # self.Thread.start()

    def change_color(self, state: Optional[bool] = False):
        """
            change color in ui
        :param state: Optional[bool]
            if it's None, it means that both markets are close
            if it's True, it means the main market is open
            and if it's False, it means the main market is close and ots is open
        """
        if self.check_asset is None:
            css = trade_none_style
        else:
            if state is None:
                css = trade_none_style
            else:
                if state:
                    css = trade_on_style
                else:
                    css = trade_off_style

        self.q_label_name.setStyleSheet(css)
        self.q_label_value.setStyleSheet(css)
        self.q_label_accuracy.setStyleSheet(css)
        self.q_label_predict.setStyleSheet(css)

    def getting_data_thread(self, stop_thread: Callable[[], bool]) -> None:
        """
            the main thread that updates df and set accuracy and predict
        :param stop_thread: this parameter can make thread stop when it's True
        """
        flag = False
        self.check_asset = self.ml_trading.check_asset()
        self.last_check_asset = self.ml_trading.check_asset()

        while not flag and self.check_asset is not None:
            flag = self.ml_trading.preprocess()
            sleep(2)
            if stop_thread():
                print("Main trade Thread ", self.trade.currency_disp(), " Stop")
                break

        while True:
            sleep(0.2)

            if (datetime.now() - self.last_update_time).total_seconds() > self.update_time:
                try:
                    self.check_asset = self.ml_trading.check_asset()

                    if self.last_check_asset != self.check_asset:
                        self.last_check_asset = self.check_asset
                        break

                    if self.check_asset is not None:
                        flag, _ = self.ml_trading.update()
                        if flag:
                            self.valid_predict = True

                        self.predict, self.accuracy = self.ml_trading.predict()
                        # value = str(self.get_real_time_data())
                        value = str(0)
                        self.q_label_value.setText(value)
                        self.q_label_accuracy.setText(str(round(self.accuracy * 100, 2)) + "%")
                        self.q_label_predict.setText(self.predict.__repr__())
                    else:
                        self.valid_predict = False
                        self.q_label_value.setText("trade is close")
                        self.q_label_accuracy.setText("0.0%")
                        self.q_label_predict.setText("trade is close")
                        self.change_color(None)

                    self.last_update_time = datetime.now()

                except Exception as e:
                    sleep(1)
                    traceback.print_exc()
                    print("error in trading getting data thread update code: ", e)
                    # add_log(1, self.trade.id, 1, str(e))

                if datetime.now().second > 10:
                    self.valid_predict = False

                self.calc_update_time()

            if stop_thread():
                print("Main trade Thread ", self.trade.currency_disp(), " Stop")
                break
            if self.ml_trading.df.shape[0] < 50:
                # print("Main trade Thread ", self.trade.currency_disp(), " Stop becuase ml_trading df shape is ",
                #       self.ml_trading.df.shape[0])
                break

    def update_model_thread(self, stop_thread: Callable[[], bool]) -> None:
        """
            the update model thread that updates model
        :param stop_thread: this parameter can make thread stop when it's True
        """

        while True:
            sleep(10)
            if (datetime.now() - self.last_model_update_time).total_seconds() > self.model_update_time:
                try:
                    if self.ml_trading.counter >= 720:
                        self.ml_trading.reduce_df_size()
                        data_gathering(self.ml_trading.trade.currency_disp())
                        self.ml_trading.update_model()
                        self.ml_trading.counter = 0
                        self.last_model_update_time = datetime.now()

                except Exception as e:
                    sleep(1)
                    traceback.print_exc()
                    print("error in trading update model thread update code: ", e)
                    # add_log(1, self.trade.id, 1, str(e))

            if stop_thread():
                print("Main trade Thread ", self.trade.currency_disp(), " Stop")
                break

    def create_order_from_predict(self, predict: Union[PredictNeutralEnums, PredictBuyEnums, PredictSellEnums]):
        """
            create order in market from predicted state
        :param predict: predict of AI that can be 3 type
        Neutral
        Buy
        sell
        """
        if predict != PredictNeutralEnums:
            # TODO:vaghti mikhare v mifroshe neveshte mide serfan bayad y True False bede
            self.data_connector.create_order(self.name, predict.get_unit())

    def check(self) -> None:
        """
            check thread is alive or not, and if it's dead,restart it
        """
        if not self.thread.is_alive() or not self.model_thread.is_alive():
            self.stop_thread = False
            self.restart_thread()

    def start_thread(self):
        """
            start thread
        """
        self.stop_thread = False
        self.thread = Thread(target=self.getting_data_thread, args=(lambda: self.stop_thread,))
        self.thread.start()
        self.model_thread = Thread(target=self.update_model_thread, args=(lambda: self.stop_thread,))
        self.model_thread.start()

    def restart_thread(self) -> None:
        """
            restart thread
        """
        if not self.thread.is_alive() or not self.model_thread.is_alive():
            self.stop_thread = True

            if self.thread.is_alive():
                self.thread.join()

            if self.model_thread.is_alive():
                self.model_thread.join()

            self.stop_thread = False
            self.thread = Thread(target=self.getting_data_thread, args=(lambda: self.stop_thread,))
            self.thread.start()
            self.model_thread = Thread(target=self.update_model_thread, args=(lambda: self.stop_thread,))
            self.model_thread.start()

    def calc_update_time(self):
        """
            calculate update thread time in sec based on the second we are in
        """
        second = datetime.now().second
        if second > 50:
            self.update_time = 1
        elif second > 10:
            self.update_time = 5

        self.model_update_time = 720 * 60
