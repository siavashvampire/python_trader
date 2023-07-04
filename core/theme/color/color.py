import PyQt5.QtCore
from PyQt5.QtGui import QColor

PB_BG_color_deactivate: str = "{r}, {g}, {b}, {a}".format(r=230, g=230, b=235, a=255)  # push a button background
# color when they deactivate
PB_Text_color_deactivate: str = "{r}, {g}, {b}, {a}".format(r=200, g=200, b=200, a=255)  # push button Text color when
# they deactivate

PB_BG_color_active: str = "{r}, {g}, {b}, {a}".format(r=60, g=120, b=160, a=255)  # push a button background
# color when they activate
PB_Text_color_active: str = "{r}, {g}, {b}, {a}".format(r=240, g=240, b=240, a=255)  # push button Text color when
# they activate

# line_edit_BG: str = "transparent"  # line edit background
line_edit_BG: str = "{r}, {g}, {b}, {a}".format(r=60, g=120, b=160, a=255)  # line edit background color
line_edit_Text_color: str = "{r}, {g}, {b}, {a}".format(r=240, g=240, b=240, a=255)  # line edit Text color

label_Text_BG: str = "transparent"  # label background color
label_Text_color: str = "{r}, {g}, {b}, {a}".format(r=0, g=90, b=90, a=255)  # label Text color

tab_selected_bg_color = "{r}, {g}, {b}, {a}".format(r=60, g=120, b=160, a=255)  # tab selected background color
tab_selected_text_color = "{r}, {g}, {b}, {a}".format(r=255, g=255, b=255, a=255)  # tab selected Text color

login_text_color = "{r}, {g}, {b}, {a}".format(r=38, g=17, b=0, a=255)  # login Text color
login_border_color = "{r}, {g}, {b}, {a}".format(r=38, g=17, b=0, a=255)  # login border color
login_bg_color = "{r}, {g}, {b}, {a}".format(r=255, g=255, b=255, a=255)  # login background color

# trade_on_bg_color = "{r}, {g}, {b}, {a}".format(r=255, g=255, b=255, a=255)  # trade on background color
trade_on_bg_color = "transparent"  # trade on background color
trade_on_text_color = "{r}, {g}, {b}, {a}".format(r=0, g=255, b=0, a=255)  # trade on text color
# trade_off_bg_color = "{r}, {g}, {b}, {a}".format(r=255, g=255, b=255, a=255)  # trade off background color
trade_off_bg_color = "transparent"  # trade off background color
trade_off_text_color = "{r}, {g}, {b}, {a}".format(r=255, g=40, b=40, a=255)  # trade off text color

DA_unit_ok_status_label_bot_bg = "{r}, {g}, {b}, {a}".format(r=19, g=164, b=70,
                                                             a=255)  # da units label back ground color
DA_unit_ok_status_label_bot_text = "{r}, {g}, {b}, {a}".format(r=255, g=255, b=255, a=255)  # da units label Text color

DA_unit_bad_status_label_bot_bg = "{r}, {g}, {b}, {a}".format(r=250, g=0, b=0,
                                                              a=255)  # da units label back ground color
DA_unit_bad_status_label_bot_text = "{r}, {g}, {b}, {a}".format(r=255, g=255, b=255, a=255)  # da units label Text color

login_line_edit_bg = "{r}, {g}, {b}, {a}".format(r=255, g=255, b=255, a=255)  # login line edit background color
login_line_edit_text = "{r}, {g}, {b}, {a}".format(r=146, g=146, b=146, a=255)  # login line edit Text color
login_line_edit_border = "{r}, {g}, {b}, {a}".format(r=38, g=17, b=0, a=255)  # login line edit Border color

login_forget_pb_bg = "{r}, {g}, {b}, {a}".format(r=119, g=65, b=1, a=0)  # login forget push button background color
login_forget_pb_text = "{r}, {g}, {b}, {a}".format(r=60, g=120, b=160, a=255)  # login forget push button Text color

login_enter_pb_bg = "{r}, {g}, {b}, {a}".format(r=60, g=120, b=160, a=255)  # login enters pushButton background color
login_enter_pb_text = "{r}, {g}, {b}, {a}".format(r=255, g=255, b=255, a=255)  # login forget push button Text color

start_splash_align = PyQt5.QtCore.Qt.AlignHCenter | PyQt5.QtCore.Qt.AlignBottom  # start splash text alignment
start_splash_color = QColor(170, 90, 30)  # start splash text color
start_splash_font_size = 12  # start splash text font

close_splash_align = PyQt5.QtCore.Qt.AlignHCenter | PyQt5.QtCore.Qt.AlignVCenter  # end splash text alignment
close_splash_color = QColor(190, 105, 40)  # end splash text color
end_splash_font_size = 15  # end splash text font
