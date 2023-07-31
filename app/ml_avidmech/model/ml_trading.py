import traceback
from datetime import datetime, timedelta
from typing import Union

import joblib
import pandas as pd
from pandas import DataFrame
from sklearn.ensemble import GradientBoostingClassifier

from app.data_connector.model.data_connector import DataConnector
from app.logging.api import add_log
from app.market_trading.model.trading_model import TradingModel
from app.ml_avidmech.model.enums import PredictEnums, PredictNeutralEnums, PredictBuyEnums, PredictSellEnums
from core.config.Config import time_format


class MlTrading:
    """
        the main trading class
    """
    df: DataFrame = DataFrame()
    model: GradientBoostingClassifier
    otc_model: GradientBoostingClassifier
    model_name: str
    otc_model_name: str
    get_last_candle: callable
    trade: TradingModel
    candle: str
    last_update_time: datetime = datetime.now().replace(second=0, microsecond=0) - timedelta(minutes=8)
    counter: int = 730
    prefer_df_size: int = 80

    def __init__(self, trade: TradingModel) -> None:
        self.trade = trade
        self.candle = trade.candle_rel.name

        main_root = 'File/trade_models/'

        data_file_root = 'File/trade_data/'
        data_file_root += 'trade_data_history_' + self.trade.currency_disp() + '_' + self.candle + '.csv'

        # self.model = joblib.load('model_1min_EUR_USD.pkl')
        self.model_name = main_root + 'trade_model_' + self.trade.currency_disp() + '_' + self.candle + '.pkl'
        self.model = joblib.load(self.model_name)

        self.otc_model_name = main_root + 'trade_model_' + self.trade.currency_disp() + '_otc_' + self.candle + '.pkl'
        self.otc_model = joblib.load(self.model_name)

        self.data_connector = DataConnector()

        self.get_last_candle = lambda: self.data_connector.get_last_candle(self.trade.currency_disp(), self.candle)
        # self.get_history = lambda start_time, end_time: self.data_connector.get_history(
        #     name=self.trade.currency_disp("_"), start_time=start_time, end_time=end_time, candle=self.candle,
        #     csv_path='app/ml_avidmech/file/trade_data/' + 'trade_data_history_' + self.trade.currency_disp(
        #         "_") + '_' + self.candle + '.csv')
        self.get_history = lambda start_time, end_time: self.data_connector.get_history(
            name=self.trade.currency_disp(), start_time=start_time.strftime(time_format),
            end_time=end_time.strftime(time_format), candle=self.candle)

        self.check_asset = lambda: self.data_connector.check_asset(name=self.trade.currency_disp())

        self.get_history_from_file = lambda: self.data_connector.get_history_from_file(data_file_root)

    def preprocess(self) -> bool:
        """
            preprocess the ml_trading
        :return:

            if its prepare correctly, its return True,
            otherwise return False
        """
        # self.df = self.get_history_from_file()

        start_time = datetime.utcnow() - timedelta(hours=3)
        end_time = datetime.utcnow()
        self.df = self.get_history(start_time, end_time)

        if self.df is None or self.df.empty:
            return False

        self.df['trend'] = self.df['o'] - self.df['c']
        self.df['MA_20'] = self.df['c'].rolling(window=20).mean()  # moving average 20
        self.df['MA_50'] = self.df['c'].rolling(window=50).mean()  # moving average 50

        self.df['L14'] = self.df['l'].rolling(window=14).min()
        self.df['H14'] = self.df['h'].rolling(window=14).max()

        self.df['%K'] = 100 * (
                (self.df['c'] - self.df['L14']) / (self.df['H14'] - self.df['L14']))  # stochastic oscilator

        self.df['%D'] = self.df['%K'].rolling(window=3).mean()

        self.df['EMA_20'] = self.df['c'].ewm(span=20, adjust=False).mean()  # exponential moving average
        self.df['EMA_50'] = self.df['c'].ewm(span=50, adjust=False).mean()

        self.df['next_trend'] = self.df['o'].shift(-1) - self.df['c'].shift(-1)
        self.df['label'] = self.df['next_trend'].apply(lambda x: 0 if x >= 0.0009 else 1 if x <= -0.0009 else 2)

        # self.v= self.df.drop(['time', 'next_trend', 'label'], axis=1)
        # self.to_predict = self.v.iloc[-1]
        # self.df = self.df.dropna()

        return True

    def preprocess_last(self, last_candle: DataFrame) -> None:
        """
            preprocess the ml_trading for the last candle
        :return:

            if its prepare correctly, its return True,
            otherwise return False
        """
        temp_df: DataFrame = self.df.iloc[-60:].reset_index(drop=True)
        temp_df = pd.concat([temp_df, last_candle], axis=0)

        temp_df = temp_df.shift(-1)[:-1]

        temp_df['trend'] = temp_df['o'] - temp_df['c']
        temp_df['MA_20'] = temp_df['c'].rolling(window=20).mean()  # moving average 20
        temp_df['MA_50'] = temp_df['c'].rolling(window=50).mean()  # moving average 50

        temp_df['L14'] = temp_df['l'].rolling(window=14).min()
        temp_df['H14'] = temp_df['h'].rolling(window=14).max()

        temp_df['%K'] = 100 * (
                (temp_df['c'] - temp_df['L14']) / (temp_df['H14'] - temp_df['L14']))  # stochastic oscilator

        temp_df['%D'] = temp_df['%K'].rolling(window=3).mean()

        temp_df['EMA_20'] = temp_df['c'].ewm(span=20, adjust=False).mean()  # exponential moving average
        temp_df['EMA_50'] = temp_df['c'].ewm(span=50, adjust=False).mean()

        temp_df['next_trend'] = temp_df['o'].shift(-1) - temp_df['c'].shift(-1)
        temp_df['label'] = temp_df['next_trend'].apply(lambda x: 0 if x >= 0.0009 else 1 if x <= -0.0009 else 2)

        second = temp_df.tail(2)
        last = second.tail(1)
        second = second.iloc[0]['next_trend']

        self.df.iloc[-1, self.df.columns.get_loc('next_trend')] = second
        self.df = pd.concat([self.df, last], axis=0)

    def update_model(self) -> GradientBoostingClassifier:
        """
            update model
        :return:
            return updated model
        """
        main_data_path = "File/trade_data/"

        otc_data_file_path = main_data_path + "trade_data_history_" + self.trade.currency_disp() + "_otc_" + self.candle + ".csv"
        data_file_path = main_data_path + "trade_data_history_" + self.trade.currency_disp() + "_" + self.candle + ".csv"
        data = pd.read_csv(data_file_path)
        otc_data = pd.read_csv(otc_data_file_path)

        temp_model = joblib.load(self.model_name)
        temp_df: DataFrame = data.iloc[-720:].reset_index(drop=True)
        temp_df2 = pd.concat([data, temp_df], axis=0)
        temp_model.fit(temp_df2.iloc[-60000:, 1:-2], temp_df2.iloc[-60000:, -1:])
        joblib.dump(temp_model, self.model_name)
        self.model = temp_model

        temp_model = joblib.load(self.otc_model_name)
        temp_df: DataFrame = otc_data.iloc[-720:].reset_index(drop=True)
        temp_df2 = pd.concat([otc_data, temp_df], axis=0)
        temp_model.fit(temp_df2.iloc[-60000:, 1:-2], temp_df2.iloc[-60000:, -1:])
        joblib.dump(temp_model, self.otc_model_name)
        self.otc_model = temp_model

        return self.model

    def update(self) -> [bool, DataFrame]:
        """
            Update system
            its check update needed or not
            and if needed its make system update
        :return:
            True for if its update is correctly
            False for if its update is wrong
            and if its update is correctly its return candle too
        """
        flag, last_candle = self.check_update_df()

        if flag:
            if self.check_last_candle(last_candle):
                self.preprocess_last(last_candle)
                self.counter += 1
                # If the counter reaches 90, update the model and reset the counter

                return True, last_candle
            else:
                return False, last_candle
        return False, last_candle

    def predict(self) -> [Union[PredictNeutralEnums, PredictBuyEnums, PredictSellEnums], float]:
        """
            get predict of trade
        :return:
            0:sell
            1:buy
            2:neutral
        """
        # self.update()
        try:
            week = datetime.today().weekday()

            if week < 5:
                predict = self.model.predict(self.df.iloc[-1, 1:-2].values.reshape(1, -1))[0]
                accuracy = (
                    round(float(max(self.model.predict_proba(self.df.iloc[-1, 1:-2].values.reshape(1, -1))[0])), 2))
            else:
                predict = self.otc_model.predict(self.df.iloc[-1, 1:-2].values.reshape(1, -1))[0]
                accuracy = (
                    round(float(max(self.otc_model.predict_proba(self.df.iloc[-1, 1:-2].values.reshape(1, -1))[0])), 2))

            if predict == 2:
                return PredictEnums().neutral, accuracy

            if predict == 0 and accuracy >= 0.9:
                return PredictEnums().sell, accuracy

            if predict == 1 and accuracy >= 0.9:
                return PredictEnums().buy, accuracy

            return PredictEnums().neutral, accuracy

        except Exception as e:
            add_log(1, self.trade.id, 1, "error in ml trading " + self.trade.currency_disp() + " predict : " + str(e))
            traceback.print_exc()
            print("error in ml trading " + self.trade.currency_disp() + " ", self.trade.id)
            print(self.df)
            # print("error in check update df : ", e)
            return PredictEnums().neutral, 0.0

    def check_update_df(self) -> [bool, DataFrame]:
        """
            Check that df of data need update or not
        :return:
            True if it needs
            False if didn't need
        """
        try:
            temp_df_time_str = self.df.tail(1)['time'].values[0]
            temp_df_time = datetime.strptime(temp_df_time_str, time_format)
            temp_df_time = temp_df_time.replace(second=0, microsecond=0)

            now_date = datetime.utcnow().replace(second=0, microsecond=0)
            delta = temp_df_time - now_date

            if int(delta.total_seconds()) == 0:
                return False, DataFrame()

            last_candle = self.get_last_candle()
            last_candle_time = pd.Timestamp(last_candle['time'].values[0])
            last_candle_time.timestamp()
            delta = temp_df_time - last_candle_time

            if int(delta.total_seconds()) == 0:
                return False, DataFrame()
            else:
                return True, last_candle

        except Exception as e:
            traceback.print_exc()
            print("error in check update df : ", e)
            return False, DataFrame()

    def check_update_df_old(self, last_candle: DataFrame) -> bool:
        """
            Check that df of data need update or not
        :param last_candle: df of last candle
        :return:
            True if it needs
            False if didn't need
        """
        try:
            last_candle_time = pd.Timestamp(last_candle['time'].values[0])

            temp_df_time_str = self.df.tail(1)['time'].values[0]
            # type_temp_df_time_str = type(temp_df_time_str)

            # if type_temp_df_time_str == str:
            #     temp_df_time = datetime.strptime(temp_df_time_str, '%Y-%m-%d %H:%M:%S+00:00')
            #     # temp_df_time = datetime.strptime(temp_df_time_str, time_format)
            # elif type_temp_df_time_str == Timestamp:
            #     temp_df_time = pd.Timestamp(temp_df_time_str)
            # else:
            #     temp_df_time = pd.Timestamp(temp_df_time_str)
            temp_df_time = datetime.strptime(temp_df_time_str, time_format)

            return not temp_df_time.timestamp() == last_candle_time.timestamp()
        except:
            return False

    def __repr__(self):
        return "<MlTrading(%r,%r)>" % (self.trade.currency_disp(), self.candle)

    def check_last_candle(self, last_candle: DataFrame) -> bool:
        """
            Check last candle is ok or not
        :param last_candle: df of last candle like
                          time o c h l
                    0 2023-07-15 05:43:00  1.12281 1.12281 1.12281 1.12281
        :return:
            True if it is ok,
            False if it is wrong
        """

        if last_candle.empty:
            add_log(1, self.trade.id, 1, "last_candle is empty")
            return False

        if last_candle.shape[0] != 1:
            add_log(1, self.trade.id, 1,
                    "last_candle dimension is wrong the number of row is : " + str(last_candle.shape[0]))
            return False

        if last_candle.shape[1] != 5:
            add_log(1, self.trade.id, 1,
                    "last_candle dimension is wrong the number of column is : " + str(last_candle.shape[1]))
            return False

        keys = last_candle.keys()

        if 'time' not in keys:
            add_log(1, self.trade.id, 1, "last_candle does not have time in keys")
            return False

        if 'o' not in keys:
            add_log(1, self.trade.id, 1, "last_candle does not have o in keys")
            return False

        if 'c' not in keys:
            add_log(1, self.trade.id, 1, "last_candle does not have c in keys")
            return False

        if 'h' not in keys:
            add_log(1, self.trade.id, 1, "last_candle does not have h in keys")
            return False

        if 'l' not in keys:
            add_log(1, self.trade.id, 1, "last_candle does not have l in keys")
            return False

        first_row = last_candle.head(1)

        if not isinstance(first_row['time'].values[0], str):
            add_log(1, self.trade.id, 1, "last_candle time is not str")
            return False
        if not isinstance(first_row['o'].values[0], float):
            add_log(1, self.trade.id, 1, "last_candle o is not float")
            return False
        if not isinstance(first_row['c'].values[0], float):
            add_log(1, self.trade.id, 1, "last_candle c is not float")
            return False
        if not isinstance(first_row['h'].values[0], float):
            add_log(1, self.trade.id, 1, "last_candle h is not float")
            return False
        if not isinstance(first_row['l'].values[0], float):
            add_log(1, self.trade.id, 1, "last_candle l is not float")
            return False

        return True

    def reduce_df_size(self):
        """
            reduce the size of main df
        """
        self.df = self.df.tail(self.prefer_df_size).reset_index(drop=True)
