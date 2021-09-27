from PyQt5.QtWidgets import QApplication
import ui.login_app as login_ui


def main():
  import sys
  app = QApplication(sys.argv)
  GUI = login_ui.LoginApplicationGUI()
  GUI.show()

  try:
    sys.exit(app.exec_())
  except SystemExit:
    print('Close...')

if __name__ == '__main__':
  main()