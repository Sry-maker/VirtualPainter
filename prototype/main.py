from PyQt5.QtWidgets import QApplication
import sys
from mainwindow import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
