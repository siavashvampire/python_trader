from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

PB_BG_color_deactivate: str = "{r}, {g}, {b}, {a}".format(r=230, g=230, b=235, a=255)  # push button back ground
# color when they deactivate
PB_Text_color_deactivate: str = "{r}, {g}, {b}, {a}".format(r=200, g=200, b=200, a=255)  # push button Text color when
# they deactivate

PB_BG_color_active: str = "{r}, {g}, {b}, {a}".format(r=230, g=230, b=235, a=255)  # push button back ground
# color when they active
PB_Text_color_active: str = "{r}, {g}, {b}, {a}".format(r=0, g=0, b=0, a=255)  # push button Text color when
# they active

line_edit_BG: str = "transparent"  # line edit back ground
line_edit_Text_color: str = "{r}, {g}, {b}, {a}".format(r=0, g=0, b=0, a=255)  # line edit Text color

tab_selected_bg_color = "{r}, {g}, {b}, {a}".format(r=139, g=56, b=0, a=255)  # tab selected back ground color
tab_selected_text_color = "{r}, {g}, {b}, {a}".format(r=255, g=255, b=255, a=255)  # tab selected Text color

login_text_color = "{r}, {g}, {b}, {a}".format(r=38, g=17, b=0, a=255)  # login Text color
login_border_color = "{r}, {g}, {b}, {a}".format(r=38, g=17, b=0, a=255)  # login border color
login_bg_color = "{r}, {g}, {b}, {a}".format(r=255, g=255, b=255, a=255)  # login back ground color

DA_unit_ok_status_label_bot_bg = "{r}, {g}, {b}, {a}".format(r=19, g=164, b=70,
                                                             a=255)  # da units label back ground color
DA_unit_ok_status_label_bot_text = "{r}, {g}, {b}, {a}".format(r=255, g=255, b=255, a=255)  # da units label Text color

DA_unit_bad_status_label_bot_bg = "{r}, {g}, {b}, {a}".format(r=250, g=0, b=0,
                                                              a=255)  # da units label back ground color
DA_unit_bad_status_label_bot_text = "{r}, {g}, {b}, {a}".format(r=255, g=255, b=255, a=255)  # da units label Text color

login_line_edit_bg = "{r}, {g}, {b}, {a}".format(r=255, g=255, b=255, a=255)  # login line edit back ground color
login_line_edit_text = "{r}, {g}, {b}, {a}".format(r=146, g=146, b=146, a=255)  # login line edit Text color
login_line_edit_border = "{r}, {g}, {b}, {a}".format(r=38, g=17, b=0, a=255)  # login line edit Border color

login_forget_pb_bg = "{r}, {g}, {b}, {a}".format(r=119, g=65, b=1, a=0)  # login forget push button back ground color
login_forget_pb_text = "{r}, {g}, {b}, {a}".format(r=119, g=65, b=1, a=255)  # login forget push button Text color

login_enter_pb_bg = "{r}, {g}, {b}, {a}".format(r=139, g=56, b=0, a=255)  # login enter pushButton back ground color
login_enter_pb_text = "{r}, {g}, {b}, {a}".format(r=255, g=255, b=255, a=255)  # login forget push button Text color

start_splash_align = Qt.AlignHCenter | Qt.AlignBottom  # start splash text alignment
start_splash_color = QColor(170, 90, 30)  # start splash text color
start_splash_font_size = 12  # start splash text font

close_splash_align = Qt.AlignHCenter | Qt.AlignVCenter  # end splash text alignment
close_splash_color = QColor(190, 105, 40)  # end splash text color
end_splash_font_size = 15  # end splash text font
