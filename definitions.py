import os
import sys
import numpy as np
import pandas as pd
import pyqtgraph as pg
from PyQt5 import QtWidgets
from gui import Ui_MainWindow
from scipy.signal import chirp
from PyQt5 import QtCore, QtGui
# import matplotlib.pyplot as plt


class AppWindow(QtWidgets.QMainWindow,Ui_MainWindow): #Test    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.actionPlot.triggered.connect(self.slider)
        self.horizontalSlider.valueChanged.connect(self.slider)

    
    def browse(self):
        self.file_path_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', " ", "(*.txt *.csv *.xls)")
        
            
    def read_data(self):
        self.file_name, self.file_extension = os.path.splitext(self.file_path_name)
        
        if self.file_extension == '.txt':
            # to skip the second row, use a list-like argument "[]"
            # fwf stands for fixed width formatted lines.
            data = pd.read.fwf(self.file_path_name, skiprows = [1])
            self.signal_name = data.columns[1]
            yaxis_values = data.iloc[:, 1] # gets second column
            # : means everything in dimension1 from the beginning to the end
            xaxis_timestamps = data.iloc[:, 0]
        elif self.file_extension == '.csv':
            data = pd.read_csv(self.file_path_name, skiprows = [1])
            self.signal_name = data.columns[1]
            yaxis_values = data.iloc[:, 1] # gets second column
            xaxis_timestamps = data.iloc[:, 0]
        xy_axes = {'xaxis': xaxis_timestamps, 'yaxis': yaxis_values}
        return xy_axes;
    
    def enlist_data(self):
        self.browse()
        data = self.read_data(self.file_path_name)
        if self.signal_name in self.signals:
            pass
        else:
            self.signals.update({self.signal_name: data})
            
    def plot(self, sample_rate):
        print('I\'m pressed');
        time = np.linspace(0, 10, sample_rate=1500)
        wave = chirp(time, f0=6, f1=1, t1=10)
        self.graphicsView_main.plot(time, wave, pen=(pg.mkPen('b')))
        
    def slider(self):
        self.graphicsView_main.plotItem.clearPlots()
        sample_rate = self.horizontalSlider.value()
        self.plot(sample_rate);
        
        
    
    
# update: for dictionaries
# append: for lists

###################[ NumPy ]#########################
# [0]     #means line 0 of your matrix
# [(0,0)] #means cell at 0,0 of your matrix
# [0:1]   #means lines 0 to 1 excluded of your matrix
# [:1]    #excluding the first value means all lines until line 1 excluded
# [1:]    #excluding the last param mean all lines starting form line 1 
#          included
# [:]     #excluding both means all lines
# [::2]   #the addition of a second ':' is the sampling. (1 item every 2)
# [::]    #exluding it means a sampling of 1
# [:,:]   #simply uses a tuple (a single , represents an empty tuple) instead 
#          of an index.
   
    
app = QtCore.QCoreApplication.instance()
if app is None:
    app = QtWidgets.QApplication(sys.argv)
w = AppWindow()

w.show() # Create the widget and show it
sys.exit(app.exec_()) # Run the app
    