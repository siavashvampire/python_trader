import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers
import tensorflow as tf
from keras.callbacks import EarlyStopping,History
import matplotlib.pyplot as plt


def getting_x_y(df):
    df.replace({"BUY": 1, "SELL": -1, "NEUTRAL": 0}, inplace=True)
    feature_list = ['bbands', 'RSI_14_sig', 'STOCH_14_3_3_sig', 'CCI_14_0.015_sig', 'AO_5_34_sig', 'MOM_10_sig',
                    'MACD_12_26_9_sig', 'EMA_10_sig', 'SMA_10_sig', 'EMA_20_sig', 'SMA_20_sig', 'EMA_30_sig',
                    'SMA_30_sig', "RSI_15_sig",'EMA_50_sig', 'SMA_50_sig', 'EMA_100_sig',
                    'SMA_100_sig', 'EMA_200_sig', 'SMA_200_sig','Percent_Change_5', 'Percent_Change_3',
                    'Percent_Change_10']

    X = df[feature_list]
    y = df["signal1"]
    return X,y


def y_encoder(y):
    # define example
    values = np.array(y)

    # first apply label encoding
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(values)

    # now we can apply one hot encoding
    onehot_encoder = OneHotEncoder(sparse=False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
    y = onehot_encoded
    return y


def test_train(x,y):
    q_80 = int(len(y) * .8)
    q_90 = int(len(y) * .9)

    x_train, y_train = x[:q_80], y[:q_80]
    x_val, y_val = x[q_80:q_90], y[q_80:q_90]
    x_test, y_test = x[q_90:], y[q_90:]

    return x_train, y_train, x_val, y_val, x_test, y_test


def model_train(x_train, y_train, x_val, y_val):
    n = x_train.shape[1]
    model = Sequential([layers.Input(n),
                        layers.Dense(32, activation='relu'),
                        layers.Dense(32, activation='relu'),
                        layers.Dense(3, activation=tf.nn.softmax)])

    cback = EarlyStopping(monitor='val_loss', min_delta=0, patience=5, verbose=0, mode='auto',
                          restore_best_weights=True)

    model.compile(loss=tf.keras.losses.binary_crossentropy,
                  optimizer=Adam(learning_rate=0.001),
                  metrics=[
                      tf.keras.metrics.BinaryAccuracy(name='accuracy'),
                      tf.keras.metrics.Precision(name='precision'),
                      tf.keras.metrics.Recall(name='recall')],)

    history = model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=10, callbacks = [cback])

    return model, history


def model_plot(history):
    # list all data in history
    print(history.history.keys())
    # summarize history for accuracy
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()


def results(model, x_test, y_test):
    y_pred = model.predict(x_test)
    y_pred = np.round(y_pred)
    num_correct_buy = 0
    num_pred_buy = 0
    num_test_buy = 0

    print(y_pred)
    print(y_test)
    for i in range(len(y_pred)):
        if int(y_pred[i][2]) == 1 and int(y_test[i][2]) == 1:
            num_correct_buy += 1
        if int(y_pred[i][2]) == 1:
            num_pred_buy += 1
        if int(y_test[i][2]) == 1:
            num_test_buy += 1

    print("*****buy******")
    print(num_pred_buy)
    print("cr/pred", num_correct_buy / num_pred_buy)
    print("cr/test", num_correct_buy / num_test_buy)

    num_correct_sell = 0
    num_pred_sell = 0
    num_test_sell = 0

    for i in range(len(y_pred)):
        if y_pred[i][0] == 1 and y_test[i][0] == 1:
            num_correct_sell += 1
        if y_pred[i][0] == 1:
            num_pred_sell += 1
        if y_test[i][0] == 1:
            num_test_sell += 1

    print("*****sell******")
    print(num_pred_sell)
    print("cr/pred", num_correct_sell / num_pred_sell)
    print("cr/test", num_correct_sell / num_test_sell)


def main():
    df = pd.read_csv('test_df.csv')
    x,y = getting_x_y(df)
    y = y_encoder(y)
    x_train, y_train, x_val, y_val, x_test, y_test = test_train(x, y)
    model, history = model_train(x_train, y_train, x_val, y_val)
    model_plot(history)
    results(model, x_test, y_test)


main()



