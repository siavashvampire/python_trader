# dataset @ https://finance.yahoo.com/quote/MSFT/history/

# If you want the exact same dataset as the YouTube video,
# use this link: https://drive.google.com/file/d/1WLm1AEYgU28Nk4lY4zNkGPSctdImbhJI/view?usp=sharing



from google.colab import drive
drive.mount('/content/drive')



import pandas as pd

df = pd.read_csv('/content/drive/Othercomputers/My Laptop/Other projects/Trading/EURUSD_M1_202301251915_202305031504.csv',sep = '\t')





df = df[['<DATE>','<TIME>', '<CLOSE>']]





import datetime

def str_to_datetime(s,t):
  split_S = s.split('.')
  split_T = t.split(':')
  year, month, day = int(split_S[0]), int(split_S[1]), int(split_S[2])
  hour, minute, second = int(split_T[0]), int(split_T[1]), int(split_T[2])
  return datetime.datetime(year=year, month=month, day=day, hour = hour, minute = minute, second = second)

datetime_object = str_to_datetime('2023.05.03','15:01:00')




df["Date"] = df.apply(lambda x: str_to_datetime(x['<DATE>'], x['<TIME>']), axis=1)





df = df.rename({'<CLOSE>':'Close'}, axis=1)




df = df[['Close','Date']]



df.index = df.pop('Date')




import matplotlib.pyplot as plt

plt.plot(df.index, df['Close'])


print(df['Close'][range(1,30)].values)

import numpy as np

n = 30
list_x = []
list_y = []
list_dates = []

for i in enumerate(zip(df.index, df['Close'])):
    ind = i[0]
    time = i[1][0]
    Price = i[1][1]

    if ind + n + 1 > len(df):
        break
    if df.index[ind + n] - df.index[ind] == df.index[0 + n] - df.index[0]:
        list_x.append(df['Close'][range(ind,ind+n)].values)
        list_y.append(df['Close'][ind + n])
        list_dates.append(df['Close'][range(ind,ind+n)])

dates = np.array(list_dates)
X = np.array(list_x)
y = np.array(list_y)

print(X)
print(y)


print(y.shape)
print(X.shape)
print(dates.shape)




X = X[..., np.newaxis]



q_80 = int(len(dates) * .8)
q_90 = int(len(dates) * .9)

dates_train, X_train, y_train = dates[:q_80], X[:q_80], y[:q_80]

dates_val, X_val, y_val = dates[q_80:q_90], X[q_80:q_90], y[q_80:q_90]
dates_test, X_test, y_test = dates[q_90:], X[q_90:], y[q_90:]

plt.plot(dates_train, y_train)
plt.plot(dates_val, y_val)
plt.plot(dates_test, y_test)

plt.legend(['Train', 'Validation', 'Test'])



from tensorflow.python.client import device_lib
def get_available_devices():
    local_device_protos = device_lib.list_local_devices()
    return [x.name for x in local_device_protos]
print(get_available_devices()) 




from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers

import tensorflow as tf

print(tf.test.gpu_device_name())
model = Sequential([layers.Input((n, 1)),
                    layers.LSTM(64),
                    layers.Dense(32, activation='relu'),
                    layers.Dense(32, activation='relu'),
                    layers.Dense(1)])

model.compile(loss='mse', 
              optimizer=Adam(learning_rate=0.001),
              metrics=['mean_absolute_error'])

model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=100)



train_predictions = model.predict(X_train).flatten()
numbers_tr = (np.sign((train_predictions - X_train[:,n-1,0])*(y_train - X_train[:,n-1,0])))
numbers_tr = numbers_tr.tolist()
numbers_1 = numbers_tr.count(1)
numbers_0 = numbers_tr.count(-1)
print(numbers_1/(numbers_1+numbers_0))
plt.plot(dates_train, train_predictions)
plt.plot(dates_train, y_train)
plt.legend(['Training Predictions', 'Training Observations'])


val_predictions = model.predict(X_val).flatten()

plt.plot(dates_val, val_predictions)
plt.plot(dates_val, y_val)
plt.legend(['Validation Predictions', 'Validation Observations'])



test_predictions = model.predict(X_test).flatten()

plt.plot(dates_test, test_predictions)
plt.plot(dates_test, y_test)
plt.legend(['Testing Predictions', 'Testing Observations'])



plt.plot(dates_train, train_predictions)
plt.plot(dates_train, y_train)
plt.plot(dates_val, val_predictions)
plt.plot(dates_val, y_val)
plt.plot(dates_test, test_predictions)
plt.plot(dates_test, y_test)
plt.legend(['Training Predictions', 
            'Training Observations',
            'Validation Predictions', 
            'Validation Observations',
            'Testing Predictions', 
            'Testing Observations'])


from copy import deepcopy

recursive_predictions = []
recursive_dates = np.concatenate([dates_val, dates_test])

for target_date in recursive_dates:
  last_window = deepcopy(X_train[-1])
  next_prediction = model.predict(np.array([last_window])).flatten()
  recursive_predictions.append(next_prediction)
  last_window[-1] = next_prediction



plt.plot(dates_train, train_predictions)
plt.plot(dates_train, y_train)
plt.plot(dates_val, val_predictions)
plt.plot(dates_val, y_val)
plt.plot(dates_test, test_predictions)
plt.plot(dates_test, y_test)
plt.plot(recursive_dates, recursive_predictions)
plt.legend(['Training Predictions', 
            'Training Observations',
            'Validation Predictions', 
            'Validation Observations',
            'Testing Predictions', 
            'Testing Observations',
            'Recursive Predictions'])





