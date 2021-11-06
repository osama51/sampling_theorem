import numpy as np
import pandas as pd
import pyqtgraph as pg
from PyQt5 import QtWidgets
import matplotlib.pyplot as plt
from gui import Ui_MainWindow
from PyQt5.uic import loadUiType
from PyQt5 import QtCore, QtGui
from scipy.fft import fft, fftfreq
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUiType
import os
from os import path
from math import sin
import sys
from operator import add , sub 

# import matplotlib.pyplot as plt

FORM_CLASS,_ = loadUiType(path.join(path.dirname(__file__), "gui.ui"))
class MainApp(QMainWindow, FORM_CLASS):
    def __init__(self , parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handle_buttons()


        self.subsignals_list =[]
        self.composer_list=[]
        self.sine_sliders()
        self.signals= dict()
        self.n_samples = 1000
        self.time_range = np.arange(0, 1000, 1)
        self.sine_sliders()
        
    #__________________________BUTTONS_______________________#
    
    def handle_buttons(self):
        self.add_to_combobox.pressed.connect(self.adding_to_combobox)
        self.add_to_composer_button.pressed.connect(self.add_to_composer)
        self.Exporting_composed_button.pressed.connect(self.exporting_to_csv)
        self.delete_from_combo.pressed.connect(self.deleting_from_main_graph)
        self.actionPlot.triggered.connect(self.plot_external_wave)
        self.actionAdd.triggered.connect(self.prepare_data)
        self.actionClear.triggered.connect(self.clear)
        self.samples_button.pressed.connect(self.show_sample_alone)
        self.actionSample.triggered.connect(self.show_samples_on_signal)
        self.horizontalSlider.valueChanged.connect(self.show_sample_alone)
        self.actionHide.triggered.connect(self.hide_show)
        self.pushButton_recover.pressed.connect(self.reconstruction)
        self.actionConfirm.triggered.connect(self.show_on_main_graph)
        self.phase_slider.valueChanged.connect(self.draw_sine_wave)
        self.freqency_slider.valueChanged.connect(self.draw_sine_wave)
        self.magnitude_slider.valueChanged.connect(self.draw_sine_wave)

    #_______________________SLIDERS_______________________#
    
    def sine_sliders(self):

        self.phase_slider.setMinimum(0)
        self.phase_slider.setMaximum(360)

        self.magnitude_slider.setMinimum(2)
        self.magnitude_slider.setMaximum(20)

        self.freqency_slider.setMinimum(1)
        self.freqency_slider.setMaximum(600)

    
    def read_slider_values(self):
        self.phase = self.phase_slider.value()
        self.magnitude = self.magnitude_slider.value()
        self.frequency = self.freqency_slider.value()
        

    #________________________COMPOSER_______________________#
     
    def adding_to_combobox(self):
        self.subsignals_list.append(self.draw_sine_wave())
        self.comboBox_subsignal.addItem(f"sine wave: {self.magnitude}Amp,{self.frequency}HZ,and {self.phase}˚ phase")

    def add_to_composer(self):

        if self.comboBox_subsignal.currentIndex() == 0 :
            self.composer_list=self.subsignals_list[0]
        else:
            self.composer_list = list( map(add, self.composer_list, self.subsignals_list[self.comboBox_subsignal.currentIndex()]) )
        self.graphicsView_sum.plotItem.clearPlots()
        self.graphicsView_sum.plot(np.arange(0,1000,1), self.composer_list)

    def exporting_to_csv(self):
        data = {'time': list(np.arange(0,1000,1)),'signal': self.composer_list }
        df = pd.DataFrame(data, columns= ['time', 'signal'])
        name = QFileDialog.getSaveFileName(self, 'Save File')
        df.to_csv (str(name[0]), index = False, header=True)
    
    #_____________________________FETCHING DATA______________________#
    
    def prepare_data(self):
        self.browse()
        data = self.read_data()
        if self.signal_name in self.signals:
            pass
        else:
            self.signals.update({self.signal_name: data})
        
    def browse(self):
        self.file_path_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', " ", "(*.txt *.csv *.xls)")
        
            
    def read_data(self):
        self.file_name, self.file_extension = os.path.splitext(self.file_path_name)
        
        if self.file_extension == '.txt':
            # to skip the second row, use a list-like argument "[]"
            # fwf stands for fixed width formatted lines.
            data = pd.read_fwf(self.file_path_name)
            self.signal_name = data.columns[1]
            self.amplitude = data.iloc[:, 1] # gets second column
            # : means everything in dimension1 from the beginning to the end
            self.timstamps = data.iloc[:, 0]
            self.interval = self.timestamps[6]- self.timestamps[5]
            
        elif self.file_extension == '.csv':
            data = pd.read_csv(self.file_path_name)
            self.signal_name = data.columns[1]
            self.amplitude = data.iloc[:, 1] # gets second column
            self.timestamps = data.iloc[:, 0]
            self.interval = self.timestamps[6]- self.timestamps[5]
        self.sampling_freq = 1000#1/interval
        # xy_axes = {'xaxis': xaxis_timestamps, 'yaxis': yaxis_values}
        # return xy_axes;
        self.getting_max_freq()

    
    #_________________________PLOTTING SIGNALS___________________________#
    
    def draw_sine_wave(self):
        
        self.read_slider_values()
        self.freq_label.setText(str(self.freqency_slider.value()))
        self.mag_label.setText(str(self.magnitude_slider.value()))
        self.phase_label.setText(str(self.phase_slider.value()))
        self.time_range = np.arange(0, 1000, 1)
        self.sine_wave = self.magnitude * np.sin((2 * np.pi * self.frequency * self.time_range / 1000) + ((np.pi / 180) * self.phase))
        self.graphicsView_sine.plotItem.clearPlots()
        self.graphicsView_sine.plot(self.time_range, self.sine_wave)

        return list(self.sine_wave)
        
    def plot_external_wave(self):
        # xy_axes = self.read_data()
        # timestamps = xy_axes['xaxis']
        # amplitude = xy_axes['yaxis']
        # xaxis = timestamps[:self.n_samples]     
        yaxis = self.amplitude[:self.n_samples]  # limiting to 1000 samples
        # time_range = np.arange(0, 1000, 1)
        if self.actionPlot.isChecked():
            self.graphicsView_main.plot( self.time_range, yaxis[0:1000], pen = (pg.mkPen('g')))
        else:
            # self.graphicsView_main.plot( self.time_range, yaxis[0:1000], pen = None)
            self.graphicsView_main.plotItem.clearPlots()
            if self.actionSample.isChecked():
                self.show_samples_on_signal()
                
                
    def getting_max_freq(self):
        self.number_of_samples = len (self.amplitude) 
        self.amp_of_freqs = fft(list(self.amplitude))
        self.freqs = fftfreq(len(self.amp_of_freqs),self.interval)[:self.number_of_samples//2] 
        threshold = 0.5 * max(abs(self.amp_of_freqs))
        mask = abs(self.amp_of_freqs) > threshold
        peaks = self.freqs[mask[:self.number_of_samples//2]]
        peaks = abs(peaks)
        self.max_freq= max(peaks)*1000
        self.horizontalSlider.setMaximum(int(3*self.max_freq))
        
        
    def sample(self):
        # fmax=50
        fmax = self.horizontalSlider.value()
        self.slider_value.setText(str(fmax))
        # xy_axes = self.read_data()
        # timestamps = xy_axes['xaxis']
        # amplitude = xy_axes['yaxis']
        yaxis = self.amplitude[:self.n_samples]
        T = (1 / fmax) *1000
        T_o = self.interval 
        steps_no = int(T / T_o)
        num_of_samples = int(1000/T)
        self.y_samples = []
        self.x_samples = []
        for counter in range(num_of_samples):
            self.y_samples.append(yaxis[int(np.round(T*counter))])
            self.x_samples.append(np.round(T*counter))
        
    def show_samples_on_signal(self):
        self.sample()
        if self.actionSample.isChecked():
            self.graphicsView_main.plot(self.x_samples, self.y_samples,
                  pen=None,
                  name="BEP",
                  symbol='+',
                  symbolPen=pg.mkPen(color=(0, 0, 255), width=0),                                      
                  symbolBrush=pg.mkBrush(0, 0, 255, 255),
                  symbolSize=7)
            
    def show_sample_alone(self):
        self.sample()
        if not self.samples_button.isChecked():
            self.graphicsView_recovered.plotItem.clearPlots()
            self.graphicsView_recovered.plot(self.x_samples, self.y_samples,
                  pen=None,
                  name="BEP",
                  symbol='o',
                  symbolPen=pg.mkPen(color=(0, 0, 255), width=0),                                      
                  symbolBrush=pg.mkBrush(0, 0, 255, 255),
                  symbolSize=7)
        else :
            self.graphicsView_recovered.plotItem.clearPlots()
            
    def show_on_main_graph(self):
        # data = {'time': list(np.arange(0,1000,1)),'signal': self.composer_list }
        self.graphicsView_main.plotItem.clearPlots()
        self.graphicsView_main.plot( self.time_range, self.composer_list, pen = (pg.mkPen(color=(223, 182, 237))))
        self.amplitude = self.composer_list
        self.interval = 1 #predefined customized interval
        self.getting_max_freq()

    def reconstruction(self):
        num_of_samples = int(len(self.x_samples))
        interval = 1.0 / 1000.0
        x = np.linspace(0.0, num_of_samples*interval, num_of_samples, endpoint=False)
        y = self.y_samples
        yfreq_domain = fft(y)
        xfreq_domain = fftfreq(num_of_samples, interval)[:num_of_samples//2]
        signal = np.fft.ifft(yfreq_domain)
        
        self.graphicsView_main.plot(self.x_samples, signal.real, pen = (pg.mkPen('y')))
        
    #_________________________FAILED MAX-FREQ_____________________________#
        
        # maximum = 0.45
        # index_of_fft= 0
        # i=0
        # for fft in poly_y:
        # 	if maximum/fft  > 124: index_of_fft=i
        # 	i+=1
        # print('fmax = ',xf[index_of_fft])
        
    #_________________________________UTILITIES_________________________#
    
    def hide_show(self):
        if self.actionHide.isChecked():
            self.graphicsView_recovered.setVisible(True)
        else:
            self.graphicsView_recovered.setVisible(False)
            
    def clear(self):
        self.graphicsView_main.plotItem.clearPlots()
        self.graphicsView_recovered.plotItem.clearPlots()

    def deleting_from_main_graph(self):

        self.comboBox_subsignal.removeItem(self.comboBox_subsignal.currentIndex())
        if self.comboBox_subsignal.count() != 0 :
            self.composer_list=list(map(sub, self.composer_list, self.subsignals_list[self.comboBox_subsignal.currentIndex()] ))
            self.subsignals_list.remove(self.subsignals_list[self.comboBox_subsignal.currentIndex()])
            
        self.graphicsView_sum.plotItem.clearPlots()
        self.graphicsView_sum.plot(self.time_range, self.composer_list)
        
        if self.comboBox_subsignal.count() == 0 :
            self.graphicsView_sum.plotItem.clearPlots()
            self.composer_list =[]
            self.subsignals_list=[]


    
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()
if __name__ == '__main__':
    main()
