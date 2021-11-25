from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImage, QFont, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextBrowser, QSpacerItem, QSizePolicy, QPushButton, QSizeGrip
from PyQt5.QtCore import QSize
from . import server_request
from . import dialogs
import requests

class MainApplicationGUI(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/data/main.ui', self)

        self.ButtonClose.clicked.connect(self.CloseWindow)
        self.FlightsPage_Top_Create.clicked.connect(lambda checked, arg=['edit']: self.CreatingDialog(arg))
        self.StartPage_Top_Refresh.clicked.connect(self.GetRocketsInfo)
        self.FlightsPage_Top_Refresh.clicked.connect(self.GetFlightsInfo)

        self.tabWidget.setCurrentIndex(0)

        self.NavBar.mouseMoveEvent = self.MoveWindow
        self.NavBar_Title.mouseMoveEvent = self.MoveWindow

        self.sizegrip = QSizeGrip(self)
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
                text = QTextBrowser()
                url = ''

                if url != item[3]:
                    url = item[3]
                    image = QImage()
                    image.loadFromData(requests.get(url).content)

                data_img = QPixmap(image).scaled(256, 256, QtCore.Qt.KeepAspectRatioByExpanding)

                img.setPixmap(data_img)
                img.setMaximumHeight(256)
                img.setAlignment(QtCore.Qt.AlignCenter)

                data_text = 'Название: ' + str(item[1]) + '\nОписание: ' + str(item[2])

                text.setText(data_text)

                font = QFont()
                font.setFamily(u'Montserrat Medium')
                font.setPointSize(10)
                text.setFont(font)

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
                rocket = server_request.rocket_by_id(item[2])
                citys = server_request.citys_by_id(item[7], item[8])
                check = server_request.is_admin(self.User)
                widget = QWidget()
                card = QHBoxLayout()
                url = ''

                img = QLabel()
                text = QTextBrowser()

                data_text = 'Название: ' + str(item[1]) + '\nРакета: ' + str(rocket[0][1]) + '\nРейс: ' + str(citys[0][1]) + ' - ' + str(citys[1][1]) + '\nЦена билета: ' + str(item[5])

                text.setText(data_text)

                font = QFont()
                font.setFamily(u'Montserrat Medium')
                font.setPointSize(10)
                text.setFont(font)

                if url != rocket[0][3]:
                    url = rocket[0][3]
                    image = QImage()
                    image.loadFromData(requests.get(url).content)

                data_img = QPixmap(image).scaled(128, 128, QtCore.Qt.KeepAspectRatioByExpanding)

                img.setPixmap(data_img)
                img.setMaximumSize(128, 128)
                img.setMinimumSize(128, 128)
                img.setAlignment(QtCore.Qt.AlignCenter)

                card.addWidget(img)
                card.addWidget(text)

                if check:
                    edit_button = QPushButton()
                    edit_button.clicked.connect(lambda checked, arg=[item, 'edit']: self.FlightsButton(arg))
                    edit_button.setStyleSheet('background: #1f1f23; border: 0px; padding: 5px; border-radius: 5px; width: 45px; height: 45px; margin-right: 10px;')
                    edit_button.setIcon(QIcon("ui/img/edit-icon.png"))
                    edit_button.setIconSize(QSize(32, 32))
                    card.addWidget(edit_button)

                    delete_button = QPushButton()
                    delete_button.clicked.connect(lambda checked, arg=[item, 'delete']: self.FlightsButton(arg))
                    delete_button.setStyleSheet('background: #1f1f23; border: 0px; padding: 5px; border-radius: 5px; width: 45px; height: 45px; margin-right: 10px;')
                    delete_button.setIcon(QIcon("ui/img/delete-icon.png"))
                    delete_button.setIconSize(QSize(32, 32))
                    card.addWidget(delete_button)

                card.setContentsMargins(5, 5, 5, 5)
                card.setSpacing(0)

                widget.setStyleSheet('background: #18181c; border-radius: 14px; padding: 10px; color: #fff;')

                widget.setLayout(card)
                widget.setMinimumHeight(138)
                widget.setMaximumHeight(138)
                self.verticalLayout_5.addWidget(widget)

            self.FlightsPage_Spacer1 = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.verticalLayout_5.addItem(self.FlightsPage_Spacer1)

        self.FlightsPage_Top_Refresh.setDisabled(False)

    def FlightsButton(self, arg):
        data = arg[0]
        type = arg[1]

        if type.lower() == 'edit':
            print('Ahahahahahah')
        elif type.lower() == 'delete':
            print('Hehehehehe')

    def CreatingDialog(self, arg):
        self.dialog = dialogs.CreationDialogGUI()
        self.dialog.show()