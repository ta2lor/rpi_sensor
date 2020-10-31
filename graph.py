import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation
from datetime import datetime

fig = plt.figure()

rect = fig.patch
rect.set_facecolor('#0079E7')
def animate(i):
    ftemp = 'temp.csv'
    fh = open(ftemp)
    temp = list()
    humi = list()
    timeC = list()
    for line in fh:
        pieces = line.split(',')
        degree = pieces[0]
        humidity = pieces[1]
        timeB = pieces[2]
        timeA = timeB[:8]
        time_string = datetime.strptime(timeA, '%H:%M:%S')

        temp.append(float(degree))
        humi.append(float(humidity))
        timeC.append(time_string)

        plt.title('degree and humidity')
        ax1 = fig.add_subplot(2,1,1)
#        ax2 = fig.add_subplot(2,1,2)
        #ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        #ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

        ax1.clear()
#        ax2.clear()
        ax1.plot(timeC, temp, 'c', linewidth=3.3)
#        ax2.plot(timeC, humi, 'c', linewidth=3.3)
        plt.xlabel('Time')


ani = animation.FuncAnimation(fig, animate, interval = 20)
plt.show()
