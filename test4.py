from app.ml.model.indicator_extraction import data_import_sia, data_import_meta
import pandas as pd
from app.ml.main import indicator_extraction, indication_trainer, LSTM_model
from app.ml.model.indicator_extraction import data_import_sia
#from app.oanda.api import get_history
import pandas as pd

csv_file_path_in = 'app/ml/file/EURUSD_S5_sia.csv'
csv_file_path_out = 'app/ml/file/EURUSD_S5_indicator_meta.csv'
h5_file_path_out = 'app/ml/file/EUR_USD_model_meta.h5'
#df = data_import_meta(csv_file_path_in)
#print(df['Close'][7])




df = data_import_sia(csv_file_path_in)
df = indicator_extraction(df)
df.to_csv(csv_file_path_out, index=False, encoding='utf-8')
#df = pd.read_csv(csv_file_path_out)
model = indication_trainer(df)
#model = LSTM_model(df)
model.save(h5_file_path_out)

