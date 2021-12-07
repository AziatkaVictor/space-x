from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QSpinBox, QDateTimeEdit, QHBoxLayout, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QPushButton, QAbstractSpinBox
from ui import server_request
from datetime import datetime

class CreationDialogGUI(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/data/dialog.ui', self)

        self.ButtonClose.clicked.connect(self.CloseWindow)

        self.NavBar.mouseMoveEvent = self.MoveWindow
        self.NavBar_Title.mouseMoveEvent = self.MoveWindow

        font = QFont(u'Montserrat Light', 12)

        # Название

        self.EditTitle = QLineEdit()
        self.EditTitleLabel = QLabel('Название рейса:')
        self.EditTitleLabel.setFont(font)
        self.Title = QVBoxLayout()
        self.Title.addWidget(self.EditTitleLabel)
        self.Title.addWidget(self.EditTitle)

        # Выбор ракеты

        self.EditRocket = QComboBox()

        for i in server_request.rockets():
            self.EditRocket.addItem(i['name'])

        self.EditRocketLabel = QLabel('Тип ракеты:')
        self.EditRocketLabel.setFont(font)
        self.Rocket = QVBoxLayout()
        self.Rocket.addWidget(self.EditRocketLabel)
        self.Rocket.addWidget(self.EditRocket)

        # Выбор цены

        self.EditCost = QSpinBox()
        self.EditCostLabel = QLabel('Цена билета:')
        self.EditCostLabel.setFont(font)
        self.EditCost.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.EditCost.setMaximum(999999999)
        self.Cost = QVBoxLayout()
        self.Cost.addWidget(self.EditCostLabel)
        self.Cost.addWidget(self.EditCost)

        # Выбор даты

        self.EditDate = QDateTimeEdit()
        self.EditDateLabel = QLabel('Дата и время рейса:')
        self.EditDateLabel.setFont(font)
        self.EditDate.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.Date = QVBoxLayout()
        self.Date.addWidget(self.EditDateLabel)
        self.Date.addWidget(self.EditDate)

        # Выбор рейса

        self.FirstCity = QComboBox()
        self.FirstCityLabel = QLabel('Откуда:')
        self.FirstCityLabel.setFont(font)

        for i in server_request.citys():
            self.FirstCity.addItem(i['name'])

        self.FirstCity.currentIndexChanged.connect(self.FillSecondCity)

        self.City1 = QVBoxLayout()
        self.City1.addWidget(self.FirstCityLabel)
        self.City1.addWidget(self.FirstCity)

        self.SecondCity = QComboBox()
        self.SecondCityLabel = QLabel('Куда:')
        self.SecondCityLabel.setFont(font)
        self.City2 = QVBoxLayout()
        self.City2.addWidget(self.SecondCityLabel)
        self.City2.addWidget(self.SecondCity)

        self.Box1 = QHBoxLayout()
        self.Box1.addLayout(self.Cost)
        self.Box1.addLayout(self.Date)

        self.Box2 = QHBoxLayout()
        self.Box2.addLayout(self.City1)
        self.Box2.addLayout(self.City2)

        self.verticalLayout_2.addLayout(self.Title)
        self.verticalLayout_2.addLayout(self.Rocket)
        self.verticalLayout_2.addLayout(self.Box1)
        self.verticalLayout_2.addLayout(self.Box2)

        self.DialogSpacer1 = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(self.DialogSpacer1)

        self.AcceptButton = QPushButton('Создать')
        self.AcceptButton.setStyleSheet('background: #18181c; border: 0px; padding: 10px; border-radius: 15px; color: #fff;')
        self.AcceptButton.setFont(font)
        self.AcceptButton.setDisabled(True)
        self.verticalLayout_2.addWidget(self.AcceptButton)

        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flags)
        
        self.AcceptButton.clicked.connect(self.CreateNew)
        self.EditTitle.textChanged.connect(self.UpdateButton)
        self.EditCost.valueChanged.connect(self.UpdateButton)
        self.EditDate.dateTimeChanged.connect(self.UpdateButton)
        self.SecondCity.currentTextChanged.connect(self.UpdateButton)

        self.UpdateButton()
        self.FillSecondCity()

    def CloseWindow(self):
        self.close()

    def CreateNew(self):
        date_time = self.EditDate.dateTime().toPyDateTime().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        print(date_time)
        server_request.add_flight(self.EditTitle.text(), server_request.get_id_by_name('Rockets', self.EditRocket.currentText()), self.EditCost.value(), date_time, server_request.get_id_by_name('Citys', self.FirstCity.currentText()), server_request.get_id_by_name('Citys', self.SecondCity.currentText()))
        self.CloseWindow()

    def UpdateButton(self):
        if self.EditTitle.text().replace(' ', ''):
            Title = True
            self.EditTitleLabel.setStyleSheet('color: #fff;')
        else:
            Title = False
            self.EditTitleLabel.setStyleSheet('color: red;')

        if self.EditCost.value() != 0:
            Cost = True
            self.EditCostLabel.setStyleSheet('color: #fff;')
        else:
            Cost = False
            self.EditCostLabel.setStyleSheet('color: red;')

        if self.EditDate.dateTime() > datetime.now():
            Time = True
            self.EditDateLabel.setStyleSheet('color: #fff;')
        else: 
            Time = False
            self.EditDateLabel.setStyleSheet('color: red;')
        
        if self.SecondCity.count() != 0:
            City = True
            self.SecondCityLabel.setStyleSheet('color: #fff;')
        else:
            City = False
            self.SecondCityLabel.setStyleSheet('color: red;')

        if Title and Cost and Time and City:
            self.AcceptButton.setDisabled(False)
        else:
            self.AcceptButton.setDisabled(True)

    def MoveWindow(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.clickPosition)
            self.clickPosition = event.globalPos()
            event.accept()
        super(CreationDialogGUI, self).mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.clickPosition = event.globalPos()
        super(CreationDialogGUI, self).mousePressEvent(event)

    def FillSecondCity(self):
        all_cities = server_request.citys_without_this(self.FirstCity.currentText())

        if self.SecondCity.count():
            self.SecondCity.clear()

        for i in all_cities:
            self.SecondCity.addItem(i['name'])