import json
from datetime import datetime
from time import sleep

from pandas import DataFrame
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
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
        ec.presence_of_element_located((By.XPATH, "//*[@id='tab-1']/form/div[1]/input")))
    email_input.send_keys("eng.tit0@yahoo.com")
    pass_input = WebDriverWait(driver, 20).until(
        ec.presence_of_element_located((By.XPATH, "//*[@id='tab-1']/form/div[2]/input")))
    pass_input.send_keys("titometi2")
    sign_button = WebDriverWait(driver, 20).until(
        ec.presence_of_element_located((By.XPATH, '//*[@id="tab-1"]/form/button')))
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
    # option = Options()
    # option.add_argument("--disable-extensions")
    # option.add_argument("--disable-notifications")
    # option.add_argument("--window-size=720,720")
    # Use a specific version of Chrome

    d = DesiredCapabilities.CHROME
    d['goog:loggingPrefs'] = {'performance': 'ALL'}
    # self.driver = uc.Chrome(headless=True, use_subprocess=False)
    driver = uc.Chrome()
    # self.driver = uc.Chrome(options=option, desired_capabilities=d)
    driver.delete_all_cookies()

    login_quotex(driver)

    ssid, websocket_cookie, user_agent, host = extract_ssid_quotex(driver)

    # print(ssid)
    # print(host)
    # print(user_agent)
    # print(websocket_cookie)

    # ssid = """42["authorization",{"session":"Ev6gXi5BrbSZofsQIYmf4lv1VnWuuocWEWCeR0Gr","isDemo":0,"tournamentId":0}]"""
    # host = "qxbroker.com"  # qxbroker.com
    # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    # websocket_cookie = "referer=https%3A%2F%2Fwww.google.com%2F; _ga_L4T5GBPFHJ=GS1.1.1688309181.1.1.1688309186.0.0.0; _ga=GA1.1.192026297.1688309182; lang=en; nas=[%22EURUSD_otc%22]; z=[[%22graph%22%2C2%2C0%2C0%2C0.8333333]]; _vid_t=Ti4cw3aCg42SaP6EWmRSuci3XkX0feu50ka0dogV30MfAMubT2fUp6kTKpBe5PHcw5/xKb7Z9QczEQ==; __vid_l3=04131deb-ae03-4bd1-b975-13ebd852c998; __cf_bm=5ZDQ.k9B8nWZ.t1Ppzt6zdcNfr903LpRX.Qg7iTpdyY-1688309182-0-Aa3BGVqtzdfn5Js37EtZ0ooR3+WesIlWwQ8aXYte0cG/O40nSGybQwvwPZtxvvp9Tg2LtsSRmc5iY1DUIG7PSJ4+DS+JhVJD06t9UnmZdsTb"

    qx_api_temp = Quotex(set_ssid=ssid, host=host, user_agent=user_agent, websocket_cookie=websocket_cookie)

    # check if connection to Quotex API was successful and change a balance type
    check, reason = qx_api_temp.connect()

    qx_api_temp.change_balance("PRACTICE")

    return qx_api_temp


qx_api = prepare_api_quotex()


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
    asset = country_from + country_to

    # TODO:zaman otc ro check kone k age otc bod az otc bekhare
    if otc_check():
        asset += "_otc"

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
    """
        closing qpi quotex
    """
    qx_api.close()


def get_real_time_data_quotex(name: str) -> float:
    currencies = name.split("_")
    country_from = currencies[0]
    country_to = currencies[1]
    asset = country_from + country_to

    # TODO:zaman otc ro check kone k age otc bod az otc bekhare
    if otc_check():
        asset += "_otc"

    qx_api.start_candles_stream(asset, 2)
    temp = qx_api.get_realtime_candles(asset)[0]
    qx_api.stop_candles_stream(asset)

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
    try:
        currencies = name.split("_")
        country_from = currencies[0]
        country_to = currencies[1]
        asset = country_from + country_to

        # TODO:zaman otc ro check kone k age otc bod az otc bekhare
        if otc_check():
            asset += "_otc"


        _time = datetime.utcnow().timestamp()

        offset = 120  # how much sec want to get     _time-offset --->your candle <---_time

        if candle == "M1":
            period = 60  # candle size in sec
        else:
            period = 60  # candle size in sec

        data = qx_api.get_candle(asset, _time, offset, period)['data'][-1]


        data2 = {
            'time': [datetime.fromtimestamp(data['time'])],
            'o': [data['open']],
            'c': [data['close']],
            'h': [data['high']],
            'l': [data['low']],
        }

        return DataFrame(data2)
    except:
        return DataFrame()

def get_history_quotex(name: str, start_time: str, end_time: str, candle: str, csv_path: str = "") -> DataFrame:
    # TODO:irad dare dakhele OTC 2 saat akharo bishtar nemide
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

    currencies = name.split("_")
    country_from = currencies[0]
    country_to = currencies[1]
    asset = country_from + country_to

    # TODO:zaman otc ro check kone k age otc bod az otc bekhare
    if otc_check():
        asset += "_otc"

    # check_connect, message = qx_api.connect()
    # print(check_connect)

    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    _time = end_time.timestamp()

    # _time = int(time())  # the candle end of time
    offset = _time - start_time.timestamp() + 60 # how much sec want to get     _time-offset --->your candle <---_time

    if candle == "M1":
        period = 60  # candle size in sec
    else:
        period = 60  # candle size in sec

    data = qx_api.get_candle(asset, _time, offset, period)['data']

    # datas = qx_api.get_candle_v2(asset,offset)
    # a=qx_api.get_candle_v2("NZDUSD_otc",180)

    # print(datetime.fromtimestamp(data['time']))

    o = []
    c = []
    h = []
    l = []

    time_temp = []

    for temp_data in data:
        time_temp.append(datetime.fromtimestamp(temp_data['time']).strftime('%Y-%m-%d %H:%M:%S+00:00'))
        o.append(temp_data['open'])
        c.append(temp_data['close'])
        h.append(temp_data['high'])
        l.append(temp_data['low'])

    data2 = {
        'time': time_temp,
        'o': o,
        'c': c,
        'h': h,
        'l': l,
    }

    return DataFrame(data2)


def open_trade_window_quotex() -> None:
    """
        open web driver
    """
    try:
        # option = Options()
        # option.add_argument("detach")
        # Use a specific version of a Chrome
        # driver = uc.Chrome(options=option)
        driver = uc.Chrome()

        login_quotex(driver)
    except Exception as e:
        print("error in quotex api : " + str(e))


def otc_check() -> bool:
    """
        Check the time, and if otc activate, it returns True otherwise returns False
    :return:
        True->if market is close
        False->if market is open
    """

    _time = datetime.utcnow()
    return True
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
