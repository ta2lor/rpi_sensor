import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation
from datetime import *
import tailer
import numpy as np
from matplotlib import rc, font_manager
import matplotlib
import matplotlib.font_manager as fm
import pandas as pd


#matplotlib.font_manager._rebuild()
#rc('font', family='NanumGothic')
path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
fontprop = fm.FontProperties(fname=path, size=10)


fig = plt.figure()
rect=fig.patch
rect.set_facecolor('#0079E7')
def animate(i):
    ftemp = 'temp.csv'
    fh = tailer.tail(open(ftemp),10)
    temp = list()
    humid = list()
    time = list()


    for line in fh:
        pis = line.split(',')
        degree = pis[0]
        humidity = pis[1]
        timeC = pis[2]
        timeB = timeC[:8]
        time_string = datetime.strptime(timeB, '%H:%M:%S')

        temp.append(float(degree)) 
        humid.append(float(humidity))
        time.append(time_string)


        plt.xticks(rotation = -45)

        ax1 = plt.subplot(211)
        graph1 = plt.plot(temp, 'c')
        ax1.set_title('온도', fontproperties=fontprop)
        ax1.get_xaxis().set_visible(False)

        ax1.set_ylim([10,50])

        ax2 = plt.subplot(212)
        graph2 = plt.plot(time,humid)
        ax2.set_ylim([0,100])
        ax2.set_title('습도', fontproperties=fontprop)


ani = animation.FuncAnimation(fig, animate, interval = 20)
plt.tight_layout()
plt.show()
