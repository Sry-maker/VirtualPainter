#-*- coding:utf-8 -*-
import sys
import tkinter as tk
from tkinter import filedialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from paho.mqtt import client as mqtt_client
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QComboBox, QFrame, QTextEdit, QLabel, QListWidget, QListWidgetItem, QAbstractItemView
from PyQt5.QtGui import QIcon, QFont, QPixmap, QMovie
from PyQt5.QtCore import Qt, QSize, QPoint
from enum import Enum
from threading import Thread
from setting import Setting

class ConnectState(Enum):
    connected = 0
    connecting = 1
    disconnected = 2


import configparser
import paho.mqtt.client as mqtt

'''
class MqttService:
    """
    on_connect_func:连接MQTT回调函数,订阅主题时触发
    """

    def __init__(self, on_connect_func=None):
        self.config = configparser.ConfigParser()
        self.host = None
        self.port = 1883
        self.keepalive = 60
        self.name = None
        self.pwd = None
        self.mqtt_info = None
        self.InitMqtt(on_connect_func)

    """
    初始化MQTT配置信息
    """

    def InitMqtt(self, on_connect_func=None):
        self.config.read("mqttConfig.ini", encoding="gbk")
        self.host = self.config.get("MqttInfo", "Host")
        self.port = self.config.get("MqttInfo", "Port")
        self.keepalive = self.config.get("MqttInfo", "Keepalive")
        self.name = self.config.get("MqttInfo", "Name")
        self.pwd = self.config.get("MqttInfo", "Pwd")
        self.mqtt_info = mqtt.Client(protocol=3)
        self.mqtt_info.on_connect = on_connect_func
        self.mqtt_info.username_pw_set(self.name, self.pwd)
        self.mqtt_info.connect(host=self.host, port=int(self.port), keepalive=int(self.keepalive))

    """
    发布消息
    topic:主题
    payload:发布的数据
    qos:模式
    """

    def MqttPublish(self, topic=None, payload=None, qos=1):
        if topic is None or payload is None:
            return None
        self.mqtt_info.publish(topic=topic, payload=payload, qos=qos)

    """
    订阅消息
    topic:主题
    qos:模式
    msg_func:接收数据回调
    on_subscribe_func:订阅回调
    """

    def MqttSubscribe(self, topic=None, qos=1, msg_func=None, on_subscribe_func=None):
        if topic is None:
            return None
        self.mqtt_info.subscribe(topic, qos)
        self.mqtt_info.on_message = msg_func
        self.mqtt_info.on_subscribe = on_subscribe_func
        self.mqtt_info.loop_forever()

def mqttmessage(client, userdata, msg):
    print("订阅的数据:" + msg.payload.decode('utf-8'))

def mqttconnect(client, userdata, flags, rc):
    print("连接成功：" + str(rc))

def mqttsubscribe(client, userdata, mid, granted_qos):
    print("消息订阅成功")

if __name__ == '__main__':
    mqtt = MqttService(on_connect_func=mqttconnect)
    mqtt.MqttPublish(topic="paint",payload="这是python发送的一条测试数据",qos=1)

    mqtt1 = MqttService(on_connect_func=mqttconnect)
    # print(res)
    mqtt1.MqttSubscribe(topic="paint", qos=1, msg_func=mqttmessage, on_subscribe_func=mqttsubscribe)
'''
class Publish():
    client1 = mqtt_client.Client()
    def __init__(self):

        # 连接信息，会根据设置界面的输入更新
        self.connect_info = {'address': '47.100.X.X', 'port': '1883', 'username': '', 'password': ''}

        self.connect()


    def click_connect_btn(self):
        self.connect()

    def click_disconnect_btn(self):
        # disconnected,这里需要取消连接
        global connect_state
        connect_state = ConnectState.disconnected

    def on_disconnect(client,userdata,rc):
        if rc==0:
            print("disconnect")

    def click_cancel_btn(self):
        self.connect_state = ConnectState.disconnected

    def click_publish_btn(self,topic,msg):
        print("publish")
        self.client1.publish(topic, msg, 1)

    def connect(self):
        self.connect_state = ConnectState.connecting
        thread = Thread(target=self.repeat_connect)
        thread.start()

    def repeat_connect(self):
        while self.connect_state == ConnectState.connecting:
            # 下面这句话替换成根据connect_info进行连接，若连接成功则state为connected
            # 连接后需要有一个线程更新data和subscribe_item，subscribe_item有inc接口用于处理数据数量加一
            client = self.connect_mqtt()
            client.loop_start()
            self.client1 = client
            self.connect_state = ConnectState.connected



    def connect_mqtt(self):
        print('connect_mqtt')
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(self.connect_info['username'])
        client.on_connect = on_connect
        client.connect(self.connect_info['address'], int(self.connect_info['port']))
        return client


if __name__ == '__main__':
    w = Publish()
    w.click_connect_btn()
    while 1:
        w.click_publish_btn("1","msg")
