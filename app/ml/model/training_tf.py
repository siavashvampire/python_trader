import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers
import tensorflow as tf
from keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.metrics import precision_recall_fscore_support
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import svm
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
import pickle




def getting_x_y(df, signal = 'signal1'):
    df.replace({"BUY": 1, "SELL": -1, "NEUTRAL": 0}, inplace=True)
    feature_list = ['bbands', 'RSI_14_sig', 'STOCH_14_3_3_sig', 'CCI_14_0.015_sig', 'AO_5_34_sig', 'MOM_10_sig',
                    'MACD_12_26_9_sig', 'EMA_10_sig', 'SMA_10_sig', 'EMA_20_sig', 'SMA_20_sig', 'EMA_30_sig',
                    'SMA_30_sig', "RSI_15_sig", 'EMA_50_sig', 'SMA_50_sig', 'EMA_100_sig',
                    'SMA_100_sig', 'EMA_200_sig', 'SMA_200_sig']

    x = df[feature_list]
    y = df[signal]
    return x, y


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


def test_train(x, y):
    q_80 = int(len(y) * .8)
    q_90 = int(len(y) * .9)

    x_train, y_train = x[:q_80], y[:q_80]
    x_val, y_val = x[q_80:q_90], y[q_80:q_90]
    x_test, y_test = x[q_90:], y[q_90:]

    return x_train, y_train, x_val, y_val, x_test, y_test


def model_train(x_train, y_train, x_val, y_val, out = 3):
    n = x_train.shape[1]
    model = Sequential([layers.Input(n),
                        layers.Dense(128, activation='relu'),
                        layers.Dense(128, activation='relu'),
                        layers.Dense(out)])

    cback = EarlyStopping(monitor='val_loss', min_delta=0, patience=5, verbose=0, mode='auto',
                          restore_best_weights=True)

    model.compile(loss=tf.keras.losses.binary_crossentropy,
                  optimizer=Adam(learning_rate=0.001),
                  metrics=[
                      tf.keras.metrics.BinaryAccuracy(name='accuracy'),
                      tf.keras.metrics.Precision(name='precision'),
                      tf.keras.metrics.Recall(name='recall')], )

    history = model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=30, callbacks=[cback], batch_size = 256)

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


def results_buy(model, x_test, y_test):
    y_pred = model.predict(x_test)
    print(y_pred)
    y_pred = np.round(y_pred)
    num_correct_buy = 0
    num_pred_buy = 0
    num_test_buy = 0
    y_test.reset_index(drop=True, inplace=True)

    print(y_pred)
    print(y_test)
    for i in range(len(y_pred)):
        if int(y_pred[i]) == 1 and int(y_test[i]) == 1:
            num_correct_buy += 1
        if int(y_pred[i][0]) == 1:
            num_pred_buy += 1
        if int(y_test[i]) == 1:
            num_test_buy += 1
    print("*****buy******")
    print(num_pred_buy)
    print("cr/pred", num_correct_buy / num_pred_buy)
    print("cr/test", num_correct_buy / num_test_buy)


def model_dtree(x_train, y_train):
    classifiers = [
    KNeighborsClassifier(5),
    SVC(kernel="linear", C=0.025),
    GaussianProcessClassifier(1.0 * RBF(1.0)),
    DecisionTreeClassifier(max_depth=8),
    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    MLPClassifier(alpha=0.2, max_iter=1000, hidden_layer_sizes=(128,)),
    MLPClassifier(alpha=0.2, max_iter=1000, hidden_layer_sizes=(64,)),
    MLPClassifier(alpha=0.2, max_iter=1000, hidden_layer_sizes=(256,)),
    MLPClassifier(alpha=0.2, max_iter=1000, hidden_layer_sizes=(32,64)),
    LogisticRegression(solver='newton-cg', random_state=0),
    LogisticRegression(penalty='l1', solver='liblinear', random_state=0, max_iter = 200),
    LogisticRegression(random_state=0),
    LogisticRegression(penalty='l2', random_state=0)
    ]
    model = tree.DecisionTreeClassifier()
    model = model.fit(x_train, y_train)
    return model


def results_tree(model, x_test, y_test):
    y_test.reset_index(drop=True, inplace=True)
    y_pred = model.predict(x_test)
    num_correct_buy = 0
    num_pred_buy = 0
    num_test_buy = 0

    print(y_pred)
    print(y_test)
    for i in range(len(y_pred)):
        if int(y_pred[i][1]) == 1 and int(y_test[i][1]) == 1:
            num_correct_buy += 1
        if int(y_pred[i][1]) == 1:
            num_pred_buy += 1
        if int(y_test[i][1]) == 1:
            num_test_buy += 1

    print("*****buy******")
    print(num_pred_buy)
    print("cr/pred", num_correct_buy / num_pred_buy)
    print("cr/test", num_correct_buy / num_test_buy)


def full_model(x_train, y_train, x_test, y_test):
    y_test.reset_index(drop=True, inplace=True)
    classifiers = [
    KNeighborsClassifier(5),
    SVC(kernel="linear", C=0.025),
    #GaussianProcessClassifier(1.0 * RBF(1.0)),
    DecisionTreeClassifier(max_depth=8),
    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    MLPClassifier(alpha=0.2, max_iter=1000, hidden_layer_sizes=(128,)),
    MLPClassifier(alpha=0.2, max_iter=1000, hidden_layer_sizes=(64,)),
    MLPClassifier(alpha=0.2, max_iter=1000, hidden_layer_sizes=(256,)),
    MLPClassifier(alpha=0.2, max_iter=1000, hidden_layer_sizes=(32,64)),
    LogisticRegression(solver='newton-cg', random_state=0),
    LogisticRegression(penalty='l1', solver='liblinear', random_state=0, max_iter = 200),
    LogisticRegression(random_state=0),
    LogisticRegression(penalty='l2', random_state=0)
    ]
    for model in classifiers:
        print(model)
        model = model.fit(x_train, y_train)
        y_pred = model.predict(x_test)
        num_correct_buy = 0
        num_pred_buy = 0
        num_test_buy = 0

        print(y_pred)
        print(y_test)
        for i in range(len(y_pred)):
            if int(y_pred[i]) == 1 and int(y_test[i]) == 1:
                num_correct_buy += 1
            if int(y_pred[i]) == 1:
                num_pred_buy += 1
            if int(y_test[i]) == 1:
                num_test_buy += 1

        print(model)
        print("*****buy******")
        print(num_pred_buy)
        if num_pred_buy > 0:
            print("cr/pred", num_correct_buy / num_pred_buy)
            print("cr/test", num_correct_buy / num_test_buy)

    return model




