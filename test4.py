import tensorflow as tf
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], enable=True)
from app.ml.model.indicator_extraction import data_import_sia, data_import_meta, winning_policy_1
import pandas as pd
from app.ml.main import indicator_extraction, indication_trainer, LSTM_model
from app.ml.model.indicator_extraction import data_import_sia
#from app.oanda.api import get_history
import pandas as pd

csv_file_path_in = 'app/ml/file/EURUSD_M1_sia.csv'
csv_file_path_out = 'app/ml/file/EURUSD_M1_indicator_meta.csv'
h5_file_path_out = 'app/ml/file/EUR_USD_M1.h5'
#df = data_import_meta(csv_file_path_in)
#print(df['Close'][7])



#
# df = data_import_sia(csv_file_path_in)
# df = indicator_extraction(df)
# df.to_csv(csv_file_path_out, index=False, encoding='utf-8')
df = pd.read_csv(csv_file_path_out)
df = winning_policy_1(df, 0.001)
df1 = df[df["signal1"] == 1]
df2 = df[df["signal1"] == -1]
print('percent of buy = ', len(df1.index) / len(df.index))
print('percent of sell = ', len(df2.index) / len(df.index))
model = indication_trainer(df)
#model = LSTM_model(df)
model.save(h5_file_path_out)

