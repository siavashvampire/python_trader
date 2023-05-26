from app.ml.model.indicator_extraction import metatrader_data_import, adding_raw_indicators, adding_indicator_signal, \
    solving_nans, adding_percent_change, winning_policy_1

csv_file = 'app/ml/file/EURUSD_M1_202301251915_202305031504.csv'
df = metatrader_data_import(csv_file)
df = adding_raw_indicators(df)
df = adding_indicator_signal(df)
df = solving_nans(df)
df = adding_percent_change(df)
df = winning_policy_1(df, 0.03)
print(df)
df.to_csv('app\ml\\file\EURUSD_indicator.csv', index=False, encoding='utf-8')

