import joblib
from pandas import DataFrame
import datetime

from app.data_connector.model.data_connector import DataConnector
from app.market_trading.model.trading_model import TradingModel


class MlTrading:
    model: object  # TODO:in bayad doros beshe man ba in lib kar nakardam
    model_name: str
    get_last_candle: callable
    trade: TradingModel
    candle: str

    def __init__(self, trade: TradingModel) -> None:
        self.trade = trade
        self.candle = trade.candle_rel.name

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
        self.df = self.df * 10000
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
        self.df['label'] = self.df['next_trend'].apply(lambda x: 0 if x >= 5 else 1 if x <= -5 else 2)

        self.v = self.df.drop(['time', 'next_trend', 'label'], axis=1)
        self.to_predict = self.v.iloc[-1]
        # self.df = self.df.dropna()

        return self.df

    # def last_process(self):
    #     self.df = self.get_last_candle()
    #     self.df = self.df.drop(['volume', 'complete'], axis=1)
    #     self.df = self.df * 10000
    #     self.df['trend'] = self.df['o'] - self.df['c']
    #     self.df['MA_20'] = self.df['c'].rolling(window=20).mean()  # moving average 20
    #     self.df['MA_50'] = self.df['c'].rolling(window=50).mean()  # moving average 50
    #
    #     self.df['L14'] = self.df['l'].rolling(window=14).min()
    #     self.df['H14'] = self.df['h'].rolling(window=14).max()
    #     self.df['%K'] = 100 * (
    #             (self.df['c'] - self.df['l']) / (self.df['h'] - self.df['l']))  # stochastic oscilator
    #     self.df['%D'] = self.df['%K'].rolling(window=3).mean()
    #
    #     self.df['EMA_20'] = self.df['c'].ewm(span=20, adjust=False).mean()  # exponential moving average
    #     self.df['EMA_50'] = self.df['c'].ewm(span=50, adjust=False).mean()
    #
    #     # self.df['next_trend'] = self.df['o'].shift(-1) - self.df['c'].shift(-1)
    #     # self.df['label'] = self.df['next_trend'].apply(lambda x: 0 if x >= 5 else 1 if x <= -5 else 2)
    #     # self.df = self.df.dropna()
    #
    #     return self.df

    def update(self):
        self.model.fit(self.get_last_candle())
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

        # TODO:ino man nemidonam chetori bayad vorodi bedid , zahmatesh miofte bara khodeton
        # print(self.df.iloc[-1, :].values.reshape(1, -1))
        # last_candle = self.get_last_candle()
        # self.last_process()
        # self.get_last_candle().preprocess()
        # self.get_last_candle().drop(['next_trend', 'label'])
        #  pred = self.model.predict(self.df['o', 'h', 'l', 'c', 'trend', 'MA_20', 'MA_50', 'L14', 'H14', '%K', '%D',
        # 'EMA_20', 'EMA_50'].iloc[-1].values.reshape(1, -1))

        pred = self.model.predict(self.to_predict.values.reshape(1, -1))
        return pred[0]
