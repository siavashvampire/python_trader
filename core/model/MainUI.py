from datetime import datetime
from time import sleep
from typing import Optional, Any, List

from PyQt5 import uic
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QLabel, QPushButton, QDesktopWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFrame

from MainCode import path
from app.data_connector.model.data_connector import DataConnector
from app.market_trading.api import get_all_trading
from app.market_trading.model.trading_thread_model import TradingThreadModel
from core.theme.color.color import label_Text_color, PB_BG_color_active


class MainUi(QFrame):
    trade_threads: list[TradingThreadModel]
    open_trade_window_pb: QPushButton
    # init backup
    # Backup_Name: list[QLineEdit]
    # Backup_Path: list[QLineEdit]
    # Backup_FileName: list[QLineEdit]
    # Backup_Time: list[QLineEdit]
    # Choose_Path_pb: list[QPushButton]
    # Backup_pb: list[QPushButton]
    # TODO:bayad ina doros beshe
    onlyInt: QIntValidator = QIntValidator(1, 100)
    tab_main: QWidget
    tab_trade_status: QWidget
    tab_setting: QWidget
    logo_label_setting: QLabel
    logo_label_trade_status: QLabel
    main_logo_label: QLabel

    def __init__(self):
        super(MainUi, self).__init__()
        uic.loadUi(path + "core/theme/ui/main.ui", self)

        self.setWindowTitle("Trading System")
        self.setWindowIcon(QIcon(path + "core/theme/icons/logo.ico"))
        self.setFrameShape(QFrame.StyledPanel)

        self.LoginNow = datetime.now()

        self.setMouseTracking(True)

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.init_ui()

    def setMouseTracking(self, flag):
        def recursive_set(parent):
            for child in parent.findChildren(QObject):
                try:
                    child.setMouseTracking(flag)
                except:
                    pass
                recursive_set(child)

        QWidget.setMouseTracking(self, flag)
        recursive_set(self)

    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()
        self.LoginNow = datetime.now()

    def init_ui(self):
        from core.theme.pic import Pics

        self.tab_main = self.findChild(QWidget, "Main")
        self.tab_trade_status = self.findChild(QWidget, "trade_status")
        self.tab_setting = self.findChild(QWidget, "Setting")

        #   Start     Colors
        from core.theme.color.color import PB_BG_color_deactivate, PB_Text_color_deactivate, PB_BG_color_active, \
            PB_Text_color_active, line_edit_BG, line_edit_Text_color, tab_selected_bg_color, tab_selected_text_color

        line_edit_style = "background: " + line_edit_BG + ";color: " + line_edit_Text_color + ";"

        deactivate_pb_style = "background-color: rgba(" + PB_BG_color_deactivate + ");" + \
                              "color: rgba(" + PB_Text_color_deactivate + ");"

        active_pb_style = "background-color: rgba(" + PB_BG_color_active + ");" + \
                          "color: rgba(" + PB_Text_color_active + ");"

        # color = QColor(245, 245, 250)
        # alpha = 255
        # values = "{r}, {g}, {b}, {a}".format(r=color.red(),
        #                                      g=color.green(),
        #                                      b=color.blue(),
        #                                      a=alpha
        #                                      )
        # self.tabWidget.setStyleSheet("background-color: rgba("+values+");color: black;")

        # stylesheet = "QTabBar::tab:selected {background-color: rgba(" + tab_selected_bg_color + ");" + \
        #              "color: rgba(" + tab_selected_text_color + ");font-size: 8pt;}" + \
        #              "QTabWidget>QWidget>QWidget{background-image: url(" + path + \
        #              "core/theme/pic/pic/Main.jpg);background-repeat: no-repeat;background-position:center;}" + \
        #              "MainUi { background-image: url(" + path + "core/theme/pic/pic/Main.jpg);" + \
        #              "background-repeat: no-repeat;background-position:center;} "
        stylesheet = "QTabBar::tab:selected {background-color: rgba(" + tab_selected_bg_color + ");" + \
                     "color: rgba(" + tab_selected_text_color + ");font-size: 8pt;}" + \
                     "QTabWidget>QWidget>QWidget{border-image: url(" + path + \
                     "core/theme/pic/pic/Main.jpg);background-repeat: no-repeat;background-position:center;}" + \
                     "MainUi { border-image: url(" + path + "core/theme/pic/pic/Main.jpg);" + \
                     "background-repeat: no-repeat;background-position:center;} "
        self.setStyleSheet(stylesheet)

        qt_rectangle = self.frameGeometry()
        qt_rectangle.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(qt_rectangle.topLeft())

        #   End     Colors

        trades = get_all_trading()

        align = 0

        self.trade_threads = []

        for trade in trades:
            if align == 0:
                alignment = "left"
                align = 1
            else:
                alignment = "right"
                align = 0

            q_labels = self.add_trade(alignment, "test", "0")
            self.trade_threads.append(TradingThreadModel(trade, q_labels[0], q_labels[1]))


        self.logo_label_setting = self.findChild(QLabel, "logo_label_setting")
        self.logo_label_trade_status = self.findChild(QLabel, "logo_label_trade_status")
        self.main_logo_label = self.findChild(QLabel, "Main_Logo_label")

        self.logo_label_setting.setPixmap(Pics.Logo)
        self.logo_label_trade_status.setPixmap(Pics.Logo)
        self.main_logo_label.setPixmap(Pics.Logo)

        self.open_trade_window_pb = self.findChild(QPushButton, "open_trade_window_pb")
        data_connector = DataConnector()
        self.open_trade_window_pb.clicked.connect(lambda :data_connector.open_trade_window())
        # self.Setting.DebugPrintFlag = self.findChild(QCheckBox, "DebugPrintFlag")

        # self.Setting.TestSensor_lineEdit = self.findChild(QLineEdit, "TestSensor_lineEdit")
        #
        # self.Sensor_Status.Sensor_Submit_pb = self.Sensor_Status.findChild(QPushButton, "Sensor_Submit_pb")

    def add_trade(self, orientation: str, name: str, value: str) -> list[QLabel]:
        verticalLayout_trade_left = self.findChild(QVBoxLayout, "verticalLayout_trade_" + orientation)
        h1 = QHBoxLayout()

        label_style = "background-color: rgba(" + PB_BG_color_active + ");" + \
                      "color: rgba(" + label_Text_color + ");"

        q_label_name = QLabel(name)
        q_label_value = QLabel(value)

        q_label_name.setAlignment(Qt.AlignCenter)
        q_label_value.setAlignment(Qt.AlignCenter)

        q_label_name.setFont(QFont('Times New Roman', 12))
        q_label_value.setFont(QFont('Times New Roman', 12))

        q_label_name.setStyleSheet(label_style)
        q_label_value.setStyleSheet(label_style)

        h1.addWidget(q_label_name)
        h1.addWidget(q_label_value)

        i = verticalLayout_trade_left.count()
        verticalLayout_trade_left.insertLayout(i - 2, h1)
        return [q_label_name, q_label_value]
