import pandas as pd
import tensorflow as tf
from app.ml.model.indicator_extraction import metatrader_data_import, adding_raw_indicators, adding_indicator_signal, \
    solving_nans, adding_percent_change, winning_policy_1
from app.ml.model.training_tf import getting_x_y, y_encoder, test_train, model_train, model_plot, results
from app.ml.model.LSTM_model import x_y_extract, lstm_model

# not finished yet
csv_file_path_in = 'app/ml/file/EURUSD_M1_202301251915_202305031504.csv'
#while True:

#df = sia_func()
df = pd.read_csv(csv_file_path_in)

# df must have Close column as the price
df = adding_raw_indicators(df[:-500])
print(list(df.columns))
df = adding_indicator_signal(df)
df = solving_nans(df)
x, y = getting_x_y(df)
y = y_encoder(y)
model = tf.keras.models.load_model('app/ml/file/model.h5')
y_pred = model.predict(df[-1])
print(y_pred)
# wait(55sec)



