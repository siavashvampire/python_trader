import joblib
import pandas as pd
from pandas import DataFrame
from sklearn.ensemble import GradientBoostingClassifier

from app.data_connector.model.data_connector import DataConnector
from app.market_trading.model.trading_model import TradingModel


class MlTrading:
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
        self.temp_df = DataFrame()

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
            name=self.trade.currency_disp("_"), start_time=start_time, end_time=end_time, candle=self.candle)

        self.get_history_from_file = lambda: self.data_connector.get_history_from_file(data_file_root)
        # preprocessed = trading.preprocess(last_candle)
        # updated_model = trading.update(model)
        # predicted_value = trading.predict(preprocessed)
        # print(f"Prediction: {predicted_value}")

    def preprocess(self) -> DataFrame:
        self.df = self.get_history_from_file()
        # self.df = self.get_last_candle()
        self.df = self.df.drop(['volume', 'complete'], axis=1)
        # self.df = self.df * 10000

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

    def preprocess_last(self) -> DataFrame:
        self.temp_df = self.df.iloc[-50:]
        # print(self.temp_df)

        last_candle = self.get_last_candle()

        # print(self.df['time'])
        temp_time = self.temp_df['time'].tail(1).values[0]
        # in beheton time dakhele temp df ro mide vali hamontori k goftam 10000 tash has bara hamin natonestam ba last candle .index checkesh konam
        # on k doros shod bayad check beshe

        print("time : ", temp_time)
        # print(self.temp_df.index.values)
        # print(self.temp_df.index[-1])
        print(last_candle.index[0])
        print(temp_time == last_candle.index[0])
        if len(self.temp_df.index.values) != 0 and self.temp_df['time'].iloc[-1] != last_candle.index:
            last_candle = last_candle.drop(['volume', 'complete'], axis=1)
            self.temp_df = pd.concat([self.temp_df, last_candle])
            self.temp_df = self.temp_df.shift(-1)[:-1]
            # last_row = temp_df[-1]
            self.temp_df['trend'] = self.temp_df['o'] - self.temp_df['c']
            self.temp_df['MA_20'] = self.temp_df['c'].rolling(window=20).mean()  # moving average 20
            self.temp_df['MA_50'] = self.temp_df['c'].rolling(window=50).mean()  # moving average 50

            self.temp_df['L14'] = self.temp_df['l'].rolling(window=14).min()
            self.temp_df['H14'] = self.temp_df['h'].rolling(window=14).max()
            self.temp_df['%K'] = 100 * (
                    (self.temp_df['c'] - self.temp_df['l']) / (
                    self.temp_df['h'] - self.temp_df['l']))  # stochastic oscilator
            self.temp_df['%D'] = self.temp_df['%K'].rolling(window=3).mean()

            self.temp_df['EMA_20'] = self.temp_df['c'].ewm(span=20, adjust=False).mean()  # exponential moving average
            self.temp_df['EMA_50'] = self.temp_df['c'].ewm(span=50, adjust=False).mean()

            self.temp_df['next_trend'] = self.temp_df['o'].shift(-1) - self.temp_df['c'].shift(-1)
            self.temp_df['label'] = self.temp_df['next_trend'].apply(
                lambda x: 0 if x >= .0004 else 1 if x <= -.0004 else 2)

            self.counter += 1
            self.counter2 += 1

            # Check if the counter reaches 10
            if self.counter == 10:
                # Call update when 10 candles are added
                self.update_model()
                self.counter = 0

            if self.counter2 == 50:
                pd.concat([self.df, self.temp_df[-49:]])
                self.counter2 = 0

            # self.v = self.df.drop(['time'], axis=1)
            # self.to_predict = self.v
            # self.df = self.df.dropna()

            # TODO:radif akhari temp_df ro b df ezafe nakardid
            # print(self.temp_df)
            return self.temp_df

    def update_model(self):
        self.model.fit(self.temp_df.iloc[:, :-2], self.temp_df.iloc[:, -2:])
        joblib.dump(self.model, self.model_name)
        print("Trading information updated.")
        return self.model

    def predict(self) -> int:
        """

        :return:
            0:sell
            1:buy
            2:neutral
        """

        last_candle = self.get_last_candle()
        print(self.temp_df)
        # TODO:in if ham ghalate
        if not (len(self.temp_df.index.values) != 0 and self.temp_df.iloc[-1].index == last_candle.index):
            self.preprocess_last()

        # self.temp_df = self.temp_df.reset_index(drop=True, inplace=True)

        pred = self.model.predict(self.temp_df.iloc[-1, 1:-2].values.reshape(1, -1))

        return pred
