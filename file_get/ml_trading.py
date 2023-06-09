import joblib
from pandas import DataFrame
import datetime

from app.market_trading.model.trading_model import TradingModel


class MlTrading:
    model: object #TODO:in bayad doros beshe man ba in lib kar nakardam
    model_name: str
    get_last_candle: callable
    trade: TradingModel
    candle: str

    def __init__(self, trade: TradingModel, candle: str, get_last_candle: callable) -> None:
        self.trade = trade
        self.candle = candle
        # self.model = joblib.load('model_1min_EUR_USD.pkl')
        self.model_name = 'model_' + candle + '_' + self.trade.currency_disp("_") + '.pkl'
        self.model = joblib.load(self.model_name)
        self.get_last_candle = lambda: get_last_candle(self.trade.currency_disp("_"), self.candle)
        # preprocessed = trading.preprocess(last_candle)
        # updated_model = trading.update(model)
        # predicted_value = trading.predict(preprocessed)
        # print(f"Prediction: {predicted_value}")

    def preprocess(self):
        end_time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        start_time = (datetime.datetime.utcnow() - datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
        self.df = self.get_history(name=self.trade.currency_disp("_"), start_time=start_time, end_time=end_time, candle="M1")
        # self.df = self.get_last_candle()
        self.df = self.df.drop(['volume', 'complete'], axis=1)
        self.df = self.df * 10000
        self.df['next_trend'] = self.df['o'].shift(-1) - self.df['c'].shift(-1)
        self.df['MA_20'] = self.df['c'].rolling(window=20).mean()  # moving average 20
        self.df['MA_50'] = self.df['c'].rolling(window=50).mean()  # moving average 50

        self.df['L14'] = self.df['l'].rolling(window=14).min()
        self.df['H14'] = self.df['h'].rolling(window=14).max()
        self.df['%K'] = 100 * (
                (self.df['c'] - self.df['l']) / (self.df['h'] - self.df['l']))  # stochastic oscilator
        self.df['%D'] = self.df['%K'].rolling(window=3).mean()

        self.df['EMA_20'] = self.df['c'].ewm(span=20, adjust=False).mean()  # exponential moving average
        self.df['EMA_50'] = self.df['c'].ewm(span=50, adjust=False).mean()
        self.df['label'] = self.df['next_trend'].apply(lambda x: 0 if x >= 5 else 1 if x <= -5 else 2)

        return self.df

    def update(self):
        self.model.fit(self.get_last_candle())
        joblib.dump(self.model, self.model_name)
        print("Trading information updated.")
        return self.model

    def predict(self, data: DataFrame):
        # TODO:ino man nemidonam chetori bayad vorodi bedid , zahmatesh miofte bara khodeton
        pred = self.model.predict(self.df.iloc[-1, :].values.reshape(1, -1))
        ## 0:sell 1:buy 2:neutral
        return pred
