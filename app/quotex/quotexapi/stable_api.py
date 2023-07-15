# python
from app.quotex.quotexapi.api import quotexapi
import time
import logging
import app.quotex.quotexapi.global_value as global_value
from app.quotex.quotexapi.expiration import get_expiration_time_quotex
from collections import defaultdict
import json
import threading


def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n - 1, type))


def ping_server(self):
    t = threading.currentThread()
    pingInterval = 0
    while getattr(t, "do_run", True):
        if global_value.check_websocket_if_connect[self.api.object_id] == 0:
            break
        time.sleep(1)
        self.ping_server_go()
        pingInterval = pingInterval + 1
        if pingInterval == 25:
            self.ping_to_server_go_2()
            pingInterval = 0


class Quotex:
    __version__ = "2.2"

    def __init__(self, email=None, password=None, set_ssid=None, host=None, user_agent=None, websocket_cookie=None,
                 proxies=None, auto_logout=True):
        global_value.quotex_netloc = host
        self.websocket_cookie = websocket_cookie

        self.SESSION_HEADER = {
            "Origin": "https://" + global_value.quotex_netloc,
            "User-Agent": user_agent,

            "Connection": "Upgrade",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",

            "Upgrade": "websocket",

            "Sec-WebSocket-Version": "13",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",

            "Sec-WebSocket-Extensions": "permessage-deflate"}

        self.SESSION_COOKIE = {}
        self.proxies = proxies
        self.set_ssid = set_ssid
        self.auto_logout = auto_logout
        self._2FA_TOKEN = None
        self.email = email
        self.password = password
        self.account_mode_isDemo = 1
        self.client_callback = None

    # --------------------------------------------------------------------------
    def logout(self):
        self.api.logout()

    def ping_server_go(self):
        self.api.ping_to_server()
        self.api_real.ping_to_server()

    def ping_to_server_go_2(self):
        self.api.ping_to_server_2()
        self.api_real.ping_to_server_2()

    def set_call_back_for_client(self, function):

        self.client_callback = function

    def set_session(self, header, cookie):
        self.SESSION_HEADER = header
        self.SESSION_COOKIE = cookie

    def get_ssid(self):
        return global_value.SSID[self.api.object_id]

    def settings(self, bol):

        self.api.settings(bol)
        self.api_real.settings(bol)

    def setting_2FA_TOKEN(self, code):
        self._2FA_TOKEN = code

    def TWO_FA(self, token, method=None, code=None):
        r = self.api.TWO_FA(token, method, code)
        return json.loads(r.text)

    def close(self):
        self._thread_ping_server.do_run = False

    def connect(self):

        try:
            self.api.close()
        except:
            pass
            # logging.error('**warning** self.api.close() fail')

        # id-iqoption.com some country only can using this url
        # Iqoption.com
        try:
            self.set_ssid = global_value.SSID[self.api.object_id]
        except:
            pass
        # old url wss://ws.qxbroker.com/socket.io/?EIO=3&transport=websocket
        url = "wss://ws2." + global_value.quotex_netloc + "/socket.io/?EIO=3&transport=websocket"
        self.api = quotexapi(url, websocket_cookie=self.websocket_cookie, email=self.email, password=self.password,
                             header=self.SESSION_HEADER, proxies=self.proxies, set_ssid=self.set_ssid,
                             auto_logout=self.auto_logout, _2FA_TOKEN=self._2FA_TOKEN)
        c, m = self.api.connect(1)

        self.api_real = quotexapi(url, websocket_cookie=self.websocket_cookie, email=self.email, password=self.password,
                                  header=self.SESSION_HEADER, proxies=self.proxies, set_ssid=self.set_ssid,
                                  auto_logout=self.auto_logout, _2FA_TOKEN=self._2FA_TOKEN)
        if self.client_callback != None:
            self.api.client_callback = self.client_callback
            self.api_real.client_callback = self.client_callback

        c_real, m_real = self.api_real.connect(0)

        if c and c_real:
            # self.change_balance("PRACTICE")
            self._thread_ping_server = threading.Thread(target=ping_server, args=(self,))
            self._thread_ping_server.start()
            self.api.subscribe_signal()

        return c and c_real, str(m) + str(m_real)

    def check_connect(self):
        # True/False

        if global_value.check_websocket_if_connect[self.api.object_id] == 0:
            return False
        else:
            return True
        # wait for timestamp getting

    # _________________________UPDATE ACTIVES OPCODE_____________________

    def _init_get_raw_balance(self):
        # [{"d":[{"value":3686.24}],"e":52},{"d":[{"value":20.10,"account_id":1250470807}],"e":50}]

        req_id = "balance"
        self.api.raw_e98[req_id] = None
        self.api.Get_Balance(req_id)

        while self.api.raw_e98[req_id] == None:
            pass
        _tmp = self.api.raw_e98[req_id]
        del self.api.raw_e98[req_id]
        for d in _tmp:
            try:
                if "account_id" in d["d"][0]:
                    global_value.balance[self.api.object_id]["REAL"]["value"] = d["d"][0]["value"]
                    global_value.balance[self.api.object_id]["REAL"]["account_id"] = d["d"][0]["account_id"]
                elif "value" in d["d"][0]:
                    global_value.balance[self.api.object_id]["PRACTICE"]["value"] = d["d"][0]["value"]
                    global_value.balance[self.api.object_id]["PRACTICE"]["account_id"] = 0
            except:
                pass

    def get_balance(self):
        if self.account_mode_isDemo == 0:
            while global_value.real_balance[self.api.object_id] == None:
                pass
            return global_value.real_balance[self.api.object_id]
        elif self.account_mode_isDemo == 1:
            while global_value.practice_balance[self.api.object_id] == None:
                pass
            return global_value.practice_balance[self.api.object_id]

    def get_asset_data(self):
        req_id = global_value.get_req_id(self.api.object_id)

        self.api.raw_e98["e_70"] = None
        self.api.Get_Asset_Data(req_id)
        while self.api.raw_e98["e_70"] == None:
            pass
        _tmp = self.api.raw_e98["e_70"]
        del self.api.raw_e98["e_70"]
        return _tmp

    def change_balance(self, Balance_MODE):
        if Balance_MODE == "REAL":

            # self.api.Auth_Mode(Balance_MODE)

            self.account_mode_isDemo = 0
        elif Balance_MODE == "PRACTICE":

            # self.api.Auth_Mode(Balance_MODE)

            self.account_mode_isDemo = 1
        else:
            logging.error('**warning** change_balance() need input "REAL"/"PRACTICE" ')

    # ________________________________________________________________________
    # _______________________        CANDLE      _____________________________
    # ________________________self.api.getcandles() wss________________________

    #######################################################
    # ______________________________________________________
    # _____________________REAL TIME CANDLE_________________
    # ______________________________________________________
    #######################################################

    def get_payment(self):
        raw_asset = self.get_raw_asset()
        ans = nested_dict(3, dict)

        # payment is for 5 or more minutes
        # turbo_payment is for 5 or less minutes

        for i in raw_asset:
            asset_name = i[1]
            ans[asset_name]["turbo_payment"] = i[18]
            ans[asset_name]["payment"] = i[19]
            ans[asset_name]["open"] = i[14]

        return ans

    def get_accept_buy_time(self):
        a = self.get_raw_asset()
        ans = {}
        for u in a:
            asset_name = u[1]
            open_time = u[15]
            time_set = set()
            for t in open_time:
                time_set.add(t["time"])
            ans[asset_name] = time_set
        return ans

    def get_raw_asset(self):
        while self.api.updateAssets_data == None:
            pass
        return self.api.updateAssets_data

    def get_all_asset_name(self):
        all_asset = self.get_raw_asset()
        ans = []
        for i in all_asset:
            ans.append(i[1])
        return ans

    def check_asset_open(self, asset):
        all_asset = self.get_raw_asset()
        for i in all_asset:
            # TODO:fekr mikonam age inja jaye 14 biaim ro hamash y for bezanim v motmaen beshim 14 omi bool hast v baad bedim behtar bashe
            if i[1] == asset:
                return i[14]
                # if True in i:
                #     return True
                # else:
                #     return False

    def check_asset(self, asset):
        all_asset = self.get_raw_asset()
        asset_data, asset_data_otc = self.get_both_asset_from_raw(all_asset, asset)

        if asset_data is None and asset_data_otc is None:
            return None

        if asset_data is not None and asset_data_otc is None:
            if asset_data[14]:
                return True
            return None

        if asset_data is None and asset_data_otc is not None:
            if asset_data_otc[14]:
                return False
            return None

        if asset_data is not None and asset_data_otc is not None:
            if asset_data[14]:
                return True
            if asset_data_otc[14]:
                return False

            return None




    def get_both_asset_from_raw(self, all_asset, asset):
        asset_data = None
        asset_data_otc = None

        for i in all_asset:
            if i[1] == asset:
                asset_data = i
            if i[1] == asset + "_otc":
                asset_data_otc = i

        return asset_data,asset_data_otc

    def start_candles_stream(self, asset, size):
        # the list of the size
        self.api.subscribe_realtime_candle(asset, size)

    def stop_candles_stream(self, asset):
        self.api.unsubscribe_realtime_candle(asset)

    def get_realtime_candles(self, asset):
        while True:
            if asset in self.api.realtime_price:
                if len(self.api.realtime_price[asset]) > 0:
                    return self.api.realtime_price[asset]

    def get_signal_data(self):
        return self.api.signal_data

    def buy_raw(self, asset, amount, dir, exp_time, option_type):
        if self.account_mode_isDemo == 1:
            c_func = self.api
        elif self.account_mode_isDemo == 0:
            c_func = self.api_real

        req_id = global_value.get_req_id(c_func.object_id)
        c_func.request_data[req_id] = None
        c_func.buy(asset, amount, dir, exp_time, req_id, option_type)
        while c_func.request_data[req_id] == None:
            time.sleep(0.1)
            pass
        _tmp = c_func.request_data[req_id]

        del c_func.request_data[req_id]
        try:
            self.api.buy_info[_tmp["id"]] = _tmp
            self.api_real.buy_info[_tmp["id"]] = _tmp
        except:
            pass
        return True, _tmp

    def buy(self, asset, amount, dir, duration):
        # the min duration is 30

        duration = get_expiration_time_quotex(time.time(), duration)

        if self.account_mode_isDemo == 1:
            c_func = self.api
        elif self.account_mode_isDemo == 0:
            c_func = self.api_real

        req_id = global_value.get_req_id(c_func.object_id)
        c_func.request_data[req_id] = None
        c_func.buy(asset, amount, dir, duration, req_id)
        while c_func.request_data[req_id] == None:
            time.sleep(0.1)
            pass
        _tmp = c_func.request_data[req_id]

        del c_func.request_data[req_id]
        try:
            self.api.buy_info[_tmp["id"]] = _tmp
            self.api_real.buy_info[_tmp["id"]] = _tmp
        except:
            pass
        return True, _tmp

    def buy_exact(self, asset, amount, dir, duration):
        if self.account_mode_isDemo == 1:
            c_func = self.api
        elif self.account_mode_isDemo == 0:
            c_func = self.api_real

        req_id = global_value.get_req_id(c_func.object_id)
        c_func.request_data[req_id] = None
        c_func.buy_exact(asset, amount, dir, duration, req_id)
        while c_func.request_data[req_id] == None:
            time.sleep(0.1)
            pass
        _tmp = c_func.request_data[req_id]

        del c_func.request_data[req_id]
        try:
            self.api.buy_info[_tmp["id"]] = _tmp
            self.api_real.buy_info[_tmp["id"]] = _tmp
        except:
            pass
        return True, _tmp

    def sell_option(self, id):
        # the min duration is 30
        self.api.sell_option(id)

    def get_candle(self, asset, time, offset, period):
        req_id = global_value.get_req_id(self.api.object_id)
        self.api.getcandle_data[req_id] = None
        self.api.getcandles(asset, time, offset, period, req_id)
        while self.api.getcandle_data[req_id] == None:
            pass
        return self.api.getcandle_data[req_id]

    def get_candle_v2(self, asset, period):
        self.api.candle_v2_data[asset] = None
        size = 10
        self.stop_candles_stream(asset)

        self.api.subscribe_realtime_candle(asset, size, period)
        while self.api.candle_v2_data[asset] == None:
            pass

            time.sleep(1)

        return self.api.candle_v2_data[asset]

    def check_win_raw(self, ticket, c_function):
        if ticket in c_function.check_win_refund_data:
            return c_function.check_win_refund_data[ticket]["amount"] - c_function.buy_info[ticket]["amount"]
        elif ticket in c_function.check_win_close_data:
            return c_function.check_win_close_data[ticket]["profit"]
        return None

    def check_win(self, ticket, polling=1):
        while True:
            time.sleep(polling)
            if self.check_win_raw(ticket, self.api) is not None:
                return self.check_win_raw(ticket, self.api)

            if self.check_win_raw(ticket, self.api_real) is not None:
                return self.check_win_raw(ticket, self.api_real)

    def get_server_time(self):
        req_id = global_value.get_req_id(self.api.object_id)
        self.api.server_timestamp[req_id] = None
        self.api.get_server_time(req_id)
        while self.api.server_timestamp[req_id] == None:
            pass
        _tmp = self.api.server_timestamp[req_id]
        del self.api.server_timestamp[req_id]
        return _tmp

    def check_user_data(self):
        import json
        import requests
        laravel_session = self.api.response_cookies["laravel_session"]
        cookies_dict = {"laravel_session": laravel_session}
        ans = None
        headers = {
            'sec-ch-ua': "\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"92\"",
            'sec-ch-ua-mobile': "?0",
            'upgrade-insecure-requests': "1",
            'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            'cache-control': "no-cache",
        }
        response = requests.get("https://" + global_value.quotex_netloc + "/en/settings", cookies=cookies_dict,
                                headers=headers)
        raw_user_data = response.text
        start_str = "window.settings = "
        start_index = raw_user_data.find(start_str) + len(start_str)
        end_indx = raw_user_data.find(";", start_index)

        user_data = raw_user_data[start_index:end_indx]

        try:
            json_user_data = json.loads(user_data)
            ans = json_user_data
        except:
            ans = None

        return ans
