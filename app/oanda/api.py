from pandas import DataFrame
from v20.pricing import ClientPrice

from app.oanda.model.tpqoa import TPQOA

from datetime import datetime, timedelta

tpqoa_api = TPQOA("File/Config/oanda.cfg")


def get_real_time_data_oanda(name: str) -> ClientPrice:
    return tpqoa_api.stream_one_data(name)


def get_history_oanda(name: str, start_time: str, end_time: str, candle: str, csv_path: str = "") -> DataFrame:
    # tpqoa_api.get_history("EUR_USD", "2020-08-03", "2023-05-21", "M1", "A")
    data = tpqoa_api.get_history(name, start_time, end_time, candle, "A")

    if csv_path != "":
        data.to_csv(csv_path, index=True, encoding='utf-8')

    return data


def get_last_candle_oanda(name: str, candle: str) -> DataFrame:
    """
    :param name: ex. "EUR_USD"
    :param candle: "S5" or "M1"
    :return:
    """
    if candle.startswith('S'):
        last_hour_date_time = datetime.utcnow() - timedelta(seconds=6)

        start = tpqoa_api.transform_datetime(last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S'))
        end = tpqoa_api.transform_datetime(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

    elif candle.startswith('M'):
        last_hour_date_time = datetime.utcnow() - timedelta(minutes=2)

        start = tpqoa_api.transform_datetime(last_hour_date_time.strftime('%Y-%m-%d %H:%M'))
        end = tpqoa_api.transform_datetime(datetime.utcnow().strftime('%Y-%m-%d %H:%M'))
    else:
        return DataFrame()

    data = tpqoa_api.retrieve_data(name, start, end, candle, "A")
    return data.tail(1)


def create_order_oanda(name: str, unit: int) -> None:
    tpqoa_api.create_order(instrument=name, units=unit, sl_distance=0.1)

# api.get_account_summary()
#
# api.account_type
#
# api.account_id
#
# api.get_instruments()
#
# instr = api.get_instruments()
#
# len(instr)
#
# instr[0]
#
#
# api.get_history(instrument="EUR_USD", start="2020-07-01", end="2020-07-31", granularity="D", price="B")
#
#
# df = api.get_history(instrument="EUR_USD", start="2020-07-01", end="2020-07-31",
#                      granularity="D", price="B")
#
#
#
# api.get_history(instrument="EUR_USD", start="2020-07-01", end="2020-07-01",
#                 granularity="D", price="A")
#
#
#
# api.get_history(instrument="EUR_USD", start="2020-07-01", end="2020-07-01",
#                 granularity="D", price="B")
#
#
# api.get_history("EUR_USD", "2020-08-03", "2020-08-05", "H1", "A")
#
#
# api.get_history("EUR_USD", "2020-08-03", "2020-08-05", "H12", "A")
#
# print(api.get_history("EUR_USD", "2023-05-20", "2023-05-21", "M1", "A"))
#
#
#
# print(api.get_history("EUR_USD", "2020-08-03", "2020-08-04", "S5", "A"))
#
# api.get_instruments()
#
#
#
# api.get_history("SPX500_USD", "2020-08-03", "2020-08-04", "H1", "A")


# msg = api.stream_one_data('EUR_USD')
# # print(msg)
# print(msg.time, float(msg.bids[0].dict()['price']), float(msg.asks[0].dict()['price']))
# api.stop_stream()

# api.create_order(instrument="EUR_USD", units=1000, sl_distance=0.1)
# sleep(3)
# api.create_order(instrument="EUR_USD", units=-10, sl_distance=0.1)
#
# print(api.get_account_summary())
#
# print(api.get_transactions())
#
# print(api.print_transactions(tid=1))
