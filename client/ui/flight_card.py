from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtWidgets import QWidget
from . import server_request
import requests


class FlightsCardGUI(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/data/flight_card.ui', self)

    def SetData(self, item):
        rocket = server_request.rocket_by_id(item['rocket'])
        start_city = server_request.citys_by_id(item['first_city'])
        end_city = server_request.citys_by_id(item['second_city'])

        data_text = 'Ракета: <font color=#cacdcf>' + str(rocket['name']) + '</font><br>Рейс: <font color=#cacdcf>' + str(start_city['name']) + ' - ' + str(end_city['name']) + '</font><br>Дата: <font color=#cacdcf>' + str(item['date_and_time']) + '</font><br>Цена билета: <font color=#cacdcf>' + str(item['cost'])
        self.title.setText(str(item['name']))
        self.text.setText(data_text)

        image = QImage()
        image.loadFromData(requests.get(rocket['img']).content)

        data_img = QPixmap(image).scaled(128, 128, QtCore.Qt.KeepAspectRatioByExpanding)

        self.img.setPixmap(data_img)
        self.img.setAlignment(QtCore.Qt.AlignCenter)

    def AddButtons(self, item):
        self.edit_button.clicked.connect(lambda checked, arg=[item, 'edit']: self.FlightsButton(arg))
        self.delete_button.clicked.connect(lambda checked, arg=[item, 'delete']: self.FlightsButton(arg))

    def FlightsButton(self, arg):
        data = arg[0]
        type = arg[1]

        if type.lower() == 'edit':
            print(data)
        elif type.lower() == 'delete':
            print(data)