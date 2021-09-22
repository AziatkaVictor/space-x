from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import QtCore

class LoginApplicationGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/data/login.ui', self)

        self.Background.setPixmap(QPixmap("ui/img/login-background.png"))
        self.Logo.setPixmap(QPixmap("ui/img/Logo.png"))
        self.ButtonClose.setIcon(QIcon("ui/img/close-icon.png"))

        self.ButtonClose.clicked.connect(self.CloseWindow)

        self.NavBar.mouseMoveEvent = self.MoveWindow
        self.NavBar_Title.mouseMoveEvent = self.MoveWindow

        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flags)

    def CloseWindow(self):
        self.close()

    def MoveWindow(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.clickPosition)
            self.clickPosition = event.globalPos()
            event.accept()
        super(LoginApplicationGUI, self).mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.clickPosition = event.globalPos()
        super(LoginApplicationGUI, self).mousePressEvent(event)
