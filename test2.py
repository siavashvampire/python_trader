from app.ml.main import indicator_extraction, indication_trainer, LSTM_model
from app.ml.model.indicator_extraction import metatrader_data_import_trview
from app.oanda.api import get_history
import pandas as pd

# csv_file_path_out = ""
# data = get_history("EUR_USD", "2023-05-1", "2023-05-26", "S5",csv_file_path_out)
# csv_file_path_in = 'app/ml/file/EURUSD_M1_202301251915_202305031504.csv'
#csv_file_path_out = 'app/ml/file/EURUSD_indicator.csv'
h5_file_path_out = 'app/ml/file/EUR_USD_model.h5'
csv_file_path_out = 'File/test3.csv'
df = metatrader_data_import_trview(csv_file_path_out)
df = indicator_extraction(df)
#df.to_csv(csv_file_path_out, index=False, encoding='utf-8')
#df = pd.read_csv(csv_file_path_out)
#model = indication_trainer(df)
model = LSTM_model(df)
model.save(h5_file_path_out)




