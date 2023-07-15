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
    df: DataFrame = DataFrame()
    model: GradientBoostingClassifier
    model_name: str
    get_last_candle: callable
    trade: TradingModel
    candle: str
    last_update_time: datetime = datetime.now().replace(second=0, microsecond=0) - timedelta(minutes=8)

    def __init__(self, trade: TradingModel) -> None:
        self.trade = trade
        self.candle = trade.candle_rel.name

        # main_root = 'app/ml_avidmech/file/trade_models/'
        main_root = 'File/trade_models/'

        # data_file_root = 'app/ml_avidmech/file/trade_data/'
        data_file_root = 'File/trade_data/'
        data_file_root += 'trade_data_history_' + self.trade.currency_disp() + '_' + self.candle + '.csv'

        # self.model = joblib.load('model_1min_EUR_USD.pkl')
        self.model_name = main_root + 'trade_model_' + self.trade.currency_disp() + '_' + self.candle + '.pkl'
        self.model = joblib.load(self.model_name)

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
        # self.df = self.get_history_from_file()

        start_time = datetime.utcnow() - timedelta(hours=8)
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
                (self.df['c'] - self.df['l']) / (self.df['h'] - self.df['l']))  # stochastic oscilator
        self.df['%D'] = self.df['%K'].rolling(window=3).mean()

        self.df['EMA_20'] = self.df['c'].ewm(span=20, adjust=False).mean()  # exponential moving average
        self.df['EMA_50'] = self.df['c'].ewm(span=50, adjust=False).mean()

        self.df['next_trend'] = self.df['o'].shift(-1) - self.df['c'].shift(-1)
        self.df['label'] = self.df['next_trend'].apply(lambda x: 0 if x >= 0.0006 else 1 if x <= -0.0006 else 2)

        # self.v= self.df.drop(['time', 'next_trend', 'label'], axis=1)
        # self.to_predict = self.v.iloc[-1]
        # self.df = self.df.dropna()

        return True

    def preprocess_last(self, last_candle: DataFrame):
        temp_df: DataFrame = self.df.iloc[-50:].reset_index(drop=True)
        temp_df = pd.concat([temp_df, last_candle], axis=0)

        temp_df = temp_df.shift(-1)[:-1]

        temp_df['trend'] = temp_df['o'] - temp_df['c']
        temp_df['MA_20'] = temp_df['c'].rolling(window=20).mean()  # moving average 20
        temp_df['MA_50'] = temp_df['c'].rolling(window=50).mean()  # moving average 50

        temp_df['L14'] = temp_df['l'].rolling(window=14).min()
        temp_df['H14'] = temp_df['h'].rolling(window=14).max()
        temp_df['%K'] = 100 * ((temp_df['c'] - temp_df['l']) / (temp_df['h'] - temp_df['l']))  # stochastic oscilator
        temp_df['%D'] = temp_df['%K'].rolling(window=3).mean()

        temp_df['EMA_20'] = temp_df['c'].ewm(span=20, adjust=False).mean()  # exponential moving average
        temp_df['EMA_50'] = temp_df['c'].ewm(span=50, adjust=False).mean()

        temp_df['next_trend'] = temp_df['o'].shift(-1) - temp_df['c'].shift(-1)
        temp_df['label'] = temp_df['next_trend'].apply(lambda x: 0 if x >= .0004 else 1 if x <= -.0004 else 2)

        second = temp_df.tail(2)
        last = second.tail(1)
        second = second.iloc[0]['next_trend']

        self.df.iloc[-1, self.df.columns.get_loc('next_trend')] = second
        self.df = pd.concat([self.df, last], axis=0)

    def update_model(self):
        self.model.fit(self.df.iloc[:, :-2], self.df.iloc[:, -2:])
        joblib.dump(self.model, self.model_name)
        print("Trading information updated.")
        return self.model

    def update(self) -> [bool, DataFrame]:
        flag, last_candle = self.check_update_df()

        if flag:
            if self.check_last_candle(last_candle):
                self.preprocess_last(last_candle)
                return True, last_candle
            else:
                return False, last_candle
        return False, last_candle

    def predict(self) -> [Union[PredictNeutralEnums, PredictBuyEnums, PredictSellEnums], float]:
        """

        :return:
            0:sell
            1:buy
            2:neutral
        """
        # self.update()
        try:
            predict = self.model.predict(self.df.iloc[-1, 1:-2].values.reshape(1, -1))[0]
            accuracy = round(float(max(self.model.predict_proba(self.df.iloc[-1, 1:-2].values.reshape(1, -1))[0])), 2)

            if predict == 2:
                return PredictEnums().neutral, accuracy

            if predict == 0 and accuracy >= 0.8:
                return PredictEnums().sell, accuracy

            if predict == 1 and accuracy >= 0.8:
                return PredictEnums().buy, accuracy

            return PredictEnums().neutral, accuracy
        except Exception as e:
            add_log(1, self.trade.id, 1, "error in ml trading predict : " + str(e))
            traceback.print_exc()
            print(self.df)
            # print("error in check update df : ", e)
            return PredictEnums().neutral, 0.0

    def check_update_df(self) -> [bool, DataFrame]:
        """
            check that df of data need update or not
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
            check that df of data need update or not
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
            check last candle is ok or not
        :param last_candle: df of last candle like
                          time                o        c        h        l
                    0 2023-07-15 05:43:00  1.12281  1.12281  1.12281  1.12281
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

        return True
