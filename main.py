import sys

from PyQt5.QtWidgets import QApplication

from menu import MainMenu

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainMenu()
    sys.exit(app.exec_())
