# -*- coding: utf-8 -*- 
import csv
import socket
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
from datetime import datetime
import subprocess
from glob import glob

sensor = Adafruit_DHT.DHT11
pin = '4'

#subprocess.call(['python', 'makecsv.py'])


#-----video
#file = '~/Desktop/mjpg.sh'
#shellscript = subprocess.Popen([file], stdin=subprocess.PIPE, shell=True)
#
#shellscript.stdin.write('yes\n')
#shellscript.stdin.close()
#returncode = shellscript.wait()
#_--------


#This is for Motion sensor
GPIO.setmode(GPIO.BCM)
PIR_PIN = 7
GPIO.setup(PIR_PIN, GPIO.IN)
#-------------------------

#This is for led control
green = 9
red = 10
blue = 11
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

Freq = 100
RED = GPIO.PWM(red, Freq)
BLUE = GPIO.PWM(blue, Freq)
GREEN = GPIO.PWM(green, Freq)

BLUE.start(0)
RED.start(0)
GREEN.start(0)
GPIO.setwarnings(False)
#-------------------------------------------led control

HOST = ""
PORT = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print('Socket created')
s.bind((HOST, PORT))
print('Socket bind complete')
s.listen(1)
print ('Socket now listening')



#def MOTION(PIR_PIN):
#    if GPIO.input(PIR_PIN) == GPIO.HIGH:
#        return ",1"
#    else:
#        return ",0"

#def save_dht11(a,b,c):
#    data = [a,b,c]
#    with open('temp.csv', "a") as output:
#        writer = csv.writer(output, delimiter=',', lineterminator='\n')
#        writer.writerow(data)

def send_data(data):
    list=[]
    #if data == "sensor":
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    timeC = time.strftime("%I")+":"+time.strftime('%M')+':'+time.strftime("%S")
    if humidity is not None and temperature is not None:
        if humidity < 100:
            data = str(int(temperature)) + "," + str(int(humidity))
            list = [temperature, humidity, timeC]
    else:
        data = 0+","+0

    try:
        if GPIO.input(PIR_PIN) == GPIO.HIGH:
            data = data + ",1"
        else:
            data = data + ",0"
    except KeyboardInterrupt:
        GPIO.cleanup()

    return data

def save_csv(data):
    if data == 'OFF':
        list=['제어가전없음','출력없음','설정온도없음']
        with open('control.csv', 'a') as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerow(list)
    else:
        pis = data.split(',')
        list = [pis[0], pis[1],pis[2]]

        with open('control.csv', 'a') as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerow(list)


while True:
    sensor_data = ""
    conn, addr = s.accept()
    print("Connected by ", addr)

    data = conn.recv(1024)
    data = data.decode("utf8").strip()
    if not data: break
    print("Received: " + data)

    aircon = "에어컨"
    boilor = "보일러"
    if boilor in data:
        BLUE.ChangeDutyCycle(0)
        RED.ChangeDutyCycle(75)
    elif aircon in data:
        RED.ChangeDutyCycle(0)
        BLUE.ChangeDutyCycle(75)
    else:
        RED.ChangeDutyCycle(0)
        BLUE.ChangeDutyCycle(0)
        GREEN.ChangeDutyCycle(75)

    save_csv(data)

    res = send_data(sensor_data)
    print(res)
    conn.sendall(res.encode("utf-8"))
    conn.close()
    time.sleep(4.5)
s.close()
