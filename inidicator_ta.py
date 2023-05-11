import pandas as pd
import pandas_ta as ta
import numpy as np

df = pd.read_csv('EURUSD_M1_202301251915_202305031504.csv', sep='\t')

df.rename(columns={'<DATE>': 'Date',
                   '<TIME>': 'Time',
                   '<OPEN>': 'Open',
                   '<HIGH>': 'High',
                   '<LOW>': 'Low',
                   '<CLOSE>': 'Close',
                   '<TICKVOL>': 'Volume'},
          inplace=True, errors='raise')

df = df[['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']]


df.drop('bbands', axis=1, inplace=True)
df.drop('buy_bbands_diff', axis=1, inplace=True)
df.drop('sell_bbands_diff', axis=1, inplace=True)

# Cover and go long when the daily closing price crosses below the lower band.
# Cover and go short when the daily closing price crosses above the upper band.

df.ta.bbands(length=30, std=2, mamode="sma", ddof=0, append=True)
buy_bbands_diff = df['BBU_30_2.0'] - df['Close']
sell_bbands_diff = df['BBL_30_2.0'] - df['Close']
bbands = np.zeros((len(buy_bbands_diff), 1))

for i in range(len(buy_bbands_diff) - 1):
    if (sell_bbands_diff[i + 1] * sell_bbands_diff[i] < 0) and (df['Close'][i + 1] < df['BBL_30_2.0'][i + 1]):
        bbands[i + 1] = -1
        bbands[i + 2] = -1
        bbands[i + 3] = -1

for i in range(len(buy_bbands_diff) - 1):
    if (buy_bbands_diff[i + 1] * buy_bbands_diff[i] < 0) and (df['Close'][i + 1] > df['BBU_30_2.0'][i + 1]):
        bbands[i + 1] = 1
        bbands[i + 2] = 1
        bbands[i + 3] = 1

df.insert(7, 'bbands', bbands)
df.insert(8, 'buy_bbands_diff', buy_bbands_diff)
df.insert(9, 'sell_bbands_diff', sell_bbands_diff)

df.drop('macd_h', axis=1, inplace=True)
df.drop('macd_sig', axis=1, inplace=True)

df.ta.macd(fast=12, slow=26, signal=9, append=True)
macd_h = df['MACDh_12_26_9']
macd_sig = np.zeros((len(macd_h), 1))

for i in range(len(buy_bbands_diff) - 3):
    if (macd_h[i + 1] * macd_h[i] < 0) and (0 > macd_h[i + 1]):
        macd_sig[i + 1] = -1
        macd_sig[i + 2] = -1
        macd_sig[i + 3] = -1

for i in range(len(buy_bbands_diff) - 3):
    if (macd_h[i + 1] * macd_h[i] < 0) and (0 < macd_h[i + 1]):
        macd_sig[i + 1] = 1
        macd_sig[i + 2] = 1
        macd_sig[i + 3] = 1

df.insert(10, 'macd_h', macd_h, allow_duplicates=True)
df.insert(11, 'macd_sig', macd_sig, allow_duplicates=True)
np.sum(df['macd_sig'])

df.to_csv('test_df.csv', index=False, encoding='utf-8')
