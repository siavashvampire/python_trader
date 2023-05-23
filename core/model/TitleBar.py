import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QIcon
from PyQt5.QtWidgets import QDialog, QToolButton, QHBoxLayout, QSizePolicy
from PyQt5.QtWidgets import QLabel, QWidget

from MainCode import path


class TitleBar(QDialog):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.setWindowFlags(Qt.FramelessWindowHint)
        css = """
        QWidget{

            color:white;
            font:12px bold;
            font-weight:bold;
            border-radius: 1px;
            height: 10px;
        }
        QDialog{
            Background-image:url('core/theme/pic/pic/title bar bg.png');
            font-size:12px;
            color: black;
            position: absolute;
            top:10px;
            Background: #8b3800;
            width : 1500px;
        }
        QToolButton{
            Background:#EE853E;
            font-size:11px;
        }
        QToolButton:hover{
            Background: #FF002A;
            font-size:11px;
        }
        """

        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.Highlight)
        self.setStyleSheet(css)

        self.close = QToolButton(self)
        self.close.setIcon(QIcon(path + 'core/theme/pic/pic/close.png'))

        self.close.setMinimumHeight(10)

        label = QLabel(self)
        label.setStyleSheet("color: white;")

        label.setText("AvidMech Trade Login")
        self.setWindowTitle("AvidMech Trade Login")
        hbox = QHBoxLayout(self)
        hbox.addWidget(label)
        hbox.addWidget(self.close)
        hbox.insertStretch(1, 500)
        hbox.setSpacing(0)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    # @staticmethod
    def show_small(self):
        self.parent.showMinimized()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent.moving = True
            self.parent.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.parent.moving:
            self.parent.move(event.globalPos() - self.parent.offset)
