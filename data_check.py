import os

import pandas as pd
import numpy as np

main_path = "File/trade_data/"
files = os.listdir(main_path)

for file in files:
    # Read the csv file
    try:
        data = pd.read_csv(main_path + file)
    except pd.errors.EmptyDataError:
        print(file, " is empty")
        continue
    except:
        print("some thing else happened")

    time = data['time']
    d = []

    if len(np.unique(np.array(time))) != data.shape[0]:
        print(data.shape[0])
        print(len(np.unique(np.array(time))))
        print(file)
