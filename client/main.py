import requests
import json
from PyQt5.QtWidgets import QApplication
import ui.login_app as ui

def main():
  import sys
  app = QApplication(sys.argv)
  GUI = ui.LoginApplicationGUI()
  GUI.show()

  try:
    sys.exit(app.exec_())
  except SystemExit:
    print('Close...')


def button_login():
  data = {
    "username": "Admin",
    "password": "Admin"
  }

  r = requests.post('http://127.0.0.1:8000/login/', data=json.dumps(data))
  print(r.text)

if __name__ == '__main__':
  main()