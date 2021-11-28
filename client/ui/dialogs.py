from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QCheckBox, QSpinBox, QDateTimeEdit, QHBoxLayout, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QPushButton, QAbstractSpinBox
from ui.server_request import rockets, citys

class CreationDialogGUI(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/data/dialog.ui', self)

        self.ButtonClose.clicked.connect(self.CloseWindow)

        self.NavBar.mouseMoveEvent = self.MoveWindow
        self.NavBar_Title.mouseMoveEvent = self.MoveWindow

        font = QFont()
        font.setFamily(u'Montserrat Light')
        font.setPointSize(12)

        # Название

        self.EditTitle = QLineEdit()
        self.EditTitleLabel = QLabel('Название рейса:')
        self.EditTitleLabel.setFont(font)
        self.Title = QVBoxLayout()
        self.Title.addWidget(self.EditTitleLabel)
        self.Title.addWidget(self.EditTitle)

        # Выбор ракеты

        self.EditRocket = QComboBox()

        for i in rockets():
            self.EditRocket.addItem(i[1])

        self.EditRocket.addItem
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

        for i in citys():
            self.FirstCity.addItem(i[1])

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
        #accept.clicked.connect(lambda checked, arg=[item, 'edit']: self.FlightsButton(arg))
        self.AcceptButton.setStyleSheet('background: #18181c; border: 0px; padding: 10px; border-radius: 15px; color: #fff;')
        self.AcceptButton.setFont(font)
        self.verticalLayout_2.addWidget(self.AcceptButton)

        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flags)

    def CloseWindow(self):
        self.close()

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
        first_city = self.FirstCity.currentText()

        if self.SecondCity.count() is not 0:
            self.SecondCity.clear()

        # TODO Заменить индекс у массива на название поля

        for i in citys():
            if i[1].lower() != first_city.lower():
                self.SecondCity.addItem(i[1])



