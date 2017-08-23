import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from PyQt5.QtCore import QTime, QTimer
import numpy as np
import functools
import sys
from time import time, sleep
import glob
import re
import datetime
from collections import deque
from scipy import stats

class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        # PySide's QTime() initialiser fails miserably and dismisses args/kwargs
        return [t.addMSecs(value).toString('HH:mm:ss') for value in values]

def updateplot(data1):
        global loc
        try:
                filename = sorted(glob.glob('/home/pete/Documents/Data/'+datetime.datetime.now().strftime("%y_%m_%d")+'/5011' + '/*'))[-1]
        except IndexError:
                sleep(5)
                filename = sorted(glob.glob('/home/pete/Documents/Data/'+datetime.datetime.now().strftime("%y_%m_%d")+'/5011' + '/*'))[-1]
        with open(filename) as latestfile:
                dataline = list(latestfile)[-1].split(',')
        print(filename)
        if dataline[0].isalpha() == False:
                #print(dataline[1].isalpha(), dataline[1])
                loc+=1
                data1[:,:-1] = data1[:,1:]
                data1[0,-1]= np.median([np.float(dataline[1]),np.float(dataline[3]),np.float(dataline[5]),np.float(dataline[7]),np.float(dataline[9]),np.float(dataline[11]),np.float(dataline[13]),np.float(dataline[15])])
                data1[1,-1]= np.float(dataline[3])
                data1[2,-1]= np.float(dataline[5])
                data1[3,-1]= np.float(dataline[7])
                data1[4,-1]= np.float(dataline[9])
                data1[5,-1]= np.float(dataline[11])
                data1[6,-1]= np.float(dataline[13])
                data1[7,-1]= np.float(dataline[15])
                data1[8,-1]= (3655.8-np.float(dataline[71])/45.759)/100
                data1[9,-1]= np.float(dataline[69])*0.0375-37.7
                data1[10,-1]= ((np.float(dataline[33])*1000-225) - (np.float(dataline[35])*1000-340))/420
                data.append({'x': t.elapsed(), 'y': data1[0,-1], 'temp_data': data1[8,-1], 'h': data1[9,-1], 'c1': data1[10,-1], 'c2': data1[11,-1]})
                x = [item['x'] for item in data]
                y = [item['y'] for item in data]
                temp_data = [item['temp_data'] for item in data]
                h = [item['h'] for item in data]
                c1 = [item['c1'] for item in data]
                #c2 = [item['c2'] for item in data]
                curve1.setData(x=x, y=y)
                curve1.setPos(-loc,0)
                temp.setData(x=x, y=temp_data)
                rh.setData(x=x, y=h)
                CO1.setData(x=x, y=c1)
                #CO2.setData(x=x, y=c2)

t = QTime()
t.start()
data = deque(maxlen=100)
data1 = np.zeros([12,300])
loc = 0
win = pg.GraphicsWindow(title='Live MOS Data')
pg.setConfigOptions(antialias=True)
timeaxis1 = TimeAxisItem(orientation='bottom')
timeaxis2 = TimeAxisItem(orientation='bottom')
timeaxis3 = TimeAxisItem(orientation='bottom')
timeaxis4 = TimeAxisItem(orientation='bottom')
p1 = win.addPlot(title='MOS signals', colspan=2,axisItems={'bottom': timeaxis1})
p1.setLabel(axis='left',text='Signal (mV)')
curve1 = p1.plot(data1[0,:],width=5)
win.nextRow()
p2 = win.addPlot(title='Temperature', axisItems={'bottom': timeaxis2})
p2.setLabel(axis='left',text='Temperature (C)')
temp = p2.plot(data1[8,:],width=5)
p3 = win.addPlot(title='Relative Humidity', axisItems={'bottom': timeaxis3})
p3.setLabel(axis='left',text='RH (%)')
rh = p3.plot(data1[9,:],width=5)
win.nextRow()
p4 = win.addPlot(title='CO sensor signals', colspan=2, axisItems={'bottom': timeaxis4})
p4.setLabel(axis='left',text='CO')
CO1 = p4.plot(data1[10,:],pen=('g'),width=5)
win.showMaximized()
plot_update = functools.partial(updateplot,data1)
timer = pg.QtCore.QTimer()
timer.timeout.connect(plot_update)
timer.start(2000)
app = QtGui.QApplication.instance()
sleep(5)

if __name__ == '__main__':
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
