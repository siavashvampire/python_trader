import PyQt5.QtCore
from PyQt5.QtGui import QColor

pb_bg_color_active: str = "rgba({r}, {g}, {b}, {a})".format(r=45, g=55, b=79, a=255)  # push a button background
# color when they activate
pb_text_color_active: str = "rgba({r}, {g}, {b}, {a})".format(r=240, g=240, b=240, a=255)  # push button Text color when
# they activate

start_trading_pb_bg_color: str = "rgba({r}, {g}, {b}, {a})".format(r=43, g=171, b=64, a=255)
hover_start_trading_pb_bg_color: str = "rgba({r}, {g}, {b}, {a})".format(r=75, g=184, b=93, a=255)
activate_account_pb_bg_color: str = "rgba({r}, {g}, {b}, {a})".format(r=50, g=95, b=76, a=255)
stop_trading_pb_bg_color: str = "rgba({r}, {g}, {b}, {a})".format(r=255, g=87, b=34, a=255)
hover_stop_trading_pb_bg_color: str = "rgba({r}, {g}, {b}, {a})".format(r=255, g=119, b=0, a=180)


# line_edit_BG: str = "transparent"  # line edit background
line_edit_bg: str = "rgba({r}, {g}, {b}, {a})".format(r=53, g=62, b=81, a=255)  # line edit background color
line_edit_text_color: str = "rgba({r}, {g}, {b}, {a})".format(r=240, g=240, b=240, a=255)  # line edit Text color

label_text_bg: str = "transparent"  # label background color
label_text_color: str = "rgba({r}, {g}, {b}, {a})".format(r=155, g=159, b=168, a=255)  # label Text color

balance_label_text_color: str = "rgba({r}, {g}, {b}, {a})".format(r=240, g=112, b=0, a=255)  # label Text color

tab_selected_bg_color = "rgba({r}, {g}, {b}, {a})".format(r=60, g=120, b=160, a=255)  # tab selected background color
tab_selected_text_color = "rgba({r}, {g}, {b}, {a})".format(r=255, g=255, b=255, a=255)  # tab selected Text color

login_text_color = "rgba({r}, {g}, {b}, {a})".format(r=38, g=17, b=0, a=255)  # login Text color
login_border_color = "rgba({r}, {g}, {b}, {a})".format(r=38, g=17, b=0, a=255)  # login border color
login_bg_color = "rgba({r}, {g}, {b}, {a})".format(r=255, g=255, b=255, a=255)  # login background color

# trade_on_bg_color = "{r}, {g}, {b}, {a}".format(r=255, g=255, b=255, a=255)  # trade on background color
trade_on_bg_color = "transparent"  # trade on background color
trade_on_text_color = "rgba({r}, {g}, {b}, {a})".format(r=43, g=171, b=64, a=255)  # trade on text color
# trade_off_bg_color = "{r}, {g}, {b}, {a}".format(r=255, g=255, b=255, a=255)  # trade off background color
trade_none_bg_color = "transparent"  # trade off background color
trade_none_text_color = "rgba({r}, {g}, {b}, {a})".format(r=255, g=40, b=40, a=255)  # trade off text color

trade_off_bg_color = "transparent"  # trade off background color
trade_off_text_color = "rgba({r}, {g}, {b}, {a})".format(r=255, g=175, b=40, a=255)  # trade off text color

login_line_edit_bg = "rgba({r}, {g}, {b}, {a})".format(r=255, g=255, b=255, a=255)  # login line edit background color
login_line_edit_text = "rgba({r}, {g}, {b}, {a})".format(r=146, g=146, b=146, a=255)  # login line edit Text color
login_line_edit_border = "rgba({r}, {g}, {b}, {a})".format(r=38, g=17, b=0, a=255)  # login line edit Border color

login_forget_pb_bg = "rgba({r}, {g}, {b}, {a})".format(r=119, g=65, b=1,
                                                       a=0)  # login forget push button background color
login_forget_pb_text = "rgba({r}, {g}, {b}, {a})".format(r=60, g=120, b=160,
                                                         a=255)  # login forget push button Text color

login_enter_pb_bg = "rgba({r}, {g}, {b}, {a})".format(r=60, g=120, b=160,
                                                      a=255)  # login enters pushButton background color
login_enter_pb_text = "rgba({r}, {g}, {b}, {a})".format(r=255, g=255, b=255,
                                                        a=255)  # login forget push button Text color

start_splash_align = PyQt5.QtCore.Qt.AlignHCenter | PyQt5.QtCore.Qt.AlignBottom  # start splash text alignment
start_splash_color = QColor(170, 90, 30)  # start splash text color
start_splash_font_size = 12  # start splash text font

close_splash_align = PyQt5.QtCore.Qt.AlignHCenter | PyQt5.QtCore.Qt.AlignVCenter  # end splash text alignment
close_splash_color = QColor(190, 105, 40)  # end splash text color
end_splash_font_size = 15  # end splash text font
