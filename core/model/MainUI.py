from datetime import datetime

from PyQt5 import uic
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QCheckBox, QLabel, QTextEdit, QPushButton, QLineEdit, QProgressBar, QTabWidget, \
    QDesktopWidget
from PyQt5.QtWidgets import QFileDialog, QWidget
from PyQt5.QtWidgets import QFrame

from MainCode import path


class MainUi(QFrame):
    # init backup
    Backup_Name: list[QLineEdit]
    Backup_Path: list[QLineEdit]
    Backup_FileName: list[QLineEdit]
    Backup_Time: list[QLineEdit]
    Choose_Path_pb: list[QPushButton]
    Backup_pb: list[QPushButton]

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
        self.Setting.onlyInt = QIntValidator(1, 100)
        self.MainTab = self.findChild(QWidget, "Main")
        self.ExelTab = self.findChild(QWidget, "Exel")
        self.Sensor_StatusTab = self.findChild(QWidget, "Sensor_Status")
        self.PLC_StatusTab = self.findChild(QWidget, "PLC_Status")
        self.BackupTab = self.findChild(QWidget, "Backup")
        self.SettingTab = self.findChild(QWidget, "Setting")

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

        stylesheet = "QTabBar::tab:selected {background-color: rgba(" + tab_selected_bg_color + ");" + \
                     "color: rgba(" + tab_selected_text_color + ");font-size: 8pt;}" + \
                     "QTabWidget>QWidget>QWidget{background-image: url(" + path + "core/theme/pic/pic/Main.jpg);}" + \
                     "MainUi { background-image: url(" + path + "core/theme/pic/pic/Main.jpg);" + \
                     "background-repeat: no-repeat;background-position:center;} "
        self.setStyleSheet(stylesheet)

        qt_rectangle = self.frameGeometry()
        qt_rectangle.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(qt_rectangle.topLeft())

        #   End     Colors

        #   Start     Threads Tab
        self.Threads.ThS_Bale = self.findChild(QPushButton, "Start_Thread_PB_Bale")
        self.Threads.ThS_Render = self.findChild(QPushButton, "Start_Thread_PB_Render")
        self.Threads.ThS_Sender = self.findChild(QPushButton, "Start_Thread_PB_Sender")
        self.Threads.ThS_PLC = self.findChild(QPushButton, "Start_Thread_PB_PLC")

        self.LogoutPB = self.findChild(QPushButton, "Logout_pb")
        self.CheckDB_pb = self.findChild(QPushButton, "CheckDB_pb")
        self.lbl_CheckDB = self.findChild(QLabel, "lbl_CheckDB")

        stylesheet = "background: transparent;"

        self.LogoutPB.setStyleSheet(stylesheet + "color: rgba(" + PB_Text_color_deactivate + ");")
        self.CheckDB_pb.setStyleSheet(active_pb_style)

        self.Threads.ThS_Bale.setStyleSheet(stylesheet)
        self.Threads.ThS_Bale.setIconSize(QSize(120, 40))
        self.Threads.ThS_Render.setStyleSheet(stylesheet)
        self.Threads.ThS_Render.setIconSize(QSize(120, 40))
        self.Threads.ThS_Sender.setStyleSheet(stylesheet)
        self.Threads.ThS_Sender.setIconSize(QSize(120, 40))
        self.Threads.ThS_PLC.setStyleSheet(stylesheet)
        self.Threads.ThS_PLC.setIconSize(QSize(120, 40))
        #   End     Threads Tab

        #   Start     logging Tab
        self.Log_Open_PB = self.findChild(QPushButton, "Log_Open_PB")
        self.Sensor_Open_PB = self.findChild(QPushButton, "Sensor_Open_PB")
        self.PLC_Open_PB = self.findChild(QPushButton, "PLC_Open_PB")
        self.Backup_Open_PB = self.findChild(QPushButton, "Backup_Open_PB")
        self.Phone_Open_PB = self.findChild(QPushButton, "Phone_Open_PB")

        self.Main_Clear_PB = self.findChild(QPushButton, "Main_Clear_PB")
        self.Render_Clear_PB = self.findChild(QPushButton, "Render_Clear_PB")
        self.PLC_Clear_PB = self.findChild(QPushButton, "PLC_Clear_PB")
        self.Sender_Clear_PB = self.findChild(QPushButton, "Sender_Clear_PB")
        self.Bale_Clear_PB = self.findChild(QPushButton, "Bale_Clear_PB")

        self.Log_Open_PB.setStyleSheet(active_pb_style)
        self.Sensor_Open_PB.setStyleSheet(active_pb_style)
        self.PLC_Open_PB.setStyleSheet(active_pb_style)
        self.Backup_Open_PB.setStyleSheet(active_pb_style)
        self.Phone_Open_PB.setStyleSheet(active_pb_style)

        self.Main_Clear_PB.setStyleSheet(active_pb_style)
        self.Render_Clear_PB.setStyleSheet(active_pb_style)
        self.PLC_Clear_PB.setStyleSheet(active_pb_style)
        self.Sender_Clear_PB.setStyleSheet(active_pb_style)
        self.Bale_Clear_PB.setStyleSheet(active_pb_style)


        # self.Log_Open_PB    .clicked.connect(lambda: JV(LoggingDBPath, "logging"))
        # self.Sensor_Open_PB .clicked.connect(lambda: JV(SensorDBPath, "Sensor"))
        # self.PLC_Open_PB    .clicked.connect(lambda: JV(PLCDBPath, "PLC"))
        # self.Backup_Open_PB .clicked.connect(lambda: JV(BackupDBPath, "Backup"))
        # self.Phone_Open_PB  .clicked.connect(lambda: JV(PhoneDBPath, "Phone"))

        self.Main_Clear_PB.clicked.connect(lambda: Logging.drop_main_db())
        self.Render_Clear_PB.clicked.connect(lambda: Logging.drop_line_monitoring_db())
        self.PLC_Clear_PB.clicked.connect(lambda: Logging.drop_da_db())
        self.Sender_Clear_PB.clicked.connect(lambda: Logging.drop_sender_db())
        self.Bale_Clear_PB.clicked.connect(lambda: Logging.drop_bale_db())
        #   End     logging Tab

        self.count_row = 0
        self.excelAddress = ""

        self.lbl_Data = [
            self.findChild(QLabel, "lbl_Data_1"),
            self.findChild(QLabel, "lbl_Data_2"),
            self.findChild(QLabel, "lbl_Data_3"),
            self.findChild(QLabel, "lbl_Data_4"),
            self.findChild(QLabel, "lbl_Data_5"),
            self.findChild(QLabel, "lbl_Data_6"),
            self.findChild(QLabel, "lbl_Data_7"),
            self.findChild(QLabel, "lbl_Data_8")]

        self.lbl_Data_Name = [
            self.findChild(QLabel, "lbl_Data_Name_1"),
            self.findChild(QLabel, "lbl_Data_Name_2"),
            self.findChild(QLabel, "lbl_Data_Name_3"),
            self.findChild(QLabel, "lbl_Data_Name_4"),
            self.findChild(QLabel, "lbl_Data_Name_5"),
            self.findChild(QLabel, "lbl_Data_Name_6"),
            self.findChild(QLabel, "lbl_Data_Name_7"),
            self.findChild(QLabel, "lbl_Data_Name_8")]

        self.lbl_Data_Status = [
            self.findChild(QLabel, "lbl_Status_1"),
            self.findChild(QLabel, "lbl_Status_2"),
            self.findChild(QLabel, "lbl_Status_3"),
            self.findChild(QLabel, "lbl_Status_4"),
            self.findChild(QLabel, "lbl_Status_5"),
            self.findChild(QLabel, "lbl_Status_6"),
            self.findChild(QLabel, "lbl_Status_7"),
            self.findChild(QLabel, "lbl_Status_8")]

        self.Logo_label_Setting = self.findChild(QLabel, "Logo_label_Setting")
        self.Logo_label_Sensor_Status = self.findChild(QLabel, "Logo_label_Sensor_Status")
        self.Logo_label_PLC_Status = self.findChild(QLabel, "Logo_label_PLC_Status")
        self.Logo_label_Excel = self.findChild(QLabel, "Logo_label_Excel")
        self.Main_Logo_label = self.findChild(QLabel, "Main_Logo_label")
        self.Logo_label_Backup = self.findChild(QLabel, "Logo_label_Backup")
        self.Logo_label_Thread = self.findChild(QLabel, "Logo_label_Thread")

        self.Logo_label_Setting.setPixmap(Pics.Logo)
        self.Logo_label_Sensor_Status.setPixmap(Pics.Logo)
        self.Logo_label_PLC_Status.setPixmap(Pics.Logo)
        self.Logo_label_Excel.setPixmap(Pics.Logo)
        self.Main_Logo_label.setPixmap(Pics.Logo)
        self.Logo_label_Backup.setPixmap(Pics.Logo)
        self.Logo_label_Thread.setPixmap(Pics.Logo)
        self.BaleStatus_label.setPixmap(Pics.deleteMark)

        self.BaleStatus_label = self.findChild(QLabel, "BaleStatus_label")

        self.tabWidget = self.findChild(QTabWidget, "tabWidget")

        self.lbl_Test_Virtual = self.findChild(QLabel, "lbl_Test_Virtual")
        self.lbl_Status = self.findChild(QLabel, "lbl_Status")
        self.Status_label_bot = self.findChild(QLabel, "Status_label_bot")

        self.PLC_Status_lbl = [
            self.findChild(QLabel, "PLC_Status_lbl_1"),
            self.findChild(QLabel, "PLC_Status_lbl_2"),
            self.findChild(QLabel, "PLC_Status_lbl_3"),
            self.findChild(QLabel, "PLC_Status_lbl_4")]

        self.PLC_Counter_lbl = [
            self.findChild(QLabel, "PLC_Counter_lbl_1"),
            self.findChild(QLabel, "PLC_Counter_lbl_2"),
            self.findChild(QLabel, "PLC_Counter_lbl_3"),
            self.findChild(QLabel, "PLC_Counter_lbl_4")]

        self.lineEdit_Name = [
            self.findChild(QLineEdit, "PLC_Name_lineEdit_1"),
            self.findChild(QLineEdit, "PLC_Name_lineEdit_2"),
            self.findChild(QLineEdit, "PLC_Name_lineEdit_3"),
            self.findChild(QLineEdit, "PLC_Name_lineEdit_4")]

        self.lineEdit_IP = [
            self.findChild(QLineEdit, "PLC_IP_lineEdit_1"),
            self.findChild(QLineEdit, "PLC_IP_lineEdit_2"),
            self.findChild(QLineEdit, "PLC_IP_lineEdit_3"),
            self.findChild(QLineEdit, "PLC_IP_lineEdit_4")]

        self.lineEdit_TestPort = [
            self.findChild(QLineEdit, "PLC_TestPort_lineEdit_1"),
            self.findChild(QLineEdit, "PLC_TestPort_lineEdit_2"),
            self.findChild(QLineEdit, "PLC_TestPort_lineEdit_3"),
            self.findChild(QLineEdit, "PLC_TestPort_lineEdit_4")]

        self.lbl_Test_Virtual = [
            self.findChild(QLabel, "lbl_Test_Virtual_1"),
            self.findChild(QLabel, "lbl_Test_Virtual_2"),
            self.findChild(QLabel, "lbl_Test_Virtual_3"),
            self.findChild(QLabel, "lbl_Test_Virtual_4")]

        self.checkBox_Test_Virtual = [
            self.findChild(QCheckBox, "checkBox_Test_Virtual_1"),
            self.findChild(QCheckBox, "checkBox_Test_Virtual_2"),
            self.findChild(QCheckBox, "checkBox_Test_Virtual_3"),
            self.findChild(QCheckBox, "checkBox_Test_Virtual_4")]

        self.checkBox_Counter = [
            self.findChild(QCheckBox, "checkBox_Counter_1"),
            self.findChild(QCheckBox, "checkBox_Counter_2"),
            self.findChild(QCheckBox, "checkBox_Counter_3"),
            self.findChild(QCheckBox, "checkBox_Counter_4")]

        self.checkBox_Test_Virtual[0].setEnabled(False)
        self.checkBox_Test_Virtual[1].setEnabled(False)
        self.checkBox_Test_Virtual[2].setEnabled(False)
        self.checkBox_Test_Virtual[3].setEnabled(False)

        self.checkBox_Counter[0].setEnabled(False)
        self.checkBox_Counter[1].setEnabled(False)
        self.checkBox_Counter[2].setEnabled(False)
        self.checkBox_Counter[3].setEnabled(False)

        self.lineEdit_TestPort[0].setStyleSheet(line_edit_style)
        self.lineEdit_TestPort[1].setStyleSheet(line_edit_style)
        self.lineEdit_TestPort[2].setStyleSheet(line_edit_style)
        self.lineEdit_TestPort[3].setStyleSheet(line_edit_style)

        self.lineEdit_IP[0].setStyleSheet(line_edit_style)
        self.lineEdit_IP[1].setStyleSheet(line_edit_style)
        self.lineEdit_IP[2].setStyleSheet(line_edit_style)
        self.lineEdit_IP[3].setStyleSheet(line_edit_style)

        self.lineEdit_Name[0].setStyleSheet(line_edit_style)
        self.lineEdit_Name[1].setStyleSheet(line_edit_style)
        self.lineEdit_Name[2].setStyleSheet(line_edit_style)
        self.lineEdit_Name[3].setStyleSheet(line_edit_style)

        self.PLC_Status.PLC_Submit_pb = self.PLC_Status.findChild(QPushButton, "PLC_Submit_pb")

        self.PLC_Status.PLC_Submit_pb.setStyleSheet(active_pb_style)

        self.lineEdit_TestPort[0].setValidator(self.Setting.onlyInt)
        self.lineEdit_TestPort[1].setValidator(self.Setting.onlyInt)
        self.lineEdit_TestPort[2].setValidator(self.Setting.onlyInt)
        self.lineEdit_TestPort[3].setValidator(self.Setting.onlyInt)

        self.Backup_Name = [
            self.findChild(QLineEdit, "Backup_Name_1"),
            self.findChild(QLineEdit, "Backup_Name_2"),
            self.findChild(QLineEdit, "Backup_Name_3"),
            self.findChild(QLineEdit, "Backup_Name_4")]

        self.Backup_Path = [
            self.findChild(QLineEdit, "Backup_Path_1"),
            self.findChild(QLineEdit, "Backup_Path_2"),
            self.findChild(QLineEdit, "Backup_Path_3"),
            self.findChild(QLineEdit, "Backup_Path_4")]

        self.Backup_FileName = [
            self.findChild(QLineEdit, "Backup_FileName_1"),
            self.findChild(QLineEdit, "Backup_FileName_2"),
            self.findChild(QLineEdit, "Backup_FileName_3"),
            self.findChild(QLineEdit, "Backup_FileName_4")]

        self.Backup_Time = [
            self.findChild(QLineEdit, "Backup_Time_1"),
            self.findChild(QLineEdit, "Backup_Time_2"),
            self.findChild(QLineEdit, "Backup_Time_3"),
            self.findChild(QLineEdit, "Backup_Time_4")]

        self.Choose_Path_pb = [
            self.findChild(QPushButton, "Choose_Path_pb_1"),
            self.findChild(QPushButton, "Choose_Path_pb_2"),
            self.findChild(QPushButton, "Choose_Path_pb_3"),
            self.findChild(QPushButton, "Choose_Path_pb_4")]

        self.Backup_pb = [
            self.findChild(QPushButton, "Backup_pb_1"),
            self.findChild(QPushButton, "Backup_pb_2"),
            self.findChild(QPushButton, "Backup_pb_3"),
            self.findChild(QPushButton, "Backup_pb_4")]

        self.Backup_pb[0].setEnabled(False)
        self.Backup_pb[1].setEnabled(False)
        self.Backup_pb[2].setEnabled(False)
        self.Backup_pb[3].setEnabled(False)

        self.Choose_Path_pb[0].setEnabled(False)
        self.Choose_Path_pb[1].setEnabled(False)
        self.Choose_Path_pb[2].setEnabled(False)
        self.Choose_Path_pb[3].setEnabled(False)

        self.Backup_pb[0].setStyleSheet(deactivate_pb_style)
        self.Backup_pb[1].setStyleSheet(deactivate_pb_style)
        self.Backup_pb[2].setStyleSheet(deactivate_pb_style)
        self.Backup_pb[3].setStyleSheet(deactivate_pb_style)

        self.Choose_Path_pb[0].setStyleSheet(deactivate_pb_style)
        self.Choose_Path_pb[1].setStyleSheet(deactivate_pb_style)
        self.Choose_Path_pb[2].setStyleSheet(deactivate_pb_style)
        self.Choose_Path_pb[3].setStyleSheet(deactivate_pb_style)

        self.Backup_Name[0].setStyleSheet(line_edit_style)
        self.Backup_Name[1].setStyleSheet(line_edit_style)
        self.Backup_Name[2].setStyleSheet(line_edit_style)
        self.Backup_Name[3].setStyleSheet(line_edit_style)

        self.Backup_Path[0].setStyleSheet(line_edit_style)
        self.Backup_Path[1].setStyleSheet(line_edit_style)
        self.Backup_Path[2].setStyleSheet(line_edit_style)
        self.Backup_Path[3].setStyleSheet(line_edit_style)

        self.Backup_FileName[0].setStyleSheet(line_edit_style)
        self.Backup_FileName[1].setStyleSheet(line_edit_style)
        self.Backup_FileName[2].setStyleSheet(line_edit_style)
        self.Backup_FileName[3].setStyleSheet(line_edit_style)

        self.Backup_Time[0].setStyleSheet(line_edit_style)
        self.Backup_Time[1].setStyleSheet(line_edit_style)
        self.Backup_Time[2].setStyleSheet(line_edit_style)
        self.Backup_Time[3].setStyleSheet(line_edit_style)

        self.Backup_Time[0].setValidator(self.Setting.onlyInt)
        self.Backup_Time[1].setValidator(self.Setting.onlyInt)
        self.Backup_Time[2].setValidator(self.Setting.onlyInt)
        self.Backup_Time[3].setValidator(self.Setting.onlyInt)

        self.Backup_Submit_pb = self.findChild(QPushButton, "Backup_Submit_pb")
        self.Backup_Submit_pb.setStyleSheet(active_pb_style)

        self.Setting.DebugPrintFlag = self.findChild(QCheckBox, "DebugPrintFlag")
        self.Setting.SendDataPrintFlag = self.findChild(QCheckBox, "SendDataPrintFlag")

        self.Setting.baleONOFFSendFlag = self.findChild(QCheckBox, "baleONOFFSendFlag")
        self.Setting.baleONOFFFlag = self.findChild(QCheckBox, "baleONOFFFlag")

        self.Setting.TestSensor_lineEdit = self.findChild(QLineEdit, "TestSensor_lineEdit")

        self.Sensor_Status.Sensor_Submit_pb = self.Sensor_Status.findChild(QPushButton, "Sensor_Submit_pb")

        self.Sensor_Status.Sensor_Submit_pb.setStyleSheet(active_pb_style)
