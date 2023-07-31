import json
import os
from datetime import datetime, timedelta
from time import sleep
from typing import Optional

import pandas as pd
from pandas import DataFrame
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import undetected_chromedriver as uc
from selenium.webdriver import DesiredCapabilities
import configparser

from app.data_connector.model.enums import APIUsed
from app.logging.api import add_log
from app.market_trading.api import get_trading_by_country_currency
from app.quotex.quotexapi.stable_api import Quotex
from app.telegram_bot.api import add_message
from core.config.Config import api_used, time_format, user_name_quotex, password_quotex

trade_window_url_quotex_main = 'https://quotex.com/en/sign-in/'
config_file_path_main = "File/Config/qoutex.cfg"
section_name_main = 'qoutex'


def check_connection_decoration(func):
    def inner1(*args, **kwargs):
        try:
            # TODO:nemidonam k in func bayad dakhele try bashe ya na
            qx_api_class.check_connection()
            return func(*args, **kwargs)
        except Exception as e:
            print("check connection decoration : ", e)
            pass

    return inner1


class QuotexAPI:
    trying_to_login_to_web_flag: bool = False
    qx_api: Quotex
    section_name: str = ""
    config_file_path: str = ""
    trade_window_url_quotex: str = ""

    def __init__(self):
        self.section_name = section_name_main
        self.config_file_path = config_file_path_main
        self.trade_window_url_quotex = trade_window_url_quotex_main
        self.prepare_api_quotex()
        self.check_connection()

        self.trying_to_login_to_web_flag: bool = False

    def read_config_from_file(self) -> [Optional[str], Optional[str], Optional[str], Optional[str]]:
        """
            read config file and extract ssid and host and user_agent and websocket_cookie
        :return:
            return str, str, str, str or None,None, None, None if something went wrong
        """

        config = configparser.RawConfigParser()
        config.read(self.config_file_path)
        try:
            ssid = config.get(self.section_name, 'ssid')
            host = config.get(self.section_name, 'host')
            user_agent = config.get(self.section_name, 'user_agent')
            websocket_cookie = config.get(self.section_name, 'websocket_cookie')
            return ssid, websocket_cookie, user_agent, host
        except Exception as e:
            # print(e)
            return None, None, None, None

    def write_config_to_file(self, ssid: str, websocket_cookie: str, user_agent: str, host: str) -> bool:
        """
            write to config file and fill ssid and host and user_agent and websocket_cookie
        :return:
            return True if write correctly and return False if something happens
        """
        try:
            if os.path.exists(self.config_file_path):
                os.remove(self.config_file_path)  # one file at a time

            cfg_file = open(self.config_file_path, 'w')
            config = configparser.RawConfigParser()
            config.add_section(self.section_name)

            config.set(self.section_name, 'ssid', ssid)
            config.set(self.section_name, 'websocket_cookie', websocket_cookie)
            config.set(self.section_name, 'user_agent', user_agent)
            config.set(self.section_name, 'host', host)

            config.write(cfg_file)
            cfg_file.close()
            return True
        except:
            return False

    @staticmethod
    def login_with_driver_quotex(driver: WebDriver) -> None:
        """
            login with a driver in a quotex
        :param driver: driver that open quotex site
        """
        driver.get("https://qxbroker.com/en/sign-in")
        wait = WebDriverWait(driver, 10)
        email_input = WebDriverWait(driver, 20).until(
            ec.presence_of_element_located((By.XPATH, "//*[@id='tab-1']/form/div[1]/input")))
        email_input.send_keys(user_name_quotex)
        pass_input = WebDriverWait(driver, 20).until(
            ec.presence_of_element_located((By.XPATH, "//*[@id='tab-1']/form/div[2]/input")))
        pass_input.send_keys(password_quotex)
        sign_button = WebDriverWait(driver, 20).until(
            ec.presence_of_element_located((By.XPATH, '//*[@id="tab-1"]/form/button')))
        sign_button.click()

    @staticmethod
    def extract_ssid_from_driver_quotex(driver: WebDriver) -> [Optional[str], Optional[str], Optional[str],
                                                               Optional[str]]:
        """
            extract ssid and host and user_agent and websocket_cookie from a driver
        :param driver:
        :return:
            ssid
            host
            user_agent
            websocket_cookie
        """
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

    def extract_ssid_from_web(self) -> [Optional[str], Optional[str], Optional[str], Optional[str]]:
        """
            we create a driver and open quotex website and extract ssid
        :return:
            its return 4 parameters ssid, websocket_cookie, user_agent, host
        """
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

        self.login_with_driver_quotex(driver)
        # driver.quit()
        return self.extract_ssid_from_driver_quotex(driver)

    def extract_ssid(self) -> [Optional[str], Optional[str], Optional[str], Optional[str]]:
        ssid, websocket_cookie, user_agent, host = self.read_config_from_file()

        if ssid is None and not self.trying_to_login_to_web_flag:  # happens if file not exists
            self.trying_to_login_to_web_flag = True
            ssid, websocket_cookie, user_agent, host = self.extract_ssid_from_web()
            self.write_config_to_file(ssid, websocket_cookie, user_agent, host)
            self.trying_to_login_to_web_flag = False

        return ssid, websocket_cookie, user_agent, host

    def prepare_api_quotex(self):
        """
            prepare api and login
        :return:
        """
        ssid, websocket_cookie, user_agent, host = self.extract_ssid()
        #
        # print(ssid)
        # print(host)
        # print(user_agent)
        # print(websocket_cookie)
        # ssid, websocket_cookie, user_agent, host = read_config_from_file()
        # ssid = """42["authorization",{"session":"Ev6gXi5BrbSZofsQIYmf4lv1VnWuuocWEWCeR0Gr","isDemo":0,"tournamentId":0}]"""
        # host = "qxbroker.com"  # qxbroker.com
        # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        # websocket_cookie = "referer=https%3A%2F%2Fwww.google.com%2F; _ga_L4T5GBPFHJ=GS1.1.1688309181.1.1.1688309186.0.0.0; _ga=GA1.1.192026297.1688309182; lang=en; nas=[%22EURUSD_otc%22]; z=[[%22graph%22%2C2%2C0%2C0%2C0.8333333]]; _vid_t=Ti4cw3aCg42SaP6EWmRSuci3XkX0feu50ka0dogV30MfAMubT2fUp6kTKpBe5PHcw5/xKb7Z9QczEQ==; __vid_l3=04131deb-ae03-4bd1-b975-13ebd852c998; __cf_bm=5ZDQ.k9B8nWZ.t1Ppzt6zdcNfr903LpRX.Qg7iTpdyY-1688309182-0-Aa3BGVqtzdfn5Js37EtZ0ooR3+WesIlWwQ8aXYte0cG/O40nSGybQwvwPZtxvvp9Tg2LtsSRmc5iY1DUIG7PSJ4+DS+JhVJD06t9UnmZdsTb"

        self.qx_api = Quotex(set_ssid=ssid, host=host, user_agent=user_agent, websocket_cookie=websocket_cookie)
        self.qx_api.connect()
        # check if connection to Quotex API was successful and change a balance type

        self.qx_api.change_balance("PRACTICE")

    def check_connection(self) -> bool:
        """
            check connection and if connections are lost extract from web and write to config file
        """
        try:
            check = self.qx_api.check_connect()
        except:
            check = False

        try:
            if not check and not self.trying_to_login_to_web_flag:  # happens if connections are lost
                self.trying_to_login_to_web_flag = True
                ssid, websocket_cookie, user_agent, host = self.extract_ssid_from_web()
                self.write_config_to_file(ssid, websocket_cookie, user_agent, host)
                self.prepare_api_quotex()
                self.trying_to_login_to_web_flag = False
        except:
            pass
        return check

    @check_connection_decoration
    def get_balance_quotex(self) -> int:
        """
            get balance of an account in quotex
        :return:
            return int that shows balance of an account in quotex
        """
        return self.qx_api.get_balance()

    @check_connection_decoration
    def check_win(self, id_in: int) -> Optional[dict]:
        """
            check_win of a trade in quotex
        :return:
            return profit
            zero for nothing
            positive for benefit
            negative for loss
        """
        return self.qx_api.check_win_once(id_in)

    # qx_api.check_win()

    @check_connection_decoration
    def create_order_quotex(self, name: str, unit: int, duration: int = 60) -> tuple[bool, dict]:
        """
    
        :param name: name = "EUR_USD" that should to convert to asset = "EURUSD"
        :param unit: unit = 10 or -10, "call" or "put"
        :param duration: durations in second
        :return: buy_info that have id of order
        {'id': 'bf09a6e0-e0b2-482d-85b6-9b9e9c2a6fdd', 'openTime': '2023-07-01 11:43:47', 'closeTime': '2023-07-01 11:45:00', 'openTimestamp': 1688211827, 'closeTimestamp': 1688211900, 'uid': 24692142, 'isDemo': 1, 'tournamentId': 0, 'amount': 1000, 'purchaseTime': 1688211870, 'profit': 870, 'percentProfit': 87, 'percentLoss': 100, 'openPrice': 1.08269, 'copyTicket': '', 'closePrice': 0, 'command': 0, 'asset': 'EURUSD_otc', 'nickname': '#24692142', 'accountBalance': 10000, 'requestId': '1', 'openMs': 388, 'currency': 'USD'}
    
        """
        # name = "EUR_USD"
        # asset = "EURUSD"

        asset = self.get_asset_from_name(name)

        amount = abs(unit)

        currencies = name.split("_")
        country_from = currencies[0]
        country_to = currencies[1]
        trade = get_trading_by_country_currency(country_from, country_to)

        if unit > 0:
            # print("we are buying "+ trade.currency_disp())
            add_log(1, trade.id, 4, "we are buying " + trade.currency_disp())

            add_message("we are buying " + trade.currency_disp())
            direction = "call"  # or "put"
        else:
            # print("we are selling "+ trade.currency_disp())
            add_log(1, trade.id, 2, "we are selling " + trade.currency_disp())

            add_message("we are selling " + trade.currency_disp())
            direction = "put"  # or "put"

        c, buy_info = self.qx_api.buy_exact(asset, amount, direction, duration)

        if 'error' in buy_info.keys():
            add_log(1, trade.id, 1, buy_info['error'] + ", in trade " + trade.currency_disp())

            return False, buy_info
        else:
            try:
                buy_info.pop('openTimestamp')
                buy_info.pop('closeTimestamp')
                buy_info.pop('uid')
                buy_info.pop('tournamentId')
                buy_info.pop('purchaseTime')
                buy_info.pop('copyTicket')
                buy_info.pop('command')
                buy_info.pop('closePrice')
                buy_info.pop('nickname')
                buy_info.pop('requestId')
                buy_info.pop('openMs')
                buy_info.pop('currency')
            except:
                pass
            add_log(1, trade.id, 6, str(buy_info))
            return True, buy_info

    def close_api_quotex(self) -> None:
        """
            closing qpi quotex
        """
        self.qx_api.close()

    def start_candles_stream_quotex(self, name):
        asset = self.get_asset_from_name(name)
        self.qx_api.start_candles_stream(asset, 2)

    def stop_candles_stream_quotex(self, name):
        asset = self.get_asset_from_name(name)
        self.qx_api.stop_candles_stream(asset)

    @check_connection_decoration
    def get_real_time_data_quotex(self, name: str) -> float:
        """
            get real time data
        :param name: asset  ex. "EUR_USD"
        :return:
            return real time value in float
        """
        asset = self.get_asset_from_name(name)

        self.start_candles_stream_quotex(name)
        temp = self.qx_api.get_realtime_candles(asset)[0]
        self.stop_candles_stream_quotex(name)

        # from datetime import datetime
        # timestamp = temp['time']
        # dt_object = datetime.fromtimestamp(timestamp)
        # print(dt_object)
        # TODO:inja time ham mide fekr konam inja bayad check konim k time age ba alan yeki nabod None pass bede

        return temp['price']

    @check_connection_decoration
    def get_last_candle_quotex(self, name: str, candle: str) -> DataFrame:
        """
        :param name: ex. "EUR_USD"
        :param candle: "S5" or "M1"
        :return:
            return DataFrame that has Five columns 'time','o',h','l','c'
        """
        try:
            asset = self.get_asset_from_name(name)

            _time = datetime.utcnow().timestamp()

            offset = 120  # how much sec want to get     _time-offset --->your candle <---_time

            if candle == "M1":
                period = 60  # candle size in sec
            else:
                period = 60  # candle size in sec

            data = self.qx_api.get_candle(asset, _time, offset, period)['data']
            if len(data) == 0:
                return DataFrame()
            data = data[-1]

            data2 = {
                'time': [datetime.fromtimestamp(data['time']).strftime(time_format)],
                'o': [data['open']],
                'c': [data['close']],
                'h': [data['high']],
                'l': [data['low']],
            }
            # df['time'] = pd.to_datetime(df['time'], format=time_format)
            return DataFrame(data2)
        except Exception as e:
            print("get last candle quotex : " + str(e))
            return DataFrame()

    @check_connection_decoration
    def get_history_quotex(self, name: str, start_time: str, end_time: str, candle: str,
                           csv_path: str = "", force_otc: Optional[bool] = None) -> DataFrame:
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

        asset = self.get_asset_from_name(name)

        if force_otc is not None:
            if force_otc:
                if "_otc" not in asset:
                    asset += "_otc"
            else:
                asset = asset.replace("_otc", "")

        start_time = datetime.strptime(start_time, time_format)
        end_time = datetime.strptime(end_time, time_format)
        start_time = start_time.replace(second=0, microsecond=0)
        end_time = end_time.replace(second=0, microsecond=0)
        end_time_temp = start_time

        if candle == "M1":
            period = 60  # candle size in sec
        else:
            period = 60  # candle size in sec

        freq = '1h'
        dr = pd.date_range(start_time, end_time, freq=freq)
        data_total = pd.DataFrame()

        for t in range(len(dr) - 1):
            end_time_temp = dr[t + 1].to_pydatetime()

            data_temp = self.get_history_detail_quotex(asset, end_time_temp)

            data_total = pd.concat([data_total, data_temp])
            end_time_temp += timedelta(minutes=1)

        start_final_temp = end_time_temp

        if start_final_temp >= end_time:
            offset = 0
        else:
            offset = (end_time - start_final_temp).seconds + 60

        if offset != 0:
            data_temp = self.get_history_detail_quotex(asset, end_time, offset=offset)
            data_total = pd.concat([data_total, data_temp])

        data_total = data_total.reset_index(drop=True)
        if csv_path != "":
            try:
                data = pd.read_csv(csv_path)
            except:
                data = pd.DataFrame()

            data_total = pd.concat([data, data_total])
            data_total.to_csv(csv_path, index=False, encoding='utf-8')

        return data_total

    @check_connection_decoration
    def check_asset(self, name: str) -> Optional[bool]:
        """
            check asset
        :param name: name of trade
        :return:
            None if both False,
            False if market is otc
            True if market is open
        """
        currencies = name.split("_")
        country_from = currencies[0]
        country_to = currencies[1]
        asset = country_from + country_to

        return self.qx_api.check_asset(asset=asset)

    @check_connection_decoration
    def change_account(self, balance_mode: int = 1):
        """
            change account
        :param balance_mode: mode of balance 0 for Real and 1 for Demo
        """

        if balance_mode == 0:
            self.qx_api.change_balance(Balance_MODE="REAL")
        elif balance_mode == 1:
            self.qx_api.change_balance(Balance_MODE="PRACTICE")
        else:
            self.qx_api.change_balance(Balance_MODE="PRACTICE")

    def open_trade_window_quotex(self) -> None:
        """
            open web driver
        """
        try:
            # option = Options()
            # option.add_argument("detach")
            # Use a specific version of a Chrome
            # driver = uc.Chrome(options=option)
            driver = uc.Chrome()

            self.login_with_driver_quotex(driver)
        except Exception as e:
            print("error in quotex api : " + str(e))

    # def otc_check(self, date_in: datetime = datetime.utcnow()) -> bool:
    #     """
    #         Check the time, and if otc activate, it returns True otherwise returns False
    #     :return:
    #         True->if market is close
    #         False->if market is open
    #     """

    # return (date_in.weekday() in [6, 7]) or date_in in holidays.XNYS()

    def otc_check(self, name: str) -> bool:
        """
            Check the time, and if otc activate, it returns True otherwise returns False
        :return:
            True->if market is close
            False->if market is open
        """
        currencies = name.split("_")
        country_from = currencies[0]
        country_to = currencies[1]
        asset = country_from + country_to

        check_asset = self.qx_api.check_asset(asset)

        if check_asset is None:
            return False
        else:
            return not check_asset

    def get_asset_from_name(self, name: str) -> str:
        currencies = name.split("_")
        country_from = currencies[0]
        country_to = currencies[1]
        asset = country_from + country_to

        if self.otc_check(name):
            asset += "_otc"

        return asset

    @check_connection_decoration
    def get_history_detail_quotex(self, asset: str, end_time: datetime, period: int = 60, offset: int = 61 * 60):
        _time = end_time.timestamp()

        data = self.qx_api.get_candle(asset, _time, offset, period)['data']

        if len(data) == 0:
            return DataFrame()

        o = []
        c = []
        h = []
        l = []

        time_temp = []

        for temp_data in data:
            # time_temp.append(datetime.fromtimestamp(temp_data['time']).strftime('%Y-%m-%d %H:%M:%S+00:00'))
            time_temp.append(datetime.fromtimestamp(temp_data['time']).strftime(time_format))
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


if api_used == APIUsed().quotex:
    qx_api_class = QuotexAPI()
