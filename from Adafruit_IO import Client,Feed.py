from Adafruit_IO import Client,Feed
from firebase import firebase
import os
import json

import pyqtgraph as pg
import time
import sys
from PyQt5.QtGui import QPixmap
from random import random
import source
import datetime
import numpy as np
import pandas as pd

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from setwindow import Ui_setRange_Window

pg.setConfigOption('background','w')
pg.setConfigOption('foreground','k')

class DataThread(QtCore.QThread):
    

    #setup signal Thread
    #setup range plot Thread
    update_range = QtCore.pyqtSignal(int,int)

    #setup plot Thread
    update_plot1 = QtCore.pyqtSignal(list,list)
    update_plot2 = QtCore.pyqtSignal(list,list)
    update_plot3 = QtCore.pyqtSignal(list,list)

    #setup present value Thread
    update_text1 = QtCore.pyqtSignal(str)
    update_text2 = QtCore.pyqtSignal(str)
    update_text3 = QtCore.pyqtSignal(str)

    #setup stat Thread
    update_stat1_1 = QtCore.pyqtSignal(bool)
    update_stat1_2 = QtCore.pyqtSignal(bool)

    update_stat2_1 = QtCore.pyqtSignal(bool)
    update_stat2_2 = QtCore.pyqtSignal(bool)

    update_stat3_1 = QtCore.pyqtSignal(bool)
    update_stat3_2 = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent=parent)
        self.isRunning = True     

    def run(self):
            
        #setup Adaffruit IO KEY and IO Username

        # ADAFRUIT_IO_KEY = '403d235a5abb43bc8f72041a8e524d52'

        ADAFRUIT_IO_KEY = 'aio_quze518jQDAN9AYOap7PqRnlighq'

        ADAFRUIT_IO_USERNAME = 'C_Project'

        
        #ADAFRUIT_IO_USERNAME = 'C_Project'
        # ADAFRUIT_IO_USERNAME = 'Bagasbudhi'

        aio = Client (ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

        # Calling Feeds from Adafruit.io

        # micron_feed1=aio.feeds('temperature')
        # micron_feed2=aio.feeds('humidity')
        # micron_feed3=aio.feeds('ph')
        
        micron_feed=aio.feeds('microndata')

        #sizing window range and counter index
        window_size=5
        idx=0

        #provide place for data
        self.xval=[]

        self.yval1=[]
        self.yval2=[]
        self.yval3=[]

        self.stat1=[]
        self.stat2=[]
        self.stat3=[]

        #setting emit signal from data adafruit

        while True:
            
            self.temp=aio.receive(micron_feed.key).value
            self.temp2=json.loads(self.temp)

            # print('nilai={0}'.format(self.value1))

            self.state1=self.temp2["state1"]
            if self.state1=="true":
                self.datastat1 = 1
            else:
                self.datastat1 = 0

            self.state2=self.temp2["state2"]
            if self.state2=="true":
                self.datastat2 = 1
            else:
                self.datastat2=0

            self.state3=self.temp2["state3"]
            if self.state3=="true":
                self.datastat3=1
            else:
                self.datastat3=0
                
            self.stat3.append(self.datastat3)  

            self.stat1.append(self.datastat1) 
            self.stat2.append(self.datastat2) 
            self.stat3.append(self.datastat3)   
            

            if idx <= window_size:

                self.xval.append(idx)

                self.yval1.append(float(self.temp2["value1"]))
                self.yval2.append(float(self.temp2["value2"]))
                self.yval3.append(float(self.temp2["value3"]))
                
                # self.stat1.append(int(self.temp2["state1"].lower()))
                # self.stat2.append(int(self.temp2["state2"].lower()))
                # self.stat3.append(int(self.temp2["state3"].lower()))


                # for i in range(0, len(self.yval1)): 
                #     self.yval1[i] = int(self.yval1[i])
                #     self.yval2[i] = int(self.yval2[i])
                #     self.yval3[i] = int(self.yval3[i])

                #     self.stat1[i] = int(self.stat1[i])
                #     self.stat2[i] = int(self.stat2[i])
                #     self.stat3[i] = int(self.stat3[i])


                self.update_range.emit(self.xval[0],self.xval[idx])

                self.update_plot1.emit(self.xval[0:idx+1],self.yval1[0:idx+1])
                self.update_text1.emit(str(round(self.yval1[idx],4)))
                if (self.stat1[idx]) == 1 :
                    self.update_stat1_1.emit(bool(True))
                else :
                    self.update_stat1_2.emit(bool(True))

                self.update_plot2.emit(self.xval[0:idx+1],self.yval2[0:idx+1])
                self.update_text2.emit(str(round(self.yval2[idx],4)))
                if (self.stat2[idx]) == 1 :
                    self.update_stat2_1.emit(bool(True))
                else :
                    self.update_stat2_2.emit(bool(True))

                self.update_plot3.emit(self.xval[0:idx+1],self.yval3[0:idx+1])
                self.update_text3.emit(str(round(self.yval3[idx],4)))
                if (self.stat3[idx]) == 1 :
                    self.update_stat3_1.emit(bool(True))
                else :
                    self.update_stat3_2.emit(bool(True))
                
                
                print('x,y,stat= ({0},{1},{2})'.format(self.xval[0:idx+1],self.yval1[0:idx+1],self.stat1[0:idx+1]))

            elif idx > window_size: 
                
                self.xval=self.xval[1:idx]
                self.xval.append(idx)

                self.yval1=self.yval1[1:idx]
                self.yval1.append(float(self.temp2["value1"]))
                self.stat1=self.stat1[1:idx]
                self.stat1.append(self.datastat1)

                self.yval2=self.yval2[1:idx]
                self.yval2.append(float(self.temp2["value2"]))
                self.stat2=self.stat2[1:idx]
                self.stat2.append(self.datastat2)

                self.yval3=self.yval3[1:idx]
                self.yval3.append(float(self.temp2["value3"]))
                self.stat3=self.stat3[1:idx]
                self.stat3.append(self.datastat3)


                # for i in range(0, len(self.yval1)): 
                #     self.yval1[i] = int(self.yval1[i])
                #     self.yval2[i] = int(self.yval2[i])
                #     self.yval3[i] = int(self.yval3[i])

                #     self.stat1[i] = int(self.stat1[i])
                #     self.stat2[i] = int(self.stat2[i])
                #     self.stat3[i] = int(self.stat3[i])

                self.update_range.emit(self.xval[0],self.xval[window_size])

                self.update_plot1.emit(self.xval[0:window_size+1],self.yval1[0:window_size+1])
                self.update_text1.emit(str(round(self.yval1[-1],4)))
                if (self.stat1[window_size]) == 1:
                    self.update_stat1_1.emit(bool(True))
                else :
                    self.update_stat1_2.emit(bool(True))
                
                self.update_plot2.emit(self.xval[0:window_size+1],self.yval2[0:window_size+1])
                self.update_text2.emit(str(round(self.yval2[-1],4)))
                if (self.stat2[window_size]) == 1 :
                    self.update_stat2_1.emit(bool(True))
                else :
                    self.update_stat2_2.emit(bool(True))

                self.update_plot3.emit(self.xval[0:window_size+1],self.yval3[0:window_size+1])
                self.update_text3.emit(str(round(self.yval3[-1],4)))
                if (self.stat3[window_size]) == 1 :
                    self.update_stat3_1.emit(bool(True))
                else :
                    self.update_stat3_2.emit(bool(True))
                
                print('x,y= ({0},{1},{2})'.format(self.xval[0:window_size+1],self.yval1[0:window_size+1],self.stat1[0:window_size+1]))
                # print('idx = {0}'.format(idx))

            if idx%window_size == 0 and idx != 0:
                self.firebase = firebase.FirebaseApplication("https://capstone-2496f.firebaseio.com/", None)

                self.xval_send = str(self.xval)

                self.yval1_send = str(round(self.yval1,4))
                self.stat1_send = str(round(self.stat1,4))

                self.yval2_send = str(round(self.yval2,4))
                self.stat2_send = str(round(self.stat2,4))

                self.yval3_send = str(round(self.yval3,4))
                self.stat3_send = str(round(self.stat3),4))

                self.testing = self.firebase.post('/DATA TEST/xval',self.xval_send)

                self.testing2 = self.firebase.post('/DATA TEST/stat1',self.stat1_send)
                self.testing3 = self.firebase.post('/DATA TEST/yval1',self.yval1_send)

                self.testing4 = self.firebase.post('/DATA TEST/stat2',self.stat2_send)
                self.testing5 = self.firebase.post('/DATA TEST/yval2',self.yval2_send)

                self.testing6 = self.firebase.post('/DATA TEST/stat3',self.stat3_send)
                self.testing7 = self.firebase.post('/DATA TEST/yval3',self.yval3_send)

            idx+=1

    @QtCore.pyqtSlot(int)
    def getWindowSize(self, new_win_size):
        print('Current Window Size : {}'.format(new_win_size))
        self.window_size = new_win_size 

    def stop(self):
        self.isRunning = False
        self.quit()
        self.wait()
            
class Ui_MainWindow(object):
    def SetWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui.setupUi(self.window)
        self.window.show()

    def cetak(self):
        def convert(s): 
            # initialization of string to "" 
            new = "" 
  
            # traverse in the string  
            for x in s: 
                new += x  
  
            # return string  
            return new

        self.firebase = firebase.FirebaseApplication("https://capstone-2496f.firebaseio.com/", None)
        self.result=self.firebase.get('/DATA TEST/',None)
        self.df = pd.DataFrame(self.result)
        # result2 = df[~df.stat1.str.contains("NaN")]
        self.z = pd.DataFrame.transpose(self.df)
        self.variable = list(self.df.columns)

        self.x = []
        self.final = []
        self.dummy=[]

        for i in range (0, len(self.z)):
            self.y = self.z.iloc[i,:]
            self.x.append(self.variable[i]+",")
            self.nest = self.y.dropna()
            self.dummy.append(len(self.nest))
            for j in range (0, len(self.nest)):
                self.val = self.nest[j]+","
                self.n = self.val.replace("[","").replace("]","").replace(" ","")
                self.x.append(self.n)
    
        self.f = 0
        self.h=np.asarray(self.x)
       
        for k in range(0,len(self.dummy)):
            self.east=self.dummy[k]+1+self.f
            # print('{0},{1}'.format(f,east))
            self.b=convert(self.h[self.f:self.east])
            self.final.append(self.b)
            self.f=self.east

        self.lost = np.asarray(self.final)
        self.cetak = pd.DataFrame(self.lost)

        # directory to save csv

        self.cetak.to_csv (r'C:\Users\BLACK\Desktop\contoh.csv')
        

    def setupUi(self, MainWindow):
        #Setup UI
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        MainWindow.setSizePolicy(sizePolicy)

        #Setup MainFrame
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.mainframe = QtWidgets.QFrame(self.centralwidget)
        self.mainframe.setObjectName("mainframe")
    
        # setup layout mainframe as formLayout
        self.frameLayout = QtWidgets.QVBoxLayout(self.mainframe)
        self.frameLayout.setObjectName("frameLayout")

        #setup frame in the top as frametop
        self.frametop = QtWidgets.QHBoxLayout()
        self.frametop.setObjectName("frametop")

        #setup Title Lable
        self.Title_Label = QtWidgets.QLabel(self.mainframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(self.Title_Label.sizePolicy().hasHeightForWidth())
        self.Title_Label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(24)
        self.Title_Label.setFont(font)
        self.Title_Label.setObjectName("Title_Label")
        self.frametop.addWidget(self.Title_Label)

        #setup spacer between title and logo
        spacer_title_logo = QtWidgets.QSpacerItem(396, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.frametop.addItem(spacer_title_logo)

        #setup label logo UGM
        self.label = QtWidgets.QLabel(self.mainframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.label.setMinimumSize(QtCore.QSize(200,60))
        self.label.setMaximumSize(QtCore.QSize(200,60))
        self.label.setPixmap(QtGui.QPixmap("Logo Horizontal Stack-Up.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.frametop.addWidget(self.label)     

        #spacer in right size label
        spacer_rightlabel = QtWidgets.QSpacerItem(68, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.frametop.addItem(spacer_rightlabel)

        #setup frame top in frame top
        self.frameLayout.addLayout(self.frametop)

        #setup frame sensor 1
        self.frame_sensor1 = QtWidgets.QHBoxLayout()
        self.frame_sensor1.setObjectName("frame_sensor1")

        #setup frame plot sensor 1
        self.frame_plot1 = QtWidgets.QFrame(self.mainframe)
        self.frame_plot1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_plot1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_plot1.setObjectName("frame_plot1")

        #setup layout frame_plot 1 as horizontalLayout
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_plot1)
        self.horizontalLayout.setObjectName("horizontalLayout")

        #setup graphics View 1
        #self.graphicsView_1 = QtWidgets.QGraphicsView(self.frame_plot1)
        self.graphicsView_1 = pg.PlotWidget(self.frame_plot1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.graphicsView_1.setSizePolicy(sizePolicy)
        self.graphicsView_1.setMinimumSize(QtCore.QSize(0, 180))
        self.graphicsView_1.setMaximumSize(QtCore.QSize(1000, 200))
        self.graphicsView_1.setObjectName("graphicsView_1")
        self.horizontalLayout.addWidget(self.graphicsView_1)
        self.frame_sensor1.addWidget(self.frame_plot1)

        #setup spacer between frame_plot1 and frame_group1 and add to frame sensor1
        plottobox_horizontalSpacer_1 = QtWidgets.QSpacerItem(38, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.frame_sensor1.addItem(plottobox_horizontalSpacer_1)

        #setup Frame group 1
        self.frame_group1 = QtWidgets.QFrame(self.mainframe)
        self.frame_group1.setMaximumSize(QtCore.QSize(270, 181))
        self.frame_group1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_group1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_group1.setObjectName("frame_group1")

        #setup frame group 1 into grid layout
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_group1)
        self.gridLayout_2.setObjectName("gridLayout_2")

        #spacer in frame gorup 1 grid layout
        #in gridlayout item dimension is (row,column,height(row),width(column))

        verticalSpacer_plot1_1 = QtWidgets.QSpacerItem(20, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(verticalSpacer_plot1_1, 1, 1, 1, 1)

        verticalSpacer_plot1_2 = QtWidgets.QSpacerItem(20, 14, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(verticalSpacer_plot1_2, 3, 1, 1, 1)

        verticalSpacer_plot1_3= QtWidgets.QSpacerItem(20, 28, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(verticalSpacer_plot1_3, 5, 1, 1, 1)

        horizontalSpacer_plot1 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(horizontalSpacer_plot1, 2, 3, 1, 1)

        #setup Sensor label 1 & Positioning in grid
        self.Sensor1_label = QtWidgets.QLabel(self.frame_group1)
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(14)
        self.Sensor1_label.setFont(font)
        self.Sensor1_label.setObjectName("Sensor1_label")
        self.gridLayout_2.addWidget(self.Sensor1_label, 0, 0, 1, 2)
       
        #Setup Radio Button Sensor 1 & Positioning in grid
        self.Normal_1 = QtWidgets.QRadioButton(self.frame_group1)
        self.Normal_1.setObjectName("Normal_1")
        self.gridLayout_2.addWidget(self.Normal_1, 4, 0, 1, 1)

        self.Fault_1 = QtWidgets.QRadioButton(self.frame_group1)
        self.Fault_1.setObjectName("Fault_1")
        self.gridLayout_2.addWidget(self.Fault_1, 4, 1, 1, 1)

        #setup Unit sensor 1 & Positioning in grid
        self.unit_1 = QtWidgets.QLabel(self.frame_group1)
        self.unit_1.setMaximumSize(QtCore.QSize(30, 30))
        self.unit_1.setObjectName("unit_1")
        self.gridLayout_2.addWidget(self.unit_1, 2, 2, 1, 1)
        
        # Setup view 1 & Positioning in grid
        self.present_yval1 = QtWidgets.QTextEdit(self.frame_group1)
        self.present_yval1.setMaximumSize(QtCore.QSize(110, 30))
        self.present_yval1.setObjectName("present_yval1")
        self.gridLayout_2.addWidget(self.present_yval1, 2, 0, 1, 2)

        # add frame_group1 into frame_sensor1
        self.frame_sensor1.addWidget(self.frame_group1)

        # add frame_sensor1 into mainframe layout
        self.frameLayout.addLayout(self.frame_sensor1)
        
        #setup frame sensor 2
        self.frame_sensor2 = QtWidgets.QHBoxLayout()
        self.frame_sensor2.setObjectName("frame_sensor2")

        #setup frame plot sensor 2
        self.frame_plot2 = QtWidgets.QFrame(self.mainframe)
        self.frame_plot2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_plot2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_plot2.setObjectName("frame_plot2")

        #setup layout frame_plot2 as horizontalLayout_4
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_plot2)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        #setup grahics view 2
        #self.graphicsView_2 = QtWidgets.QGraphicsView(self.frame_plot2)
        self.graphicsView_2 = pg.PlotWidget(self.frame_plot2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.graphicsView_2.setSizePolicy(sizePolicy)
        self.graphicsView_2.setMinimumSize(QtCore.QSize(0, 180))
        self.graphicsView_2.setMaximumSize(QtCore.QSize(1000, 200))
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.horizontalLayout_4.addWidget(self.graphicsView_2)
        self.frame_sensor2.addWidget(self.frame_plot2)

        #setup spacer between frame_plot2 and frame_group2 and add to frame sensor2
        plottobox_horizontalSpacer_2= QtWidgets.QSpacerItem(38, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.frame_sensor2.addItem(plottobox_horizontalSpacer_2)

        #setup frame group 2
        self.frame_group2 = QtWidgets.QFrame(self.mainframe)
        self.frame_group2.setMaximumSize(QtCore.QSize(270, 181))
        self.frame_group2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_group2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_group2.setObjectName("frame_group2")

        #setup frame group 1 into grid layout
        self.gridLayout_5 = QtWidgets.QGridLayout(self.frame_group2)
        self.gridLayout_5.setObjectName("gridLayout_5")

        #spacer in frame gorup 2 grid layout
        #in gridlayout item dimension is (row,column,height(row),width(column))
        verticalSpacer_plot2_1 = QtWidgets.QSpacerItem(20, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_5.addItem(verticalSpacer_plot2_1, 1, 1, 1, 1)

        verticalSpacer_plot2_2 = QtWidgets.QSpacerItem(20, 14, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_5.addItem(verticalSpacer_plot2_2, 3, 1, 1, 1)

        verticalSpacer_plot2_3 = QtWidgets.QSpacerItem(20, 28, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_5.addItem(verticalSpacer_plot2_3, 5, 1, 1, 1)

        horizontalSpacer_plot2 = QtWidgets.QSpacerItem(65, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(horizontalSpacer_plot2, 2, 3, 1, 1)

        #setup sensor label 2 & Positioning in grid
        self.Sensor2_label = QtWidgets.QLabel(self.frame_group2)
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(14)
        self.Sensor2_label.setFont(font)
        self.Sensor2_label.setObjectName("Sensor2_label")
        self.gridLayout_5.addWidget(self.Sensor2_label, 0, 0, 1, 2)

        #setup unit 2 & Positioning in grid
        self.unit_2 = QtWidgets.QLabel(self.frame_group2)
        self.unit_2.setMaximumSize(QtCore.QSize(30, 30))
        self.unit_2.setObjectName("unit_2")
        self.gridLayout_5.addWidget(self.unit_2, 2, 2, 1, 1)

        #setup view 2 & Positioning in grid
        self.present_yval2 = QtWidgets.QTextEdit(self.frame_group2)
        self.present_yval2.setMaximumSize(QtCore.QSize(110, 30))
        self.present_yval2.setObjectName("present_yval2")
        self.gridLayout_5.addWidget(self.present_yval2, 2, 0, 1, 2)

        #setup radio button 2 & Positioning in grid
        self.Normal_2 = QtWidgets.QRadioButton(self.frame_group2)
        self.Normal_2.setObjectName("Normal_2")
        self.gridLayout_5.addWidget(self.Normal_2, 4, 0, 1, 1)
        self.Fault_2 = QtWidgets.QRadioButton(self.frame_group2)
        self.Fault_2.setObjectName("Fault_2")
        self.gridLayout_5.addWidget(self.Fault_2, 4, 1, 1, 1)

        # add frame_group2 into frame_sensor2
        self.frame_sensor2.addWidget(self.frame_group2)

        # add frame_sensor2 into mainframe layout
        self.frameLayout.addLayout(self.frame_sensor2)
        
        #setup frame sensor 3
        self.frame_sensor3 = QtWidgets.QHBoxLayout()
        self.frame_sensor3.setObjectName("frame_sensor3")

        #setup frame plot 3
        self.frame_plot3 = QtWidgets.QFrame(self.mainframe)
        self.frame_plot3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_plot3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_plot3.setObjectName("frame_plot3")

        #setup layout frame_plot3 as horizontalLayout_6
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_plot3)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")

        #setup graphics View 3
        #self.graphicsView_3 = QtWidgets.QGraphicsView(self.frame_plot3)
        self.graphicsView_3 = pg.PlotWidget(self.frame_plot3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.graphicsView_3.setSizePolicy(sizePolicy)
        self.graphicsView_3.setMinimumSize(QtCore.QSize(0, 180))
        self.graphicsView_3.setMaximumSize(QtCore.QSize(1000, 200))
        self.graphicsView_3.setObjectName("graphicsView_3")
        self.horizontalLayout_6.addWidget(self.graphicsView_3)
        self.frame_sensor3.addWidget(self.frame_plot3)

        #setup spacer between frame_plot3 and frame_group3 and add to frame sensor3
        plottobox_horizontalSpacer_3 = QtWidgets.QSpacerItem(38, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.frame_sensor3.addItem(plottobox_horizontalSpacer_3)

        #setup frame group 3
        self.frame_group3 = QtWidgets.QFrame(self.mainframe)
        self.frame_group3.setMaximumSize(QtCore.QSize(270, 181))
        self.frame_group3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_group3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_group3.setObjectName("frame_group3")

        #setup layout frame_group3 as grid layout
        self.gridLayout_6 = QtWidgets.QGridLayout(self.frame_group3)
        self.gridLayout_6.setObjectName("gridLayout_6")

        #spacer in frame gorup 3 grid layout
        #in gridlayout item dimension is (row,column,height(row),width(column))

        verticalSpacer_plot3_1 = QtWidgets.QSpacerItem(20, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_6.addItem(verticalSpacer_plot3_1, 1, 1, 1, 1)

        verticalSpacer_plot3_1 = QtWidgets.QSpacerItem(20, 14, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_6.addItem(verticalSpacer_plot3_1, 3, 1, 1, 1)

        verticalSpacer_plot3_3 = QtWidgets.QSpacerItem(20, 28, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_6.addItem(verticalSpacer_plot3_3, 5, 1, 1, 1)

        horizontalSpacer_plot3 = QtWidgets.QSpacerItem(65, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(horizontalSpacer_plot3, 2, 3, 1, 1)

        #setup label sensor 3 & Positioning in grid
        self.Sensor3_label = QtWidgets.QLabel(self.frame_group3)
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(14)
        self.Sensor3_label.setFont(font)
        self.Sensor3_label.setObjectName("Sensor3_label")
        self.gridLayout_6.addWidget(self.Sensor3_label, 0, 0, 1, 2)

        #setup unit sensor 3 & Positioning in grid
        self.unit_3 = QtWidgets.QLabel(self.frame_group3)
        self.unit_3.setMaximumSize(QtCore.QSize(30, 30))
        self.unit_3.setObjectName("unit_3")
        self.gridLayout_6.addWidget(self.unit_3, 2, 2, 1, 1)

        #setup View sensor 3 & Positioning in grid
        self.present_yval3 = QtWidgets.QTextEdit(self.frame_group3)
        self.present_yval3.setMaximumSize(QtCore.QSize(110, 30))
        #self.present_yval3.setAlignment(QtCore.Qt.AlignRight)
        self.present_yval3.setObjectName("present_yval3")
        self.gridLayout_6.addWidget(self.present_yval3, 2, 0, 1, 2)

        #setup radio button 3 & Positioning in grid
        self.Normal_3 = QtWidgets.QRadioButton(self.frame_group3)
        self.Normal_3.setObjectName("Normal_3")
        self.gridLayout_6.addWidget(self.Normal_3, 4, 0, 1, 1)

        self.Fault_3 = QtWidgets.QRadioButton(self.frame_group3)
        self.Fault_3.setObjectName("Fault_3")
        self.gridLayout_6.addWidget(self.Fault_3, 4, 1, 1, 1)
        
        #setup frame_group 3 ini frame_sensor 3 layout
        self.frame_sensor3.addWidget(self.frame_group3)

        #setup frame_sensor3 in mainframe
        self.frameLayout.addLayout(self.frame_sensor3)

        #setup vertical layout in mainframe
        self.verticalLayout.addWidget(self.mainframe)

        MainWindow.setCentralWidget(self.centralwidget)

        #setup menubar and statusbar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 658, 21))
        self.menubar.setObjectName("menubar")
        
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionExit = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("exit1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon)
        self.actionExit.setIconText("exit")

        self.actionPrint = QtWidgets.QAction(MainWindow)
        self.actionPrint.setObjectName("actionPrint")

        self.actionWindowSize = QtWidgets.QAction(MainWindow)
        self.actionWindowSize.setObjectName("actionWindowSize")

        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")

        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuFile.addAction(self.actionPrint)

        self.menuEdit.addAction(self.actionWindowSize)

        self.menuAbout.addAction(self.actionAbout)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.actionWindowSize.triggered.connect(self.SetWindow)
        self.actionPrint.triggered.connect(self.cetak)

        #pyqtgraph
        self.plot_widget = pg.PlotWidget()

        #setup setwindow
        self.ui = Ui_setRange_Window()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MICRON"))
        self.Title_Label.setText(_translate("MainWindow", "Monitoring Sensor"))
        
        self.Normal_1.setText(_translate("MainWindow", "Normal"))
        self.Fault_1.setText(_translate("MainWindow", "Fault"))

        self.Normal_2.setText(_translate("MainWindow", "Normal"))
        self.Fault_2.setText(_translate("MainWindow", "Fault"))
        
        self.Normal_3.setText(_translate("MainWindow", "Normal"))
        self.Fault_3.setText(_translate("MainWindow", "Fault"))

        self.Sensor1_label.setText(_translate("MainWindow", "Kecepatan"))
        self.Sensor2_label.setText(_translate("MainWindow", "Posisi"))
        self.Sensor3_label.setText(_translate("MainWindow", "Arus"))
        
        self.unit_1.setText(_translate("MainWindow", "rpm"))
        self.unit_2.setText(_translate("MainWindow", "rad"))
        self.unit_3.setText(_translate("MainWindow", "A"))

        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuAbout.setTitle(_translate("MainWindow", "Tentang"))

        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionPrint.setText(_translate("MainWindow","Print"))
        self.actionPrint.setShortcut(_translate("MainWindow","Ctrl+P"))

        self.actionWindowSize.setText(_translate("MainWindow", "Window Size"))

        self.actionAbout.setText(_translate("MainWindow", "Tentang"))

    def startThread(self):
        
        #self.thr = threading.Thread(target=self.update)
        
        self.th = DataThread()
        self.th.update_range.connect(self.graphicsView_1.setXRange)
        self.th.update_plot2.connect(self.graphicsView_1.plot)
        self.th.update_text2.connect(self.present_yval1.setText)

        self.th.update_stat2_2.connect(self.Normal_1.setChecked)
        self.th.update_stat2_1.connect(self.Fault_1.setChecked)
        
        self.th.update_range.connect(self.graphicsView_2.setXRange)
        self.th.update_plot1.connect(self.graphicsView_2.plot)
        self.th.update_text1.connect(self.present_yval2.setText)

        self.th.update_stat1_2.connect(self.Normal_2.setChecked)
        self.th.update_stat1_1.connect(self.Fault_2.setChecked)

        self.th.update_range.connect(self.graphicsView_3.setXRange)
        self.th.update_plot3.connect(self.graphicsView_3.plot)
        self.th.update_text3.connect(self.present_yval3.setText)

        self.th.update_stat3_2.connect(self.Normal_3.setChecked)
        self.th.update_stat3_1.connect(self.Fault_3.setChecked)

        self.th.start()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.startThread()
    MainWindow.show()
    sys.exit(app.exec_())