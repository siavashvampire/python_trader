import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers
import tensorflow as tf
from training_tf import *


def x_y_extract(df, n=60):
    list_x = []
    list_y = []

    for ind in df.index:
        if ind + n + 1 > len(df):
            break
        if df.index[ind + n] - df.index[ind] == df.index[0 + n] - df.index[0]:
            list_x.append(df['Close'][range(ind, ind + n)].values)
            list_y.append(df["signal1"][ind + n])

    x = np.array(list_x)
    y = np.array(list_y)
    return x, y


def lstm_model(x_train, y_train, x_val, y_val, n=60):
    model = Sequential([layers.Input((n, 1)),
                        layers.LSTM(64),
                        layers.Dense(32, activation='relu'),
                        layers.Dense(32, activation='relu'),
                        layers.Dense(3, activation=tf.nn.softmax)])

    cback = EarlyStopping(monitor='val_loss', min_delta=0, patience=5, verbose=0, mode='auto',
                          restore_best_weights=True)

    model.compile(loss=tf.keras.losses.binary_crossentropy,
                  optimizer=Adam(learning_rate=0.001),
                  metrics=[tf.keras.metrics.BinaryAccuracy(name='accuracy'),
                           tf.keras.metrics.Precision(name='precision'),
                           tf.keras.metrics.Recall(name='recall')])

    history = model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=20, callbacks=[cback])
    return model, history


def main():
    df = pd.read_csv('test_df.csv')
    x, y = x_y_extract(df, n=60)
    y = y_encoder(y)
    x_train, y_train, x_val, y_val, x_test, y_test = test_train(x, y)
    model, history = lstm_model(x_train, y_train, x_val, y_val)
    model_plot(history)
    results(model, x_test, y_test)
