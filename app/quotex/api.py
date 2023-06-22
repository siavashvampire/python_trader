import json
from time import sleep

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

from app.quotex.quotexapi.stable_api import Quotex

from datetime import datetime

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
    return qx_api.get_balance()


# qx_api.get_candle()
# qx_api.check_win()


def create_order_quotex(name: str, unit: int) -> None:
    # asset = "EURUSD"
    asset = name
    amount = abs(unit)

    if unit > 0:
        direction = "call"  # or "put"
    else:
        direction = "put"  # or "put"

    duration = 60
    c, buy_info = qx_api.buy(asset, amount, direction, duration)


def close_api_quotex() -> None:
    qx_api.close()


def get_real_time_data_quotex(name: str) -> float:
    qx_api.start_candles_stream(name, 2)
    temp = qx_api.get_realtime_candles(name)[0]
    qx_api.stop_candles_stream(name)

    # timestamp = temp['time']
    # dt_object = datetime.fromtimestamp(timestamp)
    # print(dt_object)
    return temp['price']

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
