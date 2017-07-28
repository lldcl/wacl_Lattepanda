import numpy as np
import os.path
import datetime
import serial
import serial.tools.list_ports
import warnings
import configparser
import functools
import sys
from time import time, sleep
import glob

device_id = 0

def readsave(kill):

    global dataFolder, dataFile, filename, file_start_time, arduino, file_rollover, SN
    
    arduino_serial_number = [
            p.serial_number
            for p in serial.tools.list_ports.comports()
            if 'Uno' in p.description
        ]
    globals()['SN'] = arduino_serial_number[device_id]
    """Find location of the arduino"""
    def connect_to_arduino():
        arduino_ports = [
            p.device
            for p in serial.tools.list_ports.comports()
            if 'Uno' in p.description
        ]
        
        if not arduino_ports:
            raise IOError("No Arduino found")
        if len(arduino_ports) > 1:
            print("Multiple Arduinos found - using the", str(globals()['SN']))
        """Connect to the arduino"""
        globals()['arduino'] = serial.Serial(arduino_ports[device_id],115200)
        return(globals()['arduino'])
        
    """Load variables from config file"""
    def loadconfig():
        config = configparser.ConfigParser()
        config.read('/home/pete/Documents/config.INI')
        globals()['variables']=config['DataFileParams']['variables'].splitlines()
        globals()['file_rollover'] = int(config['DataFileParams']['file_rollover'])
        return(globals()['variables'], globals()['file_rollover'])
        
    """Write file header"""
    def writeHeadertoFile(variables):
        for v in variables:
            dataFile.write(v)
            dataFile.write('\t')
        dataFile.write('\n')
        
    """Write dataline to file"""
    def writeDatatoFile(datum,variables):
        data = datum.decode().split(',')
        """write it to file, along with a timestamp"""
        if (len(data) == len(variables)-1):
            """to match DAQfactory time"""
            dataFile.write(str(datetime.datetime.now()) + ',')
            for i in range(0,len(data)):
                dataFile.write('\t')
                dataFile.write(data[i].strip() + ',')
            dataFile.write('\n')
        else:
            print ('Arduino data length does not match header')
        
    """The main loop -- data is taken here and written to file"""
    def update():
        if (datetime.datetime.now() < globals()['file_start_time'].replace(minute=0,second=0,microsecond=0)+datetime.timedelta(minutes=globals()['file_rollover'])):
            """retrieve the numbers from the arduino"""
            globals()['arduino'].write("r".encode())
            datum = globals()['arduino'].readline()
            writeDatatoFile(datum,variables)
        else:
            globals()['dataFile'].close()
            globals()['file_start_time'] = datetime.datetime.now()
            globals()['dataFolder'] = '/home/pete/Documents/Data/'+globals()['file_start_time'].strftime("%y_%m_%d")+'/'+ str(globals()['SN'])[-4:]+'/'
            if not os.path.exists(dataFolder):
                os.makedirs(dataFolder)
            globals()['filename'] = globals()['dataFolder']+'a'+globals()['file_start_time'].strftime("%y%m%d_%H")
            if os.path.isfile(globals()['filename']):
                globals()['dataFile'] = open(globals()['filename'],'a',buffering=1)
                globals()['arduino'].write("r".encode())
                datum = globals()['arduino'].readline()
                writeDatatoFile(datum,variables)
            else:
                globals()['dataFile'] = open(globals()['filename'],'a',buffering=1)
                writeHeadertoFile(variables)
                globals()['arduino'].write("r".encode())
                datum = globals()['arduino'].readline()
                writeDatatoFile(datum,variables)
        
    """Create datafile to save incoming data"""
    variables, file_rollover = loadconfig()
    file_start_time = datetime.datetime.now()
    dataFolder = '/home/pete/Documents/Data/'+file_start_time.strftime("%y_%m_%d")+'/'+str(globals()['SN'])[-4:]+'/'
    if not os.path.exists(dataFolder):
        os.makedirs(dataFolder)
    filename = dataFolder+'a'+file_start_time.strftime("%y%m%d_%H")                                  
    if os.path.isfile(filename):
        dataFile = open(filename,'a',buffering=1)
    else:
        dataFile = open(filename,'a',buffering=1)
        writeHeadertoFile(variables)
    globals()['arduino'] = connect_to_arduino()
    while (kill == 'Run'):
        readtime = time()
        update()
        sleep(1.-((time() - readtime) % 1.))
    




""" Main part of the program that sets readsave and live plotting processes going"""
"""get rid of terminate and add ctl+c handling in subprocess"""
if __name__ == '__main__':
	status = 'Starting'
	readsave('Run')
