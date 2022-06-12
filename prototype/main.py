from PyQt5.QtWidgets import QApplication
import sys
from mainwindow import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("mycss.css",encoding='UTF-8') as f:
        qss = f.read()
        app.setStyleSheet(qss)
    w = MainWindow()
    sys.exit(app.exec_())
