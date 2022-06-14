from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QFont, QBrush, QColor
from PyQt5.QtCore import Qt



class SubscribeItem(QWidget):
    def __init__(self, parent):
        super(SubscribeItem, self).__init__()
        self.parent=parent
        self.topic=parent.topic
        self.subscribe_edit = parent.subscribe_edit
        self.subscribe_list = parent.subscribe_list
        self.subscribe_items = parent.subscribe_items
        self.update_info_list = lambda: parent.update_info_list()
        self.isMuted = False
        self.title = QLabel(self.subscribe_edit.currentText())
        self.num = QLabel('0')
        self.mute_btn = QPushButton('屏蔽')
        self.unsubscribe_btn = QPushButton('取消订阅')
        self.choose_btn=QPushButton("选择")
        self.init_ui()
        self.unsubscribe_btn.clicked.connect(lambda: self.clicked_unsubscribe_btn(self.title.text()))
        self.mute_btn.clicked.connect(lambda: self.clicked_mute_btn(self.title.text()))
        self.choose_btn.clicked.connect(lambda: self.clicked_choose_btn(self.title.text()))

    def init_ui(self):
        font = QFont()
        font.setBold(QFont.Black)
        self.title.setFont(font)
        self.num.setFixedSize(50, 20)
        self.num.setAlignment(Qt.AlignCenter)
        self.num.setStyleSheet('border-radius: 8px; background-color: gray')
        title_layout = QHBoxLayout()
        title_layout.addWidget(self.title, 0, Qt.AlignLeft)
        title_layout.addWidget(self.num, 0, Qt.AlignRight)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.mute_btn)
        btn_layout.addWidget(self.unsubscribe_btn)
        btn_layout.addWidget(self.choose_btn)
        layout = QVBoxLayout()
        layout.addLayout(title_layout)
        layout.addStretch()
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def clicked_unsubscribe_btn(self, name):
        for i in range(0, self.subscribe_list.count()):
            if self.subscribe_list.item(i).whatsThis() == name:
                self.subscribe_list.takeItem(i)
                break
        for i in range(0, self.subscribe_edit.count()):
            if self.subscribe_edit.itemText(i) == name:
                self.subscribe_edit.removeItem(i)
                break
        del self.subscribe_items[name]
        self.update_info_list()

    def clicked_mute_btn(self, name):
        for i in range(0, self.subscribe_list.count()):
            if self.subscribe_list.item(i).whatsThis() == name:
                if self.isMuted:
                    self.mute_btn.setText('屏蔽')
                    self.subscribe_list.item(i).setBackground(QBrush(QColor(0, 0, 0, 0)))
                    self.isMuted = False
                else:
                    self.mute_btn.setText('恢复')
                    self.subscribe_list.item(i).setBackground(QBrush(QColor(0, 0, 0, 210)))
                    self.isMuted = True
                break

    def clicked_choose_btn(self,name):
        self.topic=name
        self.parent.topic=name



    def inc(self):
        num = int(self.num.text())
        num = num+1
        self.num.setText(str(num))
