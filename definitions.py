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
        self.signals= dict()
        self.n_samples = 1000
        
        
        self.sine_sliders()
        self.actionPlot.triggered.connect(self.plot_external_wave)
        self.horizontalSlider.valueChanged.connect(self.slider)
        self.actionAdd.triggered.connect(self.enlist_data)
        # self.actionClear.triggered.connect()
        self.pushButton_plotsine.pressed.connect(self.plot_sine_wave)
        self.actionSample.triggered.connect(self.sample)
        self.horizontalSlider.valueChanged.connect(self.sample)
        self.actionHide.triggered.connect(self.hide_show)
        
        
    
    def browse(self):
        self.file_path_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', " ", "(*.txt *.csv *.xls)")
        
            
    def read_data(self):
        self.file_name, self.file_extension = os.path.splitext(self.file_path_name)
        
        if self.file_extension == '.txt':
            # to skip the second row, use a list-like argument "[]"
            # fwf stands for fixed width formatted lines.
            data = pd.read_fwf(self.file_path_name, skiprows = [1])
            self.signal_name = data.columns[1]
            yaxis_values = data.iloc[:, 1] # gets second column
            # : means everything in dimension1 from the beginning to the end
            xaxis_timestamps = data.iloc[:, 0]
            self.interval = xaxis_timestamps[2]- xaxis_timestamps[1]
            
        elif self.file_extension == '.csv':
            data = pd.read_csv(self.file_path_name, skiprows = [1])
            self.signal_name = data.columns[1]
            yaxis_values = data.iloc[:, 1] # gets second column
            xaxis_timestamps = data.iloc[:, 0]
            self.interval = xaxis_timestamps[2]- xaxis_timestamps[1]
        self.sampling_freq = 1000#1/interval
        xy_axes = {'xaxis': xaxis_timestamps, 'yaxis': yaxis_values}
        return xy_axes;
    
        
        
        
        
    def enlist_data(self):
        self.browse()
        data = self.read_data()
        if self.signal_name in self.signals:
            pass
        else:
            self.signals.update({self.signal_name: data})
    
    
    #_________________________PLOTTING SIGNALS___________________________        
    def plot_external_wave(self):
        
        xy_axes = self.read_data()
        
        timestamps = xy_axes['xaxis']
        amplitude = xy_axes['yaxis']
        
        xaxis = timestamps[:self.n_samples]
        yaxis = amplitude[:self.n_samples]
        time_range = np.arange(0, 1000, 1)
        self.graphicsView_main.plot( time_range, yaxis[0:1000], pen = (pg.mkPen('g')))
        
    def sample(self):
        # fmax=50
        fmax = self.horizontalSlider.value()
        xy_axes = self.read_data()
        timestamps = xy_axes['xaxis']
        amplitude = xy_axes['yaxis']
        T = 1 / fmax
        T_o = self.interval
        steps_no = int(T // T_o)
        print(self.interval)
        print(steps_no)
        y_sampled = list(amplitude)[0:999:steps_no]
        x_sampled = list(timestamps)[0:999:steps_no]
        print(self.interval)
        self.graphicsView_recovered.plotItem.clearPlots()
        self.graphicsView_recovered.plot(x_sampled, y_sampled,
              pen=None,
              name="BEP",
              symbol='o',
              symbolPen=pg.mkPen(color=(0, 0, 255), width=0),                                      
              symbolBrush=pg.mkBrush(0, 0, 255, 255),
              symbolSize=7)
        self.slider_value.setText(str(fmax))
        
        
        
    def hide_show(self):
        if self.actionHide.isChecked():
            self.graphicsView_recovered.setVisible(True)
        else:
            self.graphicsView_recovered.setVisible(False)
        
    def plot_sine_wave(self):
        print('I\'m pressed');
        time = np.linspace(0, 10, 1000)
        wave = chirp(time, f0=6, f1=1, t1=10)
        self.graphicsView_sine.plot(time, wave, pen=(pg.mkPen('r')))
        # time_range = np.arange(0, 1000, 1)
        # self.sine_wave = self.magnitude * np.sin((2 * np.pi * self.frequency * time_range / 4000) + ((np.pi / 180) * self.phase))
        
        
    def slider(self):
        self.graphicsView_main.plotItem.clearPlots()
        sample_rate = self.horizontalSlider.value()
        self.graphicsView_main.plot(sample_rate);
        
    def sine_sliders(self):

        self.phase_slider.setMinimum(0)
        self.phase_slider.setMaximum(360)

        self.magnitude_slider.setMinimum(2)
        self.magnitude_slider.setMaximum(20)

        self.freq_slider.setMinimum(1)
        self.freq_slider.setMaximum(30)


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
    