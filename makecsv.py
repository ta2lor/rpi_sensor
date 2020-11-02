import Adafruit_DHT
import time
import csv
import sys

csvfile = "temp"
als =True

while als:
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)
    if humidity is not None and temperature is not None:
        if humidity < 100 and temperature < 50 and temperature > 10:
            humidity = round(humidity, 2)
            temperature = round(temperature, 2)
            print(humidity, temperature)
            timeC = time.strftime("%I")+":"+time.strftime('%M')+':'+time.strftime("%S")
            data = [temperature,humidity, timeC]
        else:
            continue;
            #humidity = 0
            #temperature = 0
    else:
        continue

    with open('temp.csv', "a") as output:
        writer = csv.writer(output, delimiter=',', lineterminator='\n')
        writer.writerow(data)
    time.sleep(60)
