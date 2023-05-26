import pandas as pd
import pandas_ta as ta
import numpy as np
from app.ml.model.techiacals_tradingview import *


def metatrader_data_import_meta(csv_file):  # function for importing metatrader data and changing it to our form.
    df = pd.read_csv(csv_file, sep='\t')
    df.rename(columns={'<DATE>': 'Date',
                       '<TIME>': 'Time',
                       '<OPEN>': 'Open',
                       '<HIGH>': 'High',
                       '<LOW>': 'Low',
                       '<CLOSE>': 'Close',
                       '<TICKVOL>': 'Volume'},
              inplace=True, errors='raise')

    df = df[['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']]
    return df


def metatrader_data_import_trview(csv_file):  # function for importing metatrader data and changing it to our form.
    df = pd.read_csv(csv_file, sep='\t')
    df.rename(columns={'time': 'Date',
                       'o': 'Open',
                       'h': 'High',
                       'l': 'Low',
                       'c': 'Close',
                       'volume': 'Volume'},
              inplace=True, errors='raise')

    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    return df



def adding_raw_indicators(df):  # function for adding raw indicators to our dataframe.
    df.ta.macd(fast=12, slow=26, signal=9, append=True)
    df.ta.psar(append=True)
    df.ta.cci(lenght=20, append=True)
    df.ta.ao(append=True)
    df.ta.mom(append=True)

    df.ta.ichimoku(append=True)  # did not get it
    df.ta.adx()  # did not get it
    df.ta.uo(append=True)  # did not get it
    df.ta.vwma(append=True)  # did not get it

    # stock in the function
    df.ta.stoch(k=20, append=True)
    # default stock
    df.ta.stoch(append=True)
    # bbands on the internet
    df.ta.bbands(length=30, std=2, mamode="sma", ddof=0, append=True)
    # default numbers
    df.ta.bbands(append=True)
    # rsi recommended by internet:
    df.ta.rsi(length=15, scalar=3, drift=3, append=True)
    # rsi default number
    df.ta.rsi(append=True)

    # Simple moving average:
    df.ta.sma(length=5, append=True)
    df.ta.sma(length=10, append=True)
    df.ta.sma(length=20, append=True)
    df.ta.sma(length=30, append=True)
    df.ta.sma(length=50, append=True)
    df.ta.sma(length=100, append=True)
    df.ta.sma(length=200, append=True)
    # Exponential moving average:
    df.ta.ema(length=5, append=True)
    df.ta.ema(length=10, append=True)
    df.ta.ema(length=20, append=True)
    df.ta.ema(length=30, append=True)
    df.ta.ema(length=50, append=True)
    df.ta.ema(length=100, append=True)
    df.ta.ema(length=200, append=True)
    return df


def bbands_fun(df):
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

    for i in range(len(buy_bbands_diff) - 1):
        if (buy_bbands_diff[i + 1] * buy_bbands_diff[i] < 0) and (df['Close'][i + 1] > df['BBU_30_2.0'][i + 1]):
            bbands[i + 1] = 1
            bbands[i + 2] = 1

    if 'sell_bbands_diff' in df.columns.values.tolist():
        df.drop('bbands', axis=1, inplace=True)
        df.drop('buy_bbands_diff', axis=1, inplace=True)
        df.drop('sell_bbands_diff', axis=1, inplace=True)
    else:
        pass

    df.insert(7, 'bbands', bbands)
    df.insert(8, 'buy_bbands_diff', buy_bbands_diff)
    df.insert(9, 'sell_bbands_diff', sell_bbands_diff)
    return df


def adding_indicator_signal(df):
    df["RSI_14_sig"] = 'Na'
    df["RSI_15_sig"] = 'Na'
    df["STOCH_20_3_3_sig"] = 'Na'
    df["STOCH_14_3_3_sig"] = 'Na'
    df['CCI_14_0.015_sig'] = 'Na'
    df["AO_5_34_sig"] = 'Na'
    df["MOM_10_sig"] = 'Na'
    df["MACD_12_26_9_sig"] = 'Na'
    ma_list = ["EMA_10", "SMA_10", "EMA_20", "SMA_20", "EMA_30", "SMA_30", "EMA_50", "SMA_50", "EMA_100", "SMA_100",
               "EMA_200", "SMA_200"]
    for index in ma_list:
        df[index + '_sig'] = 'Na'

    df = bbands_fun(df)

    for i_0 in range(len(df.index.tolist()) - 2):
        i = i_0 + 2
        # RSI (14)
        if None not in [df['RSI_14'][i], df['RSI_14'][i - 1]]:
            df.loc[i, "RSI_14_sig"] = Compute.RSI(df['RSI_14'][i], df['RSI_14'][i - 1])

        # RSI (15)
        if None not in [df['RSI_15'][i], df['RSI_15'][i - 1]]:
            df.loc[i, "RSI_15_sig"] = Compute.RSI(df['RSI_15'][i], df['RSI_15'][i - 1])

        # Stoch 14 %K
        if None not in [df['STOCHk_14_3_3'][i], df['STOCHd_14_3_3'][i], df['STOCHk_14_3_3'][i - 1],
                        df['STOCHd_14_3_3'][i - 1]]:
            df.loc[i, "STOCH_14_3_3_sig"] = Compute.Stoch(
                df['STOCHk_14_3_3'][i], df['STOCHd_14_3_3'][i], df['STOCHk_14_3_3'][i - 1], df['STOCHd_14_3_3'][i - 1])

        # Stoch 20 %K
        if None not in [df['STOCHk_20_3_3'][i], df['STOCHd_20_3_3'][i], df['STOCHk_20_3_3'][i - 1],
                        df['STOCHd_20_3_3'][i - 1]]:
            df.loc[i, "STOCH_20_3_3_sig"] = Compute.Stoch(
                df['STOCHk_20_3_3'][i], df['STOCHd_20_3_3'][i], df['STOCHk_20_3_3'][i - 1],
                df['STOCHd_20_3_3'][i - 1])

        # CCI (20)
        if None not in [df['CCI_14_0.015'][i], df['CCI_14_0.015'][i - 1]]:
            df.loc[i, 'CCI_14_0.015_sig'] = Compute.CCI20(
                df['CCI_14_0.015'][i], df['CCI_14_0.015'][i - 1])

        # AO
        if None not in [df['AO_5_34'][i], df['AO_5_34'][i - 1]] and df['AO_5_34'][i - 2] != None:
            df.loc[i, "AO_5_34_sig"] = Compute.AO(
                df['AO_5_34'][i], df['AO_5_34'][i - 1], df['AO_5_34'][i - 2])

        # Mom (10)
        if None not in [df['MOM_10'][i], df['MOM_10'][i - 1]]:
            df.loc[i, "MOM_10_sig"] = Compute.Mom(
                df['MOM_10'][i], df['MOM_10'][i - 1])

        # MACD
        if None not in [df['MACD_12_26_9'][i], df['MACDs_12_26_9'][i]]:
            df.loc[i, "MACD_12_26_9_sig"] = Compute.MACD(
                df['MACD_12_26_9'][i], df['MACDs_12_26_9'][i])

        # MOVING AVERAGES
        for index in ma_list:
            if df[index][i] != None:
                df.loc[i, index + '_sig'] = Compute.MA(df[index][i], df['Close'][i])
    return df


def solving_nans(df):
    df = df[300:]
    df = df.reset_index(drop=True)
    return df


def adding_percent_change(df):
    df["Percent_Change_5"] = 0
    df["Percent_Change_3"] = 0
    df["Percent_Change_10"] = 0
    for i in list(df.index.values)[:-10]:
        df["Percent_Change_5"][i] = ((df["Close"][i + 5] - df["Close"][i]) / df["Close"][i]) * 100
        df["Percent_Change_3"][i] = ((df["Close"][i + 3] - df["Close"][i]) / df["Close"][i]) * 100
        df["Percent_Change_10"][i] = ((df["Close"][i + 10] - df["Close"][i]) / df["Close"][i]) * 100
    return df


def winning_policy_1(df_in, treshold):
    df_in["signal1"] = 0
    for i in list(df_in.index.values):
        if df_in["Percent_Change_10"][i] > treshold:
            df_in["signal1"][i] = 1
        elif df_in["Percent_Change_10"][i] < -treshold:
            df_in["signal1"][i] = -1

    return df_in
