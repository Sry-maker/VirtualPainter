from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QComboBox, QFrame, QTextEdit, QLabel, QListWidget, QListWidgetItem, QAbstractItemView
from PyQt5.QtGui import QIcon, QFont, QPixmap, QMovie, QTextDocumentFragment
from PyQt5.QtCore import Qt, QSize, QPoint
from enum import Enum
from threading import Thread
import json
from paho.mqtt.subscribeoptions import SubscribeOptions

from setting import Setting
from subscribe_item import SubscribeItem
from paho.mqtt import client as mqtt_client
import time

class ConnectState(Enum):
    connected = 0
    connecting = 1
    disconnected = 2


connect_state = ConnectState.disconnected

class Subscribe(QWidget):
    def __init__(self,parent):
        super(Subscribe, self).__init__()
        self.parent = parent
        # 连接信息，会根据设置界面的输入更新
        self.connect_info = {'address': '0', 'port': 60, 'username': '123', 'password': ''}
        # 订阅获取的信息
        self.data = {'123': ['2', '4', '5'], 'test': ['a', 'b', 'c']}
        # 每个订阅物品的界面
        self.subscribe_items = {}
        self.client = None
        self.connect_btn = QPushButton('连接')
        self.disconnect_btn = QPushButton('断开')
        self.cancel_btn = QPushButton('取消')
        self.loading = QLabel()
        self.setting_btn = QPushButton("设置")
        self.setting_widget = Setting(self.connect_info)
        self.light = QLabel()
        self.subscribe_edit = QComboBox()
        self.subscribe_btn = QPushButton('订阅')
        self.subscribe_list = QListWidget()
        self.info_display_title = QLabel('图片显示')
        self.info_display_id = QLabel('')
        self.info_display = QTextEdit()
        self.init_ui()
        self.init_slot()

    def init_ui(self):
        # self.setting_btn.setFixedSize(25, 25)
        self.setting_btn.setFlat(True)
        # self.setting_btn.setIcon(QIcon('pic/setting.png'))
        # self.setting_btn.setStyleSheet('QPushButton{border:none;} '
        #                                'QPushButton:hover{background-color: rgb(224,224,224);}')
        # self.setting_btn.setText("设置")

        self.disconnect_btn.setEnabled(False)

        self.cancel_btn.setVisible(False)
        movie = QMovie('pic/loading.gif')
        movie.start()
        self.loading.setMovie(movie)
        self.loading.setVisible(False)
        self.light.setFixedSize(25, 25)
        self.light.setPixmap(QPixmap('pic/red.png'))

        self.subscribe_edit.setFixedWidth(300)
        self.subscribe_edit.setEditable(True)
        self.subscribe_edit.setEnabled(False)
        self.subscribe_btn.setEnabled(False)
        horizontal_line = QFrame(self)
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Plain)
        vertical_line = QFrame(self)
        vertical_line.setFrameShape(QFrame.VLine)
        vertical_line.setFrameShadow(QFrame.Plain)
        self.subscribe_list.setFixedWidth(400)
        self.subscribe_list.setStyleSheet('background-color:transparent;border:none')
        self.subscribe_list.setSelectionMode(QAbstractItemView.MultiSelection)
        self.subscribe_list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.info_list.setFixedHeight(300)
        # self.info_list.setStyleSheet('background-color:transparent; border:none')
        # self.info_list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        font = QFont()
        font.setBold(QFont.Black)
        self.info_display_title.setFont(font)
        self.info_display_id.setFixedSize(50, 20)
        self.info_display_id.setAlignment(Qt.AlignCenter)
        self.info_display_id.setStyleSheet('border-radius: 8px; background-color: gray')
        self.info_display.setReadOnly(True)
        self.info_display.setMinimumHeight(200)
        self.info_display.setMinimumWidth(600)
        self.info_display.setStyleSheet('QTextEdit{color: white; background-color: black; border:0px;}')
        info_display_bar = QHBoxLayout()
        info_display_bar.addWidget(self.info_display_title, 0, Qt.AlignLeft)
        info_display_bar.addWidget(self.info_display_id, 0, Qt.AlignRight)
        info_display_layout = QVBoxLayout()
        info_display_layout.addLayout(info_display_bar)
        info_display_layout.addWidget(self.info_display)
        connect_control_layout = QHBoxLayout()
        connect_control_layout.addWidget(self.setting_btn)
        connect_control_layout.addWidget(self.connect_btn)
        connect_control_layout.addWidget(self.disconnect_btn)
        connect_control_layout.addStretch()
        connect_control_layout.addWidget(self.loading)
        connect_control_layout.addWidget(self.cancel_btn)
        connect_control_layout.addWidget(self.light)
        subscribe_control_layout = QHBoxLayout()
        subscribe_control_layout.addWidget(self.subscribe_edit)
        subscribe_control_layout.addWidget(self.subscribe_btn)
        right_layout = QVBoxLayout()
        right_layout.addLayout(connect_control_layout)
        # right_layout.addWidget(self.info_list)
        right_layout.addWidget(horizontal_line)
        right_layout.addLayout(info_display_layout)
        left_layout = QVBoxLayout()
        left_layout.addLayout(subscribe_control_layout)
        left_layout.addWidget(self.subscribe_list)
        layout = QHBoxLayout()
        layout.addLayout(left_layout)
        layout.addWidget(vertical_line, 0, Qt.AlignLeft)
        layout.addLayout(right_layout)
        self.setLayout(layout)
        image="<img src=\"qq.jpg\" "+"width='10px' height=10px'/>"
        self.info_display.insertHtml(image)
        # self.info_display.append("<img src=\"qq.jpg\" />")

    def init_slot(self):
        self.connect_btn.clicked.connect(self.click_connect_btn)
        self.disconnect_btn.clicked.connect(self.click_disconnect_btn)
        self.cancel_btn.clicked.connect(self.click_cancel_btn)
        self.subscribe_btn.clicked.connect(self.click_subscribe_btn)
        self.subscribe_edit.editTextChanged.connect(self.subscribe_edit_changed)
        self.setting_btn.clicked.connect(self.setting_btn_clicked)

    def click_connect_btn(self):
        self.connect_btn.setEnabled(False)
        self.loading.setVisible(True)
        self.cancel_btn.setVisible(True)
        self.connect()

    def click_disconnect_btn(self):
        global connect_state
        connect_state = ConnectState.disconnected
        self.connect_btn.setEnabled(True)
        self.setting_btn.setEnabled(True)
        self.disconnect_btn.setEnabled(False)
        self.light.setPixmap(QPixmap('pic/red.png'))
        self.subscribe_btn.setEnabled(False)
        self.subscribe_edit.clear()
        self.subscribe_edit.clearEditText()
        self.subscribe_edit.setEnabled(False)
        self.subscribe_list.clear()
        self.subscribe_items.clear()

    def click_cancel_btn(self):
        self.connect_btn.setEnabled(True)
        self.setting_btn.setEnabled(True)
        self.loading.setVisible(False)
        global connect_state
        connect_state = ConnectState.disconnected

    def click_subscribe_btn(self):
        name = self.subscribe_edit.currentText()
        self.subscribe_edit.addItem(name)
        self.subscribe_btn.setEnabled(False)
        list_item = QListWidgetItem()
        list_item.setSizeHint(QSize(400, 80))
        list_item.setWhatsThis(name)
        self.subscribe_list.addItem(list_item)
        self.subscribe_items[name] = SubscribeItem(parent=self)
        self.subscribe_list.setItemWidget(list_item, self.subscribe_items[name])

    def subscribe_edit_changed(self):
        self.subscribe_btn.setEnabled(False)
        for i in range(0, self.subscribe_edit.count()):
            if self.subscribe_edit.currentText() == self.subscribe_edit.itemText(i):
                return
        if self.subscribe_edit.currentText() != '':
            self.subscribe_btn.setEnabled(True)

    def connect(self):
        global connect_state
        connect_state = ConnectState.connecting
        self.loading.setVisible(True)
        self.cancel_btn.setVisible(True)
        thread = Thread(target=self.repeat_connect)
        thread.start()

    def repeat_connect(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                global connect_state
                connect_state = ConnectState.connected # 连接成功则state为connected
            else:
                print("Failed to connect, return code %d\n", rc)
       
        # 读取到数据!!
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload}` from `{msg.topic}` topic")
            if not self.subscribe_items[msg.topic].isMuted:
                if msg.topic in self.data.keys():
                    self.data[msg.topic].append(msg.payload.decode('utf-16'))
                else:
                    self.data[msg.topic]=[msg.payload.decode('utf-16')]
                self.subscribe_items[msg.topic].inc()
                imgCanvas = bytes(msg.payload)
                self.parent.analyse.receive_paint(imgCanvas)



        client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        self.client = mqtt_client.Client(client_id)  # ClientId不能重复，所以使用当前时间
        self.client.username_pw_set(self.connect_info['username'], self.connect_info['password'])  # 必须设置，否则会返回「Connected with result code 4」
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.connect(self.connect_info['address'],self.connect_info['port'] , 60)
        self.client.loop_start() # 另开线程，避免阻塞
        # 开始连接
        global connect_state
        while connect_state == ConnectState.connecting:
            print("wait")
            if connect_state == ConnectState.disconnected:
                print('disconnect.................')
                self.client.disconnect()
                # loop_stop() 不能写在on_disconnect 回调里, 否则 threading.current_thread() == client._thread，\
                # 客户端无法清除client._thread 子进程，以后再使用loop_start()就无效了
                self.client.loop_stop()
            elif connect_state == ConnectState.connected:
                self.light.setPixmap(QPixmap('pic/green.png'))
                self.disconnect_btn.setEnabled(True)
                self.subscribe_edit.setEnabled(True)
                self.cancel_btn.setVisible(False)
                self.loading.setVisible(False)
                self.setting_btn.setEnabled(False)
        # 持续连接获取消息
        while True:
            #print('state: ', self.client._state, 'loop进程：', self.client._thread)
            if self.client._state != 2:
                # 订阅消息
                subscribe_source = list(zip(list(self.subscribe_items.keys()),[0]*len(self.subscribe_items)))
                self.client.subscribe(subscribe_source) # 消息都在自定义的on_message函数中得到
                if connect_state == ConnectState.disconnected:
                    print('disconnect.................')
                    self.client.disconnect()
                    # loop_stop() 不能写在on_disconnect 回调里, 否则 threading.current_thread() == client._thread，\
                    # 客户端无法清除client._thread 子进程，以后再使用loop_start()就无效了
                    self.client.loop_stop()
            else:
                if connect_state != ConnectState.disconnected:
                    print('尝试重连')
                    self.client.reconnect()  # 必须重连将 client._state 从断开状态切换为初始化状态
                    self.client.loop_start()
                else:
                    print('\n客户端已断开,')
                return
            time.sleep(1)



    def update_info_display(self):
        selected_info = self.info_list.selectedItems()
        if len(selected_info) == 0:
            self.info_display_title.setText('')
            self.info_display_id.setText('')
            self.info_display.setText('')
        else:
            what_list = selected_info[0].whatsThis().split()
            name = what_list[0]
            identity = what_list[len(what_list)-1]
            self.info_display_title.setText(name)
            self.info_display_id.setText(identity)
            self.info_display.setText(self.data[name][int(identity)])

    def setting_btn_clicked(self):
        self.setting_widget.move(self.mapToGlobal(QPoint(420, 100)))
        self.setting_widget.show()
