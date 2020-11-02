import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui, QtCore, Qt
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import Adafruit_DHT
import RPi.GPIO as GPIO
import time


def sensor():
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, '4')
    return humidity, temperature


form_class = uic.loadUiType("first.ui")[0]


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.resize(640,480)
        self.humilabel.setFont(QFont('Arial', 25))
        self.templabel.setFont(QFont('Arial', 25))
        self.stufflabel.setFont(QFont('Arial', 15))
        self.initBG()

        self.humipic.setPixmap(QtGui.QPixmap("hu3.png"))
        self.temppic.setPixmap(QtGui.QPixmap("temp.png"))
        self.contpic.setPixmap(QtGui.QPixmap("control.png"))

        self.humipic.setGeometry(QtCore.QRect(140,40,120,120))
        self.temppic.setGeometry(QtCore.QRect(110,171,120,120))
        self.contpic.setGeometry(QtCore.QRect(130,320,120,120))

        self.timevar = QTimer(self)


        self.timevar.start(3000)
        self.timevar.timeout.connect(self.csv_download)
        self.timevar.timeout.connect(self.get_sensor_data)
#        self.pushButton.clicked.connect(self.get_sensor_data)

    def initBG(self):
        self.setStyleSheet("background-image: url(white.jpeg);")
        self.show()
    def get_sensor_data(self):
        #while True:
        humidity , temp = sensor()
#        print(get_sensor)
        self.humilabel.setText(str(humidity)+" %")
        self.templabel.setText(str(temp) + " °C")
        print("changed")
            #time.sleep(40)
    def csv_download(self):
        fname = 'control.csv'
        fh = open(fname)
        #stuff = list()
        #hard = list()
        #wanna_temp = list()
        for line in fh:
            print(line)
            stuff=""
            hard=""
            wanna_temp = ''
            pis = line.split(',')
            stuff1 = pis[0]
            hard1 = pis[1]
            wanna_temp1 = pis[2]

            stuff = stuff1
            hard = hard1
            wanna_temp=wanna_temp1
            self.stufflabel.setText(str('\n' + '제어가전 : '+stuff+'\n'+'출력 : '+ hard +'\n'+'온도 : ' + wanna_temp + '\n'))
            print('change')
app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()
