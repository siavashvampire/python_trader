from app.data_connector.model.data_connector import DataConnector

# from app.ml.main import indicator_extraction, indication_trainer, LSTM_model
# from app.ml.model.indicator_extraction import data_import_sia
# from app.ml_avidmech.model.enums import PredictEnums
# from app.oanda.api import get_history_oanda
# import pandas as pd
# import tensorflow as tf
csv_file_path_in = 'app/ml/file/EURUSD_S5_sia.csv'
csv_file_path_out = 'app/ml/file/EURUSD_S5_indicator_sia.csv'
h5_file_path_out = 'app/ml/file/EUR_USD_model.h5'
# csv_file_path_in = 'File/test3.csv'
# from tensorflow.keras.models import Model
# print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
# df = get_history_oanda("EUR_USD", "2023-05-24", "2023-05-26", "M1", csv_file_path_in)
# print(df)

dc = DataConnector()
dc.open_trade_window()

# from eel import chrome
# import eel
# from webbrowser import get, open
# from os import sep
#
# url = {"host": "quotex.com/en/sign-in", "port": 80}
#
# my_options = {
#     'mode': "chrome",
#     'host': url["host"],
#     'port': url["port"],
#     'chromeFlags': ["--start-fullscreen", "--browser-startup-dialog"]
# }
#
# urlT = url["host"]
#
# chrome_path = chrome.find_path()
#
# if chrome_path is not None:
#     # if open_sep:
#     #     if login_flag and username != "" and password != "":
#     #         url_with_UP = url["url_add"] + "client/access/login/test/" + username + "/" + password + \
#     #                       "?callBack=http://" + urlT
#     #         eel.start(url_with_UP, suppress_error=True, block=False, options=my_options)
#     #     else:
#
#     # eel.start("", suppress_error=True, options=my_options)
#     # else:
#     chrome_path = chrome_path.replace(sep, '/') + ' %s'
#     get(chrome_path).open(urlT)


#
# '''
# df = data_import_sia(csv_file_path_in)
# df = indicator_extraction(df)
# df.to_csv(csv_file_path_out, index=False, encoding='utf-8')
# #df = pd.read_csv(csv_file_path_out)
# model = indication_trainer(df)
# #model = LSTM_model(df)
# model.save(h5_file_path_out)
# '''
