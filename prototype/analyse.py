import json

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QLabel,  QComboBox, QPushButton, QHBoxLayout, QVBoxLayout

from threading import Thread

from PIL import Image
import cv2

import HandTrackingModule as htm
import os
import numpy as np

from publish import Publish


def AiVirtualPainter(parent):
    folderPath = "PainterImg/"
    mylist = os.listdir(folderPath)
    overlayList = []
    for imPath in mylist:
        image = cv2.imread(f'{folderPath}/{imPath}')
        overlayList.append(image)
    header = overlayList[0]
    color = [255, 0, 0]
    brushThickness = 15
    eraserThickness = 60

    cap = cv2.VideoCapture(0)  # 若使用笔记本自带摄像头则编号为0  若使用外接摄像头 则更改为1或其他编号
    cap.set(3, 1280)
    cap.set(4, 720)
    # cap.set(3, 800)
    # cap.set(4, 500)
    detector = htm.handDetector()
    xp, yp = 0, 0
    # imgCanvas = np.zeros((720, 1280, 3), np.uint8)  # 新建一个画板
    # imgCanvas = np.zeros((500, 800, 3), np.uint8)  # 新建一个画板
    while True:
        # 1.import image
        success, img = cap.read()
        img = cv2.flip(img, 1)  # 翻转

        # 2.find hand landmarks
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=True)

        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]

            # 3. Check which fingers are up
            fingers = detector.fingersUp()

            # 4. If Selection Mode – Two finger are up
            if fingers[1] and fingers[2]:
                if y1 < 153:
                    if 0 < x1 < 320:
                        header = overlayList[0]
                        color = [50, 128, 250]
                    elif 320 < x1 < 640:
                        header = overlayList[1]
                        color = [0, 0, 255]
                    elif 640 < x1 < 960:
                        header = overlayList[2]
                        color = [0, 255, 0]
                    elif 960 < x1 < 1280:
                        header = overlayList[3]
                        color = [0, 0, 0]
            img[0:1280][0:153] = header

            # 5. If Drawing Mode – Index finger is up
            if fingers[1] and fingers[2] == False:
                cv2.circle(img, (x1, y1), 15, color, cv2.FILLED)
                print("Drawing Mode")
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

                if color == [0, 0, 0]:
                    cv2.line(img, (xp, yp), (x1, y1), color, eraserThickness)  # ??
                    cv2.line(parent.imgCanvas, (xp, yp), (x1, y1), color, eraserThickness)
                else:
                    cv2.line(img, (xp, yp), (x1, y1), color, brushThickness)   # ??
                    cv2.line(parent.imgCanvas, (xp, yp), (x1, y1), color, brushThickness)

            xp, yp = x1, y1
            # Clear Canvas when all fingers are up
            # if all (x >= 1 for x in fingers):
            #     imgCanvas = np.zeros((720, 1280, 3), np.uint8)

        # 实时显示画笔轨迹的实现
        imgGray = cv2.cvtColor(parent.imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        # cv2.imwrite('C:\\Users\\Lenovo\\Desktop\\t\\a.jpg', imgInv)
        img = cv2.bitwise_and(img, imgInv)
        # cv2.imwrite('C:\\Users\\Lenovo\\Desktop\\t\\b.jpg', img)
        img = cv2.bitwise_or(img, parent.imgCanvas)
        chuanshuimg=cv2.bitwise_or(imgInv, parent.imgCanvas)
        parent.chuanshu=chuanshuimg
        a1_dtype = str(parent.chuanshu.dtype)
        a1_shape = str(parent.chuanshu.shape)
        # cv2.imwrite('C:\\Users\\Lenovo\\Desktop\\t\\d.jpg', chuanshuimg)
        img[0:1280][0:153] = header


        # cv2.imshow("Image", img)
        # cv2.imshow("Canvas", imgCanvas)
        # cv2.imshow("Inv", imgInv)
        # pyqt5界面更新
        if 1:
            height,width,bytesPerComponent = img.shape
            bytesPerLine = bytesPerComponent * width
            qImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # opencv读取的bgr格式图片转换成rgb格式

            qImg = QtGui.QImage(qImg.data,width, height, bytesPerLine,
                                  QtGui.QImage.Format_RGB888)  # pyqt5转换成自己能放的图片格式
            jpg_out = QtGui.QPixmap(qImg)  # 设置图片大小
            parent.imgLabel.setPixmap(jpg_out)  # 设置图片显示



class Analyse(QWidget):
    def __init__(self,parent):
        super(Analyse, self).__init__()
        self.parent=parent
        self.a = 0
        self.b = None
        self.init_ui()
        self.init_slot()
        self.update_paint()
        self.imgCanvas = np.zeros((720, 1280, 3), np.uint8)  # 新建一个画板
        self.chuanshu = np.zeros((720, 1280, 3), np.uint8)
        self.hebing = np.zeros((720, 1280, 3), np.uint8)
        # 发送端连接
        self.publish = Publish()
        self.publish.click_connect_btn()

    def init_ui(self):
        control_layout = QHBoxLayout()
        layout = QVBoxLayout()
        self.imgLabel = QLabel()
        control_layout.addWidget(self.imgLabel)
        self.publish_btn = QPushButton('发送')
        self.merge_btn=QPushButton("合并")
        control_layout.addWidget(self.publish_btn)
        control_layout.addWidget(self.merge_btn)
        layout.addLayout(control_layout)
        self.setLayout(layout)
        self.publish_btn.setFixedSize(25,25)
        self.merge_btn.setFixedSize(25,25)



    def init_slot(self):
        self.publish_btn.clicked.connect(self.send_paint)
        self.merge_btn.clicked.connect(self.merge)

    def update_paint(self):
        thread = Thread(target=AiVirtualPainter,args=(self,))
        thread.start()

    # 发送到paint主题下
    def send_paint(self):
        topic=self.parent.topic
        print("topic analysis"+topic)
        self.publish.click_publish_btn(topic, (self.imgCanvas.tobytes()))
    def merge(self):
        tempname = self.parent.topic + "new.jpg"
        image = Image.open(tempname)  # 用PIL中的Image.open打开图像
        image_arr = np.array(image)  # 转化成numpy数组
        self.hebing=image_arr
        self.imgCanvas = cv2.bitwise_or(self.hebing, self.imgCanvas)
        # cv2.imwrite('imgCanvas.jpg',self.imgCanvas)
        print("hebing")

    # 接收到
    def receive_paint(self, imgCanvas):
        print("test")
        # tempname = self.topic + "new.jpg"
        # image = Image.open(tempname)  # 用PIL中的Image.open打开图像
        # image_arr = np.array(image)  # 转化成numpy数组
        # self.hebing=image_arr
        # self.hebing=np.frombuffer(imgCanvas, dtype=getattr(np, 'uint8')).reshape(eval('(720, 1280, 3)'))

        # self.imgCanvas = cv2.bitwise_or(self.imgCanvas, imgCanvas)
