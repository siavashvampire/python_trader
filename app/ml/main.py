import pandas as pd
import tensorflow as tf
from app.ml.model.indicator_extraction import adding_raw_indicators, adding_indicator_signal, \
    solving_nans, adding_percent_change, winning_policy_1
from app.ml.model.training_tf import getting_x_y, y_encoder, test_train, model_train, model_plot,\
     results, results_buy, results_tree, model_dtree, full_model
from app.ml.model.LSTM_model import x_y_extract, lstm_model


def indicator_extraction(df):
    df = adding_raw_indicators(df)
    df = adding_indicator_signal(df)
    df = solving_nans(df)
    df = adding_percent_change(df)
    df = winning_policy_1(df, 0.01)
    return df


def indication_trainer(df, signal = 'signal1'):
    x, y = getting_x_y(df, signal = signal)
    y = y_encoder(y)
    x_train, y_train, x_val, y_val, x_test, y_test = test_train(x, y)
    model, history = model_train(x_train, y_train, x_val, y_val)
    model_plot(history)
    results(model, x_test, y_test)
    return model


def indication_trainer_buy(df, signal = 'signal1'):
    x, y = getting_x_y(df, signal = signal)
    x_train, y_train, x_val, y_val, x_test, y_test = test_train(x, y)
    model, history = model_train(x_train, y_train, x_val, y_val, out = 1)
    model_plot(history)
    results_buy(model, x_test, y_test)
    return model


def indicator_model_load(csv_file_path_out: str):
    df = pd.read_csv(csv_file_path_out)
    x, y = getting_x_y(df)
    y = y_encoder(y)
    model = tf.keras.models.load_model('my_model.h5')
    return model


def LSTM_model(df, signal = 'signal1'):
    x, y = x_y_extract(df, n=100, signal = signal)
    y = y_encoder(y)
    x_train, y_train, x_val, y_val, x_test, y_test = test_train(x, y)
    model, history = lstm_model(x_train, y_train, x_val, y_val)
    model_plot(history)
    results(model, x_test, y_test)
    return model


def tree_model(df, signal = 'signal3'):
    x, y = getting_x_y(df, signal = signal)
    y = y_encoder(y)
    x_train, y_train, x_val, y_val, x_test, y_test = test_train(x, y)
    model = model_dtree(x_train, y_train)
    results_tree(model, x_test, y_test)


def full_model_full(df, signal = 'signal3'):
    x, y = getting_x_y(df, signal = signal)
    x_train, y_train, x_val, y_val, x_test, y_test = test_train(x, y)
    full_model(x_train, y_train, x_test, y_test)