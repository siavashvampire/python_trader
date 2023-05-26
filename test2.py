from app.ml.model.main import learn

csv_file_path_in = 'app/ml/file/EURUSD_M1_202301251915_202305031504.csv'
csv_file_path_out = 'app/ml/file/EURUSD_indicator.csv'

learn(csv_file_path_in,csv_file_path_out)


