import numpy as np
import pandas as pd
import pyqtgraph as pg
from PyQt5 import QtWidgets
from gui import Ui_MainWindow
from PyQt5.uic import loadUiType
from scipy.signal import chirp
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUiType
import os
from os import path
import sys
from operator import add , sub 

# import matplotlib.pyplot as plt

FORM_CLASS,_ = loadUiType(path.join(path.dirname(__file__), "gui.ui"))
class MainApp(QMainWindow, FORM_CLASS):
    def __init__(self , parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)


        self.subsignals_list =[]
        self.composer_list=[]
        self.signals= dict()
        self.n_samples = 1000
        self.add_to_combobox.pressed.connect(self.adding_to_combobox)
        self.add_to_composer_button.pressed.connect(self.add_to_composer)
        self.Exporting_composed_button.pressed.connect(self.exporting_to_csv)
        self.delete_from_combo.pressed.connect(self.deleting_from_main_graph)
        self.sine_sliders()
        self.actionPlot.triggered.connect(self.plot_external_wave)
        #self.horizontalSlider.valueChanged.connect(self.slider)
        self.actionAdd.triggered.connect(self.enlist_data)
        self.actionClear.triggered.connect(self.clear)
        # self.actionClear.triggered.connect()
        #self.pushButton_plotsine.pressed.connect(self.plot_sine_wave)
        self.actionSample.triggered.connect(self.sample)
        self.horizontalSlider.valueChanged.connect(self.sample)
        self.actionHide.triggered.connect(self.hide_show)

        
        self.phase_slider.valueChanged.connect(self.draw_sine_wave)
        self.freqency_slider.valueChanged.connect(self.draw_sine_wave)
        self.magnitude_slider.valueChanged.connect(self.draw_sine_wave)

    def read_slider_values(self):
        self.phase = self.phase_slider.value()
        self.magnitude = self.magnitude_slider.value()
        self.frequency = self.freqency_slider.value()

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

    def browse(self):
        self.file_path_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', " ", "(*.txt *.csv *.xls)")
        
            
    def read_data(self):
        self.file_name, self.file_extension = os.path.splitext(self.file_path_name)
        
        if self.file_extension == '.txt':
            # to skip the second row, use a list-like argument "[]"
            # fwf stands for fixed width formatted lines.
            data = pd.read_fwf(self.file_path_name)
            self.signal_name = data.columns[1]
            yaxis_values = data.iloc[:, 1] # gets second column
            # : means everything in dimension1 from the beginning to the end
            xaxis_timestamps = data.iloc[:, 0]
            self.interval = xaxis_timestamps[4]- xaxis_timestamps[3]
            
        elif self.file_extension == '.csv':
            data = pd.read_csv(self.file_path_name)
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
        self.slider_value.setText(str(fmax))
        xy_axes = self.read_data()
        timestamps = xy_axes['xaxis']
        amplitude = xy_axes['yaxis']
        T = (1 / fmax) *1000
        T_o = self.interval 
        steps_no = int(T / T_o)
        num_of_samples = int(1000/T)
        y_samples = []
        x_samples = []
        for counter in range(num_of_samples+1):
            y_samples.append(amplitude[np.round(T*counter)])
            x_samples.append(np.round(T*counter))
                    
        print(self.interval)
        print(steps_no)
        y_sampled = list(amplitude)[0:1000:steps_no]
        x_sampled = list(timestamps)[0:1000:steps_no]
        print(self.interval)
        self.graphicsView_recovered.plotItem.clearPlots()
        self.graphicsView_recovered.plot(x_samples, y_samples,
              pen=None,
              name="BEP",
              symbol='o',
              symbolPen=pg.mkPen(color=(0, 0, 255), width=0),                                      
              symbolBrush=pg.mkBrush(0, 0, 255, 255),
              symbolSize=7)
        
        
        
    def hide_show(self):
        if self.actionHide.isChecked():
            self.graphicsView_recovered.setVisible(True)
        else:
            self.graphicsView_recovered.setVisible(False)
            
    def clear(self):
        self.graphicsView_main.plotItem.clearPlots()
        self.graphicsView_recovered.plotItem.clearPlots()
        
        
    '''def plot_sine_wave(self):
        print('I\'m pressed');
        time = np.linspace(0, 10, 1000)
        wave = chirp(time, f0=6, f1=1, t1=10)
        self.graphicsView_sine.plot(time, wave, pen=(pg.mkPen('r')))
'''
        # time_range = np.arange(0, 1000, 1)
        # self.sine_wave = self.magnitude * np.sin((2 * np.pi * self.frequency * time_range / 4000) + ((np.pi / 180) * self.phase))
        
    def summation_to_main_graph(self):
        pass

        
    def sine_sliders(self):

        self.phase_slider.setMinimum(0)
        self.phase_slider.setMaximum(360)

        self.magnitude_slider.setMinimum(2)
        self.magnitude_slider.setMaximum(20)

        self.freqency_slider.setMinimum(1)
        self.freqency_slider.setMaximum(600)
    def adding_to_combobox(self):
        #print (self.draw_sine_wave())
        #self.subsignals_list.append(self.draw_sine_wave)
        #print('sub signal before',self.subsignals_list)
        self.subsignals_list.append(self.draw_sine_wave())
        #print('sub signal after appending',self.subsignals_list)
        #print(len(self.subsignals_list))
        self.comboBox_subsignal.addItem(f"sine wave: {self.magnitude}Amp,{self.frequency}HZ,and {self.phase}˚ phase")

    def add_to_composer(self):
        print('index',self.comboBox_subsignal.currentIndex())
        self.index = int(self.comboBox_subsignal.currentIndex()-1)
        #print('gjjggj',len(self.subsignals_list))
        if self.comboBox_subsignal.currentIndex() == -1 :
            #self.composer_list = self.subsignals_list[self.index]
            
            print('0')
        elif self.comboBox_subsignal.currentIndex() == 0 :
            self.composer_list=self.subsignals_list[0]
            print('1')
        else:
            print('2')
            self.composer_list = list( map(add, self.composer_list, self.subsignals_list[self.comboBox_subsignal.currentIndex()]) )
        #print(self.composer_list,np.array(self.subsignals_list[1]))
        self.graphicsView_sum.plotItem.clearPlots()
        self.graphicsView_sum.plot(np.arange(0,1000,1), self.composer_list)
    

    def deleting_from_main_graph(self):
        #self.composer_list -= self.subsignals_list[self.index]
        self.comboBox_subsignal.removeItem(self.comboBox_subsignal.currentIndex())
        if self.comboBox_subsignal.count() != 0 :
            self.composer_list=list(map(sub, self.composer_list, self.subsignals_list[self.comboBox_subsignal.currentIndex()] ))
            print('before',self.subsignals_list)
            self.subsignals_list.remove(self.subsignals_list[self.comboBox_subsignal.currentIndex()])
            print('after',self.subsignals_list) 
        self.graphicsView_sum.plotItem.clearPlots()
        self.graphicsView_sum.plot(np.arange(0,1000,1), self.composer_list)
        if self.comboBox_subsignal.count() == 0 :
            self.graphicsView_sum.plotItem.clearPlots()
            self.composer_list =[]
            self.subsignals_list=[]
        #if self.composer_list[80] > 10**-12:


    def exporting_to_csv(self):
        data = {'time': list(np.arange(0,1000,1)),'signal': self.composer_list }
        #print(len(np.arange(0,1000,1)))
        df = pd.DataFrame(data, columns= ['time', 'signal'])
        #self.dir_path=QFileDialog.getExistingDirectory(self,"Choose Directory","E:\\")
        name = QFileDialog.getSaveFileName(self, 'Save File')
        df.to_csv (str(name[0]), index = False, header=True)


        '''
        file = open(name,'w')
        text = self.textEdit.toPlainText()
        file.write(text)
        file.close()'''


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
   
    
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()
if __name__ == '__main__':
    main()
'''
            self.composer_list = self.composer_list + self.subsignals_list[self.comboBox_subsignal.currentIndex()]
            #self.composer_list = np.array(self.composer_list)
            #self.subsignals_list[self.index] = np.array(self.subsignals_list[self.index])
            it=0
            for i , j in self.subsignals_list[self.index] , self.composer_list:
                composer_list [it] = i+j
                it += 1
            #self.composer_list += self.subsignals_list[self.index]
        #print('composer',self.composer_list,'subsignal',self.subsignals_list)'''
        