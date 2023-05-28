from time import sleep

import pandas as pd
import tensorflow as tf
from app.ml.model.indicator_extraction import data_import_meta, adding_raw_indicators, adding_indicator_signal, \
    solving_nans, adding_percent_change, winning_policy_1
from app.ml.model.training_tf import getting_x_y, y_encoder, test_train, model_train, model_plot, results
from app.ml.model.LSTM_model import x_y_extract, lstm_model
from app.oanda.api import get_history, get_last_candle

# not finished yet
csv_file_path_in = 'app/ml/file/testing.csv'
df = get_history("EUR_USD", "2023-05-25", "2023-05-26", "S5", csv_file_path_in)
sleep(5)
for i in range(1000):
    df.iloc[[0, -1]] = get_last_candle("EUR_USD", "S5")
    df = adding_raw_indicators(df[:-600])
    print(list(df.columns))
    df = adding_indicator_signal(df)
    df = solving_nans(df)
    x, y = getting_x_y(df)
    y = y_encoder(y)
    model = tf.keras.models.load_model('app/ml/file/EUR_USD_model_meta.h5')
    y_pred = model.predict(df[-1])
    print(y_pred)
    sleep(5)
    # wait(55sec)
