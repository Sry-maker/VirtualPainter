from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt

class Setting(QDialog):
    def __init__(self, info):
        super(Setting, self).__init__()
        self.info = info
        self.address_label = QLabel('地址:')
        self.address_edit = QLineEdit('47.100.197.182')
        self.port_label = QLabel('端口:')
        self.port_edit = QLineEdit('1883')
        self.username_label = QLabel('用户名:')
        self.username_edit = QLineEdit()
        self.password_label = QLabel('密码:')
        self.password_edit = QLineEdit()
        self.ok_btn = QPushButton('确认')
        self.apply_btn = QPushButton('应用')
        self.cancel_btn = QPushButton('取消')
        self.init_ui()
        self.init_solt()
        self.setWindowTitle('设置')
        self.setWindowFlag(Qt.Tool)

    def init_ui(self):
        address_layout = QHBoxLayout()
        address_layout.addWidget(self.address_label)
        address_layout.addStretch()
        address_layout.addWidget(self.address_edit)
        port_layout = QHBoxLayout()
        port_layout.addWidget(self.port_label)
        port_layout.addStretch()
        port_layout.addWidget(self.port_edit)
        username_layout = QHBoxLayout()
        username_layout.addWidget(self.username_label)
        username_layout.addStretch()
        username_layout.addWidget(self.username_edit)
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_label)
        password_layout.addStretch()
        password_layout.addWidget(self.password_edit)
        control_layout = QHBoxLayout()
        control_layout.addStretch()
        control_layout.addWidget(self.cancel_btn)
        control_layout.addWidget(self.apply_btn)
        control_layout.addWidget(self.ok_btn)
        layout = QVBoxLayout()
        layout.addLayout(address_layout)
        layout.addLayout(port_layout)
        layout.addLayout(username_layout)
        layout.addLayout(password_layout)
        layout.addLayout(control_layout)
        self.setLayout(layout)

    def init_solt(self):
        self.cancel_btn.clicked.connect(self.cancel_btn_clicked)
        self.apply_btn.clicked.connect(self.apply_btn_clicked)
        self.ok_btn.clicked.connect(self.ok_btn_clicked)
        return

    def cancel_btn_clicked(self):
        self.close()

    def apply_btn_clicked(self):
        self.info['address'] = self.address_edit.text()
        if len(self.info['address'])==0:
            self.info['address'] = '0'
        try:
            self.info['port'] = int(self.port_edit.text())
        except Exception as e:
            print(e)
            self.info['port'] = 60
        self.info['username'] = self.username_edit.text()
        self.info['password'] = self.password_edit.text()

    def ok_btn_clicked(self):
        self.apply_btn_clicked()
        self.close()
