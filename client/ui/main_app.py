from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImage, QFont, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextBrowser, QSpacerItem, QSizePolicy, QPushButton, QSizeGrip
from PyQt5.QtCore import QSize
from . import server_request
from . import flight_card
import requests
from . import dialogs


class MainApplicationGUI(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/data/main.ui', self)
        
        self.setMinimumSize(512, 512)

        self.ButtonClose.clicked.connect(self.CloseWindow)
        self.FlightsPage_Top_Create.clicked.connect(lambda checked, arg=[]: self.AddFlight())
        self.StartPage_Top_Refresh.clicked.connect(self.GetRocketsInfo)
        self.FlightsPage_Top_Refresh.clicked.connect(self.GetFlightsInfo)

        self.tabWidget.setCurrentIndex(0)

        self.NavBar.mouseMoveEvent = self.MoveWindow
        self.NavBar_Title.mouseMoveEvent = self.MoveWindow

        self.sizegrip = QSizeGrip(self)
        self.sizegrip.setStyleSheet('background: #18181c;')
        self.verticalLayout.addWidget(self.sizegrip, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)

        self.tabWidget.blockSignals(True)
        self.tabWidget.currentChanged.connect(self.UpdateTabInfo)

        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flags)
        self.tabWidget.blockSignals(False)

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

        self.GetRocketsInfo()
        self.GetFlightsInfo()

    def UpdateTabInfo(self, selected_index):
        id = int(selected_index)

        if id == 0:
            pass
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
                title = QLabel()
                text = QTextBrowser()
                url = ''
                
                data_text = '<big>Описание:</big><br><font size=16px, color=#cacdcf>' + str(item['descr']) + '</font><br>Максимальное количество пасажиров: ' + str(item['max_people_count']) + '<br>Количество запусков: ' + str(item['count_of_launches'])

                if url != item['img']:
                    image = QImage()
                    image.loadFromData(requests.get(item['img']).content)

                data_img = QPixmap(image).scaled(256, 256, QtCore.Qt.KeepAspectRatioByExpanding)

                img.setPixmap(data_img)
                img.setMaximumHeight(256)
                img.setAlignment(QtCore.Qt.AlignCenter)
                title.setText(item['name'])
                text.setText(data_text)

                font = QFont()
                font.setFamily(u'Montserrat Medium')
                font.setPointSize(10)
                text.setFont(font)
                font2 = QFont()
                font2.setFamily(u'Montserrat Light')
                font2.setPointSize(16)
                title.setFont(font2)

                text.setStyleSheet('background: #18181c; border-bottom-right-radius: 14px; border-bottom-left-radius: 14px; padding: 10px; color: #fff;')
                title.setStyleSheet('background: #18181c; padding: 10px; padding-bottom: 0px; color: #fff;')

                card.addWidget(img)
                card.addWidget(title)
                card.addWidget(text)
                card.setContentsMargins(5, 0, 5, 10)
                card.setSpacing(0)
                widget.setLayout(card)
                widget.setMaximumWidth(256)
                self.horizontalLayout_4.addWidget(widget)

            self.StartPage_Spacer2 = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.horizontalLayout_4.addItem(self.StartPage_Spacer2)

            self.StartPage_Top_Refresh.setDisabled(False)

    def GetFlightsInfo(self):
        self.FlightsPage_Top_Refresh.setDisabled(True)

        data = server_request.flights()

        if self.verticalLayout_5.count() != 0:
            self.verticalLayout_5.removeItem(self.FlightsPage_Spacer1)
            if self.verticalLayout_5.count() != 0:
                for i in reversed(range(self.verticalLayout_5.count())):
                    self.verticalLayout_5.itemAt(i).widget().deleteLater()

        if len(data) != 0:
            for item in data:
                widget = flight_card.FlightsCardGUI()
                widget.AddButtons(item)
                widget.SetData(item)
                self.verticalLayout_5.addWidget(widget, 0)

            self.FlightsPage_Spacer1 = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.verticalLayout_5.addItem(self.FlightsPage_Spacer1)

        self.FlightsPage_Top_Refresh.setDisabled(False)

    def GetArticlesInfo(self):
        self.RequestsPage_Top_Refresh.setDisabled(True)

        data = server_request.articles()

        if self.verticalLayout_7.count() != 0:
            self.verticalLayout_7.removeItem(self.FlightsPage_Spacer1)
            if self.verticalLayout_7.count() != 0:
                for i in reversed(range(self.verticalLayout_7.count())):
                    self.verticalLayout_7.itemAt(i).widget().deleteLater()

        if len(data) != 0:
            for item in data:
                widget = flight_card.ArticlesCardGUI()
                widget.AddButtons(item)
                widget.SetData(item)
                self.verticalLayout_7.addWidget(widget, 0)

            self.FlightsPage_Spacer1 = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.verticalLayout_7.addItem(self.FlightsPage_Spacer1)

        self.RequestsPage_Top_Refresh.setDisabled(False)
    
    def AddFlight(self):
        dialog = dialogs.FlightsDialogGUI()
        dialog.SetType('add', [])
        dialog.show()