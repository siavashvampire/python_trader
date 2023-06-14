from datetime import datetime, timedelta
from typing import Union

import joblib
import pandas as pd
from pandas import DataFrame, Timestamp
from sklearn.ensemble import GradientBoostingClassifier

from app.data_connector.model.data_connector import DataConnector
from app.market_trading.model.trading_model import TradingModel
from app.ml_avidmech.model.enums import PredictEnums, PredictNeutralEnums, PredictBuyEnums, PredictSellEnums


class MlTrading:
    df: DataFrame
    model: GradientBoostingClassifier
    model_name: str
    get_last_candle: callable
    trade: TradingModel
    candle: str

    def __init__(self, trade: TradingModel) -> None:
        self.trade = trade
        self.candle = trade.candle_rel.name
        self.counter = 0
        self.counter2 = 0

        main_root = 'app/ml_avidmech/file/trade_models/'

        data_file_root = 'app/ml_avidmech/file/trade_data/'
        data_file_root += 'trade_data_history_' + self.trade.currency_disp("_") + '_' + self.candle + '.csv'

        # self.model = joblib.load('model_1min_EUR_USD.pkl')
        self.model_name = main_root + 'trade_model_' + self.trade.currency_disp("_") + '_' + self.candle + '.pkl'
        self.model = joblib.load(self.model_name)

        self.data_connector = DataConnector()

        self.get_last_candle = lambda: self.data_connector.get_last_candle(self.trade.currency_disp("_"), self.candle)
        # self.get_history = lambda start_time, end_time: self.data_connector.get_history(
        #     name=self.trade.currency_disp("_"), start_time=start_time, end_time=end_time, candle=self.candle,
        #     csv_path='app/ml_avidmech/file/trade_data/' + 'trade_data_history_' + self.trade.currency_disp(
        #         "_") + '_' + self.candle + '.csv')
        self.get_history = lambda start_time, end_time: self.data_connector.get_history(
            name=self.trade.currency_disp("_"), start_time=start_time.strftime('%Y-%m-%d %H:%M:%S'),
            end_time=end_time.strftime('%Y-%m-%d %H:%M:%S'), candle=self.candle)

        self.get_history_from_file = lambda: self.data_connector.get_history_from_file(data_file_root)
        # preprocessed = trading.preprocess(last_candle)
        # updated_model = trading.update(model)
        # predicted_value = trading.predict(preprocessed)
        # print(f"Prediction: {predicted_value}")

    def preprocess(self) -> DataFrame:
        # self.df = self.get_history_from_file()
        
        start_time = datetime.utcnow() - timedelta(hours=8)
        end_time = datetime.utcnow()
        self.df = self.get_history(start_time, end_time)

        self.df = self.df.drop(['volume', 'complete'], axis=1)

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

        return self.df

    def preprocess_last(self, last_candle: DataFrame):
        last_candle = last_candle.drop(['volume', 'complete'], axis=1)

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

        # Check if the counter reaches 10
        # if self.counter == 10:
        #     # Call update when 10 candles are added
        #     self.update_model()
        #     self.counter = 0
        # print(self.temp_df.iloc[-1])
        # # if self.counter2 == 2:
        # self.df = pd.concat([self.temp_df.iloc[-1], self.df])
        # #     self.counter2 = 0
        #
        # # self.v = self.df.drop(['time'], axis=1)
        # # self.to_predict = self.v
        # # self.df = self.df.dropna()

        # print(self.temp_df)
        # print(self.df.tail())
        # return self.temp_df, self.df

    def update_model(self):
        self.model.fit(self.df.iloc[:, :-2], self.df.iloc[:, -2:])
        joblib.dump(self.model, self.model_name)
        print("Trading information updated.")
        return self.model

    def update(self) -> DataFrame:
        last_candle = self.get_last_candle()
        flag = self.check_update_df(last_candle)

        if flag:
            self.preprocess_last(last_candle)

        return last_candle

    def predict(self) -> Union[PredictNeutralEnums, PredictBuyEnums, PredictSellEnums]:
        """

        :return:
            0:sell
            1:buy
            2:neutral
        """
        self.update()

        predict = self.model.predict(self.df.iloc[-1, 1:-2].values.reshape(1, -1))[0]

        if predict == 0:
            return PredictEnums().sell
        elif predict == 1:
            return PredictEnums().buy
        elif predict == 2:
            return PredictEnums().neutral
        else:
            return PredictEnums().neutral

    def check_update_df(self, last_candle: DataFrame) -> bool:
        last_candle_time = pd.Timestamp(last_candle['time'].values[0])

        temp_df_time_str = self.df.tail(1)['time'].values[0]
        type_temp_df_time_str = type(temp_df_time_str)

        if type_temp_df_time_str == str:
            temp_df_time = datetime.strptime(temp_df_time_str, '%Y-%m-%d %H:%M:%S+00:00')
        elif type_temp_df_time_str == Timestamp:
            temp_df_time = pd.Timestamp(temp_df_time_str)
        else:
            temp_df_time = pd.Timestamp(temp_df_time_str)

        return not temp_df_time.timestamp() == last_candle_time.timestamp()
