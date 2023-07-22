import unittest
from datetime import datetime
from time import sleep

import numpy

from app.market_trading.api import get_trading
from app.ml_avidmech.model.ml_trading import MlTrading

trade_id = 4

class TestTrading(unittest.TestCase):
    def test_preprocess(self):
        trade = get_trading(id_in=trade_id)
        ml_trade = MlTrading(trade=trade)

        self.assertTrue(ml_trade.df.empty)

        ml_trade.preprocess()

        self.assertFalse(ml_trade.df.empty)

        keys = ml_trade.df.keys()
        n_df = ml_trade.df.shape[0]

        self.assertGreaterEqual(n_df, 50)
        self.assertEqual(len(keys), 16)
        self.assertTrue('time' in keys)
        self.assertTrue('o' in keys)
        self.assertTrue('c' in keys)
        self.assertTrue('h' in keys)
        self.assertTrue('l' in keys)
        self.assertTrue('trend' in keys)
        self.assertTrue('MA_20' in keys)
        self.assertTrue('MA_50' in keys)
        self.assertTrue('L14' in keys)
        self.assertTrue('H14' in keys)
        self.assertTrue('%K' in keys)
        self.assertTrue('%D' in keys)
        self.assertTrue('EMA_20' in keys)
        self.assertTrue('EMA_50' in keys)
        self.assertTrue('next_trend' in keys)
        self.assertTrue('label' in keys)

        first_row = ml_trade.df.head(1)

        self.assertIsInstance(first_row['time'].values[0], str)
        self.assertIsInstance(first_row['o'].values[0], float)
        self.assertIsInstance(first_row['c'].values[0], float)
        self.assertIsInstance(first_row['h'].values[0], float)
        self.assertIsInstance(first_row['l'].values[0], float)
        self.assertIsInstance(first_row['trend'].values[0], float)
        self.assertIsInstance(first_row['MA_20'].values[0], float)
        self.assertIsInstance(first_row['MA_50'].values[0], float)
        self.assertIsInstance(first_row['L14'].values[0], float)
        self.assertIsInstance(first_row['H14'].values[0], float)
        self.assertIsInstance(first_row['%K'].values[0], float)
        self.assertIsInstance(first_row['%D'].values[0], float)
        self.assertIsInstance(first_row['EMA_20'].values[0], float)
        self.assertIsInstance(first_row['EMA_50'].values[0], float)
        self.assertIsInstance(first_row['next_trend'].values[0], float)
        self.assertIsInstance(first_row['label'].values[0], numpy.int64)

    def test_check_update(self):
        trade = get_trading(id_in=trade_id)
        ml_trade = MlTrading(trade=trade)
        ml_trade.preprocess()

        flag, last_candle = ml_trade.check_update_df()
        self.assertFalse(flag)

        sleep(65)

        flag, last_candle = ml_trade.check_update_df()
        self.assertTrue(flag)

    def test_last_candle(self):
        trade = get_trading(id_in=trade_id)
        ml_trade = MlTrading(trade=trade)
        ml_trade.preprocess()

        last_candle = ml_trade.get_last_candle()
        print(last_candle)
        self.assertFalse(last_candle.empty)

        keys = last_candle.keys()
        n_df = last_candle.shape[0]

        self.assertEqual(n_df, 1)
        self.assertEqual(len(keys), 5)
        self.assertTrue('time' in keys)
        self.assertTrue('o' in keys)
        self.assertTrue('c' in keys)
        self.assertTrue('h' in keys)
        self.assertTrue('l' in keys)

        self.assertIsInstance(last_candle['time'].values[0], str)
        self.assertIsInstance(last_candle['o'].values[0], float)
        self.assertIsInstance(last_candle['c'].values[0], float)
        self.assertIsInstance(last_candle['h'].values[0], float)
        self.assertIsInstance(last_candle['l'].values[0], float)

    def test_reduce_df_size(self):
        trade = get_trading(id_in=trade_id)
        ml_trade = MlTrading(trade)
        ml_trade.preprocess()
        # temp_df = ml.df
        # shape_first = temp_df.shape[0]
        ml_trade.reduce_df_size()
        temp_df2 = ml_trade.df
        shape_second = temp_df2.shape[0]
        self.assertLessEqual(shape_second,ml_trade.prefer_df_size)

        first_row = ml_trade.df.head(1)

        self.assertIsInstance(first_row['time'].values[0], str)
        self.assertIsInstance(first_row['o'].values[0], float)
        self.assertIsInstance(first_row['c'].values[0], float)
        self.assertIsInstance(first_row['h'].values[0], float)
        self.assertIsInstance(first_row['l'].values[0], float)
        self.assertIsInstance(first_row['trend'].values[0], float)
        self.assertIsInstance(first_row['MA_20'].values[0], float)
        self.assertIsInstance(first_row['MA_50'].values[0], float)
        self.assertIsInstance(first_row['L14'].values[0], float)
        self.assertIsInstance(first_row['H14'].values[0], float)
        self.assertIsInstance(first_row['%K'].values[0], float)
        self.assertIsInstance(first_row['%D'].values[0], float)
        self.assertIsInstance(first_row['EMA_20'].values[0], float)
        self.assertIsInstance(first_row['EMA_50'].values[0], float)
        self.assertIsInstance(first_row['next_trend'].values[0], float)
        self.assertIsInstance(first_row['label'].values[0], numpy.int64)
