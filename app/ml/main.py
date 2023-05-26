import pandas as pd
import tensorflow as tf
from app.ml.model.indicator_extraction import metatrader_data_import, adding_raw_indicators, adding_indicator_signal, \
    solving_nans, adding_percent_change, winning_policy_1
from app.ml.model.training_tf import getting_x_y, y_encoder, test_train, model_train, model_plot, results
from app.ml.model.LSTM_model import x_y_extract, lstm_model


def indicator_extraction(csv_file_path_in: str, csv_file_path_out: str):
    df = metatrader_data_import(csv_file_path_in)
    df = adding_raw_indicators(df)
    df = adding_indicator_signal(df)
    df = solving_nans(df)
    df = adding_percent_change(df)
    df = winning_policy_1(df, 0.03)
    df.to_csv(csv_file_path_out, index=False, encoding='utf-8')


def indication_trainer(csv_file_path_out: str, h5_file_path_out: str):
    df = pd.read_csv(csv_file_path_out)
    x, y = getting_x_y(df)
    y = y_encoder(y)
    x_train, y_train, x_val, y_val, x_test, y_test = test_train(x, y)
    model, history = model_train(x_train, y_train, x_val, y_val)
    model.save(h5_file_path_out)
    model_plot(history)
    results(model, x_test, y_test)


def indicator_model_load(csv_file_path_out: str):
    df = pd.read_csv(csv_file_path_out)
    x, y = getting_x_y(df)
    y = y_encoder(y)
    model = tf.keras.models.load_model('my_model.h5')


def LSTM_model():
    df = pd.read_csv('../../../test_df.csv')
    x, y = x_y_extract(df, n=60)
    y = y_encoder(y)
    x_train, y_train, x_val, y_val, x_test, y_test = test_train(x, y)
    model, history = lstm_model(x_train, y_train, x_val, y_val)
    model_plot(history)
    results(model, x_test, y_test)
