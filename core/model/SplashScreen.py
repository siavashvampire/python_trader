from time import sleep
from threading import Thread

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QSplashScreen, QApplication


class SplashScreen:
    def __init__(self, image_resource, size=500, text=None):
        pixmap = QPixmap(image_resource).scaled(size, size, Qt.KeepAspectRatio)
        self.splash = QSplashScreen(pixmap)
        # self.splash.setMask(QRegion(pixmap.mask()))
        self.splash.setPixmap(pixmap)
        self.alignment = Qt.AlignHCenter | Qt.AlignVCenter
        self.color = QColor(170, 90, 30)
        self.save_text_show = True
        self.show_message_sleep_time = 0.2
        self.dot_sleep_time = 0.5
        flags = self.splash.windowFlags()
        flags |= Qt.WindowStaysOnTopHint
        self.splash.setWindowFlags(flags)
        self.__saved_text = ""
        self.__last_text = ""
        self.stop_Thread = False
        self.Thread = Thread(target=self.main_thread, args=(lambda: self.stop_Thread,))
        if text is not None:
            self.show_message(text)

    def show(self):
        self.splash.show()

    def hide(self):
        self.stop_Thread = True
        self.Thread.join()
        self.splash.hide()

    def show_message(self, message, program=False):
        if self.Thread.is_alive() and not program:
            self.stop_Thread = True
            self.Thread.join()

        if self.save_text_show and not program:
            message = self.__saved_text + message

        if not program:
            self.__last_text = message
            self.stop_Thread = False
            self.Thread = Thread(target=self.main_thread, args=(lambda: self.stop_Thread,))
            self.Thread.start()

        self.splash.showMessage(message, self.alignment, self.color)
        QApplication.instance().processEvents()
        sleep(self.show_message_sleep_time)

    def get_message(self):
        return self.__saved_text

    def finish(self, ui):
        self.stop_Thread = True
        self.Thread.join()
        self.splash.finish(ui)

    def set_font(self, font_size, font_weight=None):
        font = self.splash.font()
        font.setPixelSize(font_size)
        if font_weight is not None:
            font.setWeight(font_weight)
        self.splash.setFont(font)

    def add_saved_text(self, text, new_line=True):
        if new_line:
            self.__saved_text += text + "\n"
        else:
            self.__saved_text += text

    def main_thread(self, stop_thread):
        i = 0
        while True:
            add_text = ""
            add_text2 = ""
            if i == 1:
                add_text = " ."
                add_text2 = "  "
            if i == 2:
                add_text = " .."
                add_text2 = "   "
            if i == 3:
                add_text = " ..."
                add_text2 = "    "

            x = self.__last_text.split("\n")
            x[-1] = add_text2 + x[-1] + add_text
            temp_text = "\n".join(x)
            self.show_message(temp_text, True)
            sleep(self.dot_sleep_time)
            i += 1
            if i == 4:
                i = 1
            if stop_thread():
                break
