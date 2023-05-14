from tradingview_ta import TA_Handler

handler = TA_Handler(
    symbol="EURUSD",
    exchange="FX_IDC",
    screener="forex",
    interval="1m",
    timeout=None
)
analysis = handler.get_analysis()
# handler.get_indicators()
# import json
#
# import requests
#
# data = {'symbols': {'tickers': ['FX_IDC:EURUSD'], 'query': {'types': []}},
#         'columns': ['Recommend.Other|1', 'Recommend.All|1', 'Recommend.MA|1', 'RSI|1', 'RSI[1]|1', 'Stoch.K|1',
#                     'Stoch.D|1', 'Stoch.K[1]|1', 'Stoch.D[1]|1', 'CCI20|1', 'CCI20[1]|1', 'ADX|1', 'ADX+DI|1',
#                     'ADX-DI|1', 'ADX+DI[1]|1', 'ADX-DI[1]|1', 'AO|1', 'AO[1]|1', 'Mom|1', 'Mom[1]|1', 'MACD.macd|1',
#                     'MACD.signal|1', 'Rec.Stoch.RSI|1', 'Stoch.RSI.K|1', 'Rec.WR|1', 'W.R|1', 'Rec.BBPower|1',
#                     'BBPower|1', 'Rec.UO|1', 'UO|1', 'close|1', 'EMA5|1', 'SMA5|1', 'EMA10|1', 'SMA10|1', 'EMA20|1',
#                     'SMA20|1', 'EMA30|1', 'SMA30|1', 'EMA50|1', 'SMA50|1', 'EMA100|1', 'SMA100|1', 'EMA200|1',
#                     'SMA200|1', 'Rec.Ichimoku|1', 'Ichimoku.BLine|1', 'Rec.VWMA|1', 'VWMA|1', 'Rec.HullMA9|1',
#                     'HullMA9|1', 'Pivot.M.Classic.S3|1', 'Pivot.M.Classic.S2|1', 'Pivot.M.Classic.S1|1',
#                     'Pivot.M.Classic.Middle|1', 'Pivot.M.Classic.R1|1', 'Pivot.M.Classic.R2|1', 'Pivot.M.Classic.R3|1',
#                     'Pivot.M.Fibonacci.S3|1', 'Pivot.M.Fibonacci.S2|1', 'Pivot.M.Fibonacci.S1|1',
#                     'Pivot.M.Fibonacci.Middle|1', 'Pivot.M.Fibonacci.R1|1', 'Pivot.M.Fibonacci.R2|1',
#                     'Pivot.M.Fibonacci.R3|1', 'Pivot.M.Camarilla.S3|1', 'Pivot.M.Camarilla.S2|1',
#                     'Pivot.M.Camarilla.S1|1', 'Pivot.M.Camarilla.Middle|1', 'Pivot.M.Camarilla.R1|1',
#                     'Pivot.M.Camarilla.R2|1', 'Pivot.M.Camarilla.R3|1', 'Pivot.M.Woodie.S3|1', 'Pivot.M.Woodie.S2|1',
#                     'Pivot.M.Woodie.S1|1', 'Pivot.M.Woodie.Middle|1', 'Pivot.M.Woodie.R1|1', 'Pivot.M.Woodie.R2|1',
#                     'Pivot.M.Woodie.R3|1', 'Pivot.M.Demark.S1|1', 'Pivot.M.Demark.Middle|1', 'Pivot.M.Demark.R1|1',
#                     'open|1', 'P.SAR|1', 'BB.lower|1', 'BB.upper|1', 'AO[2]|1', 'volume|1', 'change|1', 'low|1',
#                     'high|1']}
#
# scan_url = 'https://scanner.tradingview.com/forex/scan'
# headers = {"User-Agent": "tradingview_ta/{}".format('3.3.0')}
# response = requests.post(scan_url, json=data, headers=headers)
#
# result = json.loads(response.text)["data"]
# print(result)