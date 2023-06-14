from time import sleep

import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from app.data_connector.model.enums import APIUsed
from app.oanda.api import get_real_time_data_oanda, get_history_oanda, get_last_candle_oanda, create_order_oanda, \
    trade_window_url_oanda
from core.config.Config import api_used
from selenium import webdriver


class DataConnector:
    driver: WebDriver
    api_enums: APIUsed

    def __init__(self):
        self.api_enums = APIUsed()

        if api_used == self.api_enums.oanda:
            self.get_real_time_data = get_real_time_data_oanda
            self.get_history = get_history_oanda
            self.get_last_candle = get_last_candle_oanda
            self.create_order = create_order_oanda
            self.trade_window_url = trade_window_url_oanda

    @staticmethod
    def get_history_from_file(name: str) -> pd.DataFrame:
        df = pd.read_csv(name)
        return df

    def open_trade_window(self):
        # option = Options()
        # option.add_argument("--kiosk")
        # option.add_argument("--start-fullscreen")
        # self.driver = webdriver.Chrome(options=option)
        self.driver = webdriver.Chrome()
        self.driver.get(self.trade_window_url)
        sleep(10)
        username_element = self.driver.find_element(By.ID, "username")
        password_element = self.driver.find_element(By.ID, "password")

        username_element.send_keys("sepahisiavash@gmail.com")
        password_element.send_keys("VamPire1468")
        sign_in_button = self.driver.find_element(By.XPATH, '/html/body/main/section/div/div/div/form/div[3]/button')
        sign_in_button.click()

