from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImage, QFont, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextBrowser, QSpacerItem, QSizePolicy
from . import server_request
import requests

class MainApplicationGUI(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/data/main.ui', self)

        self.ButtonClose.clicked.connect(self.CloseWindow)
        self.StartPage_Top_Refresh.clicked.connect(self.GetRocketsInfo)

        self.NavBar.mouseMoveEvent = self.MoveWindow
        self.NavBar_Title.mouseMoveEvent = self.MoveWindow

        self.tabWidget.blockSignals(True)
        self.tabWidget.currentChanged.connect(self.UpdateTabInfo)

        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flags)
        self.tabWidget.blockSignals(False)

        self.GetRocketsInfo()

    def CloseWindow(self):
        self.close()

    def MoveWindow(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.clickPosition)
            self.clickPosition = event.globalPos()
            event.accept()
        super(MainApplicationGUI, self).mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.clickPosition = event.globalPos()
        super(MainApplicationGUI, self).mousePressEvent(event)

    def SetUser(self, login):
        self.User = login
        self.NavBar_User.setText(self.User)

    def UpdateTabInfo(self, selected_index):
        id = int(selected_index)

        if id == 0:
            pass
            # self.GetRocketsInfo()
        elif id == 1:
            pass

    def GetRocketsInfo(self):
        self.StartPage_Top_Refresh.setDisabled(True)

        data = server_request.rockets()

        if self.horizontalLayout_4.count() != 0:
            self.horizontalLayout_4.removeItem(self.StartPage_Spacer1)
            self.horizontalLayout_4.removeItem(self.StartPage_Spacer2)
            if self.horizontalLayout_4.count() != 0:
                for i in reversed(range(self.horizontalLayout_4.count())):
                    self.horizontalLayout_4.itemAt(i).widget().deleteLater()

        if len(data) != 0:
            self.StartPage_Spacer1 = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.horizontalLayout_4.addItem(self.StartPage_Spacer1)

            for item in data:
                widget = QWidget()
                card = QVBoxLayout()

                img = QLabel()
                text = QTextBrowser()
                url = ''

                if url != item[3]:
                    url = item[3]
                    data = QImage()
                    data.loadFromData(requests.get(url).content)
                img.setPixmap(QPixmap(data))

                text.setText(str(item[2]))

                font = QFont()
                font.setFamily(u'Montserrat Medium')
                font.setPointSize(10)
                text.setFont(font)

                img.setStyleSheet('border-top-right-radius: 14px; border-top-left-radius: 14px;')
                text.setStyleSheet('background: #18181c; border-bottom-right-radius: 14px; border-bottom-left-radius: 14px; padding: 10px; color: #fff;')

                card.addWidget(img)
                card.addWidget(text)
                card.setContentsMargins(5, 0, 5, 10)
                card.setSpacing(0)
                widget.setLayout(card)
                widget.setMaximumWidth(256)
                self.horizontalLayout_4.addWidget(widget)

            self.StartPage_Spacer2 = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.horizontalLayout_4.addItem(self.StartPage_Spacer2)
            self.StartPage_Top_Refresh.setDisabled(False)