from datetime import datetime
import requests
from PyQt5.QtGui import QImage


def AttributesToText(data):
    if len(data):
        text = ''
        for item in data:
            if text != '':
                text = text + '<br>'

            text = text + item['title'] + ': <font color=#cacdcf>' + item['text'] + '</font>'

        return text
    else:
        return 'Ошибка'

def ConvertTime(data):
    try:
        date_and_time = datetime.strptime(data.replace('T', ' '), "%Y-%m-%d %H:%M:%S")
        date_and_time = date_and_time.strftime("%d.%m.%Y %H:%M")
    except ValueError:
        date_and_time = str(data)

    return date_and_time

def ConvertTimeForEdit(data):
    return datetime.strptime(data.replace('T', ' '), "%Y-%m-%d %H:%M:%S")

def DownloadAllImg(urls):
    if len(urls):
        data = {}

        for url in urls:
            image = QImage()
            image.loadFromData(requests.get(url['url']).content)
            data[str(url['url'])] = image
        
        return data
    else:
        return 'Ошибка'


