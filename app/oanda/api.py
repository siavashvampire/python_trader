from pandas import DataFrame
from selenium import webdriver

from app.data_connector.model.enums import APIUsed
from app.oanda.model.tpqoa import TPQOA

from datetime import datetime, timedelta

from core.config.Config import api_used


def prepare_api_oanda():
    pass


trade_window_url_oanda = 'https://trade.oanda.com/'

if api_used == APIUsed().oanda:
    tpqoa_api = TPQOA("File/Config/oanda.cfg")


def get_real_time_data_oanda(name: str) -> float:
    response = tpqoa_api.stream_one_data(name)
    return response.asks[0].dict()['price']


def get_history_oanda(name: str, start_time: str, end_time: str, candle: str, csv_path: str = "") -> DataFrame:
    """
        get history of data in candles

    :param name: name of trade
    :param start_time: start time of trade in '%Y-%m-%d %H:%M:%S' :"2020-08-03"
    :param end_time: end time of trade in '%Y-%m-%d %H:%M:%S' :"2023-05-21"
    :param candle:candle of trade in candle model "M1"
    :param csv_path:csv that want to save it
    :return:
        return DataFrame that has Five columns 'time','o',h','l','c'
    """
    # tpqoa_api.get_history("EUR_USD", "2020-08-03", "2023-05-21", "M1", "A")
    data = tpqoa_api.get_history(name, start_time, end_time, candle, "A")

    try:
        data = data.drop(['volume', 'complete'], axis=1)
    except:
        pass

    if csv_path != "":
        data.to_csv(csv_path, index=True, encoding='utf-8')
    data = data.reset_index()

    return data


def get_last_candle_oanda(name: str, candle: str) -> DataFrame:
    """
    :param name: ex. "EUR_USD"
    :param candle: "S5" or "M1"
    :return:
        return DataFrame that has Five columns 'time','o',h','l','c'
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
    try:
        data = data.drop(['volume', 'complete'], axis=1)
    except:
        pass

    data = data.tail(1).reset_index()
    return data


def create_order_oanda(name: str, unit: int, duration: int = 60) -> tuple[bool, dict]:
    """
        create order
    :param name: name of trade (EUR_USD)
    :param unit: unit of trade(1000)
    :param duration: duration of trade(60s)
    """
    tpqoa_api.create_order(instrument=name, units=unit, sl_distance=0.1)
    return True, {}


def get_balance_oanda() -> float:
    """
        get balance from oanda
    :return:
    """
    # TODO:bayad doros beshe in
    return 1000.00


def close_api_oanda() -> None:
    """
        should close api
    """
    pass


def open_trade_window_oanda() -> None:
    """
        open web driver
    """
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_experimental_option("detach", True)
    webdriver.Chrome(options=options).get(trade_window_url_oanda)

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
