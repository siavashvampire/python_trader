import json
from time import sleep

import pandas as pd
from pandas import DataFrame
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

# from app.logging.api import add_log
from app.market_trading.api import get_trading_by_country_currency
from app.quotex.quotexapi.stable_api import Quotex

trade_window_url_quotex = 'https://quotex.com/en/sign-in/'


def login_quotex(driver: WebDriver):
    driver.get("https://qxbroker.com/en/sign-in")
    wait = WebDriverWait(driver, 10)
    email_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='tab-1']/form/div[1]/input")))
    email_input.send_keys("eng.tit0@yahoo.com")
    pass_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='tab-1']/form/div[2]/input")))
    pass_input.send_keys("titometi2")
    sign_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="tab-1"]/form/button')))
    sign_button.click()


def extract_ssid_quotex(driver: WebDriver):
    # Extract the SSID token from the network logs
    ssid = None
    while True:
        if ssid is not None:
            break

        for entry in driver.get_log('performance'):
            try:
                shell = entry["message"]
                payloadData = json.loads(
                    shell)["message"]["params"]["response"]["payloadData"]

                if "auth" in shell and "session" in shell:
                    ssid = payloadData
            except:
                pass
        sleep(1)

    # initialize cookie variables
    _ga_L4T5GBPFHJ = None
    _ga = None
    lang = None
    nas = None
    z = None
    _vid_t = None
    __vid_l3 = None
    __cf_bm = None

    # Get the cookies from the browser session
    # Parse the cookies and save their values to individual variables
    cookies = driver.get_cookies()

    # parse the cookies and extract specific values
    for cookie in cookies:
        if cookie['name'] == '_ga_L4T5GBPFHJ':
            _ga_L4T5GBPFHJ = cookie['value']
        elif cookie['name'] == '_ga':
            _ga = cookie['value']
        elif cookie['name'] == 'lang':
            lang = cookie['value']
        elif cookie['name'] == 'nas':
            nas = cookie['value']
        elif cookie['name'] == 'z':
            z = cookie['value']
        elif cookie['name'] == '_vid_t':
            _vid_t = cookie['value']
        elif cookie['name'] == '__vid_l3':
            __vid_l3 = cookie['value']
        elif cookie['name'] == '__cf_bm':
            __cf_bm = cookie['value']

    # format cookies into a string
    websocket_cookie = f'referer=https%3A%2F%2Fwww.google.com%2F; _ga_L4T5GBPFHJ={_ga_L4T5GBPFHJ}; _ga={_ga}; lang={lang}; nas={nas}; z={z}; _vid_t={_vid_t}; __vid_l3={__vid_l3}; __cf_bm={__cf_bm}'

    # get user agent and host from the web driver
    user_agent = driver.execute_script('return navigator.userAgent;')
    host = driver.execute_script("return window.location.host;")

    # close the web driver and print extracted information
    if ssid:
        driver.quit()
        # print("ssid:", ssid)
        # print("websocket_cookie:", websocket_cookie)
        # print("user_agent:", user_agent)
        # print("host:", host)

    return ssid, websocket_cookie, user_agent, host


def prepare_api_quotex():
    option = Options()
    option.add_argument("--disable-extensions")
    option.add_argument("--disable-notifications")
    option.add_argument("--window-size=720,720")
    # Use a specific version of Chrome

    d = DesiredCapabilities.CHROME
    d['goog:loggingPrefs'] = {'performance': 'ALL'}
    # self.driver = uc.Chrome(headless=True, use_subprocess=False)
    driver = uc.Chrome()
    # self.driver = uc.Chrome(options=option, desired_capabilities=d)
    driver.delete_all_cookies()

    login_quotex(driver)

    ssid, websocket_cookie, user_agent, host = extract_ssid_quotex(driver)

    qx_api = Quotex(set_ssid=ssid, host=host, user_agent=user_agent, websocket_cookie=websocket_cookie)

    # check if connection to Quotex API was successful and change balance type
    check, reason = qx_api.connect()

    qx_api.change_balance("PRACTICE")

    return qx_api, check, reason


qx_api, check, reason = prepare_api_quotex()


def get_balance_quotex() -> int:
    """
        get balance of an account in quotex
    :return:
        return int that shows balance of an account in quotex
    """
    return qx_api.get_balance()


# qx_api.get_candle()
# qx_api.check_win()


def create_order_quotex(name: str, unit: int, duration: int = 60) -> dict:
    """

    :param name: name = "EUR_USD" that should to convert to asset = "EURUSD"
    :param unit: unit = 10 or -10, "call" or "put"
    :param duration: durations in second
    :return: buy_info that have id of order
    {'id': 'bf09a6e0-e0b2-482d-85b6-9b9e9c2a6fdd', 'openTime': '2023-07-01 11:43:47', 'closeTime': '2023-07-01 11:45:00', 'openTimestamp': 1688211827, 'closeTimestamp': 1688211900, 'uid': 24692142, 'isDemo': 1, 'tournamentId': 0, 'amount': 1000, 'purchaseTime': 1688211870, 'profit': 870, 'percentProfit': 87, 'percentLoss': 100, 'openPrice': 1.08269, 'copyTicket': '', 'closePrice': 0, 'command': 0, 'asset': 'EURUSD_otc', 'nickname': '#24692142', 'accountBalance': 10000, 'requestId': '1', 'openMs': 388, 'currency': 'USD'}

    """
    # name = "EUR_USD"
    # asset = "EURUSD"

    currencies = name.split("_")
    country_from = currencies[0]
    country_to = currencies[1]
    # asset = country_from + country_to
    asset = country_from + country_to + "_otc"

    amount = abs(unit)

    trade = get_trading_by_country_currency(country_from, country_to)

    if unit > 0:
        # add_log(1, trade.id, 4, "we are buying " + trade.currency_disp())
        direction = "call"  # or "put"
    else:
        # add_log(1, trade.id, 2, "we are selling " + trade.currency_disp())
        direction = "put"  # or "put"

    c, buy_info = qx_api.buy(asset, amount, direction, duration)
    return buy_info


def close_api_quotex() -> None:
    qx_api.close()


def get_real_time_data_quotex(name: str) -> float:
    currencies = name.split("_")
    country_from = currencies[0]
    country_to = currencies[1]
    name = country_from + country_to

    qx_api.start_candles_stream(name, 2)
    temp = qx_api.get_realtime_candles(name)[0]
    qx_api.stop_candles_stream(name)

    # from datetime import datetime
    # timestamp = temp['time']
    # dt_object = datetime.fromtimestamp(timestamp)
    # print(dt_object)
    # TODO:inja time ham mide fekr konam inja bayad check konim k time age ba alan yeki nabod None pass bede

    return temp['price']


def get_last_candle_quotex(name: str, candle: str) -> DataFrame:
    """
    :param name: ex. "EUR_USD"
    :param candle: "S5" or "M1"
    :return:
        return DataFrame that has Five columns 'time','o',h','l','c'
    """
    # if candle.startswith('S'):
    #     last_hour_date_time = datetime.utcnow() - timedelta(seconds=6)
    #
    #     start = tpqoa_api.transform_datetime(last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S'))
    #     end = tpqoa_api.transform_datetime(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    #
    # elif candle.startswith('M'):
    #     last_hour_date_time = datetime.utcnow() - timedelta(minutes=2)
    #
    #     start = tpqoa_api.transform_datetime(last_hour_date_time.strftime('%Y-%m-%d %H:%M'))
    #     end = tpqoa_api.transform_datetime(datetime.utcnow().strftime('%Y-%m-%d %H:%M'))
    # else:
    #     return DataFrame()
    #
    # data = tpqoa_api.retrieve_data(name, start, end, candle, "A")
    # try:
    #     data = data.drop(['volume', 'complete'], axis=1)
    # except:
    #     pass
    #
    # data = data.tail(1).reset_index()
    data = DataFrame()
    return data


def get_history_quotex(name: str, start_time: str, end_time: str, candle: str, csv_path: str = "") -> DataFrame:
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

    # # tpqoa_api.get_history("EUR_USD", "2020-08-03", "2023-05-21", "M1", "A")
    # data = tpqoa_api.get_history(name, start_time, end_time, candle, "A")
    #
    # if csv_path != "":
    #     data.to_csv(csv_path, index=True, encoding='utf-8')
    # data = data.reset_index()

    qx_api.get_candle()
    data = DataFrame()
    return data


def open_trade_window_quotex() -> None:
    """
        open web driver
    """
    try:
        # option = Options()
        # option.add_argument("detach")
        # Use a specific version of Chrome
        # driver = uc.Chrome(options=option)
        driver = uc.Chrome()

        login_quotex(driver)
    except Exception as e:
        print("error in quotex api : " + str(e))
    # webdriver.Chrome(options=options).get(trade_window_url_quotex)
# qx_api.get_balance()
# self.qx_api = qx_api
# self.qx_api.change_balance("PRACTICE")  # or "REAL"
#
# # define trading parameters
# asset = "EURUSD"
# amount = 1
# dir = "call"  # or "put"
# duration = 60  # in seconds
#
# # print account balance and execute trade
# print("Balance: ", self.qx_api.get_balance())
# c, buy_info = self.qx_api.buy(asset, amount, dir, duration)
#
# # print trade execution information
# print(buy_info)
# if 'id' in buy_info.keys():
#     print("----Trade----")
#     print("Get: ", self.qx_api.check_win(buy_info["id"]))
#     print("----Trade----")
#     print("Balance: ", self.qx_api.get_balance())
#     sleep(20)
# else:
#     print("BUY Fail")
# self.qx_api.close()  # close the connection to the Quotex API
