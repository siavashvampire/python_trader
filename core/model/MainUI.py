from datetime import datetime

from PyQt5 import uic
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtGui import QIcon, QFont, QIntValidator
from PyQt5.QtWidgets import QLabel, QPushButton, QDesktopWidget, QHBoxLayout, QVBoxLayout, QSpinBox, QComboBox, QWidget, \
    QFrame, QRadioButton

from MainCode import path
from app.data_connector.model.data_connector import DataConnector
from app.market_trading.api import get_all_trading, get_trading
from app.market_trading.main import MainTradingThreadModel
from app.market_trading.model.trading_model import TradingModel
from app.market_trading.model.trading_thread_model import TradingThreadModel


class MainUi(QFrame):
    main_trading_thread: MainTradingThreadModel
    trade_threads: list[TradingThreadModel]
    open_trade_window_pb: QPushButton
    start_trading_pb: QPushButton
    stop_trading_pb: QPushButton
    go_to_account_pb: QPushButton
    open_instructions_pb: QPushButton
    close_pb: QPushButton
    balance_label: QLabel
    balance_value_label: QLabel
    amount_label: QLabel
    time_label: QLabel
    trading_asset_label: QLabel
    trading_asset_value_label: QLabel
    trading_asset_prop_label: QLabel
    time_comboBox: QComboBox
    amount_spinBox: QSpinBox
    # aggressive_strategy_radioButton: QRadioButton
    optimal_strategy_radioButton: QRadioButton

    onlyInt: QIntValidator = QIntValidator(1, 100)
    tab_main: QWidget
    tab_trade_status: QWidget
    tab_setting: QWidget
    logo_label_setting: QLabel
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

        #   Start Colors
        from core.theme.color.color import PB_BG_color_deactivate, PB_Text_color_deactivate, PB_BG_color_active, \
            PB_Text_color_active, line_edit_BG, line_edit_Text_color, tab_selected_bg_color, tab_selected_text_color, \
            label_Text_color, PB_BG_color_active, label_Text_BG

        line_edit_style = "background-color: rgba(" + line_edit_BG + ");color: rgba(" + line_edit_Text_color + ");"
        line_edit_prop_style = "background-color: rgba(" + line_edit_BG + ");color: rgba(70, 240, 60, 255);"
        label_style = "background: " + label_Text_BG + ";color: rgba(" + label_Text_color + ");"
        balance_label_style = "background-color: rgba(" + label_Text_BG + ");color: rgba(240, 140, 50, 255);"

        # deactivate_pb_style = "background-color: rgba(" + PB_BG_color_deactivate + ");" + \
        #                       "color: rgba(" + PB_Text_color_deactivate + ");"
        #
        active_pb_style = "background-color: rgba(" + PB_BG_color_active + ");" + \
                          "color: rgba(" + PB_Text_color_active + ");border-radius: 7;"
        start_pb_style = "background-color: rgba(70, 240, 60, 255);" + \
                         "color: rgba(" + PB_Text_color_active + ");border-radius: 7;"
        stop_trading_pb_style = "background-color: rgba(136, 0, 27, 255);" + \
                                "color: rgba(" + PB_Text_color_active + ");border-radius: 7;"

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

        #   End Colors

        trades = get_all_trading()
        # trades = [get_trading(6)]

        self.add_trade_to_trade_threads(trades)
        # self.start_trade_threads()

        self.main_trading_thread = MainTradingThreadModel(self.trade_threads)

        self.logo_label_setting = self.findChild(QLabel, "logo_label_setting")
        self.main_logo_label = self.findChild(QLabel, "Main_Logo_label")

        self.logo_label_setting.setPixmap(Pics.Logo)
        self.main_logo_label.setPixmap(Pics.Logo)

        self.open_trade_window_pb = self.findChild(QPushButton, "open_trade_window_pb")
        data_connector = DataConnector()
        self.open_trade_window_pb.clicked.connect(lambda: data_connector.open_trade_window())

        self.open_trade_window_pb.setStyleSheet(active_pb_style)

        self.close_pb = self.findChild(QPushButton, "close_pb")
        self.close_pb.setStyleSheet(active_pb_style)

        self.go_to_account_pb = self.findChild(QPushButton, "go_to_account_pb")
        self.go_to_account_pb.setStyleSheet(active_pb_style)

        self.open_instructions_pb = self.findChild(QPushButton, "open_instructions_pb")
        self.open_instructions_pb.setStyleSheet(active_pb_style)

        self.start_trading_pb = self.findChild(QPushButton, "start_trading_pb")
        self.start_trading_pb.setStyleSheet(start_pb_style)
        self.start_trading_pb.clicked.connect(self.main_trading_start_thread)

        self.stop_trading_pb = self.findChild(QPushButton, "stop_trading_pb")
        self.stop_trading_pb.setStyleSheet(stop_trading_pb_style)
        self.stop_trading_pb.hide()
        self.stop_trading_pb.clicked.connect(self.main_trading_stop_thread)

        self.balance_label = self.findChild(QLabel, "balance_label")
        self.balance_label.setStyleSheet(label_style)

        self.balance_value_label = self.findChild(QLabel, "balance_value_label")
        self.balance_value_label.setStyleSheet(balance_label_style)

        self.amount_label = self.findChild(QLabel, "amount_label")
        self.amount_label.setStyleSheet(label_style)

        self.time_label = self.findChild(QLabel, "time_label")
        self.time_label.setStyleSheet(label_style)

        self.trading_asset_label = self.findChild(QLabel, "trading_asset_label")
        self.trading_asset_label.setStyleSheet(label_style)

        self.trading_asset_value_label = self.findChild(QLabel, "trading_asset_value_label")
        self.trading_asset_value_label.setStyleSheet(line_edit_style)

        self.trading_asset_prop_label = self.findChild(QLabel, "trading_asset_prop_label")
        self.trading_asset_prop_label.setStyleSheet(line_edit_prop_style)

        self.amount_spinBox = self.findChild(QSpinBox, "amount_spinBox")
        self.amount_spinBox.setStyleSheet(line_edit_style)

        self.time_comboBox = self.findChild(QComboBox, "time_comboBox")
        self.time_comboBox.setStyleSheet(line_edit_style)
        self.time_comboBox.setCurrentIndex(0)

        self.optimal_strategy_radioButton = self.findChild(QRadioButton, "optimal_strategy_radioButton")
        self.optimal_strategy_radioButton.setStyleSheet(line_edit_style)

        # self.aggressive_strategy_radioButton = self.findChild(QRadioButton, "aggressive_strategy_radioButton")
        # self.aggressive_strategy_radioButton.setStyleSheet(line_edit_style)

        self.main_trading_thread.max_trading_label = self.trading_asset_value_label
        self.main_trading_thread.max_trading_value_label = self.trading_asset_prop_label
        self.main_trading_thread.balance_value_label = self.balance_value_label
        self.balance_value_label.setText("$" + str(data_connector.get_balance()))
        # self.Setting.DebugPrintFlag = self.findChild(QCheckBox, "DebugPrintFlag")

        # self.Setting.TestSensor_lineEdit = self.findChild(QLineEdit, "TestSensor_lineEdit")
        #
        # self.Sensor_Status.Sensor_Submit_pb = self.Sensor_Status.findChild(QPushButton, "Sensor_Submit_pb")

    def add_trade_to_ui(self, name: str, value: str) -> dict[str, QLabel]:
        """
        add trade QH to vertical layout
        :param name: name
        :param value: value
        :return:
        """
        verticalLayout_trade = self.findChild(QVBoxLayout, "verticalLayout_trade")
        h1 = QHBoxLayout()

        from core.theme.color.color import label_Text_color, label_Text_BG

        label_style = "background: " + label_Text_BG + ";color: rgba(" + label_Text_color + ");"

        q_label_name = QLabel(name)
        q_label_value = QLabel(value)
        q_label_accuracy = QLabel("0")
        q_label_predict = QLabel("neutral")

        q_label_name.setAlignment(Qt.AlignCenter)
        q_label_value.setAlignment(Qt.AlignCenter)
        q_label_accuracy.setAlignment(Qt.AlignCenter)
        q_label_predict.setAlignment(Qt.AlignCenter)

        q_label_name.setFont(QFont('Times New Roman', 12))
        q_label_value.setFont(QFont('Times New Roman', 12))
        q_label_accuracy.setFont(QFont('Times New Roman', 12))
        q_label_predict.setFont(QFont('Times New Roman', 12))

        q_label_name.setStyleSheet(label_style)
        q_label_value.setStyleSheet(label_style)
        q_label_accuracy.setStyleSheet(label_style)
        q_label_predict.setStyleSheet(label_style)

        h1.addWidget(q_label_name)
        h1.addWidget(q_label_value)
        h1.addWidget(q_label_accuracy)
        h1.addWidget(q_label_predict)

        i = verticalLayout_trade.count()
        verticalLayout_trade.insertLayout(i - 2, h1)
        return {"q_label_name": q_label_name,
                "q_label_value": q_label_value,
                "q_label_accuracy": q_label_accuracy,
                "q_label_predict": q_label_predict}

    def main_trading_start_thread(self):
        """
            starting the main trade thread
        """
        self.amount_spinBox.setEnabled(0)
        self.time_comboBox.setEnabled(0)
        self.start_trading_pb.hide()
        self.main_trading_thread.set_time(int(self.time_comboBox.currentText()) * 60)
        self.main_trading_thread.set_amount(int(self.amount_spinBox.value()))
        self.main_trading_thread.start_thread()
        self.stop_trading_pb.show()

    def main_trading_stop_thread(self):
        """
            starting the main trade thread
        """
        self.stop_trading_pb.hide()
        self.main_trading_thread.stop_main_thread()
        self.start_trading_pb.show()
        self.amount_spinBox.setEnabled(1)
        self.time_comboBox.setEnabled(1)

    def add_trade_to_trade_threads(self, trades: list[TradingModel]):
        """
            add trade to self-trade threads
        :param trades: list[TradingModel]
        """
        self.trade_threads = []

        for trade in trades:
            q_labels = self.add_trade_to_ui(trade.currency_disp(), "0")
            self.trade_threads.append(TradingThreadModel(trade, q_labels["q_label_name"], q_labels["q_label_value"],
                                                         q_labels["q_label_accuracy"], q_labels["q_label_predict"]))

    def start_trade_threads(self):
        for trade in self.trade_threads:
            trade.start_thread()

    def stop_trade_threads(self):
        for trade in self.trade_threads:
            trade.stop_thread = True

        for trade in self.trade_threads:
            trade.thread.join()
