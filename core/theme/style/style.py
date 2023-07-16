from MainCode import path
from core.theme.color.color import pb_text_color_active, line_edit_bg, line_edit_text_color, label_text_color, \
    pb_bg_color_active, label_text_bg, login_text_color, login_bg_color, login_border_color, trade_on_bg_color, \
    trade_on_text_color, trade_off_text_color, trade_off_bg_color, trade_none_bg_color, trade_none_text_color, \
    login_forget_pb_bg, login_forget_pb_text, login_enter_pb_bg, login_enter_pb_text, balance_label_text_color, \
    start_trading_pb_bg_color, stop_trading_pb_bg_color, activate_account_pb_bg_color

line_edit_style = "background-color: " + line_edit_bg + ";color: " + line_edit_text_color + ";border-radius: 7;"
line_edit_prop_style = "background-color: " + line_edit_bg + ";color: rgba(70, 240, 60, 255);"
label_style = "background-color: " + label_text_bg + ";color: " + label_text_color + ";border-radius: 7;"

balance_label_style = "background-color: " + label_text_bg + ";color: " + balance_label_text_color + ";border-radius: 7;"

active_pb_style = "QPushButton {background-color: " + pb_bg_color_active + ";" + "color: " + \
                  pb_text_color_active + ";border-radius: 7;} QPushButton:hover {background-color: #4C5569;}"

start_trading_pb_style = "QPushButton {background-color: " + start_trading_pb_bg_color + ";" + "color: " + \
                         pb_text_color_active + ";border-radius: 7;} QPushButton:hover {background-color: #4BB85D;}"
close_pb_style = "QPushButton {border-image: url(" + path + "core/theme/pic/pic/close.png);} QPushButton:hover {background-color: #ea8e1e;}"

activate_account_pb_style = "QPushButton {background-color: " + activate_account_pb_bg_color + ";" + "color: " + \
                            pb_text_color_active + ";border-radius: 7;} QPushButton:hover {background-color: #4F8B63;}"

stop_trading_pb_style = "background-color: " + stop_trading_pb_bg_color + ";" + "color: " + \
                        pb_text_color_active + ";border-radius: 7;"
activate_label_main_style = "background-color: " + line_edit_bg + ";color: " + label_text_color + ";border-radius: 7;"

optimal_strategy_rb_style = "QRadioButton {background-color: " + line_edit_bg + ";color: " + label_text_color + ";border-radius: 7;} QRadioButton::indicator:checked{border-image: url(" + path + "core/theme/pic/pic/radio-button-green.png);width : 24px;height : 24px;}QRadioButton::indicator{width : 24px;height : 24px;}"
optimal_strategy_label_style = "background-color: " + line_edit_bg + ";color: " + line_edit_text_color + \
                               ";border-radius: 7;"
login_page_style = "background-color: " + login_bg_color + ";color: " + login_text_color + ";" + \
                   "border-radius : 7;border : 1px solid " + login_border_color + ";"
trade_none_style = "background-color:" + trade_none_bg_color + ";color: " + trade_none_text_color + ";"
trade_on_style = "background-color:" + trade_on_bg_color + ";color: " + trade_on_text_color + ";"
trade_off_style = "background-color: " + trade_off_bg_color + ";color: " + trade_off_text_color + ";"
login_forget_style = "background-color: " + login_forget_pb_bg + ";" + "color: " + login_forget_pb_text + ";"
login_enter_pb_style = "background-color: " + login_enter_pb_bg + ";" + "color: " + login_enter_pb_text + \
                       ";border-radius : 5;padding-bottom: 1px;"
