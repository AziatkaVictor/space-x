from datetime import datetime
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtWidgets import QWidget
from . import server_request
from . import dialogs
from . import functions
import requests


class FlightsCardGUI(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/data/flight_card.ui', self)

    def SetData(self, item):
        TextData = [
            {
                'title' : 'Ракета',
                'text' : str(server_request.rocket_by_id(item['rocket'])['name'])
            },
            {
                'title' : 'Рейс',
                'text' : str(server_request.citys_by_id(item['first_city'])['name']) + ' - ' + str(server_request.citys_by_id(item['second_city'])['name'])
            },
            {
                'title' : 'Дата',
                'text' : functions.ConvertTime(item['date_and_time'])
            },
            {
                'title' : 'Цена билета',
                'text' : str(item['cost'])
            },
            {
                'title' : 'Куплено билетов',
                'text' : str(server_request.get_count_of_atrticles(item['id']))
            },
        ]
        
        self.title.setText(str(item['name']))
        self.text.setText(functions.AttributesToText(TextData))

    def SetOwner(self, owner):
        self.owner = owner

    def SetImage(self, img):
        data_img = QPixmap(img).scaled(self.img.size(), QtCore.Qt.KeepAspectRatioByExpanding)
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
            dialog.SetOwner(self.owner)
            dialog.SetType(type, data)
            dialog.show()

        elif type.lower() == 'delete':
            dialog = dialogs.DeleteDialogGUI()
            dialog.SetOwner(self.owner)
            dialog.SetItem(data['id'], data['name'])
            print(data)
            dialog.show()

class ArticlesCardGUI(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/data/article_card.ui', self)

    def SetOwner(self, owner):
        self.owner = owner

    def SetData(self, item):
        TextData = [
            {
                'title' : 'Рейс',
                'text' : str(server_request.flight_by_id(item['flight'])['name'])
            },
            {
                'title' : 'Статус',
                'text' : str(server_request.status_by_id(item['status'])['name'])
            },
            {
                'title' : 'Дата',
                'text' : functions.ConvertTime(item['date'])
            },
            {
                'title' : 'Документы',
                'text' : item['docs']
            },
        ]

        self.title.setText(str(item['name']))
        self.text.setText(functions.AttributesToText(TextData))

    def AddButtons(self, item):
        self.check_button.clicked.connect(lambda checked, arg=[item]: self.CheckArticle(arg))

    def CheckArticle(self, arg):
        dialog = dialogs.ArticleDialogGUI()
        dialog.SetOwner(self.owner)
        dialog.SetItem(arg[0])
        dialog.show()