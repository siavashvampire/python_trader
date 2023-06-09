import os
from time import sleep
from datetime import datetime
from threading import Thread
from typing import Callable

from MainCode import path
from core.config.Config import db_path, logout_time
from core.database.database import create_db
from core.model.Login import LoginUI
from core.model.MainUI import MainUi
from core.model.SplashScreen import SplashScreen
from core.theme.color.color import DA_unit_ok_status_label_bot_bg, DA_unit_ok_status_label_bot_text, \
    DA_unit_bad_status_label_bot_bg, DA_unit_bad_status_label_bot_text, login_line_edit_bg, login_line_edit_text, \
    login_line_edit_border, start_splash_align, start_splash_color, close_splash_align, close_splash_color, \
    start_splash_font_size, end_splash_font_size
from core.theme.pic import Pics


class Main:
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
        self.PicsON = Pics.ON
        self.PicsOff = Pics.OFF
        self.MinusMark = Pics.MinusMark
        self.State_Render = False
        self.State_PLC = False
        self.stopCheckThread = False

        self.stopCheckRender = False
        self.stopCheckSender = False
        self.stopCheckPLC = False
        self.loginFlag = 0
        self.stop_Thread = False

        self.Thread = Thread(target=self.main_thread, args=(lambda: self.stop_Thread,))

        self.create_db_path()

        self.start_splash.show_message("\t\t initializing database connection")
        create_db()
        # TODO:nemidonam age kar nakone v db nabashe chi mishe

        self.start_splash.show_message("\t\t cheching internet connection")

        # TODO:bayad interneto check kone v check kone on dar gahi k mikhaim vasle ya na

        self.main_ui = MainUi()
        self.login_ui = LoginUI(self.main_ui)
        # ------------------------

        # self.main_ui.Backup_Submit_pb.clicked.connect(self.backup_thread.update_app)
        # self.main_ui.Sensor_Status.Sensor_Submit_pb.clicked.connect(self.line_monitoring.create_sensors)
        # self.main_ui.CheckDB_pb.clicked.connect(self.sender_thread.force_check_db)
        # self.main_ui.PLC_Status.PLC_Submit_pb.clicked.connect(self.da_units.submit_plc)
        # self.main_ui.LogoutPB.clicked.connect(self.logout)
        # self.login_ui.title_bar.close.clicked.connect(self.close)
        # TODO: should test for if call create or not and how parameter send

        # self.main_ui.Threads.ThS_Bale.clicked.connect(self.bale_org.state_thread)
        # self.main_ui.Threads.ThS_Sender.clicked.connect(self.sender_thread.state_thread)
        # self.main_ui.Threads.ThS_Render.clicked.connect(self.line_monitoring.state_thread)
        # self.main_ui.Threads.ThS_PLC.clicked.connect(self.da_units.state_thread)

        # self.run_thread()

        # self.sender_thread.run_thread()
        # self.backup_thread.run_thread()

        self.start_splash.finish(self.main_ui)
        self.login_ui.show()

    def main_thread(self, stop_thread: Callable[[], bool]) -> None:
        while True:
            sleep(5)
            try:
                self.check_threads()
                self.check_plc_status()
                if self.loginFlag:
                    login_diff = datetime.now() - self.main_ui.LoginNow
                    # TODO:check konim k login bayad koja etefagh biofte
                    if login_diff.seconds > logout_time:
                        self.logout()
                if stop_thread():
                    # Logging.bale_log("Main Send Thread", "Stop")
                    print("stop Bale Send")
                    break
            except Exception as e:
                # Logging.main_log("Main_Try", str(e))
                pass

    def run_thread(self):
        self.Thread.start()
        # Logging.sender_log("Run Thread", "Thread is run")

    def check_plc_status(self):
        if self.da_units.check_da_status():
            self.main_ui.Status_label_bot.setStyleSheet(
                "background-color: rgba(" + DA_unit_ok_status_label_bot_bg + ");" +
                "color: rgba(" + DA_unit_ok_status_label_bot_text + ");")
            self.main_ui.Status_label_bot.setText("PLCs connected")
        else:
            self.main_ui.Status_label_bot.setStyleSheet(
                "background-color: rgba(" + DA_unit_bad_status_label_bot_bg + ");" +
                "color: rgba(" + DA_unit_bad_status_label_bot_text + ");")
            self.main_ui.Status_label_bot.setText("PLCs Disconnected!")

    def check_threads(self):
        stylesheet = "background: transparent;"
        self.main_ui.Threads.ThS_Bale.setStyleSheet(stylesheet)
        self.main_ui.Threads.ThS_Render.setStyleSheet(stylesheet)
        self.main_ui.Threads.ThS_Sender.setStyleSheet(stylesheet)
        self.main_ui.Threads.ThS_PLC.setStyleSheet(stylesheet)
        if not self.stopCheckThread:
            self.bale_org.check()
            self.sender_thread.check()
            self.backup_thread.check()
            self.da_units.check()
            self.line_monitoring.check()
        #     TODO:hameye check haw bayad check beshan done done k ghat beshan vasl mishan ya na
        else:
            self.main_ui.Threads.ThS_Bale.setIcon(self.PicsOff)
            self.main_ui.Threads.ThS_Sender.setIcon(self.PicsOff)
            self.main_ui.Threads.ThS_PLC.setIcon(self.PicsOff)
            self.main_ui.Threads.ThS_Render.setIcon(self.PicsOff)
            self.bale_org.state = False
            self.sender_thread.state = False
            self.backup_thread.state = False
            self.da_units.state = False

    def stop_all_threads(self):
        self.stopCheckThread = True
        self.close_splash.show_message("closing Bale system")
        self.bale_org.state_thread(state=False, program=True)
        self.close_splash.add_saved_text("Bale system closed!")

        self.close_splash.show_message("closing shift system")
        self.shift.state_thread(state=False, program=True)
        self.close_splash.add_saved_text("shift system closed!")

        self.close_splash.show_message("closing DA units system")
        self.da_units.state_thread(state=False, program=True)
        self.close_splash.add_saved_text("DA units system closed!")

        self.close_splash.show_message("closing backup system")
        self.backup_thread.state_thread(state=False, program=True)
        self.close_splash.add_saved_text("backup system closed!")

        self.close_splash.show_message("closing line monitoring system")
        self.line_monitoring.state_thread(state=False, program=True)
        self.close_splash.add_saved_text("line monitoring system closed!")

        self.close_splash.show_message("disconnecting database")
        self.sender_thread.state_thread(state=False, program=True)
        self.close_splash.add_saved_text("database connection ended!")

        # TODO:bayad check konim k hatman doroste ya na

    def logout(self):
        self.loginFlag = 0
        self.main_ui.hide()
        self.login_ui.show()
        self.login_ui.User_Icon_Label.setPixmap(Pics.UserICO)
        self.login_ui.Pass_Icon_Label.setPixmap(Pics.passwordICO)

        self.login_ui.lineEdit_User.setStyleSheet(
            "QLineEdit{background-color: rgba(" + login_line_edit_bg + ");color:rgba(" + login_line_edit_text + ");" +
            "border-radius : 7;border : 1px solid rgba(" + login_line_edit_border + "); }" +
            "\nQLineEdit[text=\"\"]{ color:rgba(" + login_line_edit_text + "); }")
        self.login_ui.lineEdit_Pass.setStyleSheet(
            "QLineEdit{background-color: rgba(" + login_line_edit_bg + ");color:rgba(" + login_line_edit_text + ");" +
            "border-radius : 7;border : 1px solid rgba(" + login_line_edit_border + "); }" +
            "\nQLineEdit[text=\"\"]{ color:rgba(" + login_line_edit_text + "); }")
        self.login_ui.lineEdit_User.setTextMargins(10, 0, 10, 0)
        self.login_ui.lineEdit_Pass.setTextMargins(10, 0, 10, 0)

    def close(self):
        r = self.login_ui.checking_user_pass()
        if r == "Success":
            self.login_ui.close()
            self.close_splash.show()
            self.close_splash.show_message("start closing")
            self.stop_all_threads()
            self.close_splash.finish(self.main_ui)
            self.main_ui.close()
            os._exit(0)

    @staticmethod
    def create_db_path():
        from app.ResourcePath.app_provider.admin.main import resource_path as get_path

        os.makedirs(get_path(db_path), exist_ok=True)
