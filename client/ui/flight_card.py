from datetime import datetime
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtWidgets import QWidget
from . import server_request
from . import dialogs
import requests


class FlightsCardGUI(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/data/flight_card.ui', self)

    def SetData(self, item):
        rocket = server_request.rocket_by_id(item['rocket'])
        start_city = server_request.citys_by_id(item['first_city'])
        end_city = server_request.citys_by_id(item['second_city'])

        try:
            date_and_time = datetime.strptime(item['date_and_time'].replace('T', ' '), "%Y-%m-%d %H:%M:%S")
            date_and_time = str(date_and_time.strftime("%d.%m.%Y %H:%M"))
        except ValueError:
            date_and_time = str(item['date_and_time'])

        data_text = 'Ракета: <font color=#cacdcf>' + str(rocket['name']) + '</font><br>Рейс: <font color=#cacdcf>' + str(start_city['name']) + ' - ' + str(end_city['name']) + '</font><br>Дата: <font color=#cacdcf>' + date_and_time + '</font><br>Цена билета: <font color=#cacdcf>' + str(item['cost'])
        self.title.setText(str(item['name']))
        self.text.setText(data_text)

        image = QImage()
        image.loadFromData(requests.get(rocket['img']).content)

        data_img = QPixmap(image).scaled(128, 128, QtCore.Qt.KeepAspectRatioByExpanding)

        self.img.setPixmap(data_img)
        self.img.setAlignment(QtCore.Qt.AlignCenter)

    def AddButtons(self, item):
        self.edit_button.clicked.connect(lambda checked, arg=['edit', item]: self.FlightsButton(arg))
        self.delete_button.clicked.connect(lambda checked, arg=['delete', item]: self.FlightsButton(arg))

    def FlightsButton(self, arg):
        type = arg[0]
        data = arg[1]

        if type.lower() == 'edit':
            dialog = dialogs.FlightsDialogGUI()
            dialog.SetType(type, data)
            dialog.show()

        elif type.lower() == 'delete':
            dialog = dialogs.DeleteDialogGUI()
            dialog.SetItem(data['id'], data['name'])
            print(data)
            dialog.show()
