from time import sleep

import pandas as pd
import tensorflow as tf
from app.ml.model.indicator_extraction import data_import_meta, adding_raw_indicators, adding_indicator_signal, \
    solving_nans, adding_percent_change, winning_policy_5, data_import_sia
from app.ml.model.training_tf import getting_x_y, y_encoder, test_train, model_train, model_plot, results
from app.ml.model.LSTM_model import x_y_extract, lstm_model
import numpy as np

# not finished yet
csv_file_path_in = 'app/ml/file/EURUSD_M1_sia.csv'
df_main = data_import_sia(csv_file_path_in)
feature_list = ['bbands', 'RSI_14_sig', 'STOCH_14_3_3_sig', 'CCI_14_0.015_sig', 'AO_5_34_sig', 'MOM_10_sig',
            'MACD_12_26_9_sig', 'EMA_10_sig', 'SMA_10_sig', 'EMA_20_sig', 'SMA_20_sig', 'EMA_30_sig',
            'SMA_30_sig', "RSI_15_sig", 'EMA_50_sig', 'SMA_50_sig', 'EMA_100_sig',
            'SMA_100_sig', 'EMA_200_sig', 'SMA_200_sig']
df_main.reset_index()

while True:
    df = df_main[0:600]
    df = adding_raw_indicators(df)
    df = adding_percent_change(df)
    df = adding_indicator_signal(df)
    df = winning_policy_5(df, 0.01)
    df = solving_nans(df)
    x, y = getting_x_y(df, signal = 'signal5')
    model = tf.keras.models.load_model('app/ml/file/EUR_USD_M1.h5')
    test = df[feature_list]
    df.reset_index()
    y_pred = model.predict(df[0:2][feature_list]) + [-0.05, 0, -0.05]
    y_pred = y = tf.one_hot(tf.argmax(y_pred, axis=1), y_pred.shape[1])
    if y_pred[0][0] == 1:
        print('sell')
    if y_pred[0][2] == 1:
        print('buy')
    if y_pred[0][1] == 1:
        print('nothing!')
    print(y_pred)
    sleep(58)
    # wait(55sec)
