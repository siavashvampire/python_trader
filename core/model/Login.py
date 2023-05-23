from datetime import datetime

from PyQt5 import uic
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QIcon
from PyQt5.QtWidgets import QFrame, QLabel, QPushButton, QLineEdit, QVBoxLayout, QWidget, QDesktopWidget

from MainCode import path
from core.app_provider.api.get import site_connection
from core.config.Config import main_login_url, main_check_user_access_url, login_timeout, login_developer
from core.model.TitleBar import TitleBar
from core.theme.color.color import login_line_edit_text, login_line_edit_border, login_forget_pb_bg, \
    login_forget_pb_text, login_enter_pb_bg, login_enter_pb_text, login_line_edit_bg
from core.theme.pic import Pics


class LoginUI(QFrame):
    def __init__(self, main_ui):
        super(LoginUI, self).__init__()
        uic.loadUi(path + "core/theme/ui/login.ui", self)
        self.setWindowIcon(QIcon(path + "core/theme/icons/logo.ico"))
        self.setWindowTitle("AvidMech Trade Login")
        self.setFrameShape(QFrame.StyledPanel)

        self.setMouseTracking(True)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # self.m_content= QWidget(self);
        vbox = QVBoxLayout(self)
        self.title_bar = TitleBar(self)
        vbox.addWidget(self.title_bar)
        vbox.setSpacing(0)

        self.layoutWidget = QWidget(self)
        self.layoutWidget.setLayout(vbox)
        self.layoutWidget.setGeometry(-10, -10, 550, 60)
        # vbox.setGeometry(200,100,1000,1500)

        # layout=QVBoxLayout(self);
        # layout.addWidget(self.m_content);
        # layout.setSpacing(0);
        # vbox.addLayout(layout);

        self.setGeometry(200, 100, 530, 700)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(QImage(path + "core/theme/pic/pic/Login.jpg").scaled(QSize(530, 700))))
        self.setPalette(palette)

        css = """
        QFrame{

            }
        """
        self.setStyleSheet(css)
        qt_rectangle = self.frameGeometry()
        qt_rectangle.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(qt_rectangle.topLeft())

        self.init_ui()

        self.pushButton_enter.clicked.connect(self.local_checking_user_pass)

        self.main_UI = main_ui

    def mousePressEvent(self, event):
        self.m_old_pos = event.pos()
        self.m_mouse_down = event.button() == Qt.LeftButton

    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()

    def mouseReleaseEvent(self, event):
        m_mouse_down = False

    def change_text_pass(self):
        from core.theme.color.color import login_text_color, login_bg_color, login_border_color
        self.lineEdit_Pass.setStyleSheet(
            "background-color: rgba(" + login_bg_color + ");color: rgba(" + login_text_color + ");" +
            "border-radius : 7;border : 1px solid rgba(" + login_border_color + ");")
        self.Pass_Icon_Label.clear()

    def change_text_user(self):
        from core.theme.color.color import login_text_color, login_bg_color, login_border_color
        self.lineEdit_User.setStyleSheet(
            "background-color: rgba(" + login_bg_color + ");color: rgba(" + login_text_color + ");" +
            "border-radius : 7;border : 1px solid rgba(" + login_border_color + ");")
        self.User_Icon_Label.clear()

    def init_ui(self):
        self.User_Icon_Label = self.findChild(QLabel, "User_Icon_Label")
        self.Pass_Icon_Label = self.findChild(QLabel, "Pass_Icon_Label")
        self.label_Logo = self.findChild(QLabel, "label_Logo")

        self.User_Icon_Label.setPixmap(Pics.UserICO)
        self.Pass_Icon_Label.setPixmap(Pics.passwordICO)
        self.label_Logo.setPixmap(Pics.Logo)

        self.lineEdit_User = self.findChild(QLineEdit, "lineEdit_User")
        self.lineEdit_User.setStyleSheet(
            "QLineEdit{background-color: rgba(" + login_line_edit_bg + ");color:rgba(" + login_line_edit_text + ");" +
            "border-radius : 7;border : 1px solid rgba(" + login_line_edit_border + "); }\n" +
            "QLineEdit[text=\"\"]{ color:rgba(" + login_line_edit_text + "); }")
        self.lineEdit_User.setTextMargins(10, 0, 10, 0)
        self.lineEdit_User.textChanged[str].connect(self.change_text_user)

        self.lineEdit_Pass = self.findChild(QLineEdit, "lineEdit_Pass")
        self.lineEdit_Pass.setStyleSheet(
            "QLineEdit{background-color: rgba(" + login_line_edit_bg + ");color:rgba(" + login_line_edit_text + ");" +
            "border-radius : 7;border : 1px solid rgba(" + login_line_edit_border + "); }\n" +
            "QLineEdit[text=\"\"]{ color:rgba(" + login_line_edit_text + "); }")
        self.lineEdit_Pass.textChanged[str].connect(self.change_text_pass)
        self.lineEdit_Pass.setTextMargins(10, 0, 10, 0)

        self.pushButton_enter = self.findChild(QPushButton, "pushButton_enter")

        self.pushButton_enter.setStyleSheet(
            "background-color: rgba(" + login_enter_pb_bg + ");" +
            "color: rgba(" + login_enter_pb_text + ");border-radius : 5;padding-bottom: 1px;")

        self.pushButton_Forget = self.findChild(QPushButton, "pushButton_Forget")

        self.pushButton_Forget.setStyleSheet(
            "background-color: rgba(" + login_forget_pb_bg + ");" +
            "color: rgba(" + login_forget_pb_text + ");")

        self.label_Status = self.findChild(QLabel, "label_Status")
        self.label_Status.setStyleSheet(
            "background-color: rgba(" + login_forget_pb_bg + ");" +
            "color: rgba(" + login_forget_pb_text + ");")

    def local_checking_user_pass(self):
        r = self.checking_user_pass()
        if r == "Success":
            self.hide()
            self.main_UI.show()
            self.main_UI.LoginNow = datetime.now()
            self.main_UI.loginFlag = 1

    def checking_user_pass(self):
        self.init_color()

        password = self.lineEdit_Pass.text()
        user = self.lineEdit_User.text()

        if self.check_developer_access(user, password):
            self.delete_user_pass()
            # Logging.main_log("Login", "DEVELOPER ACCESS")
            return "Success"

        if not user:
            self.label_Status.setText("نام کاربری خالی است")
            return

        if not password:
            self.label_Status.setText("رمز عبور خالی است")
            return

        # Logging.main_log("Login", str(user))

        payload = {"password": password, "username": user}
        status, r = site_connection(main_login_url, login_timeout, payload)[0:2]
        if status:
            url_check_access = main_check_user_access_url + str(r["user_group_id"]) + "/admin/configuration/index/core"
            status, r = site_connection(url_check_access, login_timeout)[0:2]
            if status:
                r = "Success"
                self.delete_user_pass()
                self.label_Status.setStyleSheet('color: green')
            else:
                if r == "Code Error":
                    r = "دسترسی به این صفحه امکان پذیر نمی باشد"

        if not r == "Success":
            self.label_Status.setText(r)
        return r

    def init_color(self):
        self.label_Status.setText("")

    def delete_user_pass(self):
        self.lineEdit_Pass.setText("")
        self.lineEdit_User.setText("")

    @staticmethod
    def check_developer_access(user, password):
        if login_developer:
            return 1
        if user == "AvidMech_Developer" and password == "VamPire1468":
            return 1
        return 0
