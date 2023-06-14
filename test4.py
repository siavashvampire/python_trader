import tensorflow as tf
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], enable=True)
from app.ml.model.indicator_extraction import data_import_sia, data_import_meta, winning_policy_4 , winning_policy_5, winning_policy_3
import pandas as pd
from app.ml.main import indicator_extraction, indication_trainer, LSTM_model, indication_trainer_buy, tree_model, full_model_full, LSTM_model_buy
from app.ml.model.indicator_extraction import data_import_sia, adding_percent_change
#from app.oanda.api import get_history
import pandas as pd
import numpy as np


csv_file_path_in = 'app/ml/file/EURUSD_M1_sia.csv'
csv_file_path_out = 'app/ml/file/EURUSD_M1_indicator_meta.csv'
h5_file_path_out = 'app/ml/file/EUR_USD_M1_lstm.h5'
#df = data_import_meta(csv_file_path_in)
#print(df['Close'][7])



#
# df = data_import_sia(csv_file_path_in)
# df = indicator_extraction(df)
# df.to_csv(csv_file_path_out, index=False, encoding='utf-8')
df = pd.read_csv(csv_file_path_out)
df = adding_percent_change(df)

#df = winning_policy_1(df, 0.001)
df = winning_policy_5(df, 0.01)

#model = indication_trainer(df, signal = 'signal5')
model, history = LSTM_model(df, signal = 'signal5')
#tree_model(df, signal = 'signal3')
#full_model_full(df, signal = 'signal4')
# model = LSTM_model_buy(df)
model.save(h5_file_path_out)

