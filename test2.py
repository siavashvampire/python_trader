from app.ml.main import indicator_extraction, indication_trainer, LSTM_model
from app.ml.model.indicator_extraction import data_import_sia
from app.oanda.api import get_history_oanda
import pandas as pd
import tensorflow as tf
csv_file_path_in = 'app/ml/file/EURUSD_S5_sia.csv'
csv_file_path_out = 'app/ml/file/EURUSD_S5_indicator_sia.csv'
h5_file_path_out = 'app/ml/file/EUR_USD_model.h5'
#csv_file_path_in = 'File/test3.csv'
#from tensorflow.keras.models import Model
#print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
df = get_history_oanda("EUR_USD", "2023-05-1", "2023-05-26", "S5", csv_file_path_in)

'''
df = data_import_sia(csv_file_path_in)
df = indicator_extraction(df)
df.to_csv(csv_file_path_out, index=False, encoding='utf-8')
#df = pd.read_csv(csv_file_path_out)
model = indication_trainer(df)
#model = LSTM_model(df)
model.save(h5_file_path_out)
'''




