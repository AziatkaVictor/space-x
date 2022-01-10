from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
# from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import QtCore
from . import server_request
import ui.main_app as main_ui

class LoginApplicationGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/data/login.ui', self)

        self.ButtonClose.clicked.connect(self.CloseWindow)
        self.ButtonLogin.clicked.connect(self.Login)

        self.NavBar.mouseMoveEvent = self.MoveWindow
        self.NavBar_Title.mouseMoveEvent = self.MoveWindow

        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flags)

    def CloseWindow(self):
        self.close()

    def AuthClient(self, login):
        self.SecondWindow = main_ui.MainApplicationGUI()
        self.hide()
        self.SecondWindow.show()
        self.SecondWindow.SetUser(login)

    def Login(self):
        login = self.Username.text()
        password = self.Password.text()

        # FIXME Пофиксить на тип bool

        result = server_request.user_auth(login, password)
        print(result)

        if result is True:
            self.AuthClient(login)
        else:
            self.ErrorLabel.setText('Username or Password is incorrect!')

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
