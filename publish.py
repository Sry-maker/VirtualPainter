#-*- coding:utf-8 -*-
import sys
from threading import Thread
import random
import time

from paho.mqtt import client as mqtt_client

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


def message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

class mqtt():
    def __init__(self,topic = "/python/mqtt",on_message = message):
        self.__broker = '47.100.197.182'
        self.__port = 1883
        self.topic = topic
        # generate client ID with pub prefix randomly
        self.__subscribe_id = f'python-mqtt-{random.randint(0, 1000)}'
        self.__publish_id = f'python-mqtt-{random.randint(1000, 2000)}'
        thread1 = Thread(target=self.__init_subscribe)
        thread1.start()
        self.__on_message = on_message

    def __connect_mqtt(self,id):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                None
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(id)
        client.on_connect = on_connect
        client.connect(self.__broker, self.__port)
        return client



    def __publish(self,client):
        time.sleep(1)
        msg = f"messages: {1}"
        result = client.publish(self.topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{self.topic}`")
        else:
            print(f"Failed to send message to topic {self.topic}")


    def __subscribe(self,client: mqtt_client):
        client.subscribe(self.topic)
        client.on_message = self.__on_message

    def __init_subscribe(self):
        client = self.__connect_mqtt(self.__subscribe_id)
        self.__subscribe(client)
        client.loop_forever()

    def init_publish(self):
        client = self.__connect_mqtt(self.__publish_id)
        client.loop_start()
        self.__publish(client)




if __name__ == '__main__':
    w = mqtt()
    w.init_publish()
