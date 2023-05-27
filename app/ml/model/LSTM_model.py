import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers
from keras.callbacks import EarlyStopping
import tensorflow as tf
from app.ml.model.training_tf import y_encoder, test_train, model_plot, results
# test

def x_y_extract(df, n=1000):
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


def lstm_model(x_train, y_train, x_val, y_val):
    n = x_train.shape[1]
    model = Sequential([layers.Input((n, 1)),
                        layers.LSTM(128),
                        layers.Dense(64, activation='relu'),
                        layers.Dense(64, activation='relu'),
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
