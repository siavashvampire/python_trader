"""
        the main class that have main ui and login ui
"""

import os
from time import sleep
from datetime import datetime
from threading import Thread
from typing import Callable
from MainCode import path
from core.config.Config import logout_time
from core.database.database import create_db
from core.model.Login import LoginUI
from core.model.MainUI import MainUi
from core.model.SplashScreen import SplashScreen
from core.theme.color.color import login_line_edit_bg, login_line_edit_text, close_splash_color, start_splash_align, \
    start_splash_color, close_splash_align, login_line_edit_border, start_splash_font_size, end_splash_font_size


class Main:
    """
        the main class that have main ui and login ui
    """
    close_splash: SplashScreen
    start_splash: SplashScreen

    def __init__(self):
        super().__init__()
        self.start_splash = SplashScreen(path + "core/theme/pic/pic/start_splash.png", 500)
        self.start_splash.alignment = start_splash_align
        self.start_splash.color = start_splash_color
        self.start_splash.save_text_show = False
        self.start_splash.set_font(start_splash_font_size)

        self.close_splash = SplashScreen(path + "core/theme/pic/pic/close_splash.jpg", 500)
        self.close_splash.alignment = close_splash_align
        self.close_splash.color = close_splash_color
        self.close_splash.set_font(end_splash_font_size)

        self.start_splash.show()

        self.loginFlag = 0
        self.stop_Thread = False

        self.thread = Thread(target=self.main_thread, args=(lambda: self.stop_Thread,))

        self.start_splash.show_message("\t\t initializing database connection")
        create_db()
        # TODO:nemidonam age kar nakone v db nabashe chi mishe

        self.start_splash.show_message("\t\t checking internet connection")

        # TODO:bayad interneto check kone v check kone on dar gahi k mikhaim vasle ya na

        self.main_ui = MainUi()
        self.login_ui = LoginUI(self.main_ui)

        for trade in self.main_ui.trade_threads:
            self.start_splash.show_message("\t\t getting data for trade " + trade.name)
            sleep(0.1)

        self.main_ui.start_trade_threads()
        self.main_ui.close_pb.clicked.connect(self.close)

        # self.login_ui.title_bar.close.clicked.connect(self.close)

        self.run_thread()

        self.start_splash.finish(self.main_ui)
        self.login_ui.show()

    def main_thread(self, stop_thread: Callable[[], bool]) -> None:
        """
            the main thread
        :param stop_thread: this parameter can stop thread if it sets True
        """
        while True:
            sleep(5)
            try:
                self.check_trade_threads()
                if self.loginFlag:
                    login_diff = datetime.now() - self.main_ui.LoginNow
                    # TODO:check konim k login bayad koja etefagh biofte
                    if login_diff.total_seconds() > logout_time:
                        pass
                        # self.logout()
                if stop_thread():
                    # Logging.bale_log("Main Send Thread", "Stop")
                    break
            except Exception as e:
                # Logging.main_log("Main_Try", str(e))
                pass

    def run_thread(self):
        """
            run the main thread
        """
        self.thread.start()
        # Logging.sender_log("Run Thread", "Thread is run")

    def check_trade_threads(self):
        """
            check trade thread is alive or not and if dead reset it
        """
        for trade in self.main_ui.trade_threads:
            trade.check()
            sleep(0.1)

    def stop_all_threads(self):
        """
            stop all threads
        """
        self.close_splash.show_message("closing trades system")
        self.main_ui.stop_trade_threads(self.close_splash)
        self.close_splash.add_saved_text("trades system closed!")

        self.close_splash.show_message("closing main system")
        self.main_ui.main_trading_stop_thread()
        self.close_splash.add_saved_text("main system closed!")

    def logout(self):
        """
            logout from mainui
        """
        self.loginFlag = 0
        self.main_ui.hide()
        self.login_ui.show()

        from core.theme.pic import Pics

        self.login_ui.User_Icon_Label.setPixmap(Pics.UserICO)
        self.login_ui.Pass_Icon_Label.setPixmap(Pics.passwordICO)

        self.login_ui.lineEdit_User.setStyleSheet(
            "QLineEdit{background-color: " + login_line_edit_bg + ";color: " + login_line_edit_text + ";" +
            "border-radius : 7;border : 1px solid " + login_line_edit_border + "; }" +
            "\nQLineEdit[text=\"\"]{ color:rgba(" + login_line_edit_text + "); }")
        self.login_ui.lineEdit_Pass.setStyleSheet(
            "QLineEdit{background-color: " + login_line_edit_bg + ";color: " + login_line_edit_text + ";" +
            "border-radius : 7;border : 1px solid " + login_line_edit_border + "; }" +
            "\nQLineEdit[text=\"\"]{ color:rgba(" + login_line_edit_text + "); }")
        self.login_ui.lineEdit_User.setTextMargins(10, 0, 10, 0)
        self.login_ui.lineEdit_Pass.setTextMargins(10, 0, 10, 0)

    def close(self):
        """
            close all units in program
        """
        self.login_ui.close()
        self.close_splash.show()
        self.close_splash.show_message("start closing")
        self.stop_all_threads()
        self.close_splash.finish(self.main_ui)
        self.main_ui.close()
        os._exit(0)
