import os

import pandas as pd
import numpy as np
main_path = "File/trade_data/"
files = os.listdir(main_path)

for file in files:
    # Read the csv file
    data = pd.read_csv(main_path + file)
    time = data['time']
    d = []

    if len(np.unique(np.array(time))) != 133920:
        print(file)


