from app.ml.main import indicator_extraction, indication_trainer

csv_file_path_in = 'app/ml/file/EURUSD_M1_202301251915_202305031504.csv'
csv_file_path_out = 'app/ml/file/EURUSD_indicator.csv'
h5_file_path_out = 'app/ml/file/model.h5'

#indicator_extraction(csv_file_path_in, csv_file_path_out)
indication_trainer(csv_file_path_out, h5_file_path_out)


