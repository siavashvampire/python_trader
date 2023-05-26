from app.ml.model.indicator_extraction import metatrader_data_import, adding_raw_indicators, adding_indicator_signal, \
    solving_nans, adding_percent_change, winning_policy_1


def learn(csv_file_path_in: str, csv_file_path_out: str):
    df = metatrader_data_import(csv_file_path_in)
    df = adding_raw_indicators(df)
    df = adding_indicator_signal(df)
    df = solving_nans(df)
    df = adding_percent_change(df)
    df = winning_policy_1(df, 0.03)
    df.to_csv(csv_file_path_out, index=False, encoding='utf-8')
